"""
Problem statement:PDF viewer and editor with offline dictionary
"""



import json
from difflib import get_close_matches #used to find matching word from file
import pyttsx3 #text to speech conversion which works offline
import PyPDF2
from PyPDF2 import PdfFileWriter , PdfFileReader

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 110)
def speak(item):
    engine.say(item)
    engine.runAndWait()

data = json.load(open("Dict.json"))#it opens the file
def translate(word):
    word = word.lower()#if user types word in uppercase
    print("You searched for:",word)
    if word in data:
        return data[word]
    elif len(get_close_matches(word,data.keys()))>0:
        yn = input( "Did you mean %s instead Enter Y if Yes and N if No:" % get_close_matches(word,data.keys())[0])

        if yn=="Y" or yn == "y":
            return data[get_close_matches(word,data.keys())[0]]
        elif yn == "N" or yn == "n":
            return "Word doesn't exist"
        else:
            return "We didn't get your entry"
    else:
        return "Word doesn't exist"  #If user type an word which has no meaning


def rotator(input_pdf, output_file):
    pdf_in = open(input_pdf, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum) #search if a page isn't in portrait mode
        page.rotateClockwise(270)  #rotate page to 270 degree right
        pdf_writer.addPage(page) #Add a page in normal orientation

    pdf_out = open(output_file, 'wb')
    pdf_writer.write(pdf_out)#it will write  cahnges done in the pdf
    pdf_out.close()
    pdf_in.close()


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


def create_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)

def add_encryption(input_pdf, output_pdf, password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    pdf_writer.encrypt(user_pwd=password, owner_pwd=None,
                       use_128bit=True)

    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)


choice = int(input("1.OFFLINE DICTIONARY\n2.PDF EDITOR\n :- "))
if choice == 1:
    speak("INITIALIZING DICTONARY....")
    word = input("Enter a word\n")
    print(translate(word))
    # speak(translate(word))

else:
    speak("INITIALIZING PDF EDITOR.....")
    while(1):
        choice1=int(input("1.Press 1 To ROTATE pdf\n2.Press 2 to MERGE pdf\n3.Press 3 to WATERMARK\n4. Press 4 to ENCRYPT\n5. BREAK\n"))
        if choice1 == 1:
            try:
                rotator('1.pdf','Rotate.pdf')
            except exception as e:
                print("ERROR")
        elif choice1 == 2:
            paths = ['1.pdf', '4.pdf', '2.pdf', '3.pdf']
            merge_pdfs(paths, output='Merged.pdf')
        elif choice1 == 3:
            create_watermark(
                input_pdf='4.pdf',
                output='watermarked_notebook.pdf',
                watermark='1.pdf')
        elif choice1 == 4:
            add_encryption(input_pdf='4.pdf',
                           output_pdf='reportlab-encrypted.pdf',
                           password='1234')
        elif choice1 == 5:
            break