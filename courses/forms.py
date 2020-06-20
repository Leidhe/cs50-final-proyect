from django import forms
from .models import Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'duration', 'level', 'language', 'image', 'categories', 'description', 'content')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'courseForm'
        self.helper.form_class = 'courseForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'create_course'
        self.helper.add_input(Submit('submit', 'Save'))