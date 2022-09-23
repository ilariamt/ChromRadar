import os
import pandas as pd
from FILE NAME import FUNCTION NAME #this is for other functions


# other functions (how to import them to be recognized inside classes?)
# how to set them as globals ?
# Wrapper function to execute subprocesses
import subprocess
def bash_command(cmd):
    p = subprocess.Popen(
        ['/bin/bash', '-o', 'pipefail'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        text=True
    )
    # pid = p.pid
    # pgid = os.getpgid(pid)
    stdout, stdin = p.communicate(cmd)
    return stdout.strip('\n')



class Annot:
  def __init__(self,path):
    self.path=path
    with open(self.path) as f:
      counts=0
      for line in f:
          if line.startswith('##'):
              counts += 1
    header=counts
    # import data as dataframe
    df=pd.read_csv(self.path,skiprows=header,header=None,sep="\t")
    if len(df.columns) == 9:
      file_type="gtf"
      cols=9
    else:
      file_type="bed"
      cols=len(df.columns)
    #define some self attributes of the file
    self.name=os.path.basename(os.path.normpath(path))
    self.df=df
    self.file_type=file_type
    self.cols=cols
    
  def check_type(self):
    """check file type"""
    return self.df, self.file_type, self.cols  

  def intersect(self,chrom_segment):
    """This function performs bedtools intersect on the annotation GTF format with the 
    ChromHMM segment.bed output of the model"""
    #define segment model
    segment=chrom_segment
    #define annot model
    annot=self.path
    #define the intersect file (create dir for each different annot object)
    cwd = os.getcwd()
    intersect = cwd+"/"+self.name+"/intersect.bed"
    os.makedirs(intersect, exist_ok=True)
    cmd=f'bedtools intersect -a {annot} -b {segment} > {intersect}'
    bash_command(cmd)
    return False


    

class BED(Annot):
  def un
  pass
  return False




# subprocess.Popen() class for creation and managment of executed process
# executes only a single command with arguments as a list
# NO pipe commands

