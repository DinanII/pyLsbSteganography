import sys
import cv2
import numpy as np
import types
# from google.colab.patches import cv2.imshow('image',
# For displaying images

# Converts data into binary from different types
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
    
    # Checks if the number of bytes to encode is less than
    # maximum bytes in the img
    if(len(secretMsg) > nBytes):
        raise ValueError('Image has insufficient bytes. Minify your data or submit a bigger image')
    
    secretMsg += "#####" # Can use any string ad delimiter

    dataIndex = 0
    binSecretMsg  = decodeToBinary(secretMsg)
    dataLen = len(binSecretMsg)

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

def encodeText():
    imgName = input('Enter image name with extension')
    img = cv2.imread(imgName) # Read the image input using openCV-Python
    # Librart of Python bindings designed to solce coputer vision problems

    print('Shape of the img: ',img.shape)
    print('Resized varient of submitted img: ')
    # resizedImg = cv2.resize(img,(500,500))
    # cv2.imshow('image',resizedImg)
    #cv2.waitKey(0) # Display img

    data = input('Enter data to be encoded...')
    if(len(data) == 0):
        raise ValueError("Data is empty")

    fileName = input("Enter the name of new encoded image with extension: ")
    encodedImg = hideData(img, data) # Call to hideData to hide secret msg.

    cv2.imwrite(fileName,encodedImg)

def decodeText():
    imgName = input("Enter the name of the steganographed img that you want to decode with extension: ")
    img = cv2.imread(imgName)
    # print('The steganographed image is as shown below: ')
    # resizedImg = cv2.resize(img,(500,500)) # Rwsize
    # cv2.imshow('image',resizedImg)
    # cv2.waitKey(0) # Display img

    txt = showData(img)
    print(txt)
    return txt


def steganography():
    print("========================================")
    print("Image Steganography")
    print("========================================")
    print("0. Quit program")
    print("1. Encode data")
    print("2. Decode data into image")
    uChoice = input("Enter a choice: ")
    match uChoice:
        case "0":
            return
        case "1":
            encodeText()
        case "2":
            decodeText()

steganography()
#https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372