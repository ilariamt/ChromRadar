import os, subprocess, gzip
import pandas as pd
import numpy as np
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
    
  def intersect(self,chrom_obj_path):
    """This function performs bedtools intersect on the annotation GTF format with the ChromHMM segment.bed output of the model.
    """
    #define segmentation files
    segment=chrom_obj_path
    #define annot model
    annot=self.path
    #define the intersect file (create dir for each different annot object)
    cwd = os.getcwd()
    os.makedirs(cwd+"/intersect/", exist_ok=True)
    isect_file = cwd+"/intersect/"+self.name+"_intersect.bed"
    cmd=f'bedtools intersect -a {annot} -b {segment} -wao > {isect_file}'
    bash_command(cmd)
    self.intersectdf=file_to_df(isect_file)
    return self.intersectdf



class Bed(Annot):
  pass

  def intersect(self,chrom_obj_path):
    """Intersects a bed annotation file with Chrom_segmentation file.
    """
    return
    
  # def check_intersect(self):
  #   return self.intersectdf
  # shall I correct bed files to gtf or gtf files to bed?



  #a=Annot("./prova.gtf.gz")
# filename.gtf=Annot(".")




    



# subprocess.Popen() class for creation and managment of executed process
# executes only a single command with arguments as a list
# NO pipe commands

# ------------------------------------------------------------------------------------------------------------------
class ChromObj:
  def __init__(self,path):
    self.path=path
    self.df=file_to_df(self.path)
    self.states=np.unique(self.df.iloc[:,3])
    
  def out(self):
    """Check the dataframe obtained from segment ChromHMM file.
    """
    return self.df

  def get_path(self):
    """Returns path to ChromHMM segmentation file.
    """
    return self.path

  # def StateFiles(self,dir_name):
  #   """Separates the segment ChromHMM output file into state-specific coverage bed files.
  #   """
  #   #define directory where to put the various coverage files
  #   cwd = os.getcwd()
  #   os.makedirs(cwd+"/"+dir_name, exist_ok=True)
  #   chrom_dir=cwd+"/"+dir_name
  #   for state in self.states:
  #     cmd=f'zcat {self.path} | grep -w {state} > {chrom_dir}/{state}_coverage.bed'
  #     bash_command(cmd)
  #   return chrom_dir
    


for i in $array_num; do line=$(sed -n "${i}p" $file); echo $i; \
	segment_file=$(echo $line | awk -F' ' '{ print $3}'); echo $segment_file; folder=$(echo $line | awk -F' ' '{ print $4}'); states=$(echo $line | awk -F' ' '{ print $2}'); \
	OUTDIR="/mnt/projects/labs/GEBI/_Epigen/chipSeq/Chrom_states/Chrom_Controls/KN_variants_200bp/${folder}"; mkdir -p ${OUTDIR}; \
	declare -a states; states=$(zcat $segment_file | awk '{print $4}' | sort | uniq); echo $states; \
	zcat $segment_file | awk '{print $4}' | sort | uniq >> ${OUTDIR}/states.txt; \
	state_list=${OUTDIR}/states.txt; \
	for state in ${states[@]}; do echo $state; zcat ${segment_file} | grep -w $state > ${OUTDIR}/${state}_segment.bed; done; \