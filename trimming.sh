#!/bin/bash
# Testing version of trimming sequencing data
# Zhou (Ark) Fang zhf9@pitt.edu
inPath=. #intermidiate input file path for trimming
singleEnd=false #by default, subject to change
adapter=ADATPER_FWD

if [ "$singleEnd" = true ] ; then
    echo 'Single-end sequencing file used'
    for f in $inPath/*.fastq.gz; do
        fileName=$(echo ${f})
        if [[ $fileName != *"trimmed"* ]]; then
            echo $fileName
            echo "Processing $fileName file"
            suffix=".fastq.gz"
            outfileName=${fileName%$suffix}
            outfileName+="_trimmed.fastq.gz"
            echo $outfileName
#            cutadapt -a $adapter -m 20 -o $outPath/$outfileName\_trimmed.fastq.gz $inPath/$fileName
        fi
    done
 else
     echo 'Pair-end sequencing files used'
     for f in $inPath/*1.fastq.gz; do
         fileName1=$(echo ${f})
         if [[ $fileName != *"trimmed"* ]]; then
             suffix="1.fastq.gz"
             fileName2=${fileName1%$suffix}
             fileName2+="2.fastq.gz"
             echo "Processing $fileName1 and $fileName2 files..."
             outfileName1=${fileName1%$suffix}
             outfileName2=${fileName1%$suffix}
             outfileName1+="1_trimmed.fastq.gz"
             outfileName2+="2_trimmed.fastq.gz"
              cutadapt -a $adapter -A $adapter -m 20 -o $outPath/$outfileName\_trimmed_R1.fastq.gz $outPath/$outfileName\_trimmed_R2.fastq.gz $inPath/$fileName1 $inPath/$fileName2
         fi
     done
fi

echo "Sequencing trimming completed."