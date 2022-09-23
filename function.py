import os, subprocess, gzip
import pandas as pd
#from FILE NAME import FUNCTION NAME #this is for other functions


# other functions (how to import them to be recognized inside classes?)
# how to set them as globals ?
# Wrapper function to execute subprocesses
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

def zipped_file(filepath):
  """Determines if file is compressed gzip. Returns bool value.
  """
  with open(filepath, 'rb') as test_f:
    return test_f.read(2) == b'\x1f\x8b'

def file_to_df(filepath):
  """Converts tab delimited file to DataFrame. Returns pandas.DataFrame.
  """
  if zipped_file(filepath) == False:
    with open(filepath) as f:
      counts=0
      for line in f:
        if line.startswith('##'):
          counts += 1
    header=counts
    # import data as dataframe
    df=pd.read_csv(filepath,skiprows=header,header=None,sep="\t")
  else:
    with gzip.open(filepath,"rb") as f:
      counts=0
      for line in f:
        if line.startswith(b'##'):
          counts += 1
    df=pd.read_csv(filepath,skiprows=counts,header=None,sep="\t",compression='gzip')
  return df


class Annot:
  def __init__(self,path):
    self.path=path
    self.name=os.path.basename(os.path.normpath(self.path)).rsplit(".")[0]
    self.df=file_to_df(self.path)
    if len(self.df.columns) == 9:
      file_type="gtf"
      cols=9
    else:
      file_type="bed"
      cols=len(self.df.columns)
    #define some self attributes of the file
    self.file_type=file_type
    self.cols=cols
    
  def check_type(self):
    """check file type
    """
    return self.df, self.file_type, self.cols
    
    
  def intersect(self,chrom_segment):
    """This function performs bedtools intersect on the annotation GTF format with the ChromHMM segment.bed output of the model.
    """
    #define segment model
    segment=chrom_segment
    #define annot model
    annot=self.path
    #define the intersect file (create dir for each different annot object)
    cwd = os.getcwd()
    os.makedirs(cwd+"/"+self.name, exist_ok=True)
    is_file = cwd+"/"+self.name+"/intersect.bed"
    cmd=f'bedtools intersect -a {annot} -b {segment} > {is_file}'
    bash_command(cmd)
    self.intersectdf=file_to_df(is_file)
    return self.intersectdf
    
  def check_intersect(self):
    return self.intersectdf



  #a=Annot("./prova.gtf.gz")
# filename.gtf=Annot(".")




    



# subprocess.Popen() class for creation and managment of executed process
# executes only a single command with arguments as a list
# NO pipe commands

