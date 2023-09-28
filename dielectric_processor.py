# -*- coding: utf-8 -*-
# @Author: ZX

"""
This script is to process temperature-dependent dielectric multiple txt data.

Operating environment (required):
    Python environment
    numpy

If there is no environment, please install python3.x,
and then install module 'numpy' (Run 'pip install numpy' in command line).

Usage:
    Put this file and a series of Cp-D data txt files into the same dir.
    Set parameters of this script.
    Run this script.
    Calculated dielectric and impedence data will be output to the same dir as csv files.

Welcome to report any bug or new need to the author.

Wish you a smooth experiment!
"""

#--------------------------------------------------------------------------------------------------------------------#

#------------------#
# Vital Parameters #
#------------------#

thickness_set = 0.029    # Total thickness of film (um)
                        # e.g. thickness_set = 0.39

area_set = 0.00012    # Actual area of electrode (cm2)
                    # e.g. area_set = 0.0005

#--------------------------------------------------------------------------------------------------------------------#

import numpy as np
import os
from math import pi

epsilon_0 = 8.8541878128e-12
thickness = thickness_set * 1e-6    # m
area = area_set * 1e-4              # m2

vname = lambda v,nms: [ vn for vn in nms if id(v)==id(nms[vn])][0]

def mergeFiles(filelist: list):
    matrixes = [np.loadtxt(file, dtype=float) for file in filelist]
    matrixes.sort(key=lambda x: x[1, 0])
    matrix_out = matrixes[0]
    for matrix in matrixes[1:]:
        first = matrix[1, :]
        k = -1
        while matrix_out[k, 0] > first[0]:
            k -= 1
        last = matrix_out[k, :]
        matrix_adjusted = matrix[2:, :] / first[np.newaxis, :] * last[np.newaxis, :]
        matrix_out = np.concatenate((matrix_out[:k, :], matrix_adjusted), axis=0)
    return matrix_out

def savedata(data: np.array, dir: str, temp, freq, transpose=False):
    data_freq = np.concatenate((freq[np.newaxis,:], data), axis=0)
    data_full = np.concatenate((temp[:,np.newaxis], data_freq), axis=1)
    if transpose:
        data_full = data_full.T
    np.savetxt(dir, data_full, delimiter=',')

if __name__ == '__main__':
    txt_files = [file for file in os.listdir('./') if file.endswith('.txt')]
    all_data = mergeFiles(txt_files)
    temperature = all_data[:, 0]        # ℃
    frequency = all_data[0, 1::2]       # Hz
    capacitance = all_data[1:, 2::2]    # F
    loss = all_data[1:, 1::2]
    permittivity = capacitance * thickness / area / epsilon_0
    z2_negative = area / (capacitance * frequency[np.newaxis, :] * 2 * pi * thickness) / 1e3  # kΩ·m
    z1 = z2_negative / loss             # kΩ·m
    for data in [permittivity, loss]:
        savedata(data, f'{vname(data, locals())}.csv', temperature, frequency)
    for data in [z1, z2_negative]:
        savedata(data, f'{vname(data, locals())}.csv', temperature, frequency, transpose=True)