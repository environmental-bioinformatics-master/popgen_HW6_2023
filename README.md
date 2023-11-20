# HW6 - Stacks pipeline and population genomics

For this homework, we're going to use the Stacks pipeline to identify and genotype SNPs in two populations of threespine sticklebacks (*Gasterosteus aculeatus*), and perform some basic population genomic comparisons. Use the Stacks protocol (`Rochette & Catchen 2017.pdf`) and website (`http://catchenlab.life.illinois.edu/stacks/`) for guidance on how to process samples; you are also welcome to use any other online resources you like.

If you used additional resources, please list them here:\
>Answer:

I will give you a bare-bones walkthrough of the analyses to perform and the parameters to set for this assignment. We will be using a different (much smaller!) set of example data than that used in the protocol, to ease the computational burden on Poseidon and save time. So don't be alarmed that the protocol says it takes one week to one month, but please don't wait until the last minute either.

The samples we'll use are single-end reads from two Alaskan stickleback populations, 8 individuals each from Bear Paw Lake (freshwater) and Rabbit Slough (marine). They derive from Hohenlohe et al. 2010, which is included in this repo if you want more details.

Please copy this document and change the name to `hw6_answers_[LASTNAME].md`, and reply in the document as prompted. We'll also ask you to create and save a few additional files to be pushed with your HW repo. Everything we want you to submit is listed at the bottom of this document.

# Step 1: Set up

First, set up a conda environment called `stacks` with which to run this HW. Install Stacks (duh), SRA tools to retrieve the raw sequences, and eigensoft to run a PCA with your clean SNPs. When you set up this environment, specifically install the most recent conda version of each program. (Hint: Check the conda install pages.) Create a yaml file called `hw6_stacks_[LASTNAME].yml` that can be used to set up this environment - please make sure it is succinct and tidy, specifies version numbers, and only lists the packages you need to install independently (and **not** all of the extra dependencies that are installed along with them).

Next, set up a slurm script called `hw6_stacks-pipeline_[LASTNAME].txt`. Put **every** command you run for this HW through all of the Stacks analyses into this file to create a pipeline that can be run on Poseidon. For example, if you need to reformat a file for use in the pipeline, include the code you used to reformat that file. Comment it clearly, so it is obvious what is being done at every step. In the end, I want a script that I can run on Poseidon as-is, starting with file retrieval and ending with Stacks output, assuming I first use your yaml file above to create the appropriate environment. (You'll need to modify a few files to run smartpca later on; you can do this however you like and don't need to include these conversions in your pipeline script.)

Next, get the raw reads from the SRA. You want this file:
`SRR034310`

These are RAD-derived reads, so rather than retrieving a single demultiplexed file for each individual, you are retrieving a single lane of sequencing where all reads contain a short identifying index. You'll use the Stacks pipeline to demultiplex these samples.

There is more information on individual samples, their barcodes, etc in a file available at Zenodo, a popular data-archiving site. That information is here:\
`https://zenodo.org/record/1134547/files/Details_Barcode_Population_SRR034310.txt`

Copy this file from the web to this repo. You'll need some of this information to process your reads, but note that you will have to modify this format for downstream use. (Hint: `sed` or `awk` might be useful!) Make sure to include all code you use to copy / modify these data for downstream use in your `hw6_stacks-pipeline_[LASTNAME].txt` file.

Remember to include (and comment!) the code you used to retrieve these files in your `hw6_stacks-pipeline_[LASTNAME].txt` file.
 

# Step 2: Demultiplex reads

Now, you need to demultiplex your reads using the barcode information in the file you just retrieved from Zenodo. Use these parameters:\
Restriction enzyme: sbfI\
Clean reads\
Discard low-quality reads\
"Rescue" reads and barcodes

Hint: for reasons irritating and unknown to me, if you ask Stacks to write data to a directory that doesn't exist, it will throw an error. Save yourself some hassle and create an empty output directory before running Stacks.

Remember to include (and comment!) the code you used to demultiplex your reads in your `hw6_stacks-pipeline_[LASTNAME].txt` file.

What percentage of reads were retained after demultiplexing?
>Answer:

# Step 3: Identify SNPs

Typically, you would run this part of the process multiple times with different stack quality and distance parameters to figure out a good set of parameters for your data set. For this homework, we won't ask you to optimize parameters, but be aware that this is a best practice with experimental data. These parameters and how they affect SNP identification are explained in detail in the protocol paper and on the Stacks website here:\
`http://catchenlab.life.illinois.edu/stacks/param_tut.php`

While you could potentially run Stacks in a reference-aware way using the stickleback genome, for this homework assume there is no genome and run the _de novo_ protocol.

Use the following parameters to form stacks and identify SNPs:\
Minimum coverage to create a stack: 3\
Number of mismatches allowed between stacks (within individuals): 2\
Number of mismatches allowed between loci (between individuals): 3\
Number of threads to run on: 4 (be sure to run with slurm and request 4 nodes)

This should take approximately 2 hours on Poseidon using 4 threads (but give yourself some buffer time).

Remember to include (and comment!) the code you used to identify SNPs in your `hw6_stacks-pipeline_[LASTNAME].txt` file.

For each population, give the following information **pre-filtering**:
>*Bear Paw:*\
  Range of coverage depth (lowest and highest):\
  Polymorphic sites:\
  Private alleles:\
*Rabbit Slough:*\
  Range of coverage depth (lowest and highest):\
  Polymorphic sites:\
  Private alleles:

What's the difference between a "locus" and a "SNP", as Stacks uses those terms? (one to a few lines)
>Answer:

What does the "private alleles" count tell you? (one to a few lines)
>Answer:

What might explain any observed difference between the number of polymorphic sites and private alleles between the two populations? (one to a few lines)
>Answer:

# Step 4: Filter SNPs and calculate population genomic stats

Now, use the `populations` application of Stacks to go back through your raw SNPs, apply some additional filtering criteria, and conduct basic popgen statistics. Set the following parameters:\
Locus must be present in **both** populations\
Locus must be present in at least 7 individuals in each population\
Heterozygosity must under 70% to retain a SNP\
Minor allele must be present at least twice overall to retain a SNP\
Retain one SNP per locus (= RAD tag) at random \
Calculate F-statistics\
Export files in vcf and Genepop formats

This should run very quickly on Poseidon (<15 minutes).

Note: I feel very strongly that it is a best practice to calculate linkage disequilibrium directly rather than assuming your SNPs are unlinked if you only use one per RAD tag. However, that is a standard practice, and in the interests of streamlining this HW, go ahead and use this standard approach which is already built into Stacks.

Remember to include (and comment!) the code you used to filter SNPs in your `hw6_stacks-pipeline_[LASTNAME].txt` file.

Now that you have applied some QC for SNP coverage and completeness, give the following information again for each population:
>*Bear Paw:*\
  Polymorphic sites:\
  Private alleles:\
*Rabbit Slough:*\
  Polymorphic sites:\
  Private alleles:
  
This analysis will create a number of output files. Explore them until you find the overall pairwise Fst between the two populations, and summary statistics (Fis, Pi, expected and observed heterozygo) for each population.

What is the Fst between the Bear Paw Lake and Rabbit Slough populations?
>Answer:

What does this Fst suggest about connectivity between these two populations? (one to a few lines)
>Answer:

What are the following summary statistics for each population, calculated at variant sites only?
>*Bear Paw:*\
  Observed heterozygosity:\
  Expected heterozygosity:\
  Pi (nucleotide diversity):\
  Fis (inbreeding coefficient):\
*Rabbit Slough:*\
  Observed heterozygosity:\
  Expected heterozygosity:\
  Pi (nucleotide diversity):\
  Fis (inbreeding coefficient):
  
What do these values suggest about genetic diversity between these two populations? (one to a few lines)
>Answer:

# Step 5: Convert file format and run PCA

There are a lot of different places you could go with your SNP panel from here. We're going to use the eigensoft program to conduct a Principal Components Analysis of the cleaned SNPs you generated with Stacks. Unfortunately, like almost every population genomics software, it requires a special input format. I have provided two python scripts written by Iain Mathieson to convert your Stacks-generated `.vcf` file to the multiple input files required by eigensoft.

Convert your Stacks-provided `.vcf` file by using `vcf2eigensoft_v2.py`. Include the `popmap` file you generated earlier for Stacks with the optional `-i` flag, to assign individual samples back to populations. The other file, `gdc.py`, contains functions that will be called by `vcf2eigensoft_v2.py` so it needs to be in the same directory for the conversion to work.

Now, run some basic population genomics tests using the smartpca component of eigensoft. Be sure to submit this using slurm or after requesting time with srun so you can restrict the number of nodes it runs on - smartpca is greedy and will run on 35 threads if you let it!

To run smartpca, you need 4 files:\
`.snp`: generated by python script\
`.geno`: generated by python script\
`.ind`: generated by python script (Check as below to make sure format is correct!)\
`par.`: provided in repo as `par.example`; modify to use your filenames

Check the `.ind` file created during the file conversion process to ensure the format is correct. (It should be, if you used the `-i` flag with `vcf2eigenstrat_v2.py` and specified the correct file assigning individuals to populations.) The third column should be the name of the population the sample is from. The column in between the sample names and the population names should be "U" for every individual; it provides information on the sex of each individual and can be M(ale), F(emale), or U(nknown).

Format example:
>Sample_1	U	Pop_1\
Sample_2	U	Pop_1\
Sample_3	U	Pop_2

Open the par.example file and change the names of the input and output files according to how you have them named (input: `.snp`, `.geno`, `.ind`), or would like to have them named (output: `.evec`, `.eval`).

Run smartpca by specifying the `par.*` parameter file, and redirecting the output (which will include a lot of good stats and stuff) to a new output logfile:\
`smartpca -p par.[PAR_FILENAME] > hw6_pca_log_[LASTNAME].log`

Now, let's take a look! We are most interested in the individual PC loadings in the `*.evec` file and in some of the tests shown in the `log.txt` file.

In the `*log.txt` file, look for the row starting with `## Tracy-Widom statistics`. This gives the eigenvalue (percentage of variance explained) and significance for each numbered principal components axis.

How many principal components axes are significant?
>Answer:

For each significant principal components axis, give the following:
>Eigenvalue:\
p-value:

The `.evec` files gives the PC loading for each sample on the first 10 principal components axes. Axes are labeled by their eigenvalues, ordered from highest (= most influence on population structure) to lowest.

Using python or R (or another language of your choice*), make a scatter plot of the individuals for PC1 and PC2, using the loadings from the `.evec` file and color-coding individuals by site. (Hint: you may need to modify the `.evec` file to get your plotting program of choice to read it properly.) Feel free to do this plotting on Poseidon or your local computer, whatever you're most comfortable with. Please include the code for your plot in a file named: `hw6_pca_plot_code_[LASTNAME].[EXTENSION]`, and push that with your homework along with the plot in `.pdf` format named `hw6_pca_plot_[LASTNAME].pdf`.

\*But **do** script your plot - don't make it automatically in a GUI like Excel or SigmaPlot.

What does the PCA tell you about divergence and diversity in these stickleback populations? (a few lines, a paragraph max)
>Answer:

Look at the paper, if you haven't already. Thinking about the PCA and the statistics you calculated in Stacks, as well as your understanding of population genomics, what do you think is driving observed patterns of divergence and diversity in these stickleback populations? (a paragraph, two max)
>Answer:

About how long did this homework take you?:
>Answer:

For your homework, please push to GitHub:

1. `hw6_stacks-pipeline_[LASTNAME].txt`: COMPLETE, commented code you used from file retrieval through running Stacks (excluding PCA and plotting).
2. `hw6_answers_[LASTNAME].md`: An annotated copy of this readme file including your answers.
3. `hw6_stacks_[LASTNAME].yml`: A succinct yaml file that can be used to set up the environment to run your pipeline.
4. `hw6_pca_log_[LASTNAME].log`: The logfile from running smartpca.
5. `hw6_pca_plot_code_[LASTNAME].[EXTENSION]`: Commented code for PCA plotting.
6. `hw6_pca_plot_[LASTNAME].pdf`: PCA plot.
