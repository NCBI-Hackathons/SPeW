# SPeW: SeqPipeWrap 

## Introduction
Taking a sequencing pipeline from individual pieces on your workstation to a seamless pipeline that can be run by any user is currently a challenge. Here, we create a proof-of-principle simple RNA-seq pipeline using separate Bash shell scripts that are linked together using NextFlow as a pipeline management tool. This is then wrapped using Docker for distribution and seamless running on other workstations without dependency issues. 

## Methods 

![ScreenShot](SPeW_workflow.jpg)

To create the proof-of-principle simple RNA-seq pipeline, we started with writing simple Bash shell scripts for each step required in the analysis. These individual steps were then combined together by integrating them into NextFlow. In order to allow for seamless running on any workstation, Docker was then used to wrap the Nextflow code. By wrapping into a container such as Docker, all dependencies required for each step are automatically on the users workstation. Docker has the ability to be used by Sinularity, allowig the code to be utilized on a High Computing Cluster(HPC).

## Requirements 
Docker

## Futher Directions 
We hope to further add to the pipeline, and allow for the ability to enter the pipeline at any point. 
