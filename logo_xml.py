from xml.dom import minidom
import os

'''
The XML File Stores the Following Data:
    1) Image Name
    2) IC Image Source - FICS Dataset
    3) Logo Image Source - Fandom site
    3) Logo Name also called Logo Class
    4) Image Dimensions
    5) Logo Dimensions

<synth>
    <folder><folder>
    <file-name></file-name>
    <source>
        <ic></ic>
        <logo></logo>
    </source>
    <dimensions>
        <image>
            <height></height>
            <width></width>
        </image>
        <logo>
            <height></height>
            <width></width>
        </logo>
    </dimensions>
    <logo-coordinates>
        <vertexOne></vertexOne>
        <vertexTwo></vertexTwo>
    </logo-coordinates>
</synth>
'''

# For Testing Only. We don't use this while prepping our Data


def printAllData(imageName, logoNameClass, logo_vert, src_img_shape):
    print("Image Name: "+str(imageName))
    print("Logo Name Class: "+str(logoNameClass))
    print("Logo Vert: "+str(logo_vert))
    print("Source Image Shape: "+str(src_img_shape))


# Repository to Store the XML Files
datasetRepository = './synth_xmls'

# XML Tags
rootTag = 'synth'
folderTag = 'folder'
fileNameTag = 'file-name'
logoClassTag = 'logo-class'
sourceTag = 'source'
sourceICTag = "ic"
sourceLogoTag = "logo"
dimensionsTag = 'dimensions'
dimensionsImage = 'image'
dimnensionsLogo = 'logo'
vertexLogoOne = 'vertexOne'
vertexLogoTwo = 'vertexTwo'
logoCoordinatesLabel = 'logo-coordinates'
dimensionHeight = 'height'
dimensionWidth = 'width'


# Constants
folder = "synth_xmls"
sourceIC = "FICS Dataset"
sourceLogo = 'Fandom Site'


def fetchLogoDimensions(logo_vert):
    logo_vert = logo_vert.replace('[', '')
    logo_vert = logo_vert.replace(']', '')

    vertices = []

    for k in range(4):
        vertices.append(logo_vert.split(',')[k])

    logo_height = int(vertices[2]) - int(vertices[0])
    logo_width = int(vertices[3]) - int(vertices[1])

    return logo_height, logo_width


def fetchLogoCoordinates(logo_vert):
    logo_vert = logo_vert.replace('[', '')
    logo_vert = logo_vert.replace(']', '')
    logo_vert = logo_vert.replace(' ', '')

    vertices = []

    auditFile = open("logo.txt", "a")

    auditFile.writelines(
        "**********************************************************\n")
    auditFile.writelines("Logo Vert: "+str(logo_vert))
    auditFile.writelines("\n")

    auditFile.close()

    # print("All vertices: "+str(logo_vert))

    for k in range(4):
        vertices.append(logo_vert.split(',')[k])

    return vertices[0], vertices[1], vertices[2], vertices[3]


def prepareDataSet(imageName, logoNameClass, logo_vert, src_img_shape):
    '''
    Image Name: imageName
    Class of the Logo: logoNameClass
    logo_vert: Vertices of Logo to Compute the Logo Dimensions
    src_img_shape: Shape of the Image
    '''

    # print("Inside Prep Dataset")
    # printAllData(imageName, logoNameClass,logo_vert, src_img_shape)

    # Initiate Document
    xmlFile = minidom.Document()

    # Create Root Tag
    xmlRoot = xmlFile.createElement(rootTag)

    xmlFolder = xmlFile.createElement(folderTag)

    xmlFolderTxt = xmlFile.createTextNode(folder)
    xmlFolder.appendChild(xmlFolderTxt)

    xmlRoot.appendChild(xmlFolder)

    xmlFileName = xmlFile.createElement(fileNameTag)
    fileNameTxt = xmlFile.createTextNode(imageName)
    xmlFileName.appendChild(fileNameTxt)
    xmlRoot.appendChild(xmlFileName)

    # Logo Class
    xmlLogoClassTag = xmlFile.createElement(logoClassTag)

    logoClassTagXML = xmlFile.createTextNode(str(logoNameClass.split(".")[0]))
    xmlLogoClassTag.appendChild(logoClassTagXML)

    xmlRoot.appendChild(xmlLogoClassTag)

    # Source Tag
    xmlSource = xmlFile.createElement(sourceTag)

    # Add Subtags for Source
    xmlSourceICTag = xmlFile.createElement(sourceICTag)  # IC Tag
    xmlSourceLogoTag = xmlFile.createElement(sourceLogoTag)  # Logo Tag

    sourceICTxt = xmlFile.createTextNode(sourceIC)
    sourceLogoTxt = xmlFile.createTextNode(sourceLogo)

    xmlSourceICTag.appendChild(sourceICTxt)
    xmlSourceLogoTag.appendChild(sourceLogoTxt)

    xmlSource.appendChild(xmlSourceICTag)
    xmlSource.appendChild(xmlSourceLogoTag)

    xmlRoot.appendChild(xmlSource)

    xmlDimensions = xmlFile.createElement(dimensionsTag)

    # Add Subtags for Dimensions
    xmlDimensionsImage = xmlFile.createElement(dimensionsImage)
    xmlDimensionsLogo = xmlFile.createElement(dimnensionsLogo)

    xmlDimensionLogoHeight = xmlFile.createElement(dimensionHeight)
    xmlDimensionLogoWeight = xmlFile.createElement(dimensionWidth)

    xmlDimensionICHeight = xmlFile.createElement(dimensionHeight)
    xmlDimensionICWeight = xmlFile.createElement(dimensionWidth)

    icHeightTxt = xmlFile.createTextNode(str(src_img_shape[0]))
    icWidthTxt = xmlFile.createTextNode(str(src_img_shape[1]))

    xmlDimensionICHeight.appendChild(icHeightTxt)
    xmlDimensionICWeight.appendChild(icWidthTxt)

    xmlDimensionsImage.appendChild(xmlDimensionICHeight)
    xmlDimensionsImage.appendChild(xmlDimensionICWeight)

    # Logo Details
    logo_height, logo_width = fetchLogoDimensions(str(logo_vert))
    vert0, vert1, vert2, vert3 = fetchLogoCoordinates(str(logo_vert))

    logoHeightTxt = xmlFile.createTextNode(str(logo_height))
    logoWidthTxt = xmlFile.createTextNode(str(logo_width))

    xmlDimensionLogoHeight.appendChild(logoHeightTxt)
    xmlDimensionLogoWeight.appendChild(logoWidthTxt)

    xmlDimensionsLogo.appendChild(xmlDimensionLogoHeight)
    xmlDimensionsLogo.appendChild(xmlDimensionLogoWeight)

    # Logo Vertices
    nodeVertexOne = xmlFile.createElement(str(vertexLogoOne))
    nodeVertexTwo = xmlFile.createElement(str(vertexLogoTwo))

    logoVertexOne = [vert0, vert1]
    logoVertexTwo = [vert2, vert3]

    txtVertexOne = xmlFile.createTextNode(str(logoVertexOne))
    txtVertexTwo = xmlFile.createTextNode(str(logoVertexTwo))

    nodeVertexOne.appendChild(txtVertexOne)
    nodeVertexTwo.appendChild(txtVertexTwo)

    logoCoordinates = xmlFile.createElement(str(logoCoordinatesLabel))
    logoCoordinates.appendChild(nodeVertexOne)
    logoCoordinates.appendChild(nodeVertexTwo)

    xmlDimensions.appendChild(xmlDimensionsImage)
    xmlDimensions.appendChild(xmlDimensionsLogo)

    xmlRoot.appendChild(xmlDimensions)
    xmlRoot.appendChild(logoCoordinates)

    xmlFile.appendChild(xmlRoot)

    xmlWrite = xmlFile.toprettyxml(indent="\t")

    # Create if Not Exists
    if not os.path.exists(datasetRepository):
        os.makedirs(datasetRepository)

    filePath = datasetRepository+"//"+imageName.split(".")[0]+".xml"
    # print("File path: "+filePath)

    # Write the Data to XML
    with open(filePath, "w") as f:
        f.write(xmlWrite)
