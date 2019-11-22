# HW5_stacks
HW5 - Stacks pipeline and population genomics

For this homework, we're going to use the Stacks pipeline to identify and genotype SNPs in two populations of threespine sticklebacks (*Gasterosteus aculeatus*), and perform some basic population genomic comparisons. Use the Stacks protocol (`Rochette & Catchen 2017.pdf`) and website (`http://catchenlab.life.illinois.edu/stacks/`) for guidance on how to process samples; you are also welcome to use any other online resources you like.

If you used additional resources, please list them here:\
Answer:

I will give you a bare-bones walkthrough of the analyses to perform and the parameters to set for this assignment. We will be using a different (much smaller!) set of example data than that used in the protocol, to ease the computational burden on Poseidon and save time. So don't be alarmed that the protocol says it takes one week to one month, but please don't wait until the last minute either.

The samples we'll use are single-end reads from two Alaskan stickleback populations, 8 individuals each from Bear Paw Lake (freshwater) and Rabbit Slough (marine). They derive from Hohenlohe et al. 2010, which is included in this repo if you want more details.

# Step 1: Set up

First, set up a conda environment called `stacks` with which to run this HW. You'll want to install Stacks (duh), and SRA tools to retrieve the raw sequences. What code did you use to set this environment up?
```
```

Next, set up a slurm script called `HW5_stacks-pipeline_[LASTNAME].txt`. Put **every** command you run for this HW into this file to create a pipeline that can be run on Poseidon. For example, if you need to reformat a file for use in the pipeline, include the code you used to reformat that file. Comment it clearly, so it is obvious what is being done at every step. In the end, I want a script that I can run on Poseidon as-is, starting with file retrieval and ending with population genomics statistics, assuming I first use your conda environment set-up code above to create and activate the appropriate environment.

Next, get the raw reads from the SRA. You want this file:
`SRR034310`

These are RAD-derived reads, so rather than retrieving a single demultiplexed file for each individual, you are retrieving a single lane of sequencing where all reads contain a short identifying index. You'll use the Stacks pipeline to demultiplex these samples.

What code did you use to retrieve these reads?
```
```

There is more information on individual samples, their barcodes, etc in a file available at Zenodo, a popular data-archiving site. That information is here:\
`https://zenodo.org/record/1134547/files/Details_Barcode_Population_SRR034310.txt`

Copy this file from the web to this repo. What code did you use to do this?:
```
```

You'll need some of this information to process your reads, but note that you will have to modify this format for downstream use.

# Step 2: Demultiplex reads

Now, you need to demultiplex your reads using the barcode information in file you just retrieved from Zenodo. Use these parameters:\
Restriction enzyme: sbfI\
Clean reads\
Discard low-quality reads\
"Rescue" reads and barcodes

What code did you use to demultiplex your reads?:
```
```

What percentage of reads were retained after demultiplexing?\
Answer:

# Step 3: Identify SNPs

Typically, you would run this part of the process multiple times with different stack quality and distance parameters to figure out a good set of parameters for your data set. For this homework, we won't ask you to optimize parameters, but be aware that this is a best practice with experimental data. These parameters and how they affect SNP identification are explained in detail in the protocol paper and on the Stacks website here:\
`http://catchenlab.life.illinois.edu/stacks/param_tut.php`

Use the following parameters to form stacks and identify SNPs:\
Minimum coverage to create a stack: 3\
Number of mismatches allowed between stacks (within individuals): 2\
Number of mismatches allowed between loci (between individuals): 3\
Number of threads to run on: 4 (be sure to run with slurm and request 4 nodes)

This will take approximately 2 hours on Poseidon using 4 threads.

Note that this calculates "raw" SNPs, without any QC or filtering for coverage and completeness. For each population, give the following information:\
Bear Paw polymorphic sites:\
Bear Paw private alleles:\
Rabbit Slough polymorphic sites:\
Rabbit Slough private alleles:\

# Step 4: Filter SNPs and calculate population genomic stats

Now, use the `populations` application of Stacks to go back through your raw SNPs, apply some filtering criteria, and conduct basic popgen statistics. Set the following parameters:\
Locus must be present in **both** populations\
Locus must be present in at least 7 individuals in each population\
Heterosygosity must under 70% to retain a SNP\
Minor allele must be present at least twice overall to retain a SNP\
Retain one SNP per locus (= RAD tag) at random \
Calculate F-statistics\
Export files in vcf, STRUCTURE, and Genepop formats\
Number of threads to run on: 4 (be sure to run with slurm and request 4 nodes)

Note: By now you all know my soapbox about calculating linkage disequilibrium directly rather than assuming your SNPs are unlinked if you only use one per RAD tag. However, that is a standard practice (much as I disagree with it), and in the interests of streamlining this HW, go ahead and use this standard approach which is already built into Stacks.

Now that you have applied some QC for SNP coverage and completeness,give the following information again for each population:\
Bear Paw polymorphic sites:\
Bear Paw private alleles:\
Rabbit Slough polymorphic sites:\
Rabbit Slough private alleles:\

This analysis will create a number of output files. Explore them until you find the overall pairwise FST between the two populations, and summary statistics (Fis, Pi, expected and observed heterozygotes) for each population.

What is the Fst between the Bear Paw Lake and Rabbit Slough populations?\
Answer:

What are the following summary statistics for each population, calculated at variant sites only?\
Bear Paw:
  Observed heterozygosity:
  Expected heterozygosity:
  Pi (nucleotide diversity):
  Fis (inbreeding coefficient):
Rabbit Slough:
  Observed heterozygosity:
  Expected heterozygosity:
  Pi (nucleotide diversity):
  Fis (inbreeding coefficient):

# Step 5: Convert file format and run PCA

There are a lot of different places you could go with your SNP panel from here. We're going to use the eigensoft program to conduct a Principal Components Analysis of the cleaned SNPs you generated with Stacks. Unfortunately, like almost every population genomics software, it requires a special input format. The python file we used to filter GATK SNPs in class will convert to this format, but you will first have to export the SNPs into tabular format from the Stacks-generated .vcf file.

To create the SNP table, deactivate your Stacks conda environment and activate your `gatk` conda environment from class.

Run the resulting table through the `SNP_qual_filter.py` filtering script (in repo), setting "dummy" quality and coverage parameters (eg, min coverage of 1), so the script will produce output files in eigenstrat format without removing any SNPs since you have already filtered SNPs in Stacks.

Deactivate the `gatk` conda environment and activate the `popgen` conda environment you should have already set up for class. If you don't have that environment, set it up like this:
```
conda create -n popgen
conda activate popgen
conda install -c bioconda eigensoft=7.2.1
```

Now, activate your `popgen` conda environment and run some basic population genomics tests using the smartpca component of eigensoft. Be sure to submit this using slurm or after requesting time with srun so you can restrict the number of nodes it runs on - smartpca is greedy and will run on 35 threads if you let it!
srun -p compute --time=00:30:00 --ntasks-per-node=2 --mem=20gb --pty bash

To run smartpca, you need 4 files:
.snp: generated by python script
.eigenstratgeno: generated by python script
.indiv: modify popgen-lab_sample-info.txt per below
par.: provided in repo as par.example; modify to use your filenames

To create the .indiv file, open popgen-lab_sample-info.txt and add a column in between the sample names and the population names which is "U" for every individual. This is required information on the sex of each individual, and can be M(ale), F(emale), or U(nknown).

Open the par.example file and change the names of the input and output files according to how you have them named (input: .snp, .eigenstratgeno, .indiv), or would like to have them named (output: .evec, .eval).

Run smartpca by specifying the par. parameter file, and redirecting the output (which will include a lot of good stats and stuff) to a new output logfile:
smartpca -p par.[PAR_FILENAME] > [OUTFILE_NAME]_log.txt

Now, let's take a look! We are most interested in the individual PC loadings in the .evec file and in some of the tests shown in the log.txt file.
