# -*- coding: utf-8 -*-
"""
@author: Paul Faugeras
paul.faugeras@gmail.com
"""

from skimage import io

#threshold for differentiation the different colors
grey_threshold=85
white_threshold=210

image=io.imread('image_example.tif')

img_1c=[]   #simplifies into b&w
for ligne in range(len(image)):
    nvelle_ligne=[]
    for pixel in range(len(image[ligne])):
        nvelle_ligne.append(image[ligne][pixel][0])
    img_1c.append(nvelle_ligne)

if len(img_1c)%18!=0:
    print("height error")
if len(img_1c[0])%12!=0:
    print("width error")

nb_img_larg = len(img_1c[0])//12
nb_img_haut = len(img_1c)//18

if nb_img_larg*nb_img_haut>6:
    print("image too big")

image_binary=[]
for ligne in range(len(img_1c)):
    for colonne in range(len(img_1c[ligne])):
        pixel=img_1c[ligne][colonne]
        if pixel<grey_threshold:
            image_binary.append("00")
        elif pixel<white_threshold:
            image_binary.append("10")
        else :
            image_binary.append("01")

image_par4=[]
for k in range(len(image_binary)//4):
    par_4=""
    for i in range(4):
        par_4+=image_binary[4*k+i]
    image_par4.append(par_4)

par_image=[]
for image_ligne in range(nb_img_haut):
    for image_col in range(nb_img_larg):
        image_part_4=[]
        for ligne in range(18):
            for col in range(3):
                image_part_4.append(image_par4[18*3*image_ligne*nb_img_larg+nb_img_larg*ligne*3+3*image_col+col]) #to modify
        par_image.append(image_part_4)

file = open("final_code.txt","w")
for bloc_image in range(len(par_image)):
    file.write("digitalWrite(MAX7456SELECT,LOW);\n")
    file.write("spi_send_byte(MAX_VM0_REG, MAX_DISABLE_DISPLAY);\n")
    file.write("spi_send_byte(MAX_CMAH_REG, 0xC")
    file.write(str(bloc_image+1))
    file.write(");\n")
    file.write("\n")
    for bloc_nb in range(len(par_image[bloc_image])):
        ligne=par_image[bloc_image][bloc_nb]
        file.write("spi_send_byte(0x0A,")
        file.write(str(bloc_nb))
        file.write(");\n")
        file.write("spi_send_byte(0x0B,0b")
        file.write(ligne)
        file.write(");\n")
    file.write("\n")
    file.write("spi_send_byte(MAX_CMM_REG,0xA0);\n")
    file.write("digitalWrite(MAX7456SELECT,HIGH);\n")
    file.write("delay(200);\n")
    file.write("\n")
file.close()