import subprocess
import gzip
from xml.dom import minidom

def search_safety_planes(name_file):
    f = gzip.open('/programs/' +  name_file, 'rb')
    xmldoc = minidom.parseString(f.read())
    safetySettings = xmldoc.getElementsByTagName('SafetySettings')
    if (safetySettings.length > 0):
        if (safetySettings[0].childNodes.length > 0):
            tomlText = safetySettings[0].childNodes[0].nodeValue
            fileList = tomlText.splitlines()
            toReturn = "["
            for i in range(0,7):
                name = '[SafetyLimits BoundaryPlane%d]' % i
                planeIndex = [i for i, s in enumerate(fileList) if name in s]
                if (len(planeIndex) > 0):
                    planeIndex = planeIndex[0]
                    while(1):
                        planeIndex += 1
                        if 'planeNormal' in fileList[planeIndex]:
                            array = fileList[planeIndex].replace(' ', '').split('=')[1][1:-1]
                            toReturn += '['
                            for number in array.split(','):
                                if 'E' in number:
                                    subnumber = number.split('.')
                                    if len(subnumber) > 0:
                                        number = subnumber[0]
                                toReturn += str(number) + ","
                        elif 'distanceToOrigin' in fileList[planeIndex]:
                            toReturn += fileList[planeIndex].replace(' ', '').split('=')[1] + '],'
                        elif (planeIndex > len(fileList) or fileList[planeIndex] == ''):
                            break
            toReturn = toReturn[:-1] + ']'
            return toReturn
    return '[]'
