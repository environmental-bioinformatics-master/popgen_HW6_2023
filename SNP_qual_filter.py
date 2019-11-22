#! /usr/bin/python

# Requires sample info file, in the following format:
# SAMPLE_1	GROUP
# SAMPLE_2	GROUP
# SAMPLE_3	GROUP

import sys

Usage = "USAGE: SNP_qual_filter.py RAW_SNP_TABLE_FROM_GATK QUALITY_CUTOFF SAMPLE_INFO MISSING_PER_SITE COVERAGE_PER_GT MITO_LIST INDIVS_TO_OMIT_LIST"

if (len(sys.argv) < 7) or (len(sys.argv) > 8):
	print("Please provide the correct inputs after the script name.")
	print(Usage)
	exit()
else:
	MasterFileName = sys.argv[1]
	QualCutoff = int(sys.argv[2])
	SampleFileName = sys.argv[3]
	MissingCutoff = int(sys.argv[4])
	CoverPerGT = int(sys.argv[5])
	MitoFileName = sys.argv[6]
	if len(sys.argv) == 8:
		IndivsToOmitFileName = sys.argv[7]


OutFileName = MasterFileName.strip(".table") + "_high-qual.txt"
EigenFileName = MasterFileName.strip(".table") + "_high-qual.eigenstratgeno"
SnpFileName = MasterFileName.strip(".table") + "_high-qual.snp"
StatsFileName = MasterFileName.strip(".table") + "_stats.txt"

print("Working with file: %s" % (MasterFileName))

MasterFile = open(MasterFileName, 'r')
SampleFile = open(SampleFileName, 'r')
MitoFile = open(MitoFileName, 'r')
OutFile = open(OutFileName, 'w')
EigenFile = open(EigenFileName, 'w')
SnpFile = open(SnpFileName, 'w')
StatsFile = open(StatsFileName, 'w')

StatsFile.write("Results of filtering SNPs in file: " + MasterFileName + "\n")

Samples = dict()

IndivsToOmit = []

if len(sys.argv) == 8:
	IndivFile = open(IndivsToOmitFileName, 'r')

	for Line in IndivFile:
		indiv = Line.strip()
		IndivsToOmit.append(indiv)

	print("\nRead in the following %d samples to omit:" % (len(IndivsToOmit)))
	print("\t".join(IndivsToOmit), "\n")
	StatsFile.write("\nRead in the following "+str(len(IndivsToOmit))+" samples to omit: \n")
	StatsFile.write("\t".join(IndivsToOmit)+"\n")

	IndivFile.close()

for Line in SampleFile:
	elements = Line.strip().split("\t")
	if elements[0] not in IndivsToOmit:
		if elements[1] not in Samples:
			Samples[elements[1]] = set()
			Samples[elements[1]].add(elements[0])
		else:
			Samples[elements[1]].add(elements[0])
	else:
		pass

print("\nRead in the following sites / sample numbers:")
StatsFile.write("\nRead in the following sites / sample numbers:\n")
for key in Samples:
	print(key, len(Samples[key]))
	SiteInfo = [key, str(len(Samples[key]))]
	StatsFile.write("\t".join(SiteInfo)+"\n")

SampleFile.close()

MitoGenes = []

for Line in MitoFile:
	transcript = Line.strip()
	MitoGenes.append(transcript)

print("\nRead in %d mitochondrial transcripts for removal.\n" % (len(MitoGenes)))
StatsFile.write("\nRead in "+str(len(MitoGenes))+" mitochondrial transcripts for removal.\n")

MitoFile.close()

colNames = []
header = []
snpEls = []

LowQual = 0
NotBiallelic = 0
RareAlt = 0
PoorGenosBySite = 0
ReversedRefAndAlt = 0
PotentialParalog = 0
Mitochondrial = 0
VarsRarePostCleaning = 0

GoodGenos = 0

for Line in MasterFile:
	if "CHROM" in Line:
		colNames = Line.strip().split("\t")
		header = colNames[0:4]
		for name in colNames:
			if ".GT" in name:
				if name.strip(".GT") not in IndivsToOmit:
					header.append(name.strip(".GT"))
		OutFile.write("\t".join(header) + "\n")
	else:
		snpEls = Line.strip().split("\t")
		if float(snpEls[colNames.index("QUAL")]) < QualCutoff:
			LowQual+=1
		elif "," in snpEls[colNames.index("ALT")]:
			NotBiallelic+=1
		elif float(snpEls[colNames.index("AC")]) < 2:
			RareAlt+=1
		else:
			QualSite = 0
			MitoChecker = 0
			SiteGenos = []
			for site in Samples:
				qualBySite = []
				coverBySite = []
				HighQual=0
				HighCover=0
				for indiv in Samples[site]:
					qualBySite.append(snpEls[colNames.index(indiv+".GQ")])
					coverBySite.append(snpEls[colNames.index(indiv+".DP")])	
					SiteGenos.append(snpEls[colNames.index(indiv+".GT")])
				for qual in qualBySite:
					if (qual != "NA") and (int(qual) > QualCutoff):
						HighQual+=1
				for cover in coverBySite:
					if (cover != "NA") and (int(cover) > CoverPerGT):
						HighCover+=1
				if (HighQual >= (len(qualBySite)-MissingCutoff)) and (HighCover >= (len(qualBySite)-MissingCutoff)):
					QualSite+=1
			HomRef = SiteGenos.count(snpEls[2]+"/"+snpEls[2])
			HomAlt = SiteGenos.count(snpEls[3]+"/"+snpEls[3])
			Het = SiteGenos.count(snpEls[2]+"/"+snpEls[3])
			if QualSite < len(Samples):
				PoorGenosBySite+=1
			elif (HomAlt*2+Het) < 2 or (HomRef*2+Het) < 2:
				VarsRarePostCleaning+=1
#			elif Het > (HomRef+HomAlt+Het)*0.7:
#				PotentialParalog+=1
			elif snpEls[0] in MitoGenes:
				Mitochondrial+=1
			else:
				if (HomRef*2+Het) < (HomAlt*2+Het):
##					RefHolder = snpEls[colNames.index("REF")]
##					snpEls[colNames.index("REF")] = snpEls[colNames.index("ALT")]
##					snpEls[colNames.index("ALT")] = RefHolder
					ReversedRefAndAlt+=1			
				GoodGenos+=1
				DataToWrite = snpEls[0:4]
				EigenToWrite = []
				for item in header[4:]:
					if item not in IndivsToOmit:					
						if (snpEls[colNames.index(item+".GQ")] == "NA") or \
						(snpEls[colNames.index(item+".DP")] == "NA") or \
						(int(snpEls[colNames.index(item+".GQ")]) < QualCutoff) or \
						(int(snpEls[colNames.index(item+".DP")]) < CoverPerGT):
							DataToWrite.append("./.")
							EigenToWrite.append("9")
						else:
							DataToWrite.append(snpEls[colNames.index(item+".GT")])
							if snpEls[colNames.index(item+".GT")] == str(snpEls[2]+"/"+snpEls[2]):
								EigenToWrite.append("2")
							elif (snpEls[colNames.index(item+".GT")] == str(snpEls[2]+"/"+snpEls[3])) or \
							(snpEls[colNames.index(item+".GT")] == str(snpEls[3]+"/"+snpEls[2])):
								EigenToWrite.append("1")
							elif snpEls[colNames.index(item+".GT")] == str(snpEls[3]+"/"+snpEls[3]):
								EigenToWrite.append("0")
				OutFile.write("\t".join(DataToWrite) + "\n")
				EigenFile.write("".join(EigenToWrite) + "\n")
				SnpToWrite = ["_".join(snpEls[0:2]), "1", "0.0", "0", snpEls[2], snpEls[3]]
				SnpFile.write("\t".join(SnpToWrite) + "\n")


print("\nDropped for quality < %d: %d" % (QualCutoff, LowQual))
print("Dropped because > 2 alleles: %d" % (NotBiallelic))
print("Dropped because alt. allele occurred < 2 times: %d" % (RareAlt))
print("Dropped because good genotypes missing at > %d samples per population: %d" % (MissingCutoff,PoorGenosBySite))
print("Dropped because alt. allele occurred < 2 times in high-quality genotypes: %d" % (VarsRarePostCleaning))
print("Dropped because of potential paralogy (> 70 percent heterozygotes): %d" % (PotentialParalog))
print("Dropped because they are in mitochondrial genes: %d" % (Mitochondrial))
#print("\nReversed reference and alternate alleles: %d" % (ReversedRefAndAlt))
print("\nAlternate allele is most common for: %d" % (ReversedRefAndAlt))
print("Good genotypes defined as having quality > %d and coverage > %d reads." % (QualCutoff, CoverPerGT))
print("Remaining high-quality SNPs written to file: %d" % (GoodGenos))

MasterFile.close()	# Clean up after your damn self.
OutFile.close()
EigenFile.close()
SnpFile.close()

StatsFile.write("\nDropped for quality < "+str(QualCutoff)+": "+str(LowQual)+"\n")
StatsFile.write("Dropped because > 2 alleles: "+str(NotBiallelic)+"\n")
StatsFile.write("Dropped because alt. allele occurred < 2 times: "+str(RareAlt)+"\n")
StatsFile.write("Dropped because good genotypes missing at > "+str(MissingCutoff)+" samples per population: "+str(PoorGenosBySite)+"\n")
StatsFile.write("Dropped because alt. allele occurred < 2 times in high-quality genotypes: "+str(VarsRarePostCleaning)+"\n")
StatsFile.write("Dropped because of potential paralogy (> 70 percent heterozygotes): "+str(PotentialParalog)+"\n")
StatsFile.write("Dropped because they are in mitochondrial genes: "+str(Mitochondrial)+"\n")
#StatsFile.write("\nReversed reference and alternate alleles: "+str(ReversedRefAndAlt)+"\n")
StatsFile.write("\nAlternate allele is most common for: "+str(ReversedRefAndAlt)+"\n")
StatsFile.write("Good genotypes defined as having quality > "+str(QualCutoff)+" and coverage > "+str(CoverPerGT)+" reads.\n")
StatsFile.write("Remaining high-quality SNPs written to file: "+str(GoodGenos)+"\n")
StatsFile.write("\nHigh-quality SNP file: "+OutFileName+"\n")

StatsFile.close()
print("\nQuality filtering complete! Share and enjoy.")
