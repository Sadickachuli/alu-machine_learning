#!/usr/bin/env python3
'''
This script creates a line graph with time on the x-axis and
the fraction remaining on the y-axis to illustrate the exponential
decay of C-14 over time. The range of the x-axis is 0 to 28650 years
, and the y-axis is scaled logarithmically.

'''
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 28651, 5730)
r = np.log(0.5)
t = 5730
y = np.exp((r / t) * x)

# Plotting the line graph

plt.plot(x, y, color='blue')
plt.xlabel('Time (years)')
plt.ylabel('Fraction Remaining')
plt.yscale('log')  # This is to set the y-axis to logarithmic scale
plt.title('Exponential Decay of C-14')
plt.xlim(0, 28650)  # To range from 0 to 28650
plt.show()
