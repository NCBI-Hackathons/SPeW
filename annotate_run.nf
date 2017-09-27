#!/usr/bin/env nextflow

process test {

output:
stdout result

script:
    """
    annotate_module_v2.bash -a Reference -b /ihome/uchandran/ras143/ncbi-workshop/RNAseq_files -p /ihome/uchandran/ras143/ncbi-workshop/RNAseq_files/sample_phenotype.txt -g /ihome/uchandran/ras143/ncbi-workshop/RNAseq_files/mm10_genes.gtf
    """  
}

result.subscribe {
    println it.trim()
}

