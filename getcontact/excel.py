import os
import sys
import xlwt
import xlrd
from xlutils.copy import copy


class XLS:
    def __init__(self, restore=False):
        self.file_path = 'get_contact.xls'
        if restore:
            if not os.path.isfile(self.file_path):
                sys.stderr.write(f'Xls file from the previous session not found: {self.file_path}\n')
                sys.exit(1)
            self.book = copy(xlrd.open_workbook(self.file_path))
            self.sheet = self.book.get_sheet(0)
            self.y = len(self.sheet.rows)
        else:
            if os.path.isfile(self.file_path):
                os.remove(self.file_path)
            self.book = xlwt.Workbook(encoding="utf-8")
            self.sheet = self.book.add_sheet("Sheet")
            self.y = 0

    def write(self, names, number):
        self.sheet.write(self.y, 0, number)
        self.sheet.write(self.y, 1, names)

        self.book.save(self.file_path)
        self.y += 1

    def get_last_number(self):
        book_read = xlrd.open_workbook(self.file_path)
        sheet = book_read.sheet_by_index(0)
        return sheet.cell(sheet.nrows - 1, 0).value
