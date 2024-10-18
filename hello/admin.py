from django.contrib import admin
from .models import Student,Program,Student_Profile,CohortGroup

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ['username', 'first_name','last_name','status']
  # def get_cohort(self, obj):
  #   cohort_group = obj.cohortgroup_set.all() 
  #   return ", ".join([cohort.name for cohort in cohort_group])

  #     # Optional: Add a short description for the method (displayed as column title)
  # get_cohort.short_description = 'Cohort'




@admin.register(Student_Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['student','date_of_birth', 'rating','date_join','address']



@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
  list_display = ['student', 'courses', 'grade']


   
@admin.register(CohortGroup)
class CohortAdmin(admin.ModelAdmin):
  list_display = ('name',)
