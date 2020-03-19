from array import array
import math

def get_Coordenates (positions):

    weight, height = 6, 3
    toDegree = 180 / math.pi
    results  = [[0 for x in range(height)] for y in range(weight)]

    #positionsString1 = positionsString.replace("[", "")
    #positionsString2 = positionsString1.replace("]", "")
    #positions = positionsString2.split(",")
	
    for w in range(0, weight):
        positions[w] = float(positions[w])
        if w == 0:   # BASE
            results[w][0] =   0.0 #x
            results[w][1] =   0.0 #y
            results[w][2] =   0.0 #z
        elif w == 1: # SHOULDER
            varphi = (positions[0] * toDegree) + 270
            theta  = 90
            r      = 0.12

            theta = math.radians(theta)
            varphi = math.radians(varphi)

            results[w][0] =   r * math.sin(theta) * math.cos(varphi) #x
            results[w][1] =   r * math.sin(theta) * math.sin(varphi) #y
            results[w][2] =   r * math.cos(theta) #z

        elif w == 2: # ELBOW
            theta  = positions[1] * toDegree + 90
            if theta < 0:
                theta = abs(theta)
                varphi = (positions[0] * toDegree) + 270 + 90
            else:
                varphi = (positions[0] * toDegree) + 270 - 90

            r      = 0.244

            theta = math.radians(theta)
            varphi = math.radians(varphi)

            results[w][0] =   results[w - 1][0] +  r * math.sin(theta) * math.cos(varphi) #x
            results[w][1] =   results[w - 1][1] +  r * math.sin(theta) * math.sin(varphi) #y
            results[w][2] =   results[w - 1][2] +  r * math.cos(theta) #z

        elif w == 3: # WRIST 1
            theta  = (positions[2] + positions[1]) * toDegree + 90
            if theta < 0:
                theta = abs(theta)
                varphi = (positions[0] * toDegree) + 270 + 90
            else:
                varphi = (positions[0] * toDegree) + 270 - 90
            r      = 0.213


            theta = math.radians(theta)
            varphi = math.radians(varphi)

            results[w][0] =   results[w - 1][0] +  r * math.sin(theta) * math.cos(varphi) + 0.093 * math.cos(math.radians((positions[0] * toDegree) + 90)) #x
            results[w][1] =   results[w - 1][1] +  r * math.sin(theta) * math.sin(varphi) + 0.093 * math.sin(math.radians((positions[0] * toDegree) + 90)) #y
            results[w][2] =   results[w - 1][2] +  r * math.cos(theta) #z
        elif w == 4: # WRIST 2
            results[w][0] =   results[w - 1][0]  + 0.104 * math.cos(math.radians((positions[0] * toDegree) + 270))#x
            results[w][1] =   results[w - 1][1]  + 0.104 * math.sin(math.radians((positions[0] * toDegree) + 270)) #y
            results[w][2] =   results[w - 1][2]  #z
        else:        # WRIST 3
            theta  = positions[3] * toDegree + 90
            if theta < 0:
                theta = abs(theta)
                varphi = (positions[0] * toDegree) + 270 + 90
            else:
                varphi = (positions[0] * toDegree) + 270 - 90

            r      = 0.085

            theta = math.radians(theta)
            varphi = math.radians(varphi)

            results[w][0] =   results[w - 1][0] +  r * math.sin(theta) * math.cos(varphi) #x
            results[w][1] =   results[w - 1][1] +  r * math.sin(theta) * math.sin(varphi) #y
            results[w][2] =   results[w - 1][2] +  r * math.cos(theta) #z
    return results
    return 1


if __name__ == '__main__':
    positions = "[2.07, -1.05, 1.57, -1.34, -1.17, 0.61]"
    print(get_Coordenates(positions)[0])
    print(get_Coordenates(positions)[1])
    print(get_Coordenates(positions)[2])
    print(get_Coordenates(positions)[3])
    print(get_Coordenates(positions)[4])
    print(get_Coordenates(positions)[5])
