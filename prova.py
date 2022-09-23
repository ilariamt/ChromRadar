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


# final code:
path="path"
a=Annot(path)
df,type,cols=a.check_type()