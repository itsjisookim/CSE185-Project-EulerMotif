import numpy as np
import sys
import os
import csv
# Input: 
#   Peak file
#   boolean: print sorted peaks
# Output: 
#   Returns Dictionary of peaks {Chromosome: Numpy array [Start, End]}
#   Writes an ordered file if SortPrint = True
def SortPeaks(Peakfile, SortPrint=False, c=None):
    file_name = ""
    if SortPrint:
        file_name = Peakfile.name
        file_name = file_name.partition('.')[0]
        file_name = file_name + "_ordered.csv"
    first_time = True
    chromosome = ""
    bool_chr = False
    finish = False
    if c:
        chromosome = c
        bool_chr = True
        first_time = False
    locations = []
    retVal = {}
    toPrint = {}
    #with open(Peakfile, 'r') as file:
    for line in Peakfile:
        if line[0] == '#':
            continue

        temp = line.split(None, 4)


        if first_time == True:
            chromosome = temp[1]
            first_time = False
        elif bool_chr and chromosome != temp[1]:
            finish = True
            continue
        elif chromosome != temp[1]:
            toPrint[chromosome] = locations
            nparray = np.array(locations)
            nparray = nparray[nparray[:,0].argsort()]
            retVal[chromosome] = nparray
            chromosome = temp[1]
            locations.clear()
            if finish:
                break
        locations.append([int(temp[2]),int(temp[3])])
        bool_chr = False 


    if SortPrint:
        fields = ['chromosome', 'start-end']
        with open(file_name, 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(fields)
            for k,v in toPrint.items():
                writer.writerow([k] + v)


    return retVal



if __name__=='__main__':

    file1 = sys.argv[1]

    with open(file1, 'r') as f:
        retVal = SortPeaks(f, True)
    print(retVal)
