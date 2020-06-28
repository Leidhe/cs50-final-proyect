from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.files.images import get_image_dimensions
from .models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    firstname = forms.CharField(max_length=255, required=False)
    lastname = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username','email', 'firstname', 'lastname', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        'placeholder':'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'placeholder':'Password'
        }
    ))

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name',
                  'email',)
    picture_profile = forms.ImageField(required = False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'UserEditForm'
        self.helper.form_class = 'UserEditForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse(
            'edit_account')
        self.helper.add_input(Submit('submit', 'Save'))

    def clean_picture_profile(self):            
        picture_profile = self.cleaned_data['picture_profile']

        if picture_profile:

            try:
                w, h = get_image_dimensions(picture_profile)

                #validate dimensions
                max_width = max_height = 100
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Please use an image that is '
                        '%s x %s pixels or smaller.' % (max_width, max_height))

                #validate content type
                main, sub = picture_profile.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                        'GIF or PNG image.')

            except AttributeError:
                pass

            return picture_profile
        else:
            pass