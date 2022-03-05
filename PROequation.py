import numpy as np
import math


##Import data
#Observation distance
R = np.array([24115224.586, 23852690.710, 22389912.802, 24577319.825, 23384340.177, 24479081.841], dtype='float32').reshape(6,1)
#Satellite position
Xs = np.array([4791839.793, 24513555.750, 14424694.880, 2438267.619, 24699645.220, 20750469.480], dtype='float32').reshape(6,1)
Ys = np.array([-16027953.710, 2290238.988, -12687500.250, -27845730.100, -2345295.901, -18429010.410], dtype='float32').reshape(6,1)
Zs = np.array([23259013.420, 14685609.220, 20602453.000, 3484060.793, 14750395.800, -7962146.345], dtype='float32').reshape(6,1)

##Init data
#Correction
V = np.array([0, 0, 0, 0, 0, 0], dtype='float32').reshape(6,1)
#Parameter
Para = np.array([0, 0, 0, 0], dtype='float32').reshape(4,1)
#Position
X = float(0)
Y = float(0)
Z = float(0)
#T=C*dt
T = float(0)
#Geometry distance
R0 = np.array([0, 0, 0, 0, 0, 0], dtype='float32').reshape(6,1)
#Partial derivative 
A1 = np.array([0, 0, 0, 1], dtype='float32')
A = np.tile(A1, (6, 1))

##Caculation
for i in range(6):
    for j in range(6):
        R0[j][0] = math.sqrt(pow((Xs[j][0] - X), 2) + pow((Ys[j][0] - Y), 2) + pow((Zs[j][0] - Z), 2))
    #Derivative
    for j in range(6):
        A[j][0] = (X - Xs[j][0])/R0[j][0]
        A[j][1] = (Y - Ys[j][0])/R0[j][0]
        A[j][2] = (Z - Zs[j][0])/R0[j][0]
    #print(A)
    L = R - R0
    #Get detaX,Y,Z,T
    Para = np.dot(np.linalg.pinv(np.dot(A.T, A)),np.dot(A.T, L))
    #Get Qx
    Qx = np.linalg.pinv(np.dot(A.T, A))
    print('iteration',i+1)
    print('Qx\n', Qx)
    #Get Correction
    V=np.dot(A, Para) - L
    print('V\n', V)
    print('Para\n', Para)
    #Renovate X,Y,Z
    X = X + Para[0][0]
    Y = Y + Para[1][0]
    Z = Z + Para[2][0]
    T = T + Para[3][0]
    if Para[0][0]<pow(10, -7) and Para[1][0]<pow(10, -7) and Para[2][0]<pow(10, -7) and Para[3][0]<pow(10, -7):
        break
    
#Display
print(X.round(5),Y.round(5),Z.round(5))
m0 = float(math.sqrt(np.dot(V.T, V)/2))
D = np.dot(pow(m0, 2), Qx)
print('D\n', D)