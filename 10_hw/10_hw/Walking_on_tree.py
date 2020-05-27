import os
import datetime
import xlwt

def get_time(time):
    full_time = datetime.datetime.fromtimestamp(time)
    return full_time.strftime('%d-%m-%Y %H:%M:%S')


def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def create_stat(my_path):
    try:
        book = xlwt.Workbook()
        sheet = book.add_sheet('Statistics')
        columns = ['nesting', 'feature', 'name', 'size', 'time', 'abspath']
        data = []
        for root, dirs, files in os.walk(my_path):  
            path = root.split(os.sep)
            current_info = [
                len(path) - 1,
                'd',
                os.path.basename(root),
                sizeof_fmt(os.path.getsize(root)),
                get_time(os.path.getmtime(root)),
                os.path.abspath(root)
            ]
            data.append(current_info)
            print((len(path) - 1) * '---', (len(path)-1), 'd', os.path.basename(root), 
            sizeof_fmt(os.path.getsize(root)), os.path.getmtime(root), os.path.abspath(root)) 

            for file in files:
                current_info_file = [
                    len(path),
                    'f',
                    os.path.basename(root+'/'+file),
                    sizeof_fmt(os.path.getsize(root+'/'+file)),
                    get_time(os.path.getmtime(root+'/'+file)),
                    os.path.abspath(root+'/'+file)
                ]
                data.append(current_info_file)
                print(len(path) * '---', len(path), 'f', file, sizeof_fmt(os.path.getsize(root+'/'+file)), 
                os.path.getmtime(root+'/'+file), os.path.abspath(root+'/'+file))

        print(f'Строчек будет {len(data)}')

        for number, info in enumerate(data):
            row = sheet.row(number)
            for index, value in enumerate(info):
                row.write(index, value)

        book.save('Statistics.xlsx')
    except Exception as e:
        print(f'Случилась ошибка: {e}')