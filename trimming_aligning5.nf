#!/usr/bin/env nextflow
/* Testing for NCBI SpEW project, trimming module
* Zhou (Ark) Fang zhf9@pitt.edu
*/
inPath = "/zfs1/ncbi-workshop/AP/nextflow/"
inFiles = "$inPath/*.fastq.gz"
singleEnd = true
adapter1 = "ADATPER_FWD"
adapter2 = "ADATPER_REV"
params.in = "/zfs1/ncbi-workshop/AP/nextflow/*.fastq"
sequences = file(params.in)
/* records = "/zfs1/ncbi-workshop/AP/RNAseq/AlignedReads/"  */

process modules{
script:
        """
	module load FastQC
       	module load bowtie2
        module load tophat
        module load cutadapt
        """
}

process fastqc{
input:
file reads from sequences

script:
	"""
	mkdir fastqc_logs
	fastqc -o fastqc_logs -f fastq -q ${reads}
	"""
}

process trimming{

input:
file inFiles

output:
file 'trimmed_*' /* into records */

script:
   if (singleEnd==true)
   """
   bash trimming.sh -i inPath -s -a1 adapter1 -a2 adapter2
   """
   else
   """
   bash /zfs1/nci-workshop/AP/nextflow/trimming.sh -i inPath -a1 adapter1 -a2 adapter2
   """
}

process alignment {

        input:
        file '*.fastq.gz'

        output:
        file 'aligned_*' into /* records */

        """
	bash /zfs1/ncbi-workshop/AP/nextflow/align2.sh
	"""
}