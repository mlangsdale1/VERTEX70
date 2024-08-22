# -*- coding: utf-8 -*-
"""
Purpose: 
    Read in txtfile from ECOSTRESS spectral library and plot spectra

@author: Mary Langsdale
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('classic')

def ESL_import(ifp):
    
    file = open(ifp)
    data = file.readlines()
    file.close()
    
    metadata = data[0:20]
    columns = []
    row = []
    for line in metadata:
        columns.append(line.split(':')[0])
        row.append(line.split(':')[1][0:-1])
    meta = pd.DataFrame(row, index =columns)
        
    wvs = []
    spec = []
    
    for line in data[21:]:
        wvs.append(float(line.split('\t')[0]))
        spec.append(float(line.split('\t')[1][0:-1]))
        
    spectra_dict = {meta.loc['X Units'][0] :wvs, meta.loc['Y Units'][0]:spec}
    spectra = pd.DataFrame(spectra_dict)
    
    return meta, spectra

def ESL_plot(meta, spectra):
    sample = meta.loc['Name'][0]
    x_units = meta.loc['X Units'][0]
    y_units = meta.loc['Y Units'][0]
    
    plt.plot(spectra[x_units], spectra[y_units])
    plt.xlabel(x_units)
    plt.ylabel(y_units)
    plt.title(sample)
    
    return

ifp = 'C:/Users/maryl/Dropbox/PhD/Data/ESL/vegetation.grass.avena.fatua.tir.vh352.ucsb.nicolet.spectrum.txt'
meta, spectra = ESL_import(ifp)
ESL_plot(meta,spectra)