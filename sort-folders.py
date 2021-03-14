import cv2
import numpy as np
from PIL import Image
import os
from os import listdir

#Define Input and Output Folders
inputDirectory = r'.\Logos'
outputDirectory = r'.\sorted-logos'
testOutputDirectory = r'.\sorted-logos-test'


#Define Directory HIerarchies
#First Hierarchy
squareDir = "squareImages"
rectangleDir = "rectangleImages"

#Second Hierarchy
categoryA = "A-BothAreLessThan50px" #Both Height and Width are < 50px
categoryB = "B-LengthIsLarger" #Larger Length. Height is less than 50px
categoryC = "C-HeightisLarger" #Larger Height. Width is less than 50px
categoryD = "D-BothAreLarge" #Both are Larger than 50px


def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def createAllDirectories():
    createDirectory(outputDirectory)

    createDirectory(outputDirectory+"\\"+squareDir)
    createDirectory(outputDirectory+"\\"+rectangleDir)

    createDirectory(outputDirectory+"\\"+squareDir+"\\"+categoryA)
    createDirectory(outputDirectory+"\\"+squareDir+"\\"+categoryB)
    createDirectory(outputDirectory+"\\"+squareDir+"\\"+categoryC)
    createDirectory(outputDirectory+"\\"+squareDir+"\\"+categoryD)
    createDirectory(outputDirectory+"\\"+rectangleDir+"\\"+categoryA)
    createDirectory(outputDirectory+"\\"+rectangleDir+"\\"+categoryB)
    createDirectory(outputDirectory+"\\"+rectangleDir+"\\"+categoryC)
    createDirectory(outputDirectory+"\\"+rectangleDir+"\\"+categoryD)


def sort():
    #createAllDirectories()
    createDirectory(outputDirectory)
    createDirectory(testOutputDirectory)

    auditFile = open("audit.txt", "w")
    auditFile.close()

    for dir in os.listdir(inputDirectory):
        for file in os.listdir(inputDirectory+"\\"+dir):
            firstHierarchy = ""
            secondHierarchy = ""


            fileName = inputDirectory + "\\" + dir + "\\" + file
            image = Image.open(fileName)
            image = np.array(image.convert('RGB'))
            image = image[:, :, ::-1].copy()

            height, width = image.shape[:2]

            aspectRatio = height/width

            if aspectRatio < 1.2 and aspectRatio > 0.8:
                firstHierarchy = squareDir
            else:
                firstHierarchy = rectangleDir

            createDirectory(outputDirectory+"\\"+firstHierarchy)
            createDirectory(testOutputDirectory+"\\"+firstHierarchy)


            if height<50 and width<50:
                secondHierarchy = categoryA
            elif height<50 and width >=50:
                secondHierarchy = categoryB
            elif height >= 50 and width < 50:
                secondHierarchy = categoryC
            else:
                secondHierarchy = categoryD

            createDirectory(outputDirectory+"\\"+firstHierarchy+"\\"+secondHierarchy)
            createDirectory(testOutputDirectory+"\\"+firstHierarchy+"\\"+secondHierarchy)


            finalRepo = outputDirectory+"\\"+firstHierarchy+"\\"+secondHierarchy+"\\"+dir
            createDirectory(finalRepo)


            #cv2.imshow('img',image)
            #cv2.waitKey(0)

            cv2.imwrite(finalRepo+"\\"+file,image)

            auditFile = open("audit.txt", "a")
            line = "Manufacturer Name: "+str(dir)+" "+"Image Dimensions: Height: "+str(height)+" Width: "+str(width)+" "+"Aspect ratio: "+str(aspectRatio)+" "+"First Hierarchy: "+str(firstHierarchy)+" "+"Second Hierarchy: "+str(secondHierarchy)
            auditFile.writelines(line)
            auditFile.writelines("\n")
            auditFile.close()

            finalRepo = testOutputDirectory+"\\"+firstHierarchy+"\\"+secondHierarchy
            cv2.imwrite(finalRepo+"\\"+str(dir)+".png",image)

            print("Image Data: "+line)

if __name__ == '__main__':
    sort()
