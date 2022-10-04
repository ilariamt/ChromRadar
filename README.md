# ChromRadar    
*Python function for quantifying state fold enrichment on user specified genomic annotation and visualizing the results*    
    
[chromHMM](http://compbio.mit.edu/ChromHMM/) is a chromatin segmentation tool used for charcterizing and annotating chromatin states on the genome, based on ChIP-seq signal. Once a model is learned, each genomic bin is assigned to a specific state. All the coordinates and the assignments are written inside the `segments.bed` output file.   
The `LearnModel` function automatically returns an `overlap.txt`, a matrix representing the enrichment of each annotation within a state, normalized by the annotation's genomic coverage. As the [Manual](http://compbio.mit.edu/ChromHMM/ChromHMM_manual.pdf) cites:   

$$ enrichment = { \frac{bp\ annotation ∩ state}{bp\ state} ÷ \frac{bp\ genome ∩ annotation}{bp\ genome} } $$   

This normalization stategy can be useful for state identification and comparison. However, for my workflow, I wanted to quantitatively compare state-enrichment profiles of different annotations, especially not well characterized ones. My aim was to observe specific enrichments of an epigenetic profile on my regions of interest.   
     
Here I developed `ChromRadar`, a function for annotation-centric normalization and enrichment track visualization through radarplots.   
   
**Basic workflow:**   
1. The full paths to annotation files are specified as a list within the `config` file, both *.gtf* and *.bed* formats are accepted
2. The full path to the `segments.bed` file is specified inside the `config` file.
3. *ChromRadar* computes the fraction of the states overlapping each annotation. These values are divided by the fraction of the states covering the genome. The resulting value is thus a fold change state enrichment on a given annotation with respect to the state enrichment on the genome.
4. These values are visualized on a radarplot, to underline the combinatorial nature of state enrichments on different classes of genomic elements.

... :warning: CODING WORK IS STILL IN PROGRESS :warning: ...