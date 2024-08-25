from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Retype Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password didn\'t match!')
        return cd['password2']
    
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role', 'department')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('prn', 'admin_number')    

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Replace with `User` if you're using the default User model
        fields = ['name', 'username', 'department', 'role', 'email', 'password']  # Add other fields as necessary
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = True

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user     
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['prn', 'admin_number']       