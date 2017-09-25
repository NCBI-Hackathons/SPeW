#!/bin/bash
#fastqc module
#Natalie nlr23@pitt.edu

while getopts i:o: option
do 
	case "${option}"
	in
	i) inPath=${OPTARG};;
	o) outPath=${OPTARG};;
	esac
done

echo 'Performing QC of fastq files'
module load FastQC
for f in $inPath/*.fastq.gz; do
	fileName=$(echo ${f})
	echo "Processing $fileName file"
	fastqc $fileName -f fastq -o $outPath	
done
	
echo "QC of fastq files completed"