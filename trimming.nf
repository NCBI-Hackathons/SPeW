/* Testing for NCBI SpEW project, trimming module
* Zhou (Ark) Fang zhf9@pitt.edu
*/
inPath = "./RNAseq_files"
singleEnd = true
adapter1 = "ADATPER_FWD"
adapter2 = "ADATPER_REV"

process trimming{
script:
    if (singleEnd==true)
    """
    bash ~/SPEW/trimming.sh -i inPath -s -a1 adapter1 -a2 adapter2
    """
    else
    """ 
    bash ~/SPEW/trimming.sh -i inPath -a1 adapter1 -a2 adapter2
    """
}