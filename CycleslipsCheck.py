import numpy as np


##Algorithm based on Finite Difference
#Init data
polyphase = np.array([0, 0, 0, 0, 0, 0], dtype = np.float).reshape(6,1)
polytime = np.array([0, 0, 0, 0, 0, 0], dtype = np.float).reshape(6,1)
Time1 = np.array([1, 0, 0, 0, 0], dtype = np.float)
Time = np.tile(Time1,(6,1))
A = np.array([0, 0, 0, 0, 0], dtype = np.float).reshape(5,1)
evaluation = float(0)
t0 = float(0)
#Import data
data = np.loadtxt('D:\Code\Python_work\GNSS\CheckData.csv', delimiter=',')
#[0]-week number [1]-week seconds [2]-distance [3]-phase
(m,n) = np.shape(data)
#Polyfit and evaluate(step = 1, per_batch_data = 6)
#use the first data as a symbol
i = 1
slip_num = 0
while i < m - 6:
    t0 = data[i - 1][1]
    phase0 = data[i - 1][3]
    t = data[i + 6][1]
    phase = data[i + 6][3]
    for j in range(6):
        polyphase[j][0] = data[i+j][3] - phase0
        polytime[j][0] = data[i+j][1]
    for k in range(6):
        Time[k][1] = polytime[k][0] - t0
        Time[k][2] = pow((polytime[k][0] - t0), 2)
        Time[k][3] = pow((polytime[k][0] - t0), 3)
        Time[k][4] = pow((polytime[k][0] - t0), 4)
    A = np.dot(np.linalg.pinv(np.dot(Time.T, Time)),np.dot(Time.T, polyphase))
    #print(A)
    evaluation = phase0
    for x in range(5):
        evaluation = evaluation + A[x][0]*pow(7, x)
    #print(evaluation)
    #print(phase)
    #Adjust if slip happen(threshhold = 10)
    if (abs(A[0][0]) < 1e+06) and (abs(A[1][0]) < 1e+06) and (abs(A[2][0]) < 1e+06) and (abs(A[3][0]) < 1e+06) and (abs(A[4][0]) < 1e+06):    
        if abs(evaluation - phase) > 10:
            print('Cycle Slip happend at ', t, ' seconds')
            #Cycle slip happend at the 7th data(predict phase), use the 8th to be new init data(data i-1) 
            i = i + 9
            slip_num = slip_num + 1
            evaluation = 0
        else:
                evaluation = 0
                i = i + 1
    else:
        print('Cycle Slips happend at the first batch--Changing data')
        evaluation = 0
        i = i + 1
print('Cycle Slips happend ', slip_num, ' times')


##Test of Algorithm
#t0=data[0][1]
#phase0=data[0][3]
#t=data[7][1]
#phase=data[7][3]
#for j in range(6):
#    polytime[j][0]=data[i+j][1]
#    polyphase[j][0]=data[i+j][3]-phase0
#for k in range(6):
#    Time[k][1]=polytime[k][0]-t0
#    Time[k][2]=pow((polytime[k][0]-t0), 2)
#    Time[k][3]=pow((polytime[k][0]-t0), 3)
#    Time[k][4]=pow((polytime[k][0]-t0), 4)
#A=np.dot(np.linalg.pinv(np.dot(Time.T, Time)),np.dot(Time.T, polyphase))
#print(polyphase)
#print(Time)
#print(A)
#evaluation=phase0
#for x in range(5):
#    evaluation = evaluation + A[x][0]*pow(7, x)
#print(abs(evaluation-phase))