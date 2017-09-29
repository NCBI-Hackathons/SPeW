#!/bin/shell/
#

while true; do
	read -p "Do you wish to fastqc your input?"
	case $yn in
		[Yy]* ) ./nextflow fastqc.nf
		[Nn]* ) exit;;
		*  ) echo "Please answer yes or no."
	esac
done

while true; do
	read -p "Do you wish to trim your input?"
	case $yn in
		[Yy]* ) ./nextflow trim.nf
		[Nn]* ) exit;;
		*  ) echo "Please answer yes or no."
	esac
done

while true; do
	read -p "Do you wish to align your input?"
	case $yn in
		[Yy]* ) ./nextflow align.nf
		[Nn]* ) exit;;
		*  ) echo "Please answer yes or no."
	esac
done

while true; do
	read -p "Do you wish to annotate your input?"
	case $yn in
		[Yy]* ) ./nextflow annotate.nf
		[Nn]* ) exit;;
		*  ) echo "Please answer yes or no."
	esac
done

while true; do
	read -p "Do you wish to analyze Differential Gene Expression?"
	case $yn in
		[Yy]* ) ./nextflow DGE.nf
		[Nn]* ) exit;;
		*  ) echo "Please answer yes or no."
	esac
done

