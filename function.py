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
    self.df=df
    self.file_type=file_type
    self.cols=cols

  def check(self):
        return self.df, self.file_type, self.cols



