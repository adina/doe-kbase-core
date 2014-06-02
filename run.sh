#generates simulated metagenomes combined into one file
cat *renamed > metagenome-cumulative.fa

#requires khmer and dependencies
python ~/khmer/scripts/normalize-by-median.py -k 20 -C 10 -N 4 -x 3e8 -s norm10k20.kh metagenome-cumulative.fa
rm norm10k20.kh #do not need
rm metagenome-cumulative.fa #do not need


#requires velvet install
velveth assembly 21 metagenome-cumulative.fa.keep
velvetg assembly

#can be done anytime after assembly but prior to bedtools
python coverage-bed-reference.py contigs.fa #produces contigs.fa.bed

#requires bowtie2
mv assembly/contigs.fa .
rm -r assembly #do not need
bowtie2-build contigs.fa assembly
#can be done in parallel
for x in *renamed; do bowtie2 -x assembly -f $x -S $x.sam; done 

#requires samtools, can be done in parallel
for x in *sam; do samtools view -b -t contigs.fa $x > $x.bam; done

#requires bedtools, can be done in parallel
for x in *bam; do bedtools bamtobed -i $x > $x.bed; done
#requires preceding completed
for x in meta*bed; do coverageBed -a $x -b contigs.fa.bed > $x.reads.mapped; done
#alternate for preceeding, user dependent
#for x in meta*bed; do coverageBed -a $x -b contigs.fa.bed -d > $x.bed.coverage.perbase; done

#requires all bedfiles completed, can be run in parallel but on the same computer, ask andreas about dict structures
for x in *mapped; do python get-rpkm.py $x; done
#requires all rpkm calculated
python merge.py *rpkm

#requires curl
curl "http://api.metagenomics.anl.gov/1/annotation/similarity/mgm4566339.3?type=ontology&source=Subsystems" > annotations.txt

python best-hit.py annotations.txt 

#requires R and dependencies phyloseq, plyr, ggplot, saves output as RData
#also requires a meta.txt file
R < core.R --vanilla
