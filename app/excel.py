import xlwt
import os
from config import basedir

def write2excel(name, data):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(name)
    for r, row in enumerate(data): 
        for c, cell in enumerate(row):
            worksheet.write(r,c,cell)
    dir = os.path.join(basedir, 'app', 'static', 'out')
    try:
        os.makedirs(dir)
    except OSError:
        pass
    file = os.path.join(dir, name+'.xls')
    workbook.save(file)
    return os.path.join('out', name+'.xls')
