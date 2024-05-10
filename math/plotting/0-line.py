#!/usr/bin/env python3
'''
This is a script to plot a line graph with even values from 
0 to 10 on the x axis and 0 to 1000(each number raised to power of 3)
on th y axis.
'''
import numpy as np
import matplotlib.pyplot as plt

y = np.arange(0, 11) ** 3

x = np.arange(0, 11) ** 1 #To label even number from 0 to 10
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Line Graph')
plt.plot(x, y, color="red") # Plot the axes and use color red for the line
plt.show()

