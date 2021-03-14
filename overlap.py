
# CV and ML Libraries
from logo_blend import logo_create
import os
import csv
import config

inputICs = r'./component-annotations'
inputLogos = r'./ocr-annotations'
'''
Section of Code dealing with Auditing Info
'''
# Initiate an Audit File
'''

def createAuditFile():
    auditFile = open("audit.txt", "w")
    logoAuditFile = open("logo.txt", "a")
    auditFile.close()
    logoAuditFile.close()

# Start the Audit Process


def initiateAudit(fileName):
    auditFile = open("audit.txt", "a")

    auditFile.writelines(
        "**********************************************************\n")
    auditFile.writelines("File Name: "+str(fileName))
    auditFile.writelines("\n\n")
    auditFile.close()

# Record the Data for Audit


def recordForAudit(line, header):
    auditFile = open("audit.txt", "a")

    auditFile.writelines(str(header)+":")
    auditFile.writelines("\n")

    auditFile.writelines(str(line))
    auditFile.writelines("\n")

    auditFile.close()

# Call Audit on IC and Logo Data


def audit(ics, logos):
    recordForAudit(ics, "ICs")
    recordForAudit(logos, "Logos")

'''
'''
End of the Audit Section
'''


def extractRectVertices(vertices):
    vertices = vertices.replace('[', '')
    vertices = vertices.replace(']', '')
    vertices = vertices.replace(' ', '')

    v = []

# (0,8) because some components are annotated with a Polygon
# rather than a Rectanlgle. We dont want those polygons for now.
    for k in range(0, 8):
        v.append(vertices.split(',')[k])
    return v


def extractVertices(vertices):
    vertices = vertices.replace('[', '')
    vertices = vertices.replace(']', '')
    vertices = vertices.replace(' ', '')

    v = []
    vert = vertices.split(',')

    x = []
    y = []

    k = 0
    while k < len(vert)-1:
        x.append(vert[k])
        k = k+1
        y.append(vert[k])
        k = k+1

    x.sort()
    y.sort()
    v = [x[0], y[len(y)-1], x[0], y[0], x[len(x)-1],
         y[len(y)-1], x[len(x)-1], y[0]]
    return v


def isLogoInIC(vertIC, vertLogo):
    vertICX = [int(vertIC[0].strip()), int(vertIC[2].strip()),
               int(vertIC[4].strip()), int(vertIC[6].strip())]
    vertICY = [int(vertIC[1].strip()), int(vertIC[3].strip()),
               int(vertIC[5].strip()), int(vertIC[7].strip())]
    vertICX.sort()
    vertICY.sort()
    vertLogoX = [int(vertLogo[0].strip()), int(vertLogo[2].strip()), int(
        vertLogo[4].strip()), int(vertLogo[6].strip())]
    vertLogoY = [int(vertLogo[1].strip()), int(vertLogo[3].strip()), int(
        vertLogo[5].strip()), int(vertLogo[7].strip())]
    vertLogoX.sort()
    vertLogoY.sort()

    ret = (vertICX[0] <= vertLogoX[0]) and (
        vertICY[2] >= vertLogoY[2]) and (
            vertICX[2] >= vertLogoX[2]) and (
                vertICY[0] <= vertLogoY[0])
    return ret


def identifyOverlaps():

    # createAuditFile()
    global countr
    for icCSV in os.listdir(inputICs):
        # This Block executes once per Component File
        # (Component File is the            File with IC Annotations).
        # icfile = open(inputICs+"/"+icCSV,mode='r')

        print("IC File: "+str(icCSV))

        icList = []
        logoList = []

        # with open(inputICs+"\\"+icCSV,mode='r') as icfile:
        with open(inputICs+"\\"+icCSV, mode='r') as icfile:
            # 1
            icReader = csv.DictReader(icfile, delimiter=',')

            fileName = icCSV.split("_")[0]

            # initiateAudit(fileName)

            for logoCSV in os.listdir(inputLogos):
                # This Block executes once per OCR File.
                if logoCSV.split("_")[0] == fileName:
                    with open(inputLogos+"\\"+logoCSV, mode='r') as logofile:
                        logoReader = csv.DictReader(logofile, delimiter=',')

                        for row in icReader:
                            if row["Class"] == "IC":
                                entry = {
                                    "Instance ID: ": row["Instance ID"],
                                    "Source": row["Source Image Filename"],
                                    "Vertices": row["Vertices"]}
                                icList.append(entry)

                        for row in logoReader:
                            if not row["Logo"] == "":
                                entry = {
                                    "Instance ID: ": row["Instance ID"],
                                    "Source": row["Source Image Filename"],
                                    "Vertices": row["Vertices"]}
                                logoList.append(entry)
                        # 4
            # 2

        ics = []
        logos = []

        for ic in icList:

            vertIC = extractVertices(ic.get('Vertices'))
            for logo in logoList:
                vertLogo = extractVertices(logo.get('Vertices'))
                if isLogoInIC(vertIC, vertLogo):
                    ics.append(vertIC)
                    logos.append(vertLogo)

        if len(ics) == 0 and len(logos):
            print("YO Bad luck: "+str(fileName))
            print("No ICs and Logos Overlap: "+ic.get("Source"))
        else:
            # audit(ics, logos)
            print("File is: "+str(fileName))
            logo_create(ics, logos, fileName)


if __name__ == '__main__':
    identifyOverlaps()
