#!/bin/sh
#
# for alignment with classic bowtie
bowtie -t homo_sapiens $1 homo_sapiens.map


#for alignment with bowtie2
# bowtie2 -t homo_sapiens $1 homo_sapiens.map
