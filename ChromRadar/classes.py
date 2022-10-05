#!/usr/bin/env python
import os, subprocess, gzip
import pandas as pd
import numpy as np
from function import bash_command, zipped_file, file_to_df


class Annot:
  def __init__(self,path):
    self.path=path
    self.name=os.path.basename(os.path.normpath(self.path)).rsplit(".")[0]
    self.zip=zipped_file(self.path)
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

  def check(self):
    """check file type
    """
    return self.df, self.file_type, self.cols, self.zip
    
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

  def by_state_cov(self):
    """Returns bp coverage for each state on given annotation. In table form, sorted by ascending state name.
    """
    # only take chr,start,end (annot), chr,start,end (state), state_id, cov_width
    reduced=self.intersectdf.iloc[:,[0,1,2,-5,-4,-3,-2,-1]]
    state=reduced.columns[-2]                         #rename columns
    width=reduced.columns[-1]
    state_cov=reduced.groupby([state]).sum()          # groupby state and sum all the other entries (new df)
    self.state_cov=state_cov.loc[:,[width]]           # extract from state_cov df only summed widths
    # remove ".", loci where no state covers annotation (usually this happens if segment files does not cover all chr's or scaffolds, use of different chromsizes)
    # print the number of uncovered bp
    if any(self.state_cov.index=="."):
        if int(self.state_cov.loc[(self.state_cov.index=="."),width])==0:
            self.state_cov=self.state_cov.loc[(self.state_cov.index!="."),:]
        else:
            print(int(self.state_cov.loc[(self.state_cov.index=="."),width]),"bp of annotation",self.name,"are not assigned to any state")
            self.state_cov=self.state_cov.loc[(self.state_cov.index!="."),:]
    # modify state_cov df for better downstream manipulation
    self.state_cov.index.name = None                                                          # no index title
    self.state_cov.rename(columns={self.state_cov.columns[0]: self.name }, inplace = True)    # colnames as the annotation name
    self.state_cov.sort_index(ascending=True)                                                 # sort the rows by state_id
    return self.state_cov

#   def ByStateCov(self):
#     """Returns bp coverage for each state on given annotation. In table form, sorted by ascending state name.
#     """
#     reduced=self.intersectdf.iloc[:,[0,3,4,9,10,11,12,col]]
#     state_cov=reduced.groupby([12]).sum()
#     self.state_cov=state_cov.loc[:,[col]]
#     if any(self.state_cov.index=="."):
#         if int(self.state_cov.loc[(self.state_cov.index=="."),col])==0:
#             self.state_cov=self.state_cov.loc[(self.state_cov.index!="."),:]
#         else:
#             print(int(self.state_cov.loc[(self.state_cov.index=="."),col]),"bp of annotation",self.name,"are not assigned to any state")
#             self.state_cov=self.state_cov.loc[(self.state_cov.index!="."),:]
#     self.state_cov.index.name = None
#     self.state_cov.rename(columns={self.state_cov.columns[0]: self.name }, inplace = True)
#     self.state_cov.sort_index(ascending=True)
#     return self.state_cov
    
class Bed(Annot):
  pass

  def intersect(self,chrom_obj_path):
    """Intersects a bed annotation file with Chrom_segmentation file.
    """
    #define segmentation files
    segment=chrom_obj_path
    #define annot model
    annot=self.path
    #define the intersect file (create dir for each different annot object)
    cwd = os.getcwd()
    os.makedirs(cwd+"/intersect/", exist_ok=True)
    isect_file = cwd+"/intersect/"+self.name+"_intersect.bed"
    if self.zip == True:
      cmd=f'zcat {annot} | cut -f 1,2,3 | bedtools intersect -a - -b {segment} -wao > {isect_file}'
    else:
      cmd=f'cat {annot} | cut -f 1,2,3 | bedtools intersect -a - -b {segment} -wao > {isect_file}'
    bash_command(cmd)
    self.intersectdf=file_to_df(isect_file)
    return self.intersectdf


class ChromObj:
  def __init__(self,path):
    self.path=path
    self.df=file_to_df(self.path)
    self.states=np.unique(self.df.iloc[:,3])
    
  def get_df(self):
    """Check the dataframe obtained from segment ChromHMM file.
    """
    return self.df
    
  def get_states(self):
    """Returns states and number of states of ChromHMM segmentation file.
    """
    return self.states, len(self.states)
    
  def get_path(self):
    """Returns path of ChromHMM segmentation file.
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