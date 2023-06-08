import math
import time
import cv2 as cv
import numpy as np
import pyautogui

couleursColoriage = [
	[0, 80, 205], # bleu foncé
	#[255, 255, 255], # blanc
	[38, 201, 255],
	[1, 116, 32],
	[153, 0, 0],
	[150, 65, 18],
	[17, 176, 60],
	[255, 0, 19],
	[255, 120, 41],
	[176, 112, 28],
	[153, 0, 78],
	[203, 90, 87],
	[255, 193, 38],
	[255, 0, 143],
	[254, 175, 168],
	[170, 170, 170], # gris clair
	[102, 102, 102], # gris foncé 
	[0, 0, 0], # noir
]


couleursDisponibles = [
	[0, 0, 0],
	[102, 102, 102],
	[0, 80, 205],
	[255, 255, 255],
	[170, 170, 170],
	[38, 201, 255],
	[1, 116, 32],
	[153, 0, 0],
	[150, 65, 18],
	[17, 176, 60],
	[255, 0, 19],
	[255, 120, 41],
	[176, 112, 28],
	[153, 0, 78],
	[203, 90, 87],
	[255, 193, 38],
	[255, 0, 143],
	[254, 175, 168],
]

coordonneesCouleurs = [
	
	( 722, 527 ),
	#( 597, 593 ),
	( 722, 593 ),
	( 597, 658 ),
	( 662, 661 ),
	( 722, 659 ),
	( 597, 728 ),
	( 662, 727 ),
	( 722, 728 ),
	( 597, 793 ),
	( 662, 793 ),
	( 722, 809 ),
	( 597, 861 ),
	( 662, 862 ),
	( 722, 862 ),
	( 662, 592 ),
	( 662, 525 ),
	( 597, 521 ),
]

def convertir_en_pourcentage(coordonnees, largeur_ecran, hauteur_ecran):
    coordonnees_en_pourcentage = []
    for coordonnee in coordonnees:
        x_pixel, y_pixel = coordonnee
        x_percentage = (x_pixel / largeur_ecran) * 100
        y_percentage = (y_pixel / hauteur_ecran) * 100
        coordonnees_en_pourcentage.append((x_percentage, y_percentage))
    return coordonnees_en_pourcentage

def convertir_en_pixel(coordonnees, largeur_ecran, hauteur_ecran):
    coordonnees_en_pixel = []
    for coordonnee in coordonnees:
        x_percentage, y_percentage = coordonnee
        x_pixel = (x_percentage / 100) * largeur_ecran
        y_pixel = (y_percentage / 100) * hauteur_ecran
        coordonnees_en_pixel.append((x_pixel, y_pixel))
    return coordonnees_en_pixel

largeur_ecran = 2560
hauteur_ecran = 1600



#click using pyautogui
def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


def drawLine(point1, point2):
    pyautogui.moveTo(point1[0], point1[1])
    pyautogui.dragTo(point2[0], point2[1], button='left')





if __name__ == "__main__":

    # wait 5 seconds
    # time.sleep(5)

    point1 = (0, 0)
    point2 = (0, 0)

    img = cv.imread("image.png")
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    coordonnees_en_pourcentage = convertir_en_pourcentage(coordonneesCouleurs, largeur_ecran, hauteur_ecran)

    coordonnees_en_pixel = convertir_en_pixel(coordonnees_en_pourcentage, largeur_ecran, hauteur_ecran)

    # resize the image to fit bewteen the two points
    width = abs(point2[0] - point1[0])
    height = abs(point2[1] - point1[1])
    print(width, height)
    img = cv.resize(img, (width, height))

    # for each pixel, change color to the closest color in the list
    for i in range(img.rows):
        for j in range(img.cols):
            pixel = img[i, j]
            distance = 255 * 3
            colorIndex = -1
            for k in range(len(couleursDisponibles)):
                newDistance = math.sqrt(pow((pixel[0] - couleursDisponibles[k][0]), 2) + pow((pixel[1] - couleursDisponibles[k][1]), 2) + pow((pixel[2] - couleursDisponibles[k][2]), 2))

                if newDistance < distance:
                    distance = newDistance
                    colorIndex = k
            pixel[0] = couleursDisponibles[colorIndex][0]
            pixel[1] = couleursDisponibles[colorIndex][1]
            pixel[2] = couleursDisponibles[colorIndex][2]

    lines = []
    #for each rows
    for i in range(0, img.shape[0]):
        # create a start point
        startPoint = (point1[0], point1[1] + i)
        # create a end point
        endPoint = (point1[0], point1[1] + i)
        # for each columns
        for j in range(0, img.shape[1]):
            # get the pixel color
            pixel = img[i, j]
            k = j
            # loop until we find a pixel that is not the same color as the first one
            while k < img.shape[1]:
                pixel2 = img[i, k]
                if pixel[0] != pixel2[0] or pixel[1] != pixel2[1] or pixel[2] != pixel2[2]:
                    break
                k += 1
            j = k
            # update the end point
            endPoint = (point1[0] + k, point1[1] + i)
            # add the line to the list
            lines.append((pixel, (startPoint, endPoint)))
            # update the start point
            startPoint = (point1[0] + k, point1[1] + i)

    # for coord in range(len(coordonnees_en_pixel)):
    #     # click on the color
    #     click(coordonnees_en_pixel[coord][0], coordonnees_en_pixel[coord][1])

    #     # draw the lines
    #     for i in range(len(lines)):
    #         if lines[i][0] == couleursColoriage[coord]:
    #             # check if user press escape
    #             if cv.waitKey(1) == 27:
    #                 break
    #             drawLine(lines[i][1][0], lines[i][1][1])
