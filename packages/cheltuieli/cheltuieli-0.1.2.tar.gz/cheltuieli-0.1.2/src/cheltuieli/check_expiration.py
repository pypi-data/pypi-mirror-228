import decimal
import os.path
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
import numpy as np
from datetime import datetime, timedelta
import datetime as dt
from dateutil.relativedelta import *
import sys
import os
import matplotlib.pyplot as plt
from __init__ import __version__ as packVersion
sys.path.append(r'D:\Python\MySQL\SQL_Query')
import connect
np.set_printoptions(linewidth=250)
__version__ = 'V1'


class CheltPlanificate:
    def __init__(self, db_type, data_base_name):
        self.dataBase = connect.DataBase(db_type, data_base_name)

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

    def excludeNone(self, tableHead, table):
        if None in table[:, tableHead.index('valid_to')]:
            newTable = table[table[:, tableHead.index('valid_to')] != np.array(None)]
        return tableHead, newTable

    def get_days_to_expire(self, tableHead, table):
        print(sys._getframe().f_code.co_name, tableHead)

        newTableHead = []
        for col in tableHead:
            newTableHead.append(col)
        newTableHead.append('days2Expire')

        newCol = np.empty((table.shape[0], 1), dtype=object)
        newCol.fill('')
        table = np.append(table, newCol, 1)
        for row in table:
            expDate = row[tableHead.index('valid_to')]
            today = dt.date.today()
            if expDate is not None:
                time2exp = (expDate - today).days
                row[-1] = time2exp
        return newTableHead, table

    def hideExpired(self, tableHead, table):
        print(sys._getframe().f_code.co_name, tableHead)
        newTable = table[table[:, tableHead.index('days2Expire')] > 0]
        return tableHead, newTable

    def relevantOnly(self, tableHead, table, days):
        print(sys._getframe().f_code.co_name, tableHead)
        colIndx = tableHead.index('path')
        indxPath = [x for x, item in enumerate(table[:, colIndx]) if (item == '' or item is None)]
        colIndx = tableHead.index('days2Expire')
        indxExp = [x for x, item in enumerate(table[:, colIndx]) if item != '' and 0<item<days]
        indx = [*indxPath, *indxExp]
        indx = list(set(indx))
        newTable = table[indx]
        return tableHead, newTable


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        path2src, pyFileName = os.path.split(__file__)
        uiFileName = 'check_expiration.ui'
        path2GUI = os.path.join(path2src, 'GUI', uiFileName)
        Ui_MainWindow, QtBaseClass = uic.loadUiType(path2GUI)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        title = '{}_{}'.format(pyFileName, __version__)
        self.setWindowTitle(title)
        self.expDays = int(self.ui.SB_expDays.text())

        self.db_type = 'MySQL'
        self.data_base_name = 'myfolderstructure'
        self.cheltPlan = CheltPlanificate(self.db_type, self.data_base_name)
        self.tableHead = ['id', 'name', 'valid_from', 'valid_to', 'auto_ext', 'path']
        self.newRows = []
        self.pathUpdates = []

        self.ui.planTable.horizontalHeader().sectionClicked.connect(self.sortPlan)
        self.ui.planTable.horizontalHeader().sectionDoubleClicked.connect(self.setFilter)
        self.ui.PB_update.clicked.connect(self.updateSQL)
        self.prepareTablePlan()

        self.ui.CB_hideExpired.stateChanged.connect(self.prepareTablePlan)
        self.ui.CB_relOnly.stateChanged.connect(self.prepareTablePlan)
        self.ui.CB_excludeNone.stateChanged.connect(self.prepareTablePlan)
        self.ui.planTable.cellDoubleClicked.connect(self.updatePath)

    def prepareTablePlan(self):
        print(sys._getframe().f_code.co_name)
        tableHead, table = self.cheltPlan.get_all_sql_vals(self.tableHead)
        table = np.atleast_2d(table)
        if self.ui.CB_excludeNone.isChecked():
            tableHead, table = self.cheltPlan.excludeNone(tableHead, table)
        tableHead, table = self.cheltPlan.get_days_to_expire(tableHead, table)
        if self.ui.CB_hideExpired.isChecked():
            tableHead, table = self.cheltPlan.hideExpired(tableHead, table)
        elif self.ui.CB_relOnly.isChecked():
            tableHead, table = self.cheltPlan.relevantOnly(tableHead, table, self.expDays)

        self.populateExpensesPlan(tableHead, table)
        self.colorCells(tableHead)

    def populateExpensesPlan(self, tableHead, table):
        print(sys._getframe().f_code.co_name)
        self.ui.planTable.clear()
        self.ui.planTable.setColumnCount(len(tableHead))
        self.ui.planTable.setHorizontalHeaderLabels(tableHead)
        self.ui.planTable.setRowCount(table.shape[0])
        txt = 'No. of rows: {}'.format(table.shape[0])
        self.ui.label.setText(txt)
        for row in range(table.shape[0]):
            for col in range(table.shape[1]):
                # if tableHead[col] == 'path':
                #     print('*****', str(table[row, col]))
                if isinstance(table[row, col], int) or isinstance(table[row, col], float):
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, table[row, col])
                    self.ui.planTable.setItem(row, col, item)
                elif tableHead[col] == 'path' and str(table[row, col]) != '':
                    path = table[row, col]
                    if path:
                        url = bytearray(QUrl.fromLocalFile(path).toEncoded()).decode()
                        item = QLabel()
                        text = "<a href={}>Link</a>".format(url)
                        item.setText(text)
                        item.setOpenExternalLinks(True)
                        self.ui.planTable.setCellWidget(row, col, item)
                    else:
                        item = QTableWidgetItem(str(table[row, col]))
                        self.ui.planTable.setItem(row, col, item)
                elif tableHead[col] == 'path' and str(table[row, col]) == '':
                    item = QTableWidgetItem(str(table[row, col]))
                    self.ui.planTable.setItem(row, col, item)
                else:
                    item = QTableWidgetItem(str(table[row, col]))
                    self.ui.planTable.setItem(row, col, item)

    def updateSQL(self):
        self.readTable()
        for row in self.newRows:
            tableName, id = row
            table = connect.Table(self.db_type, self.data_base_name, tableName)
            matches = ('id', id)
            row = table.returnRowsWhere(matches)[0]

            cols = []
            vals = []
            for i, col in enumerate(table.columnsNames):
                if col == 'id' or col == 'path':
                    continue
                cols.append(col)
                vals.append(row[i])

            newRowId = table.add_row(cols, vals)
            valid_to = row[table.columnsNames.index('valid_to')]
            freq = row[table.columnsNames.index('freq')]
            newValid_to = valid_to + relativedelta(months=freq)
            newValid_from = valid_to + relativedelta(days=1)
            table.changeCellContent('valid_to', newValid_to, 'id', newRowId)
            table.changeCellContent('valid_from', newValid_from, 'id', newRowId)
            table.changeCellContent('auto_ext', 1, 'id', newRowId)
            table.changeCellContent('auto_ext', 0, 'id', id)
        for row in self.pathUpdates:
            tableName, id, path = row
            table = connect.Table(self.db_type, self.data_base_name, tableName)
            # matches = ('id', id)
            # row = table.returnRowsWhere(matches)[0]
            # newRowId = table.add_row(table.columnsNames[1:], row[1:])
            # valid_to = row[table.columnsNames.index('valid_to')]
            # freq = row[table.columnsNames.index('freq')]
            # newValid_to = valid_to + relativedelta(months=freq)
            # newValid_from = valid_to + relativedelta(days=1)
            # table.changeCellContent('valid_to', newValid_to, 'id', newRowId)
            # table.changeCellContent('valid_from', newValid_from, 'id', newRowId)
            table.changeCellContent('path', path, 'id', id)
        self.prepareTablePlan()

    def readTable(self):
        print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        rows = self.ui.planTable.rowCount()
        cols = self.ui.planTable.columnCount()
        for row in range(rows):
            for column in range(cols):
                cell = self.ui.planTable.item(row, column)
                headerName = self.ui.planTable.horizontalHeaderItem(column).text()
                if headerName == 'table':
                    table = cell.text()
                elif headerName == 'id':
                    id = cell.text()
                if headerName == 'newRow':
                    widget = self.ui.planTable.cellWidget(row, column)
                    if cell is not None:
                        if cell.text():
                            colValue = cell.text()
                        elif cell.checkState() == QtCore.Qt.Checked:
                            tup = (table, id)
                            self.newRows.append(tup)
        # return updates

    def colorCells(self, tableHead):
        print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        rows = self.ui.planTable.rowCount()
        cols = self.ui.planTable.columnCount()
        self.ui.planTable.insertColumn(cols)
        tableHead.append('newRow')
        cols = self.ui.planTable.columnCount()
        self.ui.planTable.setHorizontalHeaderLabels(tableHead)
        for row in range(rows):
            for column in range(cols):
                cell = self.ui.planTable.item(row, column)
                headerName = self.ui.planTable.horizontalHeaderItem(column).text()
                if headerName == 'days2Expire':
                    if cell.text():
                        days2Expire = int(cell.text())
                        if self.expDays > days2Expire > 0:
                            self.ui.planTable.item(row, column).setBackground(QtGui.QColor('red'))
                elif headerName == 'path':
                    widget = self.ui.planTable.cellWidget(row, column)
                    if widget is None:
                        self.ui.planTable.item(row, column).setBackground(QtGui.QColor('red'))
                elif headerName == 'newRow':
                    cell = QTableWidgetItem()
                    cell.setFlags(QtCore.Qt.ItemIsUserCheckable |QtCore.Qt.ItemIsEnabled)
                    cell.setCheckState(QtCore.Qt.Unchecked)
                    self.ui.planTable.setItem(row, column, cell)

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

    def updatePath(self, row, col):
        print(sys._getframe().f_code.co_name)
        headerName = self.ui.planTable.horizontalHeaderItem(col).text()
        if headerName == 'path':
            inpFile, _ = QFileDialog.getOpenFileName(None, 'Select file', '', '')
            if inpFile:
                if os.path.exists(inpFile):
                    item = QTableWidgetItem(str(inpFile))
                    self.ui.planTable.setItem(row, col, item)
                    self.ui.planTable.item(row, col).setBackground(QtGui.QColor('green'))
                    cols = self.ui.planTable.columnCount()
                    for col in range(cols):
                        headerName = self.ui.planTable.horizontalHeaderItem(col).text()
                        if headerName == 'table':
                            table = self.ui.planTable.item(row, col).text()
                        elif headerName == 'id':
                            id = self.ui.planTable.item(row, col).text()
                    tup = (table, id, inpFile)
                    self.pathUpdates.append(tup)

    def setFilter(self, logical_index):
        print(sys._getframe().f_code.co_name)
        colName = self.expensesTableReal.columnsNames[logical_index]
        colType = self.expensesTableReal.get_column_type(colName)
        if colType == 'int':
            filt = FilterWindow.getIntInterval(colName)
            if not filt:
                return
            if isinstance(filt, tuple):
                minInt, maxInt = filt
                filterVals = (str(minInt), str(maxInt))
            elif isinstance(filt, str):
                filterVals = filt
            self.applyFilter(colName, filterVals)
        elif colType == 'date':
            filt = FilterWindow.getDateInterval(colName)
            if not filt:
                return
            if isinstance(filt, tuple):
                minDate, maxDate = filt
                minDate = minDate.toPyDate()
                maxDate = maxDate.toPyDate()
                filterVals = (str(minDate), str(maxDate))
            elif isinstance(filt, str):
                filterVals = filt
            self.applyFilter(colName, filterVals)
        else:
            header = self.ui.realTable.horizontalHeader()

            geom = QtCore.QRect(header.sectionViewportPosition(logical_index), 0, header.sectionSize(logical_index),
                                header.height())
            item = QLineEdit(header)
            item.setGeometry(geom)
            item.show()
            item.setFocus()
            item.editingFinished.connect(lambda: (self.applyFilter(colName, item.text()),
                                                  item.clear(),
                                                  item.hide(),
                                                  item.deleteLater()))

    def applyFilter(self, colName, filter):
        print(sys._getframe().f_code.co_name)
        if filter == '':
            return

        if self.defaultFilter:
            self.ui.lineEditFilterList.clear()
            self.defaultFilter = False

        filterText = self.ui.lineEditFilterList.text()
        if not filterText:
            if isinstance(filter, str):
                filterText += '{}="{}"'.format(colName, filter)
            elif isinstance(filter, tuple):
                filterText += '{} < {} < {}'.format(filter[0], colName, filter[1])
            elif isinstance(filter, list):
                filterText += '{} in {}"'.format(str(filter), colName)
        else:
            if isinstance(filter, str):
                filterText += '; {}="{}"'.format(colName, filter)
            elif isinstance(filter, tuple):
                filterText += '; {} < {} < {}'.format(filter[0], colName, filter[1])
            elif isinstance(filter, list):
                filterText += '; {} in {}"'.format(str(filter), colName)

        self.ui.lineEditFilterList.setText(filterText)

        tup = (colName, filter)
        self.filterList.append(tup)
        realExpenses = self.expensesTableReal.filterRows(self.filterList)
        payments4Interval = self.apply_dates_interval_filter(realExpenses)
        payments, income = self.split_expenses_income(payments4Interval)

        realExpenses = np.atleast_2d(payments)
        realIncome = np.atleast_2d(income)
        if realExpenses.shape == (1, 0):
            realExpenses = np.empty((0, len(self.expensesTableReal.columnsNames)))
        if realIncome.shape == (1, 0):
            realIncome = np.empty((0, len(self.expensesTableReal.columnsNames)))

        self.populateTableReal(realExpenses)
        self.populateTableIncome(realIncome)


class FilterWindow(QDialog):
    def __init__(self, colType, colName):
        super(FilterWindow, self).__init__()
        path2src, pyFileName = os.path.split(__file__)
        uiFileName = 'filterWindow.ui'
        path2GUI = os.path.join(path2src, 'GUI', uiFileName)
        Ui_MainWindow, QtBaseClass = uic.loadUiType(path2GUI)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.colName = colName
        self.ui.GB_DateInterval.setVisible(False)
        self.ui.GB_IntInterval.setVisible(False)
        self.ui.checkBoxDateInterval.stateChanged.connect(self.openDateInterval)
        self.ui.checkBoxIntInterval.stateChanged.connect(self.openIntInterval)

        self.rejected.connect(self.byebye)

        if colType == 'int':
            self.ui.GB_IntInterval.setVisible(True)
            self.ui.lineEdit_max.setEnabled(False)
        if colType == 'date':
            self.ui.GB_DateInterval.setVisible(True)
            self.ui.dateEditTo.setEnabled(False)

    def openIntInterval(self):
        if self.ui.checkBoxIntInterval.isChecked():
            self.ui.lineEdit_max.setEnabled(True)
            self.ui.label_int.setText('< {} <'.format(self.colName))
        else:
            self.ui.lineEdit_max.setEnabled(False)
            self.ui.label_int.setText('= {}'.format(self.colName))

    def openDateInterval(self):
        if self.ui.checkBoxDateInterval.isChecked():
            self.ui.dateEditTo.setEnabled(True)
            self.ui.label_date.setText('< {} <'.format(self.colName))
        else:
            self.ui.dateEditTo.setEnabled(False)
            self.ui.label_date.setText('= {}'.format(self.colName))

    def byebye(self):
        self.close()

    def intInterval(self):
        if self.ui.checkBoxIntInterval.isChecked():
            tup = (self.ui.lineEdit_min.text(), self.ui.lineEdit_max.text())
            return tup
        else:
            return self.ui.lineEdit_min.text()

    def dateInterval(self):
        if self.ui.checkBoxDateInterval.isChecked():
            tup = (self.ui.dateEditFrom.date(), self.ui.dateEditTo.date())
            return tup
        else:
            return self.ui.dateEditFrom.date()

    @staticmethod
    def getIntInterval(colName):
        dialog = FilterWindow('int', colName)
        result = dialog.exec_()
        filt = dialog.intInterval()
        if result == QDialog.Accepted:
            return filt
        else:
            return None

    @staticmethod
    def getDateInterval(colName):
        dialog = FilterWindow('date', colName)
        result = dialog.exec_()
        filt = dialog.dateInterval()
        if result == QDialog.Accepted:
            return filt
        else:
            return None


def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
