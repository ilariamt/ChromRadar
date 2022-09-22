class Annot:
  def __init__(self,path):
    self.path=path

  def import_data(self):
    with open(self.path) as f:
      counts=0
      for line in f:
          if line.startswith('##'):
              counts += 1
    self.header=counts
    # import data as dataframe
    df=pd.read_csv(self,skiprows=self.header,header=None,sep="\t")
    if len(df.columns) == 9:
      self.file_type="gtf"
      self.cols=9
    else:
      self.file_type="bed"
      self.cols=len(df.columns)
    return [self.file_type]


  def check(self):
    print(self)
    print(self.file_type)


    self.type = file_type		#possible: gtf, bed file
    
   def FileToDataframe(self):
	
    return self.grade
  
class Course:
  def __init__(self, name, max_students):
    self.name=name
    self.max_students=max_students
    self.students= []
    
   def add_students(self, student):
    if len(self.students) < self.max_students:
      self.students.append(student)
      return True
    return False
  
  def get_average_grade(self):
    value=0
    for student in self.students:
      value+=student.get_grade()
    return value/len(self.students)