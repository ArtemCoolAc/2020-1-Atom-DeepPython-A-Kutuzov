from subprocess import check_output 
import io
import re
from PyPDF2 import PdfFileReader


def get_num_pages(pdf_path): 
    output = check_output(["pdfinfo", pdf_path]).decode() 
    pages_line = [line for line in output.splitlines() if "Pages:" in line][0] 
    num_pages = int(pages_line.split(":")[1]) 
    return num_pages


def simple_get_num(pdf_path):
    f2 = b''.join([byte for byte in io.BytesIO(open(pdf_path, 'rb').read())])
    f4 = ''.join(list(map(chr, f2)))
    try:
        num_pages = int(re.sub('Count ', '', re.findall(r'Count [\d]+', f4)[0]))

    except Exception as e:
        num_pages = int(re.findall(r'[\d]*/T', f4)[0][:-2])

    return num_pages

if __name__ == "__main__":
    truth = []
    names = ['503_Кутузов (1).pdf', 'Отчет_МПС.pdf', 'Ряды_доп_теор.pdf', 'Ряды_теория_теоремы.pdf',
    'Списки_школы.pdf', 'Shustova_L_I_Tarakanov_O_V_-_Bazy_dannykh_Uchebnik_Vysshee_obrazovanie_-_2016.pdf']

    for name in names:
        truth.append(get_num_pages(name) == simple_get_num(name) == PdfFileReader(name).getNumPages())

    print(all(truth))

