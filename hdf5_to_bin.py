""" 
.hdf5-to-fat file exporter with few tweaks.
Cell (0,0) value of the pattern matrix
represents the phase identified for 
that point on the map: 0 - notIndexed, 1 - iron gamma, 2 - iron alpha
"""

import os
import numpy as np
import h5py
#from PIL import Image

path = '/Users/user/Downloads/hf/'
### iterate over files in PATH and get .h5 file
for file in os.listdir(path):
    array = []
    pattern = []
    if file.endswith('.h5'):
        data = h5py.File(path+file, 'r')  
         
### iterate over .h5 file structure, find map data, define paths and get the patterns, nrows, ncols, phase 
        for name in data:
            if name.startswith('map'):
                patterns = data['/'+str(name)+'/EBSD/Data/Pattern'][()] 
                ncols = int(data['/'+str(name)+'/EBSD/Header/nColumns'][()]) 
                nrows = int(data['/'+str(name)+'/EBSD/Header/nRows'][()]) 
                phase = data['/'+str(name)+'/EBSD/Data/Phase'][()] 

### iterate over the patterns in .h5 file and make a list with all of them, changing first values in each image to represent phase data for particular pattern.
                for i in range(len(patterns)):
                    pattern = patterns[i]
                    pattern[0,0] = phase[i] 
                    array.append(pattern)
                    #img = Image.fromarray(patterns[i])
                    #img.save(path+'/img/'+file[:-3]+'_'+str(i)+'.tiff')
            else:
                continue
        
### take every nth chunk of the array and export to binary file
        array = np.array(array)
        k = 1
        for j in range(len(array)//ncols):
            with open(path+file[:-3]+'_Map_line_'+str(j), 'wb') as f:
                temp = array[j*ncols:k*ncols]
                np.array(temp, dtype=np.uint16).tofile(f)
                k += 1
    else:
        continue

        
        

