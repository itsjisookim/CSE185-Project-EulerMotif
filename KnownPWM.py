import argparse
from datetime import datetime
import numpy as np
import pandas as pd
import math
import random
import sys
import scipy.stats
        
def getPWM(ppm,background_freqs=[0.25, 0.25, 0.25, 0.25]):#Convert PPM to PWM with default equal background frequencies
    pwm = np.zeros(shape = (len(ppm), 4))
    for i in range(len(ppm)):
        for j in range(len(ppm[i,:])):
            #p_ij = pfm[i,j]/sum(pfm[i])
            pwm[i,j] = math.log2(ppm[i,j]/background_freqs[j])
    return pwm

def ScoreSeq(pwm, sequence, columns):# Score a sequence using a PWM
    score = 0
    n = pwm.shape[1]
    for i in range(len(sequence)-n+1):
        seq = sequence[i:i+n]
        temp=0
        for j in range(len(seq)):
            idx = columns.index(seq[j])
            temp += pwm[j, idx]
        
        if (temp > score):
            score=temp
            
    return score

def GetThreshold(null_dist, pval): #Find the threshold to achieve a desired p-value
    # set this  below to be the score threshold to obtain a p-value <0.01
    threshold = int(pval*len(null_dist))
    
    null_dist.sort(reverse=True)
    for i in range(len(null_dist)):
        if (i==threshold):
            thresh = null_dist[i]
            break

    return thresh

def RandomSequence(n, nucs, freqs):#Generate a random string of nucleotides of length n
    #print(n, nucs, freqs)
    seq = ''.join(random.choices(nucs, weights=freqs, k=n))
    return seq

def getSequences(PeakSeq, n): #Get all n-mer of all consensus sequences where n is size of respective motif
    seqs = {}
    for PS in PeakSeq:
        for i in range(len(PS)-n+1):
            sequence = PS[i:i+n]
            if sequence in seqs:
                seqs[sequence].append(PS)
            else:
                seqs[sequence] = [PS]
    
    return seqs

def readPeakSeq(Seqfile, nucs): ##Read through peakfile once
    seqf = open(seqFile, 'r')
    data = seqf.readlines()
    seqf.close()
    PeakSeq = {}
    RevComp = []
    Total_seq = 0
    for d in data:
        if '#' in d:
            d = d.strip('#')
            samples = d.split()[1:]
        else:
            d = d.split()
            if d[0] in PeakSeq:
                continue
            else:
                PeakSeq[d[0]] = [int(i) for i in d[1:]]
                Total_seq+=sum(PeakSeq[d[0]])
                RevComp.append(ReverseComplement(d[0]))
                
    freqs = ComputeNucFreqs(list(PeakSeq.keys()) + RevComp, nucs)
    return PeakSeq, freqs, samples, Total_seq

def ReverseComplement(sequence):
    revcomp = ""
    for i in range(0, len(sequence)):
        if sequence[i] == "A":
            revcomp = revcomp + "T"
        if sequence[i] == "C":
            revcomp = revcomp + "G"
        if sequence[i] == "G":
            revcomp = revcomp + "C"
        if sequence[i] == "T":
            revcomp = revcomp + "A"
    revcomp = revcomp[::-1]
    return revcomp

def FindMaxScore(pwm, sequence, nucs): ##Finds max PWM score of forward and reverse of sequence
    max_score = -1*np.inf
    reverse = ReverseComplement(sequence)
    reverse_score = ScoreSeq(pwm,reverse, nucs)
    seq_score = ScoreSeq(pwm,sequence, nucs)

    if (reverse_score > seq_score):
        max_score = reverse_score
    if (reverse_score < seq_score):
        max_score = seq_score
    if (reverse_score == seq_score):
        max_score = seq_score
        
    return max_score
    
def ComputeEnrichment(peak_total, peak_motif, bg_total, bg_motif):
    pval = -1
    # your code here
    table = [[peak_motif, peak_total-peak_motif],[bg_motif, bg_total-bg_motif]]
    odds_ratio, pval = scipy.stats.fisher_exact(table)
    
    return pval

def ComputeNucFreqs(sequences, nuc):
    freqs = [0,0,0,0] #A, C, G, T
    total = 0
    for s in sequences:
        total+=len(s)
        for i in range(len(nuc)):
            freqs[i] += s.count(nuc[i])
        
    freqs = [j/float(total) for j in freqs]
    
    return freqs

def getMotifMatch(motif_lib, seqFile):
    with open (motif_lib, 'r') as f:
        lines = f.read().split('>')
    f.close()
    
    nucs = ['A', 'C', 'G', 'T']
    count = 0
    FINAL = {}
    SEQ = {}
    PeakSeq, freqs, samples, Total_seq = readPeakSeq(seqFile, nucs)
    #print(PeakSeq)
    #print(freqs)
    #print(samples)
    out = open('test_consesus.PASS.txt', 'w')
    Columns = ['Motif_Name', 'Euler_tag'] + samples
    out.write('\t'.join(Columns) + '\n')
    for l  in lines:
        data = l.split('\n')
        count+=1
        if len(data) <= 1:
            continue
        else:
            tag = data[0]
            for i in range(1,len(data)):
                if len(data[i]) <=1: #remove any none data lines
                    del data[i] 
                else:
                    data[i] = [float(j) for j in data[i].split('\t')]
            
            motif_ID = data[0].split('\t')[1]
            ppm = np.array(data[1:]) #position probability matrix of each known motif
            pwm = getPWM(ppm) #conver ppm to pwm
            
            #scan through the consensus sequences and find matching motifs that meets threshold criteria
            n = len(pwm)
            
            ##get Threshold score for significant match with p-val <0.01 of each motif PWM
            numsim = 10000
            bg_seq = RandomSequence(n, nucs, freqs)
            null_scores = [ScoreSeq(pwm, bg_seq, nucs) for i in range(numsim)]
            #print(null_scores)
            threshold = GetThreshold(null_scores, 0.01)
            
            ## final data to store info
            FINAL[motif_ID] = []
            num_bg_pass=0
            num_seq = 0
            Sample_peaks_pass={sample: 0 for sample in samples}
            Bg_peaks_pass={sample: 0 for sample in samples}
            
            for seq in PeakSeq:
                score = FindMaxScore(pwm, seq, nucs)
                bg_score = FindMaxScore(pwm, bg_seq, nucs)
                if score > threshold:
                    for s in range(len(samples)):
                        Sample_peaks_pass[samples[s]]+=PeakSeq[seq][s]
                if bg_score > threshold:
                    for s in range(len(samples)):
                        Bg_peaks_pass[samples[s]]+=PeakSeq[seq][s]
 
            #print(motif_ID) 
            consensus_Tag = []
            #out = open('test_consesus.PASS.txt', 'w')
            temp = [motif_ID]  + ['0' for s in samples]
            tag = []
            for sample in Sample_peaks_pass:
                pval = ComputeEnrichment(Total_seq, Sample_peaks_pass[sample], Total_seq, Bg_peaks_pass[sample])
                if pval < 0.01:
                    #print(sample, pval)
                    idx = samples.index(sample)
                    temp[idx+1] = str(Sample_peaks_pass[sample])
                    tag.append(sample.split('_')[0])
            if len(tag) <= 0:
                temp.insert(1, 'NA')
            else:
                temp.insert(1, '&'.join(tag))
            print(temp)
            out.write('\t'.join(temp) + '\n')          
                
    out.close()


#### Execution
start = datetime.now()
seqFile = sys.argv[1]
MM = getMotifMatch('data/Known.motifs', seqFile)
print(datetime.now()-start)