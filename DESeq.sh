#!/usr/bin/env Rscript 

source("https://bioconductor.org/biocLite.R")
biocLite(c("DESeq2","RcolorBrewer","ggplot2","gplots","Annotate")) 
library(DESeq2)
library(annotate)
library(RColorBrewer)
library(ggplot2)
library(gplots)

## Download necessary modules 

countdata <- readRDS("counts_0530.rds")
counts=countdata$counts
colnames(counts) <- gsub("\\.[sb]am$", "", colnames(counts))
condition <- factor(c(rep("C", 12), rep("T", 12)))
coldata <- data.frame(row.names=colnames(counts), condition)
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)
rld <- rlogTransformation(dds)
dds=DESeq(dds)
res <- results(dds)
res <- res[order(res$padj), ]
resdata <- merge(as.data.frame(res), as.data.frame(counts(dds, normalized=TRUE)), by="row.names", sort=FALSE)
write.table(resdata,"DGEtable.txt",sep="\t",row.names = T,col.names = T)

##plot PCA
plotPCA(rld, intgroup="condition")
data <- plotPCA(rld, intgroup="condition", returnData=TRUE) 
percentVar <- round(100 * attr(data, "percentVar"))
ggplot(data, aes(PC1, PC2, color=condition)) + geom_point(size=3) + xlab(paste0("PC1: ",percentVar[1],"% variance")) + ylab(paste0("PC2: ",percentVar[2],"% variance")) + coord_fixed()

#plot Heatmap
heatmap.2(assay(rld),dendrogram="none",col=colorRampPalette(brewer.pal(name="RdBu",n=11))(200),Colv=FALSE,Rowv=FALSE,labRow=fdr20$`Gene symbol`,
          labCol=rownames(df),main=i$name,ylab=paste("Significant Genes by log2FC",",",i$pValue,"FDR"),trace="none",key=TRUE,keysize=1.0,density.info="none",scale="row",margins=c(6,7))


