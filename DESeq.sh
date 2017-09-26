#!/usr/bin/env Rscript 

source("https://bioconductor.org/biocLite.R")
biocLite("DESeq2") 
library(DESeq2)
library(annotate)
library(org.Mm.eg.db)
library(pheatmap)
library(RColorBrewer)
library(ggplot2)
library(gplots)

## Download necessary modules 
samples=read.table("./sample_phenotype.txt",sep="\t",header=FALSE)
countdata <- read.table("./htseq_count.txt",sep="\t",header=TRUE)
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

#plotPCA(rld, intgroup="condition")
data <- plotPCA(rld, intgroup="condition", returnData=TRUE) 
percentVar <- round(100 * attr(data, "percentVar"))
png(filename ="PCA.png",width = 700, height=800)
ggplot(data, aes(PC1, PC2, color=condition)) + geom_point(size=3) + xlab(paste0("PC1: ",percentVar[1],"% variance")) + ylab(paste0("PC2: ",percentVar[2],"% variance")) + coord_fixed()
dev.off()


