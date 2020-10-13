#!/usr/local/bin/python
import serial
import sys
from appJar import gui


def read():
    bitStr = a.getEntry("Input")
    a.clearTextArea("Status")
    a.setTextArea("Status", "Flag: 01111000\n")
    isValid = True
    for look in bitStr:
        if look != '0' and look != '1':
            isValid = False
            a.setValidationEntry("Input", state="invalid")
            return
    if isValid:
        a.setValidationEntry("Input", state="valid")
        #Флаг равен 01111000. После 7 символов (0111100) вставляем "1" независимо от 8 символа.
        bitStr = bitStr.replace("0111100", "0111100 1 ")
        a.setTextArea("Status", bitStr, callFunction = False)

def write():
    a.clearTextArea("Output")
    bitStr = a.getEntry("Input")
    isValid = True
    for look in bitStr:
        if look != '0' and look != '1':
            isValid = False
            a.setValidationEntry("Input", state="invalid")
            return
    bitStr = bitStr.replace("0111100 1 ", "0111100")
    a.setTextArea("Output", bitStr, end = False, callFunction = False)

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

a = gui("Bit Stuffing Application", "500x500")

a.setBg("lightgrey")
graphics()
