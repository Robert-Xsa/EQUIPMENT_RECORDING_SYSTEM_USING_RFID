from django import forms
from .models import Equipment, Borrowing, Student, Arduino_COM

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'tag', 'model_number']

class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['equipment', 'student']
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_number', 'first_name', 'middle_name', 'last_name', 'course']

