/* 
 * pipeline input parameters 
 */
counts=file('./bin/htseq_count.txt')
Samples=file('./bin/sample_phenotype.txt')
//params.counts = "$baseDir/htseq_counts.txt"
//params.outdir = "DGE_results"
//params.sample = "$baseDir/sample_phenotype.txt"
//println """\
//         R N A S E Q - N F   P I P E L I N E    
//         ===================================
//         Counts:            ${params.counts}
//         phenotype        : ${params.sample}
//         outdir        :    ${params.outdir}
//         """
//         .stripIndent()

/* 
 * create a transcriptome file object given then transcriptome string parameter
 */
 // counts_file = file(params.counts)
 //sample=file(params.sample)
 
/* 
 * define the `index` process that create a binary index 
 * given the transcriptome file
 */


process DGE {
    tag "DGE"

    input:
    val 'input1' from Samples
    val 'input2' from counts
   

    output:
    file("DGE_logs") into DGE_test
    
      
    script:
    """

    
    mkdir DGE_logs
    DESeq.sh $input1 $input2
    """  
}  
result.subscribe { println it }
