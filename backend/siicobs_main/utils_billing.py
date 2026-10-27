import math
import re
import os

import barcode
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from django.conf import settings
from barcode.writer import ImageWriter


def verhoeff(num, times):
    d = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]
    p = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
    for i in range(times, 0, -1):
        c = 0
        for i in range(len(num) - 1, -1, -1):
            c = d[c][p[((len(num) - i) % 8)][int(num[i])]]
        num += str(inv[c])
    return num


def arc4(msg, key):
    state = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + state[i] + ord(key[i % len(key)])) % 256
        temp = state[i]
        state[i] = state[j]
        state[j] = temp
    x = y = 0
    output = ''
    for i in range(len(msg)):
        x = (x + 1) % 256
        y = (state[x] + y) % 256
        temp = state[x]
        state[x] = state[y]
        state[y] = temp
        output += "{:02x}".format(ord(msg[i]) ^ state[(state[x] + state[y]) % 256])
    return output.upper()


def base64(number):
    result = ''
    dic = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'
    while number > 0:
        result = dic[number % 64] + result
        number = math.floor(number / 64)
    return result


def get_control_code(number_authorization, number_billing, nit, date, total, dosage_key):
    code = ''
    number = verhoeff(number_billing, 2)
    nit = verhoeff(nit, 2)
    date = verhoeff(date, 2)
    total = verhoeff(total, 2)
    vf = verhoeff(str(
        int(number) +
        int(nit) +
        int(date) +
        int(total)
    ), 5)[-5:]

    input = [number_authorization, number, nit, date, total]
    idx = 0
    for i in range(5):
        code += input[i] + dosage_key[idx:idx + 1 + int(vf[i])]
        idx += 1 + int(vf[i])
    code = arc4(code, dosage_key + vf)

    final_sum = 0
    total_sum = 0
    partial_sum = [0, 0, 0, 0, 0]
    for i in range(len(code)):
        partial_sum[i % 5] += ord(code[i])
        total_sum += ord(code[i])
    for i in range(5):
        final_sum += math.floor((total_sum * partial_sum[i]) / (1 + int(vf[i])))

    matched = []
    for regexp in re.findall('.{2}', arc4(base64(final_sum), dosage_key + vf)):
        matched.append(regexp)
    code = '-'.join(matched)

    return code


def get_qr_code(setting, nit_client, code_control, total, invoice, id):
    monto = str(total)
    nit = setting.nit
    nit = str(nit)  # nit o ci
    ndf = str(invoice.nro)
    nda = str(setting.nro_authorization)
    fde = str(invoice.register_at.strftime('%d/%m/%Y'))
    ibpcf = monto
    nit_c = str(nit_client)
    i_c_t = 0
    ivng = 0
    inscf = 0
    dbr = 0
    text_value = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (
        nit, ndf, nda, fde, monto, ibpcf, code_control, nit_c, i_c_t, ivng, inscf, dbr)
    build_picture_qr(text_value, id, 'billing')
    return text_value


def build_picture_qr(qr_string, file_name, type):
    qrw = QrCodeWidget(qr_string, barBorder=1)
    b = qrw.getBounds()
    w = b[2] - b[0]
    h = b[3] - b[1]
    d = Drawing(480, 480, transform=[480. / w, 0, 0, 480. / h, 0, 0])
    d.add(qrw)
    dir = settings.BASE_DIR

    default_folder = ''
    if type == 'donor':
        default_folder = 'media/donor'
    elif type == 'billing':
        default_folder = 'media/billing'
    elif type == 'bag':
        default_folder = 'media/bag'
    elif type == 'extraction':
        default_folder = 'media/extraction'
    elif type == 'clinical-history':
        default_folder = 'media/clinical-history'
    elif type == 'protocol-serology':
        default_folder = 'media/protocol-serology'
    elif type == 'distribution':
        default_folder = 'media/distribution'
    elif type == 'apheresis':
        default_folder = 'media/apheresis'

    d.save(formats=['png'], outDir=os.path.join(dir, default_folder), fnRoot=str(file_name))


def build_picture_barcode(text, file_name, label):
    new_text = text
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(new_text, writer=ImageWriter(), )
    module_with = 0.6
    if len(new_text) == 4:
        module_with = 0.9

    fullname = ean.save('media/extraction/' + file_name,
                        options={'write_text': False, 'text': label, 'font_size': 12,
                                 'module_width': module_with, },
                        text=False)
def build_picture_barcode_bg(text, file_name):
    text_0_missing = 14 - len(text)
    new_text = '01' + (text_0_missing * '0') + text
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(new_text, writer=ImageWriter(), )
    module_with = 0.6
    if len(new_text) == 4:
        module_with = 0.9

    fullname = ean.save('media/laboratory/' + file_name,
                        options={'write_text': False, 'text': new_text, 'font_size': 12,
                                 'module_width': module_with, },
                        text=False)
def build_picture_barcode_prod_bg(text, file_name):
    new_text = '0' + text
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(new_text, writer=ImageWriter(), )
    module_with = 0.6
    if len(new_text) == 4:
        module_with = 0.9

    fullname = ean.save('media/laboratory/' + file_name,
                        options={'write_text': False, 'text': new_text, 'font_size': 12,
                                 'module_width': module_with, },
                        text=False)
