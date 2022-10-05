#!/usr/bin/env python
import os, subprocess, gzip
import pandas as pd
import numpy as np
from function import bash_command, zipped_file, file_to_df
from classes import Annot, Bed, ChromObj


a=Annot("./prova.gtf.gz")
df,type_f,cols, zipped = a.check_type()
if type_f=="bed":
	a=Bed()    # change class: has a special intersect method
c = ChromObj("./prova_segment.bed")
# call intersect on the chrom_segment file
intersectdf = a.intersect(c.GetPath())
print(a.ByStateCov())
	#t=a.extract()
	# intersect gets a 14 field gtf:
	# (1-8) chr1	HAVANA	gene	91949343	92014426	.	+	.
	# (9) gene_id "ENSG00000137948.19"; gene_type "protein_coding"; gene_name "BRDT"
	# (10-14) chr1	91951200	91951400	E17	200

	# intersect with a bed file (genome col=6)
	# (1-6) chr1	0	248956422	.	248956422	.
	# (7-11) chr1	0	10200	E18	10200

	# intersect with a peak bed file (genome col=10)
	# needs to first be intersected
	# (1-10) chr1	955000	1014999	0.0	140.53137740928133	.	11587	7230	0.0	1.4053137740928132
	# (11-15) chr1	955200	955600	E5	400