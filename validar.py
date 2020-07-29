from pathlib import Path
import cv2 as cv
import glob 
import math

xi1, yi1, xf1, yf1, ca1, cl1 = [], [], [], [], [], []
xi2, yi2, xf2, yf2, ca2, cl2 = [], [], [], [], [], []

windowName = 'Imagem'
cv.namedWindow(windowName)


def areaPoligono1(X, Y, n):  
    area = 0.0 
    j = n - 1
    for i in range(0,n): 
        area += (X[j]+X[i]) * (Y[j]-Y[i]) 
        j = i  
    return int(abs(area/2.0)) 

def areaPoligono2(X, Y, n):  
    area = 0.0 
    j = n - 1
    for i in range(0,n): 
        area += (X[j]+X[i]) * (Y[j]-Y[i]) 
        j = i  
    return int(abs(area/2.0)) 

def limpaVar1():
        xi1.clear()
        yi1.clear()
        xf1.clear()
        yf1.clear()
        ca1.clear()
        cl1.clear()

def limpaVar2():
        xi2.clear()
        yi2.clear()
        xf2.clear()
        yf2.clear()
        ca2.clear()
        cl2.clear()


def main():
        path = glob.glob("Dataset/*.png")
        for i in range(1, len(path)+1):
                print('IMAGEM', i, "\n")
                image =  "Dataset/" + str(i) + ".png"
                img = cv.imread(image)
                

                path_M = "Manual/" + str(i) + ".txt" 
                path_A = "Automatico/" + str(i) + ".txt"
                path_R = "Resultados/" + str(i) + ".txt"

                f1 = open(path_M, "r")
                f2 = open(path_A, "r")
                result = open(path_R, 'w+')

                data1 = (f1.readlines())
                data2 = (f2.readlines())
                for line in data1:
                        l = line.split(" ")
                        xi1.append(int(float(l[0])))
                        yi1.append(int(float(l[1])))
                        xf1.append(int(float(l[2])))
                        yf1.append(int(float(l[3])))
                        ca1.append(float(l[4]))
                        cl1.append(float(l[5]))
                for line in data2:
                        l = line.split(" ")
                        xi2.append(int(float(l[0])))
                        yi2.append(int(float(l[1])))
                        xf2.append(int(float(l[2])))
                        yf2.append(int(float(l[3])))
                        ca2.append(float(l[4]))
                        cl2.append(float(l[5]))
                
                for x in range(0, len(xi1)):
                        cv.line(img, (xi1[x], yi1[x]), (xf1[x], yf1[x]), (255,0,0), 2)
                        cv.line(img, (xi2[x], yi2[x]), (xf2[x], yf2[x]), (0,0,255), 2)
                        det = (xf2[x]-xi2[x])*(yf1[x]-yi1[x]) - (yf2[x]-yi2[x])*(xf1[x]-xi1[x])
                        if (det == 0.0):
                                X1 = [xf1[x], xi2[x], xi1[x]]
                                Y1 = [yf1[x], yi2[x], yi1[x]]
                                n1 = len(X1)
                                X2 = [xf1[x], xi2[x], xf2[x]]
                                Y2 = [yf1[x], yi2[x], yf2[x]]
                                n2 = len(X2)  
                                areaTotal = int(areaPoligono1(X1, Y1, n1) + areaPoligono2(X2, Y2, n2))
                                print('Area', areaTotal)
                        else:
                                s = ((xf2[x]-xi2[x])*(yi2[x]-yi1[x]) - (yf2[x]-yi2[x])*(xi2[x]-xi1[x]))/det
                                t = ((xf1[x]-xi1[x])*(yi2[x]-yi1[x]) - (yf1[x]-yi1[x])*(xi2[x]-xi1[x]))/det
                                px = xi1[x] + (xf1[x]-xi1[x])*s
                                py = yi1[x] + (yf1[x]-yi1[x])*s
                                if (234 < py and py < 468) & (0 < px and px < 832):
                                        #print(px,py)
                                        X1 = [xi1[x], xi2[x], px]
                                        Y1 = [yi1[x], yi2[x], py]
                                        n1 = len(X1) 
                                        #print(areaPoligono1(X1, Y1, n1)) 
                                        X2 = [xf1[x], xf2[x], px]
                                        Y2 = [yf1[x], yf2[x], py]
                                        n2 = len(X2) 
                                        #print(areaPoligono2(X2, Y2, n2)) 
                                        areaTotal = int(areaPoligono1(X1, Y1, n1) + areaPoligono2(X2, Y2, n2))
                                        print('Area', areaTotal)
                                else:
                                        X1 = [xf1[x], xi2[x], xi1[x]]
                                        Y1 = [yf1[x], yi2[x], yi1[x]]
                                        n1 = len(X1)
                                        X2 = [xf1[x], xi2[x], xf2[x]]
                                        Y2 = [yf1[x], yi2[x], yf2[x]]
                                        n2 = len(X2)  
                                        areaTotal = int(areaPoligono1(X1, Y1, n1) + areaPoligono2(X2, Y2, n2))
                                        print('Area', areaTotal)
                        
                                distEucli = (((xi2[x]-xi1[x])**2+(yi2[x]-yi1[x])**2)**(1/2))
                                print('Distancia Euclidiana', distEucli)
                                angRetas = round(math.degrees(math.atan(abs((ca1[x]-ca2[x])/(1+(ca1[x]*ca2[x]))))), 2)
                                print('Angulo entre retas', angRetas)

                                if (ca2[x] < 0):
                                        ang = round((math.degrees(math.atan(abs(ca2[x])))), 2)
                                        print('Angulo ', ang, "\n")
                                else:
                                        ang = round(180 - (math.degrees(math.atan(ca2[x]))), 2)
                                        print('Angulo ', ang, "\n")


                                txt = result.readlines()
                                txt.append(str(areaTotal))
                                txt.append(' ')
                                txt.append(str(angRetas))
                                txt.append(' ')
                                txt.append(str(distEucli))
                                txt.append(' ')
                                txt.append(str(ang))
                                txt.append("\n")
                                result.writelines(txt)
                result.close()                     
                limpaVar1()
                limpaVar2()
                f1.close()
                f2.close()

                cv.imshow('Imagem', img)
                cv.waitKey(0)
        cv.destroyAllWindows()
        
if __name__ == '__main__':
	main()
