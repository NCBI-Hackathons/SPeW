#!/bin/bash
# Testing version of trimming sequencing data
# Zhou (Ark) Fang zhf9@pitt.edu

# e.g. ./trimming.sh -i ./RNAseq_files -s -a1 ADATPER_FWD -a2 ADATPER_REV

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -i|--inPath)
    inPath="$2"
    shift # past argument
    shift # past value
    ;;
    -s|--singleEnd)
    singleEnd=true
    shift # past argument
    ;;
    -a1|--adapter1)
    adapter1="$2"
    shift # past argument
    shift # past value
    ;;
    -a2|--adapter2)
    adapter2="$2"
    shift # past argument
    shift # past value
    ;;
    --default)
    DEFAULT=true
    shift # past argument
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# echo FILE EXTENSION  = "${EXTENSION}"

if [ $DEFAULT = true ];  then
    inPath=./RNAseq_files #intermidiate input file path for trimming
    singleEnd=false #by default, subject to change
    adapter1=ADATPER_FWD
    adapter2=ADATPER_REV
fi

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
            cutadapt -a $adapter1 -m 20 -o $outfileName $fileName &
        fi
    done
    wait
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
           cutadapt -a $adapter1 -A $adapter2 -m 20 -o $outfileName1 $outfileName2 $fileName1 $fileName2 &
         fi
     done
     wait
fi

echo "Sequencing trimming completed."