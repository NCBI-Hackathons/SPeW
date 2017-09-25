#!/bin/bash
#Just a testing version of trimming sequencing data
#Ark zhf9@pitt.edu
inPath=./ #intermidiate input file path for trimming
singleEnd=true
outPath=./
adapter=ADATPER_FWD

mkdir $outPath

if [ "$singleEnd" = true ] ; then
    echo 'Single-end sequencing file used'
    for f in $inPath/*.fastq.gz; do
        fileName=$(echo ${f})
        echo "Processing $fileName file"
        outfileName=${fileName%".fastq.gz"*} #fix
        cutadapt -a $adapter -m 20 -o $outPath/$outfileName\_trimmed.fastq.gz $inPath/$fileName
    done
else
    echo 'Pair-end sequencing files used'
    for f1 in $inPath/*1.fastq.gz; do
        fileName1=$(echo ${f1})
        fileName2=$(echo ${f2})
        echo "Processing $fileName1 and $fileName2 files..."
        outfileName=${fileName%"1.fastq.gz"*} #fix
        cutadapt -a file:
        cutadapt -a $adapter -A $adapter -m 20 -o $outPath/$outfileName\_trimmed_R1.fastq.gz $outPath/$outfileName\_trimmed_R2.fastq.gz $inPath/$fileName1 $inPath/$fileName2
    done
fi

echo "Sequencing trimming completed."