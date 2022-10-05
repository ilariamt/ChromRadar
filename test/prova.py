import os
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd
import seaborn as sns
import subprocess

#installed: pip, matplotlib, pandas, seaborn, (conda install...)
# conda install -c bioconda bedtools

def bash_command(cmd):
    p = subprocess.Popen(
        ['/bin/bash', '-o', 'pipefail'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        text=True
    )
    pid = p.pid
    pgid = os.getpgid(pid)
    stdout, stdin = p.communicate(cmd)
    return stdout.strip('\n')
os.makedirs("./", exist_ok=True)
intersect = "." + '/' + 'prova_intersect.bed'
intersect ='prova_intersect.bed'
gtf="prova.gtf"
bed="prova.bed"
name="prova"
cmd=f'bedtools intersect -a {gtf} -b {bed} > {intersect}'
bash_command(cmd)

with open("./prova1.gtf") as f:
	counts=0
	for line in f:
		if line.startswith('##'):
			counts += 1


class BED(Annot):
  def un
  pass
  return False


def dataframe(filename):
    """Open an optionally gzipped GTF file and return a pandas.DataFrame.
    """
    # Each column is a list stored as a value in this dict.
    result = defaultdict(list)

    for i, line in enumerate(lines(filename)):
        for key in line.keys():
            # This key has not been seen yet, so set it to None for all
            # previous lines.
            if key not in result:
                result[key] = [None] * i

        # Ensure this row has some value for each column.
        for key in result.keys():
            result[key].append(line.get(key, None))

    return pd.DataFrame(result)



# subprocess.Popen() class for creation and managment of executed process
# executes only a single command with arguments as a list
# NO pipe commands

# adding method to check if it's a tab delimitet file and else error!




# final code:
path="path"
a=Annot(path)
a=Annot("./prova.gtf.gz")
df,type_f,cols, zipped = a.check_type()
if type_f=="bed":
    a=Bed()    # change class: has a special intersect method
c=ChromObj("./prova_segment.bed")
# call intersect on the chrom_segment file
intersectdf = a.intersect(c.GetPath())
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




