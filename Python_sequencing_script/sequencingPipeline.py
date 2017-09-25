'''
information about program
	
	
	usage:
		python RNAseq_Pipeline.py -[options] [type] 
'''
#!/usr/bin/env python

import os, sys, time, subprocess, getopt

#what the arguments mean
def usage():
	print >>sys.stderr,"\nusage: python sequencingPipeline.py [options] [type]"
	print >>sys.stderr,"\noptions:\n\t-1 FASTQ_FILE, --mate1 FASTQ_FILE \n\t\tFastq file (can be zipped). First mate for paired-end or file for single-end. (REQUIRED)"
	print >>sys.stderr,"\n\t-2 FASTQ_FILE, mate2 FASTQ_FILE \n\t\tFastq file (can be zipped). Second mate for paired-end."
	print >>sys.stderr,"\n\t-o DIRECTORY, --out DIRECTORY\n\t\tLocation for output files to be placed. Will put files in current directory if not specified."
	print >>sys.stderr,"\n\t-p NUMBER, --threads NUMBER \n\t\tInteger value between 1 and 16 inclusive for number of threads used during process. \n\t\tDefault:8."
	print >>sys.stderr,"\n\t-g GENOME, --genome GENOME \n\t\tGenome for sequence to be aligned to. Only mm9, mm10, hg19,and hg38 are handeled unless \n\t\tfolder made containing all necessary files is added to ref folder. (REQUIRED)"
	print >>sys.stderr,"\n\t-n NAME, --name NAME \n\t\tName of sample."
	print >>sys.stderr,"\n\t-a (FILE or n or t), --adapter (FILE or n or t) \n\t\tEither 'n' for Nextera or 't' for Truseq or a fasta file containing the adapter \n\t\tsequences to be removed during trimming. Trimming will be skipped if not supplied."
	print >>sys.stderr,"\n\t-h  \n\t\tDisplays how the program is run and what the arguments are."
	print >>sys.stderr,"\ntype: type of sequencing that was performed. \n\t-Right now ATAC,ChIP, and RNA-seq can be handled by using 'atac','chip', or 'rna' respectively "

#trim	
def trim(file1,file2,name,adapter):
	#change to directory containing fastq files
	if os.path.split(file1)[0] =='':
		os.chdir(os.getcwd())
	else:
		os.chdir(os.path.split(file1)[0])
	print >>sys.stderr, '\ncurrent working directory is: '+os.getcwd()
	#single-end
	if file2==None:
		if os.path.isfile(adapter)==True:
			print >>sys.stderr, '\nThe code used for trimming is: \n\tcutadapt -a file:'+adapter+' -m 20 -o '+name+'_trimmed.fastq.gz '+file1
			subprocess.call('cutadapt -a file:'+adapter+' -m 20 -o '+name+'_trimmed.fastq.gz '+file1, shell = True)
			trim1=os.getcwd()+'/'+name+'_trimmed.fastq.gz'
			trim2=None
		else:
			print >>sys.stderr, '\nThe code used for trimming is: \n\tcutadapt -a '+adapter+' -m 20 -o '+name+'_trimmed.fastq.gz '+file1
			subprocess.call('cutadapt -a '+adapter+' -m 20 -o '+name+'_trimmed.fastq.gz '+file1, shell = True)
			trim1=os.getcwd()+'/'+name+'_trimmed.fastq.gz'
			trim2=None
	#paired-end
	else:
		if os.path.isfile(adapter)==True:
			print >>sys.stderr, '\nThe code used for trimming is: \n\tcutadapt -a file:'+adapter+' -A file:'+adapter+' -m 20 -o '+name+'_trimmed_R1.fastq.gz -p '+name+'_trimmed_R2.fastq.gz '+file1+' '+ file2
			subprocess.call('cutadapt -a file:'+adapter+' -A file:'+adapter+' -m 20 -o '+name+'_trimmed_R1.fastq.gz -p '+name+'_trimmed_R2.fastq.gz '+file1+' '+ file2, shell = True)
			trim1=os.getcwd()+'/'+name+'_trimmed_R1.fastq.gz'
			trim2=os.getcwd()+'/'+name+'_trimmed_R2.fastq.gz'
		else:
			print >>sys.stderr, '\nThe code used for trimming is: \n\tcutadapt -a '+adapter+' -A '+adapter+' -m 20 -o '+name+'_trimmed_R1.fastq.gz -p '+name+'_trimmed_R2.fastq.gz '+file1+' '+ file2
			subprocess.call('cutadapt -a '+adapter+' -A '+adapter+' -m 20 -o '+name+'_trimmed_R1.fastq.gz -p '+name+'_trimmed_R2.fastq.gz '+file1+' '+ file2, shell = True)
			trim1=os.getcwd()+'/'+name+'_trimmed_R1.fastq.gz'
			trim2=os.getcwd()+'/'+name+'_trimmed_R2.fastq.gz'
	#return values
	return trim1, trim2

#align wth bowtie2 (for atac and chip)
def bowtie2(file1,file2,threads,out,align,name,ref):
	if file2 == None: #single-end
		print >>sys.stderr, '\nThe code for aligning is: \n\tbowtie2 -x '+ref+' -X 650 -I 20 -t --very-sensitive  -p '+str(threads)+' -U '+ file1+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt'
		command = ('bowtie2 -x '+ref+' -X 650 -I 20 -t --very-sensitive  -p '+str(threads)+' -U '+file1+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt')
		subprocess.call(command, shell = True)
		
	else: #paired-end
		print >>sys.stderr, '\nThe code for aligning is: \n\tbowtie2 -x '+ref+' -p '+str(threads)+' -X 650 -I 20 -t --very-sensitive -1 '+ file1+' -2 '+ file2+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt'
		command = ('bowtie2 -x '+ref+' -p '+str(threads)+' -X 650 -I 20 -t --very-sensitive -1 '+file1+' -2 '+file2+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt')
		subprocess.call(command, shell = True)
		
	os.chdir(out)
	#change sort file and do sam to bam to save space
	samtobam = 'samtools view -b '+name+'.sam | samtools sort -T temp_'+name+' -O bam -o '+ name +'_aligned.bam -'
	print >>sys.stderr, '\nsamtobam: \n\t'+samtobam
	subprocess.call(samtobam, shell = True)
	#remove sam file to save space
	os.remove(name+'.sam')
	print >>sys.stderr, '\nThe sam file was removed'
	print >>sys.stderr,'\n Alignment is complete \n\n'

#align with hisat2 (for rna)		
def hisat2(file1,file2,threads,out,align,name,ref):
	if file2 == None: #not paired-end
		print >>sys.stderr, '\nThe code for aligning is: \n\thisat2 -fr -t -q -x '+ref+' -p '+threads+' -U '+ file1+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt'
		command = ('hisat2 -fr -t -q -x '+ref+' -p '+threads+' -U '+file1+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt')
		subprocess.call(command, shell = True)
		
	else: #paired-end
		print >>sys.stderr, '\nThe code for aligning is: \n\thisat2 -fr -t -q -x '+ref+' -p '+str(threads)+' -1 '+ file1+' -2 '+ file2+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt'
		command = ('hisat2 -fr -t -q -x '+ref+' -p '+str(threads)+' -1 '+file1+' -2 '+file2+ ' -S '+out+'/'+name+'.sam 2> '+align+'/'+name+'_stats.txt')
		subprocess.call(command, shell = True)
		
	os.chdir(out)
	#change sort file and do sam to bam to save space
	samtobam = 'samtools view -b '+name+'.sam | samtools sort -T temp_'+name+' -O bam -o '+ name +'_aligned.bam -'
	print >>sys.stderr, '\nsamtobam: \n\t'+samtobam
	subprocess.call(samtobam, shell = True)
	#remove sam file to save space
	os.remove(name+'.sam')
	print >>sys.stderr, '\nThe sam file was removed'
	print >>sys.stderr,'\nAlignment is complete \n\n'
	
		
#main function 
def main():
	sl=os.getcwd()#location of script so dependent files can be accessed such as reference files ##better way of doing this?
	print >>sys.stderr,'\nscript location: \n\t'+os.getcwd()
		
	type=None
	filename1=None
	filename2=None
	trim1=None
	trim2=None
	outputFolder=None
	threads=8
	genome=None
	sampleName=None
	adapter=None
	
	shortOpts='1:2:o:p:g:n:a:h'
	longOpts=['help','mate1=','mate2=','out=','threads=','genome=','name=','adapter=']
	try:
		opts,args = getopt.getopt(sys.argv[1:],shortOpts,longOpts)
		for i in range(len(opts)):
			print>>sys.stderr, opts[i]
		print >>sys.stderr, args
	except getopt.GetoptError, e:
		print >>sys.stderr, e
		print >>sys.stderr, args
		usage()
		sys.exit()
	
	if len(args) != 1:
		print >>sys.stderr, '\nError: command arguments are not supported'
		usage( )
		sys.exit( )
		
	for opt, value in opts:
		if opt in ('-h','--help'):
			usage()
			sys.exit()
			
		if opt in ('-1', '--mate1'):
			if(os.path.isfile(value) == True):
				filename1=value
			else:
				usage()
				sys.exit('\nERROR: Input file (-1,--mate1) does not exist. Exiting!')
				
		if opt in ('-2', '--mate2'):
			if(os.path.isfile(value) == True):
				filename2=value
			else:
				usage()
				sys.exit('\nERROR: Input file (-2, --mate2) does not exist. Exiting!')
			
		if opt in ('-o', '--out'):
		#see if folder exists and if it doesn't create it (if path not given make folder in current directory)
			if(os.path.exists(value) == True):
				outputFolder=value
			elif(os.path.exists(value) == False and os.path.split(value)[0] != ''):
					os.mkdir(value)
					outputFolder=value
			else:
				file = sl+'/'+value
				if os.path.exists(file) == True:
					outputFolder=file
				else:
					os.mkdir(file)
					outputFolder=file			
		
		if opt in ('-p', '--threads'):
			try:
				if(int(value), int == True and int(value) >= 1 and int(value) < 17):
					threads=value
				else:
					print >>sys.stderr, '\nNumber of threads is not valid. Default of 8 will be used.'
			except(ValueError):
				print >>sys.stderr, '\nValue provided for theads is not an integer. Default of 8 will be used.'
			
		if opt in ('-g', '--genome'):
			genome=value
		
		if opt in ('-n', '--name'):
			sampleName=value
			
		if opt in ('-a','--adapter'):
			if 'n' in value:
				print >>sys.stderr, '\nUsing Nextera adapters for trimming'
				adapter = sl+'/adapters/Nextera.fa'
			elif 't' in value:
				print >>sys.stderr, '\nUsing Truseq3 adapters for trimming'
				adapter = 'AGATCGGAAGAGC'
			elif os.path.isfile(value):
				print >>sys.stderr, '\nUser provided adapters will be used for trimming'
				adapter = value
			else:
				print >>sys.stderr, '\nAdapters: not a file or incorrect value provided. Trimming will be skipped.'
	
	#if the first input file does not exist exit 
	if filename1==None:
		usage()
		sys.exit('\nERROR: Input file (-1,--mate1) does not exist. Exiting!')
		
	if genome in ('mm9','mm10','hg19','hg38'):#CHECK TO MAKE SURE THAT IS CORRECT FILE STRUCTURE
		gtf = sl+'/ref/'+genome+'/'+genome+'.gtf'
		fa = sl+'/ref/'+genome+'/'+genome
		size = sl+'/ref/'+genome+'/'+genome+'.chrom.sizes'
	else:
		usage()
		sys.exit('\nERROR: The genome provided is not accepted. Only genomes located in the ref folder are accepted.')
	
	#get sampleName if not provided
	if sampleName==None:
		print >>sys.stderr,'\nSample name not provided. Extracting from filename.'
		if 'gz' in filename1:
			fn = os.path.splitext(os.path.basename(filename1))[0]
			fn = os.path.splitext(fn)[0]
		elif 'gz' not in filename1:
			fn = os.path.splitext(os.path.basename(filename1))[0]
		else:
			sys.exit('\nERROR: Unknown if file is zipped or not. Cannot get sample name. Exiting!')
		#remove '_R1' and '_R2'
		if('_R1' in fn) or ('_R2' in fn):
			param, value = fn.split('_R1',1)
			sampleName = param
		else:
			sampleName=fn
				
	#make outputfolder the current working directory if not provided
	if outputFolder==None:
		print >>sys.stderr,'\nOutput folder not provided. Putting all output files in current directory.'
		outputFolder=os.getcwd()
	
	#determine if type of sequencing is accepted and run pipeline if it is
	if args[0] in ('atac','ATAC','chip', 'ChIP','rna', 'RNA'):
		#makes alignment folder
		if(os.path.exists(outputFolder+'/alignment') == False): 
			os.mkdir(outputFolder+'/alignment')
		#makes sample folder in alignment folder 
		if(os.path.exists(outputFolder+'/alignment/'+sampleName) == False):
			os.mkdir(outputFolder+'/alignment/'+sampleName)
		#assign outputlocation for alignment files
		outputLoc = outputFolder+'/alignment/'+sampleName
		#makes alignment stat folder
		if(os.path.exists(outputFolder+'/alignment/alignStats') == False):
			os.mkdir(outputFolder+'/alignment/alignStats')
		alignStats = outputFolder+'/alignment/alignStats'
		
		#trim fastq files and run alignment based on args value
		if adapter!=None:
			trim1,trim2=trim(filename1,filename2,sampleName,adapter)
			if trim2==None:
				subprocess.call('fastqc ' + trim1+' -f fastq -o ' + outputLoc, shell = True)
			else:
				subprocess.call('fastqc ' + trim1+' -f fastq -o ' + outputLoc, shell = True)
				subprocess.call('fastqc ' + trim2+' -f fastq -o ' + outputLoc, shell = True)
		else:
			print >>sys.stderr,'\nNo adapters provided. Skipping trim'
			if filename2==None:
				subprocess.call('fastqc ' + filename1+' -f fastq -o ' + outputLoc, shell = True)
			else:
				subprocess.call('fastqc ' + filename1+' -f fastq -o ' + outputLoc, shell = True)
				subprocess.call('fastqc ' + filename2+' -f fastq -o ' + outputLoc, shell = True)
				
		#Run alignment code
		print >>sys.stderr,'\nRunning Alignment for '+sampleName+'\n'	
		#determine type of sequencing performed 
		if args[0] in ('atac','ATAC','chip', 'ChIP'):
			#see if trim worked before running alignment
			if os.path.isfile(trim1)==False:	
				trim1 = None
			else:
				pass
			#run Bowtie2	
			if trim1==None:#if trimming does not work use original fastq files
				bowtie2(filename1,filename2,threads,outputLoc,alignStats,sampleName,fa)
			else:
				bowtie2(trim1,trim2,threads,outputLoc,alignStats,sampleName,fa)
			
			os.chdir(outputLoc)
			#create bw files bam->bg->bw
			print >>sys.stderr, 'make bigwig file of original files'
			bg = 'samtools view -b '+sampleName+'_aligned.bam | genomeCoverageBed -split -bg -ibam stdin -g '+size+' | sort -k1,1 -k2,2n > '+sampleName+'_original.bg'
			bw = 'bedGraphToBigWig '+sampleName+'_original.bg '+size+' '+sampleName+'_original.bw'
			subprocess.call(bg, shell = True)
			subprocess.call(bw, shell = True)
					
			rmvdup = 'java -jar /ihome/sam/apps/picard-tools/picard-tools-1.140/picard.jar MarkDuplicates I='+sampleName+'_aligned.bam O='+sampleName+'_no_duplicates.bam M='+sampleName+'_marked_dup_metrics.txt REMOVE_DUPLICATES=true'
			print >>sys.stderr, 'remove duplicates with: \n\t'+rmvdup
			subprocess.call(rmvdup,shell=True)
			#extend/shift??
			
			index = 'samtools index -b '+outputLoc+'/'+sampleName+'_no_duplicates.bam'
			subprocess.call(index, shell = True)
			
			#create bw files bam->bg->bw
			print >>sys.stderr, 'make bigwig file with duplicates removed'
			bg = 'samtools view -b '+sampleName+'_no_duplicates.bam | genomeCoverageBed -split -bg -ibam stdin -g '+size+' | sort -k1,1 -k2,2n > '+sampleName+'_nodups.bg'
			bw = 'bedGraphToBigWig '+sampleName+'_nodups.bg '+size+' '+sampleName+'_nodups.bw'
			subprocess.call(bg, shell = True)
			subprocess.call(bw, shell = True)
			
			if args in ('atac','ATAC'):
				if 'mm' in genome:
					g = 'mm'
				elif 'hg' in genome:
					g = 'hs'
				else:
					sys.exit('The genome cannot be used with default macs peak calling. Exiting!')
			
				narrow = 'macs2 callpeak -t '+sampleName+'_no_duplicates.bam --call-summits --verbose 3 -g '+g+' -f BAM -n '+sampleName+' -B -p 1e-7 --outdir '+outputFolder+'/narrowPeaks'
				broad = 'macs2 callpeak -t '+sampleName+'_no_duplicates.bam --broad --verbose 3 -g '+g+' -f BAM -n '+sampleName+' -B -p 1e-7 --outdir '+outputFolder+'/braodPeaks'
				subprocess.call(narrow, shell = True)
				subprocess.call(broad, shell = True)
				
		else:#for rnaseq
			#see if trim worked before running alignment
			if os.path.isfile(trim1)==False:	
				trim1 = None
			else:
				pass
			#run Hisat2
			if trim1==None:#if trimming does not work use original fastq files
				hisat2(filename1,filename2,threads,outputLoc,alignStats,sampleName,fa)
			else:
				hisat2(trim1,trim2,threads,outputLoc,alignStats,sampleName,fa)
				
			#create folder for rawcounts	
			if(os.path.exists(outputFolder+'/alignment/rawcounts') == False):
				os.mkdir(outputFolder+'/alignment/rawcounts')
			else:
				pass
			#get raw counts with featureCounts
			rawcounts='featureCounts -a '+gtf+' -o '+outputFolder+'/alignment/rawcounts/'+sampleName+'_featurecounts.txt '+ outputFolder+'/'+sampleName+'/'+ sampleName +'_aligned.bam'
			print >>sys.stderr, 'getting feature counts with subread:\n\t'+rawcounts
			subprocess.call(rawcounts, shell = True)

			#run cufflinks to get fpkm values
			if(os.path.exists(outputFolder+'/annotation') == False): 
				os.mkdir(outputFolder+'/annotation')
			if(os.path.exists(outputFolder+'/annotation/'+sampleName) == False): 
				os.mkdir(outputFolder+'/annotation/'+sampleName)
			annOut = outputFolder+'/annotation/'+sampleName
			cl = ('cufflinks --library-type fr-firststrand -p '+str(threads)+' -G '+gtf+' -b '+fa+'.fa -o '+annOut+' '+outputLoc+'/'+sampleName+'_aligned.bam')
			print>>sys.stderr, 'getting fpkm values with cufflinks:\n\t'+cl
			subprocess.call(cl, shell = True)
			
			index = 'samtools index -b '+outputLoc+'/'+ sampleName +'_aligned.bam'
			subprocess.call(index, shell = True)
			
			os.chdir(outputLoc)
			#create bw files bam->bg->bw
			print >>sys.stderr, 'make bigwig file'
			bg = 'samtools view -b '+sampleName+'_aligned.bam | genomeCoverageBed -split -bg -ibam stdin -g '+size+' | sort -k1,1 -k2,2n > '+sampleName+'.bg'
			bw = 'bedGraphToBigWig '+sampleName+'.bg '+size+' '+sampleName+'.bw'
			subprocess.call(bg, shell = True)
			subprocess.call(bw, shell = True)

	#type argument not correct, exit	
	else:
		sys.exit('\nERROR: No valid sequencing type provided (ie. atac,chip, or rna). Exiting!')
		
	
if __name__ == "__main__": main()