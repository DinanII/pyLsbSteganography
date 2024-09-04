import sys
import cv2
import numpy as np
import types
from tkinter import Tk
from tkinter import filedialog
from tkinter import simpledialog
# ===========================
#
#   Helper Functions
#
# ===========================
def askForString(msg,isDialogue = False):
    isValid = False
    uInput = ''
    while(not isValid):
        if (not isDialogue):
            print(msg)
            uInput = input()
        else:
            Tk().withdraw()
            uInput = simpledialog.askstring("Input",msg)
        if(uInput != ''):
            return uInput

# Requires actual img from cv2.imread
def showImg(img):
    resizedImg = cv2.resize(img,(500,500))
    cv2.imshow('image',resizedImg)
    cv2.waitKey(0)

# Waits until the user submit the input
def waitForUsr(msg = "Press <Enter> to proceed.>"):
    print(msg)
    input()


# ===========================
#
#   Code & Decoding
#
# ===========================
def decodeToBinary(msg):
    if (type(msg) == str):
        return ''.join([format(ord(i),"08b") for i in msg])
    elif (type(msg) == bytes or type(msg) == np.ndarray):
        return [format(i,"08b") for i in msg]
    elif(type(msg) == int or type(msg) == np.uint8):
        return format(msg,"08b")
    else:
        raise TypeError("The submitted input type is not supported.")


# Hides the secret message into the image
def hideData(img, secretMsg):
    # Calculating the maximum bytes to encode into binary
    nBytes = img.shape[0] * img.shape[1] * 3 // 8
    
    # Checks if the secretMsg is larger than the image size and raises a error if so.
    if(len(secretMsg) > nBytes):
        raise ValueError('Image has insufficient bytes. Minify your data or submit a bigger image')
    
    secretMsg += "#####"

    # Initialization for hiding msg into binary
    dataIndex = 0
    binSecretMsg  = decodeToBinary(secretMsg)
    dataLen = len(binSecretMsg)

 # This loop hides the message in the image by altering the LSB's
    for vals in img:
        for px in vals:
            # Convert RGB vals to binary format
            r, g, b = decodeToBinary(px)

            # Modify the LSB only if there's data to store
            if(dataIndex < dataLen):
                # Hide data into the LSB of red pixel
                px[0] = int(r[:-1] + binSecretMsg[dataIndex],2)
                dataIndex += 1
            if(dataIndex < dataLen):
                # Hide data into the LSB of green pixel
                px[1] = int(g[:-1] + binSecretMsg[dataIndex],2)
                dataIndex += 1
            if(dataIndex < dataLen):
                # Hide data into the LSB of blue pixel
                px[2] = int(b[:-1] + binSecretMsg[dataIndex], 2)
                dataIndex += 1
            # Data encoded? Break out of the loop
            if(dataIndex >= dataLen):
                break
    return img

def showData(img):
    binData = ""
    for vals in img:
        for px in vals:
            # Convert rgb vals into binary
            r, g, b = decodeToBinary(px)

            # Extracting data from the LSB's
            binData += r[-1] 
            binData += g[-1]
            binData += b[-1]

    # Split by 8-bits
    allBytes = [binData[i: i+8] for i in range(0, len(binData), 8)]

    # Convert from bits to chars
    decodedData = ""
    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        if decodedData[-5:] == "#####":  # Checks if we reached delimiter, which is #####
            break

    return decodedData[:-5]  # Removes delimiter to show original hidden output


# ===========================
#
#   Input & Output
#
# ===========================
def encodeText():
    imgName = openFilePicker(dialogTitle = "Choose image to hide data in.") #askForString('Enter image name inputwith extension')
    if(not imgName):
        steganography()
        return
    img = cv2.imread(imgName) # Read the image input using openCV-Python
    # Librart of Python bindings designed to solce coputer vision problems

    # print('Shape of the img: ',img.shape)
    # print('Resized varient of submitted img: ')


    data = askForString("Enter data that should be encoded / hidden into the img: ",True)
    if(len(data) == 0):
        raise ValueError("Data is empty")

    #fileName = askForString("Enter the name of new encoded image with extension: ")
    Tk().withdraw()
    path = filedialog.asksaveasfilename(title = "Enter filename to save encoded img", defaultextension=".png", filetypes=[("PNG file", "*.png")])
    encodedImg = hideData(img, data) # Call to hideData to hide secret msg.
    cv2.imwrite(path,encodedImg)


def decodeText():
    imgName = openFilePicker(dialogTitle = "Choose steganographed image to decode ") #askForString("Enter the name of the steganographed img that you want to decode with extension: ")
    if(not imgName):
        steganography()
        return
    img = cv2.imread(imgName)
    txt = showData(img)
    print(txt)
    waitForUsr()

def openFilePicker(fileTypes=[('Image Files', '*.png')],dialogTitle="Choose a file"):
    Tk().withdraw() 
    filePath = filedialog.askopenfilename(filetypes = fileTypes,title=dialogTitle)
    if(filePath):
        isValid = True
        print("FilePath: "+filePath)
        return filePath

def dialogueTest():
    Tk().withdraw()
    uInput = simpledialog.askstring("Title","Prompt")
    print(uInput)
    

def steganography():
    print("========================================")
    print("Image Steganography")
    print("========================================")
    print()
    print("Hide or retrieve a hidden message from an image.")
    print("Please note en- and decoding can take a while.")
    print("Choose one of the following options to proceed")
    print()
    print("0. Quit program")
    print("1. Encode data into image")
    print("2. Decode data from image")
    print("3. input dialogue test")
    uChoice = askForString("Enter a choice: ")
    match uChoice:
        case "0":
            return
        case "1":
            encodeText()
        case "2":
            decodeText()
        case "3":
            dialogueTest()
    steganography()

steganography()