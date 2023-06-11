import numpy as np
import sys
import os
import csv
# Author: John Gervasoni
def toCSV(file_name, chromosome, MotifDict):
    print("MADE IT!")
    f = file_name + '.' + chromosome + '.csv'
    with open(f, 'w') as csvFile:
        header = "Motif\tGenome\tChromosome\tTotal\tLocations\n"
        csvFile.write(header) 
        for key,value in MotifDict.items():
            count = str(len(value))
            #value_string = np.array2string(value, separator=',')
            value_string = "".join(value)
            line = key + '\t' + file_name + '\t' + chromosome + '\t' + count + '\t' + value_string + '\n'
            csvFile.write(line)
    return

def GetMotifs(genome, peak_filename, chromosome, chromosome_string, Values):
    print("Inside GetMotifs")
    np_index = 0
    MotifDict = {}
    while(np_index < len(Values)):
        row = Values[np_index,:]
        start = row[0]
        end = row[1]
        motif = chromosome_string[start:end]
        Genome_chromosome_Peakfile_Starting_Location = genome + '.' + chromosome + '.' + peak_filename + '.' + str(row[0])
        if motif in MotifDict:
            print("Copy" + motif)
            values = MotifDict[motif]
            values.append(Genome_chromosome_Peakfile_Starting_Location)
            MotifDict[motif] = values
        else:
            MotifDict[motif] = [Genome_chromosome_Peakfile_Starting_Location]
        np_index = np_index + 1

    return MotifDict

def Candies(fasta, peak_filename, peakDict):
    MotifDict = {}
    print("In Candies")
    file_name = os.path.basename(fasta)
    file_name = file_name.partition('.')[0]
    peak_keys = list(peakDict.keys())
    #print(peak_keys)
    chromosome_string = ""
    chromosome = ""
    inPeak = False
    #print(file_name)
    with open(fasta, 'r') as read_file:
        print("In Candies Loop")
        for line in read_file:
            #print('s')
            if line[0] == '>':
                #print("Chromosome equals")
                #print(chromosome)
                if chromosome_string != "":
                    Values = peakDict[chromosome]
                    temp_Dict = GetMotifs(file_name, peak_filename, chromosome, chromosome_string, Values)
                    MotifDict.update(temp_Dict)
                if len(line) > 7:
                    chromosome = line.partition(file_name + ':')[2]
                    chromosome = chromosome.partition(':')[0] 
                    #print("Current chromosome")
                else:
                    chromosome = str(line[4:])
                    chromosome = chromosome.rstrip('\n')
                    #print("Small chromosome")
                    #print(chromosome)
                    #print(type(chromosome))
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
            temp_Dict = GetMotifs(file_name, peak_filename, chromosome, chromosome_string, Values)
            MotifDict.update(temp_Dict)

    return MotifDict



if __name__=='__main__':

   peak_dict = { 17:[[3792733, 3792807],[3962082, 3962156],[4220301, 4220375],[4349017, 4349091],[4351472, 4351546],[5781978, 5782052],[6267607, 6267681],[6450983, 6451057],[6494985, 6495059],[8667137, 8667211],[8711917, 8711991],[8907453, 8907527],[8915764, 8915838],[9393684, 9393758],[10731855, 10731929],[10950067, 10950141],[11621678, 11621752],[12068571, 12068645],[13487296, 13487370],[14132749, 14132823],[14471012, 14471086],[14892438, 14892512],[16063668, 16063742],[16145552, 16145626],[16677172, 16677246],[16849723, 16849797],[17183323, 17183397],[17363375, 17363449],[18270789, 18270863],[18356216, 18356290],[18425827, 18425901],[18426270, 18426344],[18471897, 18471971],[19325126, 19325200],[19419886, 19419960],[19563684, 19563758],[19878348, 19878422],[20523069, 20523143],[21105451, 21105525],[21911489, 21911563],[21950342, 21950416],[22165739, 22165813],[22166203, 22166277],[22189576, 22189650],[22267864, 22267938],[22631300, 22631374],[22901878, 22901952],[27271294, 27271368],[33237587, 33237661],[34520604, 34520678],[36331840, 36331914],[36437859, 36437933],[37259855, 37259929],[37300696, 37300770],[37483005, 37483079],[37627289, 37627363],[37794514, 37794588],[37861876, 37861950],[37950110, 37950184],[38091618, 38091692],[38309765, 38309839],[38809099, 38809173],[39016828, 39016902],[40109405, 40109479],[40632586, 40632660],[41564223, 41564297],[41751134, 41751208],[41967494, 41967568],[42051170, 42051244],[42082040, 42082114],[48690442, 48690516]]}

