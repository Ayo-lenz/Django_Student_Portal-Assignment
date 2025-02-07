from django import forms
from .models import Student, Student_Profile, Program

class StudentForm(forms.ModelForm):
  class Meta:
    model = Student
    fields = '__all__'  # Include fields you want to edit

    widgets = {
            'status': forms.CheckboxInput(),  # Ensures checkbox visibility
      }


class ProgramForm(forms.ModelForm):
  class Meta:
    model = Program
    fields = '__all__'


class StudentProfileForm(forms.ModelForm):
  class Meta:
    model = Student_Profile
    fields = '__all__'