import decimal
import os.path
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import *
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import sys
import matplotlib.pyplot as plt
from MySQLquerys import connect

np.set_printoptions(linewidth=250)
__version__ = 'V4'


class CheltPlanificate:
    def __init__(self, ini_file, data_base_name):
        try:
            self.dataBase = connect.DataBase(ini_file, data_base_name)
        except FileNotFoundError as err:
            iniFile, a = QFileDialog.getOpenFileName(None, 'Open data base configuration file', os.getcwd(), "data base config files (*.ini)")
            if os.path.exists(iniFile):
                self.dataBase = connect.DataBase(iniFile, data_base_name)
            # ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)
        except Exception as err:
            print(traceback.format_exc())

    def get_all_sql_vals(self, tableHead):
        # print(sys._getframe().f_code.co_name, tableHead)
        all_chelt = []
        for table in self.dataBase.tables:
            self.dataBase.active_table = table
            check = all(item in list(self.dataBase.active_table.columnsProperties.keys()) for item in tableHead)
            if check:
                vals = self.dataBase.active_table.returnColumns(tableHead)
                for row in vals:
                    row = list(row)
                    row.insert(0, table)
                    all_chelt.append(row)

        newTableHead = ['table']
        for col in tableHead:
            newTableHead.append(col)

        return newTableHead, all_chelt

    def filter_dates(self, tableHead, table, selectedStartDate, selectedEndDate):
        print(sys._getframe().f_code.co_name, tableHead)

        tableHead.append('payDay')
        validFromIndx = tableHead.index('valid_from')
        validToIndx = tableHead.index('valid_to')
        freqIndx = tableHead.index('freq')
        payDayIndx = tableHead.index('pay_day')
        postPayIndx = tableHead.index('post_pay')
        autoExtIndx = tableHead.index('auto_ext')
        nameIndx = tableHead.index('name')

        payments4Interval = []
        for val in table:
            validfrom, validTo, freq, payDatum, postPay, autoExt = val[validFromIndx], \
                                                              val[validToIndx], \
                                                              val[freqIndx], \
                                                              val[payDayIndx], \
                                                              val[postPayIndx], \
                                                              val[autoExtIndx]

            if autoExt is None or autoExt == 0:
                autoExt = False
            else:
                autoExt = True
            if postPay is None or postPay == 0:
                postPay = False
            else:
                postPay = True

            #daca data expirarii este mai mica decat data de start selectata continua
            if validTo:
                if validTo < selectedStartDate and not autoExt:
                    if not postPay:
                        continue
            if not freq:
                continue

            if postPay:
                paymentDate = validTo
            else:
                paymentDate = validfrom

            try:
                payDay = datetime(paymentDate.year, paymentDate.month, payDatum).date()
                if payDay < paymentDate:
                    payDay = datetime(paymentDate.year, paymentDate.month, payDatum).date() + relativedelta(months=1)
            except ValueError:
                payDay = datetime(paymentDate.year, paymentDate.month+1, 1).date() - relativedelta(days=1)
            except TypeError:
                payDay = paymentDate
            except Exception:
                print('OOOO')
                print(traceback.format_exc())
                sys.exit()

            toBePayed = False
            # cat timp data de end selectata este mai mare decat data platii...
            while selectedEndDate >= payDay:
                if selectedStartDate <= payDay <= selectedEndDate:
                    if not validTo:
                        tup = [x for x in val]
                        tup.append(payDay)
                        payments4Interval.append(tup)
                        toBePayed = True
                    elif payDay <= validTo:
                        tup = [x for x in val]
                        tup.append(payDay)
                        payments4Interval.append(tup)
                        toBePayed = True
                    elif payDay >= validTo and autoExt:
                        tup = [x for x in val]
                        tup.append(payDay)
                        payments4Interval.append(tup)
                        toBePayed = True
                    elif payDay >= validTo and postPay and selectedStartDate <= payDay <= selectedEndDate:
                        tup = [x for x in val]
                        tup.append(payDay)
                        payments4Interval.append(tup)
                        toBePayed = True
                if val[nameIndx] == 'BadEndorf Quartalabrechnung_Q4':
                    print(val, payDay)

                payDay = payDay + relativedelta(months=+freq)
                try:
                    payDay = datetime(payDay.year, payDay.month, payDatum).date()
                except ValueError:
                    payDay = datetime(payDay.year, payDay.month + 1, 1).date() - relativedelta(days=1)
                except TypeError:
                    payDay = payDay
                except Exception:
                    print('OOOO')
                    print(traceback.format_exc())
                    sys.exit()
                # print(payDay, type(payDay), freq, type(freq), payDay.month+freq)
            if not toBePayed:
                continue
        payments4Interval = np.atleast_2d(payments4Interval)
        return tableHead, payments4Interval

    def filter_conto(self, tableHead, table, currentConto):
        # print(sys._getframe().f_code.co_name, tableHead, currentConto)
        if table.shape[1] > 0:
            if currentConto == 'all':
                indxConto = np.where(table[:, tableHead.index('table')] != 'expenses')
            else:
                indxConto = np.where(table[:, tableHead.index('myconto')] == currentConto)
            return tableHead, table[indxConto]
        else:
            return tableHead, np.empty((0, len(tableHead)))

    def split_expenses_income(self, tableHead, table):
        # print(sys._getframe().f_code.co_name)
        indxValue = tableHead.index('value')
        payments = []
        income = []
        for row in table:
            if row[indxValue] > 0:
                income.append(row)
            if row[indxValue] < 0:
                payments.append(row)
        payments = np.atleast_2d(payments)
        income = np.atleast_2d(income)

        return payments, income


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        path2src, pyFileName = os.path.split(__file__)
        uiFileName = 'chelt_plan.ui'
        path2GUI = os.path.join(path2src, 'GUI', uiFileName)
        Ui_MainWindow, QtBaseClass = uic.loadUiType(path2GUI)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        title = '{}_{}'.format(pyFileName, __version__)
        self.setWindowTitle(title)

        ini_file = r"D:\Python\MySQL\database.ini"
        data_base_name = 'myfolderstructure'
        self.cheltPlan = CheltPlanificate(ini_file, data_base_name)
        self.tableHead = ['name', 'value', 'myconto', 'freq', 'pay_day', 'valid_from', 'valid_to', 'auto_ext', 'post_pay']

        self.myAccountsTable = connect.Table(ini_file, data_base_name, 'banca')
        self.myContos = self.myAccountsTable.returnColumn('name')

        self.populateCBConto()
        self.populateDatesInterval()
        self.prepareTablePlan()

        self.ui.cbActiveConto.currentIndexChanged.connect(self.prepareTablePlan)
        self.ui.DEFrom.dateTimeChanged.connect(self.prepareTablePlan)
        self.ui.DEBis.dateTimeChanged.connect(self.prepareTablePlan)
        self.ui.planTable.horizontalHeader().sectionClicked.connect(self.sortPlan)
        self.ui.PB_plotTablePie.clicked.connect(self.plotTablePie)
        self.ui.PB_plotNamePie.clicked.connect(self.plotNamePie)
        self.ui.PB_Plot.clicked.connect(self.plotGraf)

    def populateCBConto(self):
        print(sys._getframe().f_code.co_name)
        # self.ui.cbActiveConto.addItem('all')
        self.ui.cbActiveConto.addItems(self.myContos)

    def populateDatesInterval(self):
        print(sys._getframe().f_code.co_name)
        self.ui.DEFrom.setDate(QDate(datetime.now().year,
                                             datetime.now().month,
                                             datetime.now().day))

        if datetime.now().month != 12:
            mnth = datetime.now().month + 1
            lastDayOfMonth = datetime(datetime.now().year, mnth, 1) - timedelta(days=1)
        else:
            lastDayOfMonth = datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)

        self.ui.DEBis.setDate(QDate(lastDayOfMonth))
        self.ui.DEFrom.setCalendarPopup(True)
        self.ui.DEBis.setCalendarPopup(True)

    def prepareTablePlan(self):
        print(sys._getframe().f_code.co_name)
        currentConto = self.ui.cbActiveConto.currentText()

        selectedStartDate = self.ui.DEFrom.date()
        selectedEndDate = self.ui.DEBis.date()
        selectedStartDate = selectedStartDate.toPyDate()
        selectedEndDate = selectedEndDate.toPyDate()

        tableHead, table = self.cheltPlan.get_all_sql_vals(self.tableHead)

        tableHead, payments4Interval = self.cheltPlan.filter_dates(tableHead, table, selectedStartDate, selectedEndDate)

        tableHead, payments4Interval = self.cheltPlan.filter_conto(tableHead, payments4Interval, currentConto)

        payments4Interval, income = self.cheltPlan.split_expenses_income(tableHead, payments4Interval)

        if payments4Interval.shape == (1, 0):
            payments4Interval = np.empty((0, len(tableHead)))
        if income.shape == (1, 0):
            income = np.empty((0, len(tableHead)))

        self.populateExpensesPlan(tableHead, payments4Interval)
        self.populateIncomePlan(tableHead, income)
        self.totals()

    def populateExpensesPlan(self, tableHead, table):
        print(sys._getframe().f_code.co_name)
        self.ui.planTable.setColumnCount(len(tableHead))
        self.ui.planTable.setHorizontalHeaderLabels(tableHead)
        self.ui.planTable.setRowCount(table.shape[0])
        for col in range(table.shape[1]):
            for row in range(table.shape[0]):
                if isinstance(table[row, col], int) or isinstance(table[row, col], float):
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, table[row, col])
                elif isinstance(table[row, col], decimal.Decimal):
                    val = float(table[row, col])
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, val)
                else:
                    item = QTableWidgetItem(str(table[row, col]))
                self.ui.planTable.setItem(row, col, item)

        if table.shape[1] > 0:
            allValues = table[:, tableHead.index('value')]
            if None in allValues:
                allValues = allValues[allValues != np.array(None)]
            # for i in allValues:
            #     print(i, type(i))
            totalVal = sum(allValues.astype(float))
            self.ui.LEtotalNoOfTransactions.setText(str(len(table)))
            self.ui.LEtotalValue.setText(str(totalVal))

    def populateIncomePlan(self, tableHead, table):
        print(sys._getframe().f_code.co_name)
        self.ui.planTableIncome.setColumnCount(len(tableHead))
        self.ui.planTableIncome.setHorizontalHeaderLabels(tableHead)
        self.ui.planTableIncome.setRowCount(table.shape[0])
        for col in range(table.shape[1]):
            for row in range(table.shape[0]):
                if isinstance(table[row, col], int) or isinstance(table[row, col], float):
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, table[row, col])
                elif isinstance(table[row, col], decimal.Decimal):
                    val = float(table[row, col])
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, val)
                else:
                    item = QTableWidgetItem(str(table[row, col]))
                self.ui.planTableIncome.setItem(row, col, item)

        if table.shape[1] > 0:
            allValues = table[:, tableHead.index('value')]
            if None in allValues:
                allValues = allValues[allValues != np.array(None)]
            # for i in allValues:
            #     print(i, type(i))
            totalVal = sum(allValues.astype(float))
            self.ui.LEtotalNoOfIncome.setText(str(len(table)))
            self.ui.LEtotalIncome.setText(str(totalVal))

    def totals(self):
        if self.ui.LEtotalNoOfTransactions.text():
            expensesTrans = int(self.ui.LEtotalNoOfTransactions.text())
        else:
            expensesTrans = 0
        if self.ui.LEtotalNoOfIncome.text():
            incomeTrans = int(self.ui.LEtotalNoOfIncome.text())
        else:
            incomeTrans = 0

        if self.ui.LEtotalValue.text():
            expenses = float(self.ui.LEtotalValue.text())
        else:
            expenses = 0
        if self.ui.LEtotalIncome.text():
            income = float(self.ui.LEtotalIncome.text())
        else:
            income = 0

        trans = expensesTrans + incomeTrans
        total = expenses + income

        self.ui.LEtotalNo.setText(str(trans))
        self.ui.LEtotalVa.setText(str(total))

    def sortPlan(self, logical_index):
        print(sys._getframe().f_code.co_name)
        header = self.ui.planTable.horizontalHeader()
        order = Qt.DescendingOrder
        if not header.isSortIndicatorShown():
            header.setSortIndicatorShown(True)
        elif header.sortIndicatorSection() == logical_index:
            order = header.sortIndicatorOrder()
        header.setSortIndicator(logical_index, order)
        self.ui.planTable.sortItems(logical_index, order)

    def readPlanExpenses(self):
        rows = self.ui.planTable.rowCount()
        cols = self.ui.planTable.columnCount()
        planExpenseTable = np.empty((rows, cols), dtype=object)
        planExpenseTableHead = []
        for row in range(rows):
            for column in range(cols):
                cell = self.ui.planTable.item(row, column)
                planExpenseTable[row, column] = cell.text()
                colName = self.ui.planTable.horizontalHeaderItem(column).text()
                if colName not in planExpenseTableHead:
                    planExpenseTableHead.append(colName)

        return planExpenseTable, planExpenseTableHead

    def readPlanIncome(self):
        rows = self.ui.planTableIncome.rowCount()
        cols = self.ui.planTableIncome.columnCount()
        planIncomeTable = np.empty((rows, cols), dtype=object)
        planIncomeTableHead = []
        for row in range(rows):
            for column in range(cols):
                cell = self.ui.planTableIncome.item(row, column)
                planIncomeTable[row, column] = cell.text()
                colName = self.ui.planTableIncome.horizontalHeaderItem(column).text()
                if colName not in planIncomeTableHead:
                    planIncomeTableHead.append(colName)

        return planIncomeTable, planIncomeTableHead

    def plotTablePie(self):
        realExpenseTable, realExpenseTableHead = self.readPlanExpenses()
        allValues = realExpenseTable[:, realExpenseTableHead.index('value')].astype(float)
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalVal = sum(allValues)

        colTableName = realExpenseTable[:, realExpenseTableHead.index('table')]
        labels = []
        sizes = []
        for table in np.unique(colTableName):
            indx = np.where(realExpenseTable[:, realExpenseTableHead.index('table')]==table)
            smallArray = realExpenseTable[indx]
            values = sum(smallArray[:, realExpenseTableHead.index('value')].astype(float))
            txt = '{} = {:.2f}'.format(table, values)
            labels.append(txt)
            size = (values/totalVal)*100
            sizes.append(size)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
        ax1.axis('equal')
        plt.legend(title='Total: {:.2f}'.format(totalVal))

        plt.show()

    def plotNamePie(self):
        realExpenseTable, realExpenseTableHead = self.readPlanExpenses()
        allValues = realExpenseTable[:, realExpenseTableHead.index('value')].astype(float)
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalVal = sum(allValues)

        colTableName = realExpenseTable[:, realExpenseTableHead.index('name')]
        labels = []
        sizes = []
        for table in np.unique(colTableName):
            indx = np.where(realExpenseTable[:, realExpenseTableHead.index('name')]==table)
            smallArray = realExpenseTable[indx]
            values = sum(smallArray[:, realExpenseTableHead.index('value')].astype(float))
            txt = '{} = {:.2f}'.format(table, values)
            labels.append(txt)
            size = (values/totalVal)*100
            sizes.append(size)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
        ax1.axis('equal')
        plt.legend(title='Total: {:.2f}'.format(totalVal))

        plt.show()

    def plotGraf(self):
        realExpenseTable, realExpenseTableHead = self.readPlanExpenses()
        planIncomeTable, planIncomeTableHead = self.readPlanIncome()
        x_exp = []
        y_exp = []
        for date in np.unique(realExpenseTable[:, realExpenseTableHead.index('payDay')]):
            indx = np.where(realExpenseTable[:, realExpenseTableHead.index('payDay')] == date)
            arr = realExpenseTable[indx, realExpenseTableHead.index('value')].astype(float)
            x_exp.append(date)
            y_exp.append(abs(sum(arr[0])))

        x_inc = []
        y_inc = []
        for date in np.unique(planIncomeTable[:, planIncomeTableHead.index('payDay')]):
            indx = np.where(planIncomeTable[:, planIncomeTableHead.index('payDay')] == date)
            arr = planIncomeTable[indx, planIncomeTableHead.index('value')].astype(float)
            x_inc.append(date)
            y_inc.append(abs(sum(arr[0])))

        fig1, ax1 = plt.subplots()
        ax1.plot(x_exp, y_exp)
        ax1.plot(x_inc, y_inc)
        # plt.setp(plt.get_xticklabels(), rotation=30, ha="right")
        fig1.autofmt_xdate()
        plt.grid()
        plt.show()


def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    # sys.exit(app.exec_())
    app.exec_()


if __name__ == '__main__':
    main()


