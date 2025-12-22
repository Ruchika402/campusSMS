from django import forms
from .models import Student, ClassRoom

# Student form
class StudentForm(forms.ModelForm):
    classroom = forms.ModelChoiceField(
        queryset=ClassRoom.objects.all(),
        empty_label="-- No Class Available --",  # placeholder text
        required=False
    )

    class Meta:
        model = Student
        fields = '__all__'

# ClassRoom form
class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name']


from .models import Marks

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'marks_obtained']


from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']  # adjust if you have more fields
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter subject name'})
        }

from django import forms
from .models import ClassRoom

class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name']  # or whatever fields your ClassRoom model has
  