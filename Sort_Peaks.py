import numpy as np
import sys
import os
import csv

# Author: John Gervasoni

# Input: 
#   Peak file
#   boolean: print sorted peaks
# Output: 
#   Returns Dictionary of peaks {Chromosome: Numpy array [Start, End]}
#   Writes an ordered file if SortPrint = True
def SortPeaks(Peakfile, c=None):
    file_name = os.path.basename(Peakfile)
    file_name = file_name.partition('.')[0]
    '''
    if SortPrint:
        file_name = Peakfile.name
        file_name = file_name.partition('.')[0]
        file_name = file_name + "_ordered.csv"
    '''
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
    #toPrint = {}
    with open(Peakfile, 'r') as file:
        for line in file:
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
                #print("Inside elif")
                #print(temp[1])
                #toPrint[chromosome] = locations
                #print("locations equals")
                #print(locations)
                nparray = np.array(locations)
                if chromosome in retVal:
                    arr = retVal[chromosome]
                    nparray = np.concatenate((nparray,arr),axis=0)
                    nparray = nparray[nparray[:,0].argsort()]
                    retVal[chromosome] = nparray
                else:
                    nparray = nparray[nparray[:,0].argsort()]
                    retVal[chromosome] = nparray
                chromosome = temp[1]
                locations.clear()
                if finish:
                    break
            locations.append([int(temp[2]),int(temp[3])])
            bool_chr = False 

    nparray = np.array(locations)
    if chromosome in retVal:
        arr = retVal[chromosome]
        nparray = np.concatenate((nparray,arr),axis=0)
        nparray = nparray[nparray[:,0].argsort()]
        retVal[chromosome] = nparray
    else:
        nparray = nparray[nparray[:,0].argsort()]
        retVal[chromosome] = nparray

    '''
    if SortPrint:
        fields = ['chromosome', 'start-end']
        #print(toPrint)
        with open(file_name, 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(fields)
            for k,v in toPrint.items():
                writer.writerow([k] + v)
    '''

    return retVal



if __name__=='__main__':


    peaks = ["17-16	17	35504041	35504115	+	1991.0	0.834	77.000000	342.0	8.0	42.84	0.00e+00	35.43	0.00e+00	0.97",
    "17-12	17	15208248	15208322	+	1734.8	0.705	79.000000	298.0	2.0	149.31	0.00e+00	61.28	0.00e+00	0.94",
    "17-13	17	37079108	37079182	+	1653.3	0.658	78.000000	287.0	8.0	35.95	0.00e+00	41.01	0.00e+00	0.95",
    "17-29	17	29187360	29187434	+	1449.6	0.764	71.000000	249.0	6.0	41.59	6.85e-300	52.63	1.22e-319	1.04",
    "17-18	17	48616395	48616469	+	1432.1	0.708	76.000000	251.0	1.0	251.52	0.00e+00	50.17	2.87e-308	0.95", 
    "19-1	19	61321052	61321126	+	87.3	0.938	11.000000	15.0	1.0	15.03	2.73e-13	1985.00	1.14e-44	1.17",
    "8-1	8	129234531	129234605	+	69.9	0.650	11.000000	12.0	2.0	6.01	1.34e-06	12.12	6.87e-10	1.03",
    "8-4	8	129234668	129234742	+	46.6	0.571	7.000000	8.0	0.5	16.03	5.79e-08	6.91	8.99e-05	0.97",
    "17-399	17	29399370	29399444	+	145.5	0.544	25.000000	25.0	3.0	8.35	2.94e-15	8.50	1.96e-15	0.86",
    "17-554	17	29539277	29539351	+	145.5	0.659	21.000000	25.0	5.0	5.01	1.53e-10	12.16	5.95e-19	1.03",
    "17-505	17	31529539	31529613	+	145.5	0.686	22.000000	25.0	3.0	8.35	2.94e-15	8.35	2.91e-15	0.98",
    "17-460	17	34962647	34962721	+	145.5	0.805	23.000000	25.0	0.5	50.10	1.11e-33	10.09	4.28e-17	0.94",
    "17-509	17	35940128	35940202	+	145.5	0.806	22.000000	25.0	3.0	8.35	2.94e-15	5.56	4.51e-11	0.95",
    "17-464	17	39067755	39067829	+	145.5	0.565	23.000000	26.0	1.0	26.05	8.66e-28	11.14	4.48e-18	0.94",
    "17-513	17	40900052	40900126	+	145.5	0.658	22.000000	25.0	2.0	12.53	3.02e-19	8.38	2.75e-15	0.94",
    "17-466	17	46694948	46695022	+	145.5	0.633	23.000000	25.0	4.0	6.26	1.50e-12	11.90	4.83e-18	0.95",
    "17-468	17	48505081	48505155	+	145.5	0.745	23.000000	25.0	1.0	25.05	2.26e-26	10.28	1.19e-16	0.91",
    "17-634	17	49033876	49033950	+	145.5	0.630	20.000000	25.0	3.0	8.35	2.94e-15	9.43	1.97e-16	1.03"]



    retVal = SortPeaks(peaks)    
    print(retVal)
