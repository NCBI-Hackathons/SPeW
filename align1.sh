#!/bin/sh
#
#tophat GRChr38 "{$1}_1.fq" "{$1}_2.fq"
#tophat GRChr38 "{$2}_1.fq" "{$2}_2.fq"



for f in *.fast* 
	do tophat GRChr38 '%s\n' "${f%.shp}.fq"
	done

for f in *.fast*
	do cufflinks '%s\n' "${f%.shp}.fq" '%s\n' "${f%.shp}thout/accepted_hits.bam"
	done


