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

What perentage of reads were retained after demultiplexing?\
Answer:

# Step 3: 
