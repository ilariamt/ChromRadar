#!/usr/bin/env python
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

#def radar_plot()



