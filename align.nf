#!/usr/bin/env nextflow
# Testing for NCBI SpEW project, alignment module
# Argus Sun argus@ucsd.edu
#

params.in = "/zfs1/ncbi-workshop/AP/RNAseq/*.fastq"
sequences = file(params.in)
records = "/zfs1/ncbi-workshop/AP/RNAseq/AlignedReads/"

process alignment {

	input:
	file '*.fastq.gz' from trimmed_sequences

	output:
	file 'aligned_*' into records

	"""
 	for f in *.fast*; do tophat -o "${f%.fastq.gz}.fq" mm10_genes.gtf -p 8 -G mm10genes.gtf "${f%.fastq.gz}.fastq.gz"; done
	"""