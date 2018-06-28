import xlwt
import xlrd
from xlutils.copy import copy
import xlsxwriter

count_book = xlrd.open_workbook('university.xls')
r_sheet = count_book.sheet_by_index(0)

all_row = r_sheet.nrows
all_col = r_sheet.ncols

book = copy(count_book)
w_sheet = book.get_sheet(0)
for row in range(55):
    for j in range(1,6):
        print(r_sheet.row_values(row,j-1,j)[0])
    # if r_sheet.row_values(row,0,1) == ['<br/>']:
    #     print('no name ')
#         w_sheet.write(row, 0, '无数据')
# book.save('university.xls')

###################################################################
# book = xlsxwriter.Workbook('pict111.xlsx')
#
# sheet = book.add_worksheet('国外学校')
# sheet.set_column(2, 2, 16)
# for row in range(1, all_row ):
#     sheet.set_row(row, 100)
#     for col in range(all_col):
#         cell_value = r_sheet.cell_value(row,col,)
#         if col == 2:
#             sheet.insert_image(row, 2, './lo/%s.jpg' % (row + 1))
#         else:
#             sheet.write(row,col,cell_value)
#
# book.close()
