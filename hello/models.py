from django.db import models
from django.utils.text import slugify
import random
import string
# Create your models here.

class Student(models.Model):
  username = models.CharField(max_length=100)
  slug = models.SlugField(unique=True, blank=True, editable=False)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField(max_length=250,null=True, default='examples@gmail.com')
  status = models.BooleanField(default=True)
  

  class Meta:
    ordering = ['first_name']


  def __str__(self):
    return f"{self.first_name} {self.last_name}"
  
  def save(self,*args, **kwargs ):
    if not self.slug:
      student_slug_num_gen  = "".join(random.choices(string.digits,k=9))
      self.slug = slugify(f"{self.first_name}-{self.last_name}-{student_slug_num_gen}")
    super().save(*args, **kwargs)





class Student_Profile(models.Model):
  student = models.OneToOneField(Student,on_delete=models.CASCADE)
  bio = models.TextField()
  date_of_birth =models.DateField()
  address = models.CharField(max_length=300)
  rating = models.FloatField(default=0.0)
  profile_picture = models.ImageField(upload_to='student_profile')
  date_join = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.student.username}"






class Program(models.Model):
  courses = models.CharField(max_length=500)
  grade = models.IntegerField(default=0.0)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.courses}"




from django.db import models

# Create your models here.


cohort_names = [
  ('Cohort 1', 'Cohort 1'),
  ('Cohort 2', 'Cohort 2'),
  ('Cohort 3', 'Cohort 3'),
]



class CohortGroup(models.Model):
  name = models.CharField(max_length=200, choices=cohort_names)
  date_join = models.DateTimeField(auto_now_add=True)
  students = models.ManyToManyField(Student, related_name='cohort_groups')
  def __str__(self):
    return f"{self.name}"
  