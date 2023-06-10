import numpy as np
import sys
import os
import csv

def toCSV(file_name, chromosome, MotifDict):
    print("MADE IT!")
    f = file_name + '.' + chromosome + '.csv'
    with open(f, 'w') as csvFile:
        header = "Motif\tFile.Chromosome\tTotal\tLocations\n"
        csvFile.write(header) 
        f = f[:-4]
        for key,value in MotifDict.items():
            count = str(len(value))
            #value_string = np.array2string(value, separator=',')
            value_string = "".join(str(value))
            line = key + '\t' + f + '\t' + count + '\t' + value_string + '\n'
            csvFile.write(line)
    return

def GetMotifs(file_name, chromosome, chromosome_string, Values):
    print("Inside GetMotifs")
    np_index = 0
    MotifDict = {}
    while(np_index < len(Values)):
        row = Values[np_index,:]
        start = row[0]
        end = row[1]
        motif = chromosome_string[start:end]
        if motif in MotifDict:
            print("Copy" + motif)
            values = MotifDict[motif]
            values.append(int(row[0]))
            MotifDict[motif] = values
        else:
            MotifDict[motif] = [int(row[0])]
        np_index = np_index + 1

    toCSV(file_name, chromosome, MotifDict)

    return

def Candies(fasta, peakDict):
    print("In Candies")
    file_name = os.path.basename(fasta)
    file_name = file_name.partition('.')[0]
    peak_keys = list(peakDict.keys())
    print(peak_keys)
    chromosome_string = ""
    chromosome = ""
    inPeak = False
    #print(file_name)
    with open(fasta, 'r') as read_file:
        print("In Candies Loop")
        for line in read_file:
            #print('s')
            if line[0] == '>':
                print("Chromosome equals")
                print(chromosome)
                if chromosome_string != "":
                    Values = peakDict[chromosome]
                    GetMotifs(file_name, chromosome, chromosome_string, Values)
                if len(line) > 7:
                    chromosome = line.partition(file_name + ':')[2]
                    chromosome = chromosome.partition(':')[0] 
                    print("Current chromosome")
                else:
                    chromosome = str(line[4:])
                    chromosome = chromosome.rstrip('\n')
                    print("Small chromosome")
                    print(chromosome)
                    print(type(chromosome))
                if chromosome in peak_keys:
                    inPeak = True
                else:
                    inPeak = False
                chromosome_string = ""
            elif inPeak:
                temp = line.rstrip('\n')
                chromosome_string = chromosome_string + temp
        if chromosome_string != "":
            Values = peakDict[chromosome]
            GetMotifs(file_name, chromosome, chromosome_string, Values)

        '''
        loc = 0
        motifDict = {}
        #Loop through genome
        line = read_file.readline()
        print(line)
        np_index = 0
        print("IN HERE!")
        while(True):
            # Find out if the line specifies chromosome
            if line == "":
                break
            if line[0] == '>':
                loc = 0
                if motifDict:
                    toCSV(chromosome, motifDict)
                if len(line) > 7:
                    chromosome = line.partition(file_name + ':')[2]
                    chromosome = chromosome.partition(':')[0] 
                else:
                    chromosome = line[1:]
                line = read_file.readline()
            elif chromosome not in peak_keys:
                line = read_file.readline()
                continue
            else:
                Values = peakDict[chromosome]
                row = Values[np_index,:]
                while(True):
                    line = line.rstrip('\n')
                    loc = loc + len(line)
                    bool_start = True
                    end_in_one_line = False
                    start = 0
                    end = 0
                    motif = ""
                    # When peak is located, loop through until finished
                    while (True):
                        # continue if not at a peak
                        if loc < row[0]:
                            break
                        # store starting location
                        elif loc > row[0] and bool_start == True:
                            bool_start = False 
                            end_in_one_line = True 
                            # Store starting pointer
                            start = row[0] - loc 
                        # If peak has ended 
                        elif loc > row[1]:
                            # Get end location
                            end = row[1] - loc
                            # Check if peak is in one line
                            if end_in_one_line == True:
                                motif = line[start:end]
                            else:
                                # Add remaining bases to motif
                                motif = motif + line[:e]
                            # Check to see if motif is already in motifDict
                            if motif in motifDict:
                                Val_array = motifDict[motif]
                                Val_array.append(row[0])
                                motifDict[motif] = Val_array
                            else:
                                motifDict[motif] = [row[0]]
                            # Increase numpy array index
                            np_index = np_index + 1
                            # Check if finished
                            if np_index >= len(Values):
                                break
                            #Else change to new row
                            row = Values[np_index,:]
                            # Reset motif
                            motif = ""
                        elif end_in_one_line == True:
                            motif = line[s:]
                            end_in_one_line = False
                            break
                        # If motif isn't empty
                    else:
                        motif = motif + line
                        break
                # Check if finished
                if np_index >= len(Values):
                    break
                else:
                    line = read_file.readline()

        '''
    return 



if __name__=='__main__':

   peak_dict = { 17:[[3792733, 3792807],[3962082, 3962156],[4220301, 4220375],[4349017, 4349091],[4351472, 4351546],[5781978, 5782052],[6267607, 6267681],[6450983, 6451057],[6494985, 6495059],[8667137, 8667211],[8711917, 8711991],[8907453, 8907527],[8915764, 8915838],[9393684, 9393758],[10731855, 10731929],[10950067, 10950141],[11621678, 11621752],[12068571, 12068645],[13487296, 13487370],[14132749, 14132823],[14471012, 14471086],[14892438, 14892512],[16063668, 16063742],[16145552, 16145626],[16677172, 16677246],[16849723, 16849797],[17183323, 17183397],[17363375, 17363449],[18270789, 18270863],[18356216, 18356290],[18425827, 18425901],[18426270, 18426344],[18471897, 18471971],[19325126, 19325200],[19419886, 19419960],[19563684, 19563758],[19878348, 19878422],[20523069, 20523143],[21105451, 21105525],[21911489, 21911563],[21950342, 21950416],[22165739, 22165813],[22166203, 22166277],[22189576, 22189650],[22267864, 22267938],[22631300, 22631374],[22901878, 22901952],[27271294, 27271368],[33237587, 33237661],[34520604, 34520678],[36331840, 36331914],[36437859, 36437933],[37259855, 37259929],[37300696, 37300770],[37483005, 37483079],[37627289, 37627363],[37794514, 37794588],[37861876, 37861950],[37950110, 37950184],[38091618, 38091692],[38309765, 38309839],[38809099, 38809173],[39016828, 39016902],[40109405, 40109479],[40632586, 40632660],[41564223, 41564297],[41751134, 41751208],[41967494, 41967568],[42051170, 42051244],[42082040, 42082114],[48690442, 48690516]]}

