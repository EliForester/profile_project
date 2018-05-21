from django.forms import ModelForm, DateField, EmailField, forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password


class UserProfileForm(ModelForm):

    dob = DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'])

    class Meta:
        model = UserProfile
        fields = ['dob', 'bio', 'image']
        labels = {'Date of Birth', 'Bio', 'Profile Image'}

    def clean(self):
        data = self.cleaned_data
        if data['bio']:
            if len(data['bio']) < 10:
                raise forms.ValidationError(
                    'Bio must be 10 or more characters')


class StrongPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def clean(self):
        special_chars = ['!', '#', '$', '%', '&']
        required_character_types = {'uppercase': 0,
                                    'lowercase': 0,
                                    'numeric': 0,
                                    'special_chars': 0}
        data = self.cleaned_data
        new_password = data['new_password1']

        # Make sure new password != old password
        if check_password(new_password, self.user.password):
            raise forms.ValidationError(
                'Password must not be the same as previous password')

        # Enforce character requirements
        for letter in new_password:
            if letter in special_chars:
                required_character_types['special_chars'] = 1
            if str.isupper(letter):
                required_character_types['uppercase'] = 1
            if str.islower(letter):
                required_character_types['lowercase'] = 1
            if str.isnumeric(letter):
                required_character_types['numeric'] = 1
        for character_type in required_character_types:
            if required_character_types[character_type] != 1:
                raise forms.ValidationError(
                    'Password must contain at least one of each: '
                    'upper, lower, numeral, and a special character ! # $ % &')


class UserForm(ModelForm):
    email2 = EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'First Name', 'Last Name', 'Email'}

    def clean(self):
        data = self.cleaned_data
        email2 = data['email2']
        if data['email'] != email2:
            raise forms.ValidationError('Email addresses do not match')
