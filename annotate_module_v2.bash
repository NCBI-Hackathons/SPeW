#!/bin/bash

module purge
module load compiler/java/1.8.0_65-oracle
module load samtools/1.2-gcc5.2.0
module load tophat/2.1.1
module load bowtie2/2.3.2-gcc5.2.0
module load cufflinks/2.2.1
module load HTSeq/0.9.0

while getopts ha:b:p:g: option
do
 case "${option}"
 in
 h) echo -ne "Usage:\$ bash $0 -a annotate-method -b bam_directory -p sample_phenotype -g reference_gtf\n"
    echo -ne "Options\n-a: Method of annotation with values Cufflinks or Reference (default: Reference)\n"
    echo -ne "-b: Input bam directory full-path(default: current working directory)\n"
    echo -ne "-p: Input sample phynotype file in directory full-path(default: current working directory)\n"
    echo -ne "-g: Input Reference gtf file full-path(default: current working directory)\n"
    exit 1;;
 a) annot=${OPTARG};;
 b) bamdir=${OPTARG};;
 p) sm_phtype=${OPTARG};;
 g) refseq_gtf=${OPTARG};;
 esac

done

if [ -z "$annot" ]
then
 annot="Reference"
fi

if [ -z "$bamdir" ]
then
 echo "No gtf path specified. Looking in current $(pwd)"
 dir=$(pwd)
 bam=$(ls ${dir}/*.bam)
fi

if [ -z "$sm_phtype" ]
then
 echo "No gtf path specified. Looking in current $(pwd)"
 dir=$(pwd)
 sm_phtype=${dir}/sample_phenotype.txt
fi

if [ -z "$refseq_gtf" ]
then
 echo "No gtf path specified. Looking in current $(pwd)"
 dir=$(pwd)
 refseq_gtf=$(ls ${dir}/*.gtf)
fi

#################################################

if [ $annot = "Cufflinks" ]

then

 ####### Assembly #################################

 ### cufflinks  ###################

 echo "Running cufflinks..."

 for file in $(ls ${bamdir}/*.bam)

 do
 
  sample=$(basename $file .bam)
  
  echo "Sample: $readname"

  cufflinks_out=${readname}_cufflinks

  if [ $(samtools view -c -f 1 $file) -gt 0 ]

  then

    cufflinks -p 1 -g $refseq_gtf -o $cufflinks_out --library-type fr-firststrand $file 2> ${cufflinks_out}.log &

  else
 
   cufflinks -p 1 -g $refseq_gtf -o $cufflinks_out $file 2> ${cufflinks_out}.log &

  fi

  echo "$cufflinks_out/transcripts.gtf" >> assembly_list.txt

 done

 wait

 #### cuffmerge ############################### 

 cuffmerge_out=cuffmerge_output

 cuffmerge -s ${index}.fa -g $refseq_gtf -p 1 -o $cuffmerge_out assembly_list.txt
 
 input_gtf=${cuffmerge_out}/merged.gtf
 
#####################################################

else

 input_gtf=$refseq_gtf

fi

####  HTSeq counts #########################

out_count=HTSeq_count

mkdir -p $out_count

#### Checking and sorting bam files for paired-end reads

echo "Checking and sorting bam files for paired-end reads"

for file in $(ls ${bamdir}/*.bam)

do

 if [ $(samtools view -c -f 1 $file) -gt 0 ]

 then

  mkdir -p name_sorted

  sample=$(basename $file .bam)

  echo "Sample: $sample"

 # To run HTSeq on paired end sort bam file by name
  samtools sort -n $file ${bamdir}/name_sorted/${sample}.name_sorted &

 fi

done

wait

##### Running HTSeq

echo "HTSeq count"

for file in $(ls ${bamdir}/*.bam)

do

 sample=$(basename $file .bam)

 echo "Sample: $sample"

 if [ $(samtools view -c -f 1 $file) -gt 0 ]

 then

 htseq-count -f bam --stranded=no ${bamdir}/name_sorted/${sample}.name_sorted.bam $input_gtf > ${out_count}/${sample}_count.no_strand.txt &

 else

 htseq-count -f bam --stranded=no $file $input_gtf > ${out_count}/${sample}_count.no_strand.txt &

 fi

done

wait

###### Combining files

cd $out_count

echo "gene_id" > gene_id; cat *.txt | cut -f 1 | sort -u >> gene_id

while read line; do sm=$(echo "$line" | cut -f 1); echo "$sm" > ${sm}_count; cat ${sm}*.txt | sort -k 1,1 | cut -f 2 >> ${sm}_count; done < $sm_phtype

paste gene_id *_count > htseq_count.txt

############################################################
