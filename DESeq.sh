#!/usr/bin/env Rscript 

#source("http://bioconductor.org/biocLite.R")
#biocLite(c("DESeq2","ggplot2","gplots")) 
library(DESeq2)
library(ggplot2)
library(gplots)

## Download necessary modules 
samples=read.table("$1",sep="\t",header=FALSE)
countdata <- read.table("$2",sep="\t",header=TRUE)
rownames(countdata)=countdata[,1]
counts=countdata[,-1]

#counts=countdata$counts
#colnames(counts) <- gsub("\\.[sb]am$", "", colnames(counts))
condition <- factor(c(rep("C", length(samples[samples$V2 == "Control",])), rep("T", length(samples[samples$V2 =="Case",]))))
coldata <- data.frame(row.names=colnames(counts), condition)
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)
rld <- rlogTransformation(dds)
dds=DESeq(dds)
res <- results(dds)
res <- res[order(res$padj), ]
resdata <- merge(as.data.frame(res), as.data.frame(counts(dds, normalized=TRUE)), by="row.names", sort=FALSE)
write.table(resdata,"DGEtable.txt",sep="\t",row.names = T,col.names = T)

##plot PCA
#options(device=png)
#plotPCA(rld, intgroup="condition")
data <- plotPCA(rld, intgroup="condition", returnData=TRUE) 
percentVar <- round(100 * attr(data, "percentVar"))

bitmap(file ="PCA.jpg",type="jpeg")
ggplot(data, aes(PC1, PC2, color=condition)) + geom_point(size=3) + xlab(paste0("PC1: ",percentVar[1],"% variance")) + ylab(paste0("PC2: ",percentVar[2],"% variance")) + coord_fixed()
dev.off()


