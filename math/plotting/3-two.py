#!/usr/bin/env python3
'''This script plots the exponential decay of two
 radioactive elements, C-14 and Ra-226, over time.
'''
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 21000, 1000)
r = np.log(0.5)
t1 = 5730
t2 = 1600
y1 = np.exp((r / t1) * x)
y2 = np.exp((r / t2) * x)
plt.plot(x, y1, linestyle='dashed', color='red', label='C-14')
plt.plot(x, y2, linestyle='-', color='green', label='Ra-226')
plt.xlabel('Time (years)')
plt.ylabel('Fraction Remaining')
plt.title('Exponential Decay of Radioactive Elements')
plt.xlim(0, 20000)  # For x-axis range
plt.ylim(0, 1)  # For y-axis range
plt.legend(loc='upper right')  # Add the legend
plt.show()
plt.show()
