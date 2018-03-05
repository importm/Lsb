#!/usr/bin/python
#-*- coding:utf-8 -*-
from PIL import Image

def encodeDataInImage(image, data):
    def makeImageEven(image):
        pixels = list(image.getdata())
        evenPixels = [(r>>1<<1, g>>1<<1, b>>1<<1, t>>1<<1)for[r, g, b, t] in pixels]
        evenImage = Image.new(image.mode, image.size)
        evenImage.putdata(evenPixels)
        return evenImage
    def constLenBin(int):
        binary = "0" * (8 - (len(bin(int)) - 2)) + bin(int).replace('0b', '')
        return binary
    evenImage = makeImageEven(image)
    binary = ''.join(map(constLenBin, bytearray(data, 'utf-8')))
    if len(binary) > len(image.getdata()) * 4:
        raise Exception("Error: Can't encode more than" + len(evenImage.getdata()) * 4 + "bits in this image.")
    encodedPixels = [(r+int(binary[index*4+0]),g+int(binary[index*4+1]),b+int(binary[index*4+2]),t+int(binary[index*4+3])) if index*4 < len(binary) else (r,g,b,t) for index,(r,g,b,t) in enumerate(list(evenImage.getdata()))]
    encodedImage = Image.new(evenImage.mode, evenImage.size)
    encodedImage.putdata(encodedPixels)
    return encodedImage

def decodeImage(image):
    def binaryToString(binary):
        index = 0
        string = []
        rec = lambda x, i: x[2:8] + (rec(x[8:], i-1) if i > 1 else '') if x else ''
        fun = lambda x, i: x[i+1:8] + rec(x[8:], i-1)
        while index + 1 < len(binary):
            chartype = binary[index:].index('0')
            length = chartype*8 if chartype else 8
            string.append(chr(int(fun(binary[index:index+length],chartype),2)))
            index += length
        return ''.join(string)
    pixels = list(image.getdata())
    binary = ''.join([str(int(r>>1<<1!=r))+str(int(g>>1<<1!=g))+str(int(b>>1<<1!=b))+str(int(t>>1<<1!=t)) for (r,g,b,t) in pixels])  
    locationDoubleNull = binary.find('0000000000000000')
    endIndex = locationDoubleNull+(8-(locationDoubleNull % 8)) if locationDoubleNull%8 != 0 else locationDoubleNull
    data = binaryToString(binary[0:endIndex])
    return data


# 写入实例 encodeDataInImage(Image.open("coffee.png"), '你好世界，Hello world!').save('encodeImage.png')
# 读取实例 print(decodeImage(Image.open("encodeImage.png")))
