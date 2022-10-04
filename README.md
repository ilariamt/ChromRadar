# ChromRadar    
*Python function for quantifying state fold enrichment on user specified genomic annotation and visualizing the results*    
    
[chromHMM](http://compbio.mit.edu/ChromHMM/) is a chromatin segmentation tool used for charcterizing and annotating chromatin states on the genome, based on ChIP-seq signal. Once a model is learned, each genomic bin is assigned to a specific state. All the coordinates and the assignments are written inside the `segments.bed` output file.   
The `LearnModel` function automatically returns an `overlap.txt`, a matrix representing the enrichment of each annotation within a state, normalized by the annotation's genomic coverage. As the [Manual](http://compbio.mit.edu/ChromHMM/ChromHMM_manual.pdf) cites:   

$$ enrichment = { \frac{bp\ annotation ∩ state}{bp\ state} ÷ \frac{bp\ genome ∩ annotation}{bp\ genome} } $$   

This normalization stategy can be useful for state identification and comparison. However, for my workflow, I wanted to quantitatively compare state-enrichment profiles of different annotations.   
     
Here I developed `ChromRadar`, a function for annotation-centric normalization and enrichment track visualization through radarplots.   
**Basic workflow:**   
1. The annotation files are specified as a list within the `.config
