import numpy as np
import sys
import os
from pathlib import Path


def Candies(indices, Files):
    
    snipDict = {}
    #TODO: Make this more efficient.
    for DNA in Files:
        loc = 0
        np_index = 0
        row = indices[0,:]
        '''
        print(type(row))
        print(row)
        '''
        current_line = ""
        s = 0
        #Boolean to see if new line has occurred
        bool_new_line = False
        # Boolean for if within one line
        One_line = False

        with open(DNA, 'r') as file:
            # Get the file name
            file_name = str(DNA)
            file_index = file_name.index('/')
            file_name = file_name[file_index+1:]
            file.readline()
            for line in file:
                line = line.rstrip('\n')
                loc = loc + len(line)
                while(True):
                    if loc < row[0]:
                        break
                    # Check if peak section has started            
                    elif loc > row[0] and bool_new_line == False:
                        # If true, first check if the peak also ends before loc
                        bool_new_line = True
                        One_line = True
                        # Store start pointer
                        s = row[0]-loc
                    # If the peak section has ended for the current row
                    elif loc > row[1]:
                        # Get the end index 
                        e = row[1] - loc
                        # Check if peak is contained in one line
                        if One_line == True:
                            current_line = line[s:e]
                            One_line = False
                        else:
                            # Add remaining bases to the current line
                            current_line = current_line + line[:e]
                        # Check to see if current_line is already in snipDict
                        if current_line in snipDict:
                            # If it is, retrieve the snipDict value
                            tempDict = snipDict[current_line]
                            # Check to see if the current DNA file is in the value
                            if file_name in tempDict:
                                # If it is retieve that value, and then add location
                                key_location = tempDict[file_name]
                                key_location.append(row[0])
                                # And reassign the key to the updated value
                                tempDict[file_name] = key_location
                            else:
                                # If not, create a new key, value pair
                                tempDict = {file_name: [row[0]]}
                            # Update the value for the current_line in dictionary
                            snipDict[current_line] = tempDict
                        else:
                            # If not in snipDict, create the value
                            tempDict = {file_name: [row[0]]}
                            # And add it to the snipDict
                            snipDict[current_line] = tempDict
                        # And increase the index of our numpy array
                        np_index = np_index + 1
                        # Check if finished
                        if np_index >= len(indices):
                            break
                        # Else change to the new row
                        row = indices[np_index,:]
                        # Reset current_line
                        current_line = ""
                        # Reset new line boolean
                        bool_new_line = False
                    elif One_line == True:
                        current_line = line[s:]
                        One_line = False
                        break
                    # If current_line isn't empty...
                    else:
                        current_line = current_line + line
                        break
                         
                # Check if finished
                if np_index >= len(indices):
                    break

    return snipDict



if __name__=='__main__':

    file1 = sys.argv[1]
    source_dir = Path('Fasta/')
    Files = source_dir.glob('*.fasta')
    lists = []
    with open(file1, 'r') as file:
        for line in file:
            if line[0] == '#':
                continue
            else:
                temp = line.split()
                lists.append([int(temp[2]),int(temp[3])])

    indices = np.array(lists) 
    indices = indices[indices[:,0].argsort()]

    retVal = Candies(indices,Files)

    print(retVal)
