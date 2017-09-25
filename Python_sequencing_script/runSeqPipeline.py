'''
information about program
	Use to get arguments for sequencingPipeline.py
	
	usage:
		python RunPipeline.py 
'''
#!/usr/bin/env python


import os, sys, time, subprocess, csv

def getType():
	check = False
	type = raw_input('What is the type of sequencing performed?: \n\t')
	while check == False:
		if type in ('atac','ATAC','chip','ChIP','rna','RNA'):
			return type
			check = True
		else:
			print >>sys.stderr, 'That sequencing type is not supported. Please try again.'
			type = raw_input('What is the type of sequencing performed?: \n\t')
		
def getFilePath():
	check = False
	filePath = raw_input('What is the path to the fastq files? (everything but the *.fastq file): \n\t')
	while(check == False):
		if(os.path.exists(filePath) == False):
			print >>sys.stderr,"That isn't a vaild path. Please make sure to spell everything correctly."
			filePath = raw_input('What is the path to the fastq files? (everything but the *.fastq file): \n\t')
		else:
			return filePath
			check = True
			
def getOutputFilePath():
	check = False
	filePath = raw_input('What is the path to the output folder where you want all the files to go? (there should NOT be a "/" after the final folder): \n\t')
	while(check == False):
		if(os.path.exists(filePath) == False):
			new = raw_input('That is path does not exist. Would you like to create this directory (yes/no)?: \n\t')
			if(new == 'yes'):
				head = os.path.split(filePath)[0]
				if os.path.exists(head) == True:
					os.mkdir(filePath)
					return filePath
					check = True
				else:
					print >>sys.stderr,'There is a mistake in the begining of your path. Cannot make directory.'
					filePath = raw_input('Please type a valid path for the files to go: ')
			elif(new == 'no'):
				filePath = raw_input('Please type a valid path for the files to go? (there should NOT be a "/" after the final folder): \n\t')
			else:
				filePath = raw_input('That was not a valid response of yes or no, so we will treat it like a no. Please enter a valid path for the files to go. \n\t') 
		else:
			return filePath
			check = True
			
def getNumThreads():
	numThreads = raw_input('How many threads do you wish to use? (defualt is 8): \n\t')
	try:
		if (int(numThreads) >= 1 and int(numThreads) <= 16):
			print >>sys.stderr,'The number of threads that will be used is: '+numThreads
			return numThreads
		else:
			print >>sys.stderr,'You did not choose a vaild number of threads so the default will be used (8).'
			numThreads = '8'
			return numThreads
	except(ValueError):
		print >>sys.stderr,'That was not a valid number of threads so the default will be used (8).'
		numThreads = '8'
		return numThreads
		
def getSample(file):
	if 'gz' in file: 
		fn = os.path.splitext(os.path.basename(file))[0]
		fn = os.path.splitext(fn)[0]
	else: 
		fn = os.path.splitext(os.path.basename(file))[0]	
	if ('_S0' in fn) or ('_S1' in fn) or ('_S2' in fn) or ('_S3' in fn) or ('_S4' in fn) or ('_S5' in fn) or ('_S6' in fn) or ('_S7' in fn) or ('_S8' in fn) or ('_S9' in fn):
		param, value = fn.split('_S',1)
		sample = param
	elif('_R1' in fn) or ('_R2' in fn):
		param, value = fn.split('_R',1)
		sample = param
	else: 
		sample = fn
	return sample
	
def getGenome(sl):
	genomes = os.listdir(sl+'/ref')
	check = False
	genome = raw_input('\nWhat organism and genome version would you like to use?:\n\t')
	while(check == False):
		if genome in genomes:
			return genome
			check = True
		else:
			print >>sys.stderr, '\nThat was not a valid genome. Please try again.'
			print >>sys.stderr, '\nGenomes available:'
			for i in range(len(genomes)):
				print >>sys.stderr,'\t'+genomes[i]
			genome = raw_input('\nWhat organism and genome version would you like to use?:\n\t')
			
def getAdapter():
	ada = raw_input('\nDo you have a fasta file or would you like to use the default Nextera or Truseq adapters (file, Nextera, or Truseq)?:\n\t')
	while ada not in ('file','nextera','Nextera','truseq','Truseq'):
		print >>sys.stderr, '\nThat was not an acceptable response. Please try again'
		ada = raw_input('\nDo you have a fasta file or would you like to use the default Nextera or Truseq adapters (file, Nextera, or Truseq)?:\n\t')
	check = False	
	if ada in ('file','nextera','Nextera','truseq','Truseq'):
		if ada == 'file':
			file = raw_input('\nWhat is the name of the file containing the adapters?:\n\t')
			while check == False:
				if(os.path.isfile(file) and '.fa' in file):
					return file
					check = True
				elif(os.path.isfile(file) and '.fa' not in file):
					print >>sys.stderr, '\nThis is not the correct file format. A fasta file is required.'
					file = raw_input('\nWhat is the name of the file containing the adapters?:\n\t')
				else:
					print >>sys.stderr, '\nThat file does not exist. Please try again.'
					file = raw_input('\nWhat is the name of the file containing the adapters?:\n\t')			
		elif ada in ('nextera','Nextera'):
			adapter= 'n'
			return adapter
		elif ada in ('truseq','Truseq'):
			adapter = 't'
			return adapter
		else:
			sys.exit('\nThere is something wrong with adapter code that needs to be fixed')
	else:
		sys.exit('\nThere is something wrong with adapter code that needs to be fixed')
		
def getAnno():
	ans = raw_input('\nDo you want to get fpkm values, tpm values, or both?:\n\t')
	while ans not in ('tpm','fpkm','both','TPM','FPKM','Both','BOTH'):
		print >>sys.stderr,'\nThat was not a valid response. Please try again.'
		ans = raw_input('\nDo you want to get fpkm values, tpm values, or both?:\n\t')
	return ans
	
def combineFPKMs(sl,out,genome):
	print >>sys.stderr,'\nCombining the fpkm files now.'
	combine = sl + '/combineFiles/combine.sbatch'
	with open(combine, 'w+') as f:
		f.write('#!/bin/bash\n#\n#SBATCH -J combine\n#SBATCH -N 1\n#SBATCH --cpus-per-task=16\n#SBATCH --mem=230g\n#SBATCH -t 3-00:00\n')
		f.write('\ncd '+sl+'/combineFiles\n')
		f.write('\ncp gene_tracking_cp.sh '+ out + '/annotation\n')
		f.write('mkdir ' + out + '/annotation/iso\n')
		f.write('cp fpkm_extract3.sh ' + out +'/annotation/iso/fpkm_extract3.sh\n')
		f.write('cd ' + out + '/annotation\n')
		f.write('\nsh gene_tracking_cp.sh\n')
		f.write('cd iso\n')
		f.write('sh fpkm_extract3.sh\n')
		f.write("\njoin -a 1 -t $'\t' <(tail -n +2 allresults.txt | sort -k1b,1) <(sort -k1b,1 "+sl+"/ref/"+genome+"/"+genome+"_refGene.txt) > allresults.annot.txt\n")
		f.write('\nhead -1 allresults.txt > geneFPKMs.xls')
		f.write('\ncat allresults.annot.txt >> geneFPKMs.xls')
	subprocess.call('sbatch ' + sl + '/combineFiles/combine.sbatch', shell=True)
	
def getTPMs(sl,out):
	print >>sys.stderr,'\nMaking TPM combined file.'
	tpm = sl +'/combineFiles/tpm.sbatch'
	with open(tpm, 'w+') as f:
		f.write('#!/bin/bash\n#\n#SBATCH -J tpm\n#SBATCH -N 1\n#SBATCH --cpus-per-task=8\n#SBATCH --mem=175g\n#SBATCH -t 0-05:00\n')
		f.write('\nmodule load R\n')
		f.write('\ncp ' + sl + '/combineFiles/getTPM.R ' + out + '/alignment/rawcounts/getTPM.R\n')
		f.write('\ncd ' + out + '/alignment/rawcounts\n')
		f.write('\nRscript getTPM.R')
	subprocess.call('sbatch ' + sl + '/combineFiles/tpm.sbatch', shell=True)
		
def runPipeline(sl,type,file1,file2,out,threads,name,genome,adapter):
	if file2 == None:
		sbatch = sl + '/sbatchFiles/' + name + '_RNAseq.sbatch'
		with open(sbatch, 'w') as f:
			f.write('#!/bin/bash\n#\n#SBATCH -J RNAseq\n#SBATCH -N 1\n#SBATCH --cpus-per-task=8\n#SBATCH --mem=150g\n#SBATCH -t 3-00:00\n')
			f.write('\nmodule load compiler/python/2.7.10-Anaconda-2.3.0')
			f.write('\nmodule load FastQC')
			f.write('\nmodule load cufflinks/2.2.1')
			f.write('\nmodule load cutadapt')
			f.write('\nmodule load HISAT2/2.0.5-64-ngs.1.3.0')
			f.write('\nmodule load bowtie2/2.2.6-gcc5.2.0')
			f.write('\nmodule load samtools/1.3.1-gcc5.2.0')
			f.write('\nmodule load bedtools/2.25.0-gcc5.2.0')
			f.write('\nmodule load ucsc/kentUtils/v331')
			f.write('\nmodule load subread')
			f.write('\nmodule load MACS')
			f.write('\nmodule load picard-tools/1.140\n')
			f.write('\ncd ' + sl+ '/\n')
			f.write('\npython sequencingPipeline.py -1 '+file1+' -o '+out+' -p '+str(threads)+' -g '+genome+' -n '+name+' -a '+adapter +' '+ type)
	else:
		sbatch = sl + '/sbatchFiles/' + name + '_RNAseq.sbatch'
		with open(sbatch, 'w') as f:
			f.write('#!/bin/bash\n#\n#SBATCH -J RNAseq\n#SBATCH -N 1\n#SBATCH --cpus-per-task=8\n#SBATCH --mem=150g\n#SBATCH -t 3-00:00\n')
			f.write('\nmodule load compiler/python/2.7.10-Anaconda-2.3.0')
			f.write('\nmodule load FastQC')
			f.write('\nmodule load cufflinks/2.2.1')
			f.write('\nmodule load cutadapt')
			f.write('\nmodule load HISAT2/2.0.5-64-ngs.1.3.0')
			f.write('\nmodule load bowtie2/2.2.6-gcc5.2.0')
			f.write('\nmodule load samtools/1.3.1-gcc5.2.0')
			f.write('\nmodule load bedtools/2.25.0-gcc5.2.0')
			f.write('\nmodule load ucsc/kentUtils/v331')
			f.write('\nmodule load subread')
			f.write('\nmodule load MACS')
			f.write('\nmodule load picard-tools/1.140\n')
			f.write('\ncd ' + sl+ '/\n')
			f.write('\npython sequencingPipeline.py -1 '+file1+' -2 '+file2+' -o '+out+' -p '+str(threads)+' -g '+genome+' -n '+name+' -a '+adapter+' '+ type)	
			
	print >>sys.stderr, '\nRunning the pipeline\n'
	subprocess.call('sbatch ' + sl + '/sbatchFiles/' +name + '_RNAseq.sbatch', shell=True)

def getCSV():
	#csv file should have three columns. One for treatment files,one for control and one for what the samples new name should be
	csv = raw_input('\nWhat is the name of the csv file containing the treatment/ control pairs?:\n\t')
	while os.path.isfile(csv)==False:
		print >>sys.stderr, 'That was not a valid file. Please try again'
		csv = raw_input('\nWhat is the name of the csv file containing the treatment/ control pairs?:\n\t')
	return csv
		
def main():
	sl = os.getcwd()
	print >>sys.stderr, '\nthe current working directory is: ' + sl
 	type = getType()
	dir = getFilePath()
	os.chdir(dir)
	
	out = getOutputFilePath()
	threads = getNumThreads()
	genome = getGenome(sl)
	adapter = getAdapter()
	if type in ('rna','RNA'):
		annotate = getAnno()
	else:
		annotate = None
	files = os.listdir(dir)#gets list of files in folder
	if type in ('chip','ChIP'):
		csv_file = getCSV()
	else:
		pass
	print >>sys.stderr, files
	files.sort()#sort the list of files in the folder
	print >>sys.stderr, files
	
	#make lists of R1 and R2(if paired end)
	fileList1 = []
	fileList2 = []
	sampleList = []
	for x in files:
		if(('.fastq' in x) or ('.fq' in x)) and ('trim' not in x): 
			if ('_R1' in x) and ('trim' not in x): 
				fileList1.append(x)
				print >>sys.stderr, 'fileList1 appended with: '+x
			elif ('_R2' in x) and ('trim' not in x):
				fileList2.append(x)
				print >>sys.stderr, 'fileList2 appended with: '+x
			elif (('.fastq' in x) or ('.fq' in x)) and ('trim' not in x): 	
				fileList1.append(x)
				print >>sys.stderr, 'fileList1 appended with: '+x
			else: 
				sys.exit('\nThe fastq files were not put into the list to be used')
		else:
				pass
			
	##write sbatch for running pipeline
	for y in range(len(fileList1)):
		file1 = os.path.join(dir,fileList1[y])
		if fileList2 == []:
			file2 = None
		else: 
			file2 = os.path.join(dir,fileList2[y])
		name = getSample(file1)
		runPipeline(sl,type,file1,file2,out,threads,name,genome,adapter)
		sampleList.append(name)
	print >>sys.stderr, '\nthis is the sample list: '
	for i in range(len(sampleList)):
		print >>sys.stderr,'\t'+sampleList[i]
	print >>sys.stderr, '\nChecking if all *.bw files are complete'
	for x in sampleList: 
		if os.path.isfile(out+'/alignment/'+x+'/'+x+'.bw')==False:
			wait = True
			while wait == True: 
				time.sleep(120)
				if os.path.isfile(out+'/alignment/'+x+'/'+x+'.bw')==True:
					wait = False
				else:
					time.sleep(120)
		else:
			pass
	
	if type in ('chip','ChIP'):
		pairs=[]
		with open(csv_file,'r') as csvfile:
			reader=csv.reader(csvfile)
			for row in reader:
				pairs.append(row)
		macs2=sl+'/macs2_sbatch.sbatch'
		with open(macs2, 'w') as f:
			f.write('#!/bin/bash\n#\n#SBATCH -J Macs2\n#SBATCH -N 1\n#SBATCH --cpus-per-task=8\n#SBATCH --mem=150g\n#SBATCH -t 3-00:00\n')
			f.write('\nmodule load MACS\n\n')
			if 'mm' in genome:
				g = 'mm'
			elif 'hg' in genome:
				g = 'hs'
			else:
				#cant think of a better way to skip this stuff
				sys.exit('The genome cannot be used with default macs peak calling. Exiting!')
			for x in pairs:
				if x[0] in sampleList:
					f.write('\nmacs2 callpeak -t '+out+'/alignment/'+x[0]+'/'+x[0]+'_no_duplicates.bam -c '+out+'/alignment/'+x[1]+'/'+x[1]+'_no_duplicates.bam --call-summits --verbose 3 -g '+g+' -f BAM -n '+x[2]+' -B -p 1e-5 --outdir '+out+'/peakcalling')

	elif type in ('rna','RNA'):	
		if annotate in ('both','Both','BOTH'):
			#print >>sys.stderr, '\nboth tpm and fpkm'
			combineFPKMs(sl,out,genome)
			getTPMs(sl,out)
		elif annotate in ('tpm','TPM'):
			#print >>sys.stderr, '\njust tpm'
			getTPMs(sl,out)
		elif annotate in ('fpkm','FPKM'):
			#print >>sys.stderr, '\njust fpkm'
			combineFPKMs(sl,out,genome)
		else:
			print >>sys.stderr, '\nNone of the annotation combining processes will be run.'
		
 		for sample in sampleList:
 			os.chdir(out + '/annotation/'+ sample)
 			#print >>sys.stderr, 'rename genes.fpkm_tracking'
 			os.rename('genes.fpkm_tracking', sample + '_genes.fpkm_tracking')
 			#print >>sys.stderr, 'rename genes.fpkm_tracking' 
 			os.rename('isoforms.fpkm_tracking', sample + '_isoforms.fpkm_tracking') 
	else:
		pass

if __name__ == "__main__": main()