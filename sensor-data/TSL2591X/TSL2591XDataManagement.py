import matplotlib.pyplot as plt
import numpy as np
import serial
import time
import pandas as pd
import numpy as np
import csv
import os


data = []
time.sleep(0.05)
ser = serial.Serial('COM8', 115200)


for i in range(1000):
    b = ser.readline().rstrip()
    str_rn = b.decode()
    print(type(str_rn))
    data.append(str_rn)
    time.sleep(0.05)
data1 = data[2:]
data2 = data1[1::2]
print(data2)


plt.plot(data2)
##plt.ylabel('Relative light units %')
##plt.ylim([0, 100])
##plt.xlabel('data points')
plt.show()



##data1 = [data.remove('INT=1') for i in data]
##LuxValues = [data.remove('INT = 1') for i in data]
##print(LuxValues)