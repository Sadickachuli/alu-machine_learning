#!/usr/bin/env python3
'''This script generates a histogram of student grades for a
 project, where the x-axis represents grades and the y-axis
represents the number of students.
'''
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(5)
student_grades = np.random.normal(68, 15, 50)

bins = range(0, 101, 10)  # set bins every 10 units
plt.hist(student_grades, bins=bins, edgecolor='black')
plt.xlabel('Grades')
plt.ylabel('Number of Students')
plt.xticks(range(0, 101, 10))
plt.xlim(0, 100)  # To set a range from 0 to 100
plt.yticks(np.arange(0, 31, 5))
plt.title('Project A')
plt.show()
