# EulerMotif
(Work in Progress)
This is our final profect for UCSD [CSE185 : Advanced Bioinformatics Lab](https://catalog.ucsd.edu/courses/CSE.html#:~:text=CSE%20185.%20Advanced%20Bioinformatics%20Laboratory%20(4)). EulerMotif is a known motif enrichement visualization tool where is shows the relationships of overlapping motif enrichment across multiple samples. This version only allows chromosome specific DNA motif analysis with [HOMER](http://homer.ucsd.edu/homer/motif/) known motif library and ChIP-seq sample peak files generated through HOMER.


### EulerMotif Pipeline
---
<p align="center">
  <img src="https://github.com/itsjisookim/CSE185-Project-EulerMotif/blob/main/figures/EulerMotif_Pipeline.v1.png" />
</p>


# Installation Instructions
Step-by-step guide to run [EulerMotif]
1. Clone the Repository into your IDE
<pre><code>git clone https://github.com/itsjisookim/CSE185-Project-EulerMotif.git
</code></pre>
2. Create Fasta and Peak folders
3. Load files of interest into their respective folder
4. Run pre_controller to create a motif CSV named "Results.csv"
</code></pre>
For Mac or Linux version simply run:
<pre><code>$ python pre_controller.py [-chr/-h]  
   [-h] - help message
   [-chr C] - specify chromosome C
</code></pre>


# Demo pre_controller  
The purpose of the pre_simulator is the generate a limited number (5) of generated peaks from a large genome fasta file.
To demo pre_controller run pre_simulator 
<pre><code>$ python pre_simulator [Fasta file] [Number of Lines to Read Per Chromosome]
</code></pre>

3. Usage of EulerMotif requires installing ==eulerr== library to be installed. If unable to install, you can use EulerStat.csv and produce final plots via [online eulerr](https://eulerr.co/)
For Windows version:
<pre><code>
</code></pre>
For Mac version:
<pre><code>
</code></pre>

4. After installation, typing the following command to see Euler usage message
For Windows version:
<pre><code>py eulermotif --help
</code></pre>
For Mac version:
<pre><code>python3 eulermotif --help
</code></pre>

# EulerMotif Options
The **required** inputs to run `eulermotif` are:
- -r/-ref [RFERENCE GENOME] : Reference genome fasta file

Some **optional** inputs that could be useful:
- -o/-out [OUTPUT PATH] : output directory where the final output files will be located (default : )
- 

# Basic Usage (including Demo)
The basic usage of `eulermotif` is:
For Windows version:
<pre><code>
</code></pre>
For Mac version:
<pre><code>
</code></pre>

# EulerMotif Demo

# File Formate
### Input Data
- [HOMER motif library](http://homer.ucsd.edu/homer/custom.motifs) were downloaded from the [HOME database website](http://homer.ucsd.edu/homer/motif/motifDatabase.html)
- Three transcription factor ChIP-seq files 
- CSE185 SP23 LAB5 data
- Reference Genome Fasta file (GRC38.fa, hg19.fa, etc.)
### Output Data
- KnownEuler.html : HTML file with enriched motif euler plot of all samples `AND` Motif information table with logo plots
- EulerStat.csv : CSV file of enriched motif counts for each sample combination to produce euler plot.
