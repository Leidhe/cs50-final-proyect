from django import forms
from django.shortcuts import reverse
from .models import Course, Section, File, Task, Unit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'duration', 'level', 'language',
                  'image', 'categories', 'description', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'courseForm'
        self.helper.form_class = 'courseForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'create_course'
        self.helper.add_input(Submit('submit', 'Save'))


class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'duration', 'level', 'language',
                  'image', 'categories', 'description', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'courseForm'
        self.helper.form_class = 'courseForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'edit_course', args=[self.instance.id])
        self.helper.add_input(Submit('submit', 'Save'))


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'unitForm'
        self.helper.form_class = 'unitForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'create_unit', kwargs={'course_id': course_id})
        self.helper.add_input(Submit('submit', 'Save'))


class UnitEditForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'uniteditForm'
        self.helper.form_class = 'uniteditForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'edit_unit', kwargs={'course_id': course_id, 'unit_id': self.instance.id})
        self.helper.add_input(Submit('submit', 'Save'))

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'content')

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        unit_id = kwargs.pop('unit_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'sectionForm'
        self.helper.form_class = 'sectionForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'create_section', kwargs={'course_id': course_id, 'unit_id': unit_id})
        self.helper.add_input(Submit('submit', 'Save'))

