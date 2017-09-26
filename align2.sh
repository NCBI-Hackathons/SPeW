#!/bin/sh
#
for f in *.fast*; do tophat -o  "${f%.fastq.gz}.fq" mm10_genes.gtf -p 8 -G mm10genes.gtf "${f%.fastq.gz}.fastq.gz"; done;