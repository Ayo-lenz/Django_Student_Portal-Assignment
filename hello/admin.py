from django.contrib import admin
from .models import Student,Program,Student_Profile,CohortGroup
import random
import string

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ['username', 'first_name','last_name','status', 'slug']
  readonly_fields = ('slug', )

  #student_slug_num_gen  = "".join(random.choices(string.digits,k=9))
  #prepopulated_fields = {'slug': 'first_name'-'last_name'-f"{student_slug_num_gen}"}

  #prepopulated_fields = {"slug": ("first_name", "last_name")}



@admin.register(Student_Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['student','date_of_birth', 'rating','date_join','address']



@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
  list_display = ['student', 'courses', 'grade']


   
@admin.register(CohortGroup)
class CohortAdmin(admin.ModelAdmin):
  list_display = ('name',)
