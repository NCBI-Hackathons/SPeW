#!/bin/bash
#fastqc module
#Natalie nlr23@pitt.edu

inPath=./#fastqfile to go through quality control program

echo 'Performing QC of fastq files'

for f in $inPath/*.fastq.gz; do
	fileName=$(echo ${f})
	echo "Processing $fileName file"
	fastqc $fileName -f fastq -o $outPath	
done
	
echo "QC of fastq files completed"