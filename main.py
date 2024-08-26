import cv2
import numpy as np
import types
from google.colab.patches import cv2_imshow 
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
                px[2] = int(b[:-1] + binSecretMsg(dataIndex),2)
                dataIndex += 1
            # Data encoded? Break out of the loop
            if(dataIndex >= dataLen):
                break
    return img