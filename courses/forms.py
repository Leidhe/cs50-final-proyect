from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone
from multiupload.fields import MultiFileField, MultiImageField, MultiMediaField

from .models import Course, Homework, Section, Task, Unit


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'duration', 'level', 'language',
                  'image', 'categories', 'description', 'content', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'courseForm'
        self.helper.form_class = 'courseForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'create_course'
        self.helper.add_input(Submit('submit', 'Save'))

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        now = datetime.date(timezone.now())
        if end_date < now:

            raise forms.ValidationError(
                'You cannot set a date earlier than today. Choose a valid date.')
        else:
            return end_date


class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'duration', 'level', 'language',
                  'image', 'categories', 'description', 'content', 'end_date')

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
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('course_details', args=[self.instance.id]))))
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        now = datetime.date(timezone.now())
        if end_date < now:

            raise forms.ValidationError(
                'You cannot set a date earlier than today. Choose a valid date.')
        else:
            return end_date


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
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('course_details', args=[course_id]))))


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
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('course_details', args=[course_id]))))


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
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('course_details', args=[course_id]))))


class SectionEditForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'editsectionForm'
        self.helper.form_class = 'editsectionForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'edit_section', kwargs={'section_id': self.instance.id})
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('view_section', args=[self.instance.id]))))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'content', 'end_date')

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        unit_id = kwargs.pop('unit_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'taskForm'
        self.helper.form_class = 'taskForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'create_task', kwargs={'course_id': course_id, 'unit_id': unit_id})
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('course_details', args=[course_id]))))

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        course = Course.objects.get(pk=course_id)
        course_date = course.end_date
        now = datetime.date(timezone.now())
        if end_date < now:
            raise forms.ValidationError(
                'You cannot set a date earlier than today. Choose a valid date.')
        
        elif course_date < end_date:
            raise forms.ValidationError(
                'You cannot set a date beyond the end of the course. Choose a valid date.')
        else:
            return end_date


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'content', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'edit_taskForm'
        self.helper.form_class = 'edit_taskForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'edit_task', kwargs={'task_id': self.instance.id})
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('view_task', args=[self.instance.id]))))

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        course = Course.objects.get(pk=course_id)
        course_date = course.end_date
        now = datetime.date(timezone.now())
        if end_date < now:
            raise forms.ValidationError(
                'You cannot set a date earlier than today. Choose a valid date.')
        
        elif course_date < end_date:
            raise forms.ValidationError(
                'You cannot set a date beyond the end of the course. Choose a valid date.')
        else:
            return end_date

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ('answer', )

    file_field = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        task_id = kwargs.pop('task_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'HomeworkForm'
        self.helper.form_class = 'HomeworkForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'view_task', kwargs={'task_id': task_id})
        self.helper.add_input(Submit('submit', 'Save'))


class HomeworkEditForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ('answer',)

    file_field = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        task_id = kwargs.pop('task_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'HomeworkEditForm'
        self.helper.form_class = 'HomeworkEditForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'review_task', kwargs={'task_id': task_id, 'homework_id': self.instance.id})
        self.helper.add_input(Submit('submit', 'Save'))


class CorrectionForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ('grade',)

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        task_id = kwargs.pop('task_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'CorrectionForm'
        self.helper.form_class = 'CorrectionForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'correction', kwargs={'task_id': task_id, 'user_id': user_id, 'homework_id': self.instance.id})
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('view_task', args=[task_id]))))
