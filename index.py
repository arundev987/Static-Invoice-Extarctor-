from PIL import Image
import pytesseract
import argparse
import cv2
import os, fnmatch
import csv


def extractTextFromImage(imageURI) :
    image = cv2.imread(imageURI)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    filename = "tempImg.png"
    cv2.imwrite(filename, gray)

    img = Image.open(filename)
    pytesseract.pytesseract.tesseract_cmd = '.\\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(img)
    os.remove(filename)

    return text

def findAllImagesInPath(directory) :
    listOfFiles = os.listdir(directory)
    pattern = "*.png"
    invoiceList = []

    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            invoiceList.append(entry)

    return invoiceList


invoices = findAllImagesInPath("./invoiceImages")

print(invoices)

txtData = []
invoiceData = []

for invoice in invoices:
    txtData.append(extractTextFromImage("./invoiceImages/" + invoice))


for invoice in txtData:
    
    if "Service Fee" in invoice:
        
        cnt = 0
        
        for line in invoice.split('\n'):
            
            if cnt is 28:
                invoiceData.append(line.split(' ')[0])
                break
            else: 
                cnt = cnt + 1

    elif "Invoice number" in invoice :
        
        for line in invoice.split('\n'):
            
            if "Invoice number" in line:
                invoiceData.append(line.split(' ')[3])


with open('invoices.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["invoice"])

    for invoiceId in invoiceData:
        writer.writerow([invoiceId])
