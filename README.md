# HW5_stacks
HW5 - Stacks pipeline and population genomics

For this homework, we're going to use the Stacks pipeline to identify and genotype SNPs in two populations of threespine sticklebacks (*Gasterosteus aculeatus*), and perform some basic population genomic comparisons. Use the Stacks protocol (`Rochette & Catchen 2017.pdf`) and website (`http://catchenlab.life.illinois.edu/stacks/`) for guidance on how to process samples; I will give you a bare-bones walkthrough of the analyses to perform and the parameters to set for this assignment. We will be using a different (much smaller!) set of example data than that used in the protocol, to ease the computational burden on Poseidon and save time. (So don't be alarmed that the protocol says it takes one week to one month, but please don't wait until the last minute either.)

The samples we'll use are single-end reads from two Alaskan stickleback populations, 8 individuals each from Bear Paw Lake (freshwater) and Rabbit Slough (marine). They derive from Hohenlohe et al. 2010, which is included in this repo if you want more details.

# Step 1: Set up

First, set up a conda environment called `stacks` with which to run this HW. You'll want to install Stacks (duh), and SRA tools to retrieve the raw sequences. What code did you use to set this environment up?\
```
```

Next, get the raw reads from the SRA. You want this file:\
`SRR034310`

These are RAD-derived reads, so rather than retrieving a single demultiplexed file for each individual, you are retrieving a single lane of sequencing where all reads contain a short identifying index. You'll use the Stacks pipeline to demultiplex these samples.

What code did you use to retrieve these reads?\
```
```

# Step 2: Demultiplex reads

