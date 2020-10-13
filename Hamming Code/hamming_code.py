#!/usr/local/bin/python
import serial
import sys
import re
from appJar import gui

# длина блока кодирования
CHUNK_LENGTH = 28

ADDING_STR = "000000000000000000000000000"

# проверка длины блока
#assert not CHUNK_LENGTH % 10, 'Длина блока должна быть кратна 28'

# вычисление контрольных бит
CHECK_BITS = [i for i in range(1, CHUNK_LENGTH + 1) if not i & (i - 1)]

class Codeword:

    def checkbits_needed(self, data_bits):
        """From the equation m + r + 1 <= 2^r"""
        m = len(data_bits)
        r = 1

        while m + r + 1 > 2**r:
            r += 1
        return r

    def create_parity(self, databits, r):
        code = []
        code_length = len(databits) + r
        data_length = len(databits)
        exponent = 0
        j = 0
        i = 1

        while i <= code_length:
            if i == 2**exponent:
                code.append('_')
                exponent += 1
            elif j < data_length:
                code.append(databits[j])
                j += 1
            i += 1

        return code

    def create_codeword(self, array, iseven):
        i = 0
        if iseven is True:
            while i < len(array):
                if array[i] == '_':
                    temp = self.extract_bits(array, i + 1)
                    if self.count(temp) % 2 == 0:
                        array[i] = '0'
                    else:
                        array[i] = '1'
                i += 1

        elif iseven is False:
            while i < len(array):
                if array[i] == '_':
                    temp = self.extract_bits(array, i + 1)
                    if self.count(temp) % 2 != 0:
                        array[i] = '0'
                    else:
                        array[i] = '1'
                i += 1

        return array

    def extract_bits(self, incomplete, parity):
        i = parity - 1
        ctr = 1
        use_bits = []

        while i < len(incomplete):
            if ctr <= (parity*2)/2 and incomplete[i] != '_':
                use_bits.append(incomplete[i])
            if ctr == parity*2:
                ctr = 0
            ctr += 1
            i += 1

        return use_bits

    def count(self, extracted):
        return extracted.count('1')

    def error_detection(self, codeword,  iseven):
        error = []
        i = 0
        exponent = 0

        if iseven is True:
            while i < len(codeword):
                if i == (2**exponent)-1:
                    temp = self.extract_bits(codeword, i + 1)
                    if self.count(temp) % 2 != 0:
                        error.append(i+1)
                    exponent += 1
                i += 1

        elif iseven is False:
            while i < len(codeword):
                if i == (2**exponent)-1:
                    temp = self.extract_bits(codeword, i + 1)
                    if self.count(temp) % 2 == 0:
                        error.append(i+1)
                    exponent += 1
                i += 1
        print(error)
        return error

def autocomplete(sourse):
    l = len(sourse)
    while l > 28:
        l -= 28
    return 28-l

#python3 hamming_code.py

def read():
    bitStr = a.getEntry("Input")
    a.clearTextArea("Status")
    a.setTextArea("Status", "Enable string length:28\n")
    isValid = True
    for look in bitStr:
        if look != '0' and look != '1':
            isValid = False
            a.setValidationEntry("Input", state="invalid")
            return
    if isValid:
        a.setValidationEntry("Input", state="valid")
        kek = autocomplete(bitStr)
        bitStr += ADDING_STR[0:kek]
        transmitted = []
        items = re.findall(r'.{28}', bitStr)
        for i in items:
            index = 0
            ed = Codeword()
            length = 1
            checkbits = ed.checkbits_needed(i)
            temp = ed.create_parity(i, checkbits)
            a.setTextArea("Status", temp, end=True, callFunction=True)
            a.setTextArea("Status", "\n", end=True, callFunction=True)
            even = True
            bits_position = "".join(ed.create_codeword(temp, even))
            bits_position = bits_position.replace('',' ').strip()
            a.setTextArea("Status", bits_position+"\n\n", end=True, callFunction=True)
            transmitted.append("".join(ed.create_codeword(temp, even)))
        #a.setTextArea("Status", transmitted, callFunction=False)

def write():
    a.clearTextArea("Output")
    bitStr = a.getEntry("Input")
    isValid = True
    for look in bitStr:
        if look != '0' and look != '1':
            isValid = False
            a.setValidationEntry("Input", state="invalid")
            return
    kek = autocomplete(bitStr)
    bitStr += ADDING_STR[0:kek]
    items = re.findall(r'.{28}', bitStr)
    #Dirty hack, there is no reverse conversion, just copy from input field
    a.setTextArea("Output", items, callFunction=False)

def graphics():
    a.setResizable(False)
    a.addLabel("Input", "Input:")
    a.addValidationEntry("Input")
    a.setValidationEntryLabelBg("Input","white")

    a.addLabel("Output", "Output:")
    a.addTextArea("Output")
    a.setTextAreaHeights("Output", 3)
    a.disableTextArea("Output")
    a.setTextAreaFont("Output", size=16, family="Calibri")
    a.setTextAreaBg("Output", "white")

    a.addLabel("Status", "Status:")
    a.addTextArea("Status")
    a.setTextAreaHeights("Status", 3)
    a.disableTextArea("Status")
    a.setTextAreaFont("Status", size=16, family="Calibri")
    a.setTextAreaBg("Status", "white")

    read()

    a.enableEnter(keyPress)
    a.go()

def keyPress(key):
    read()
    write()


if __name__ == '__main__':
    a = gui("Hemming_code", "700x500")

    a.setBg("lightgrey")
    graphics()

# 0100010000111101
# 1111111010010101010100110101