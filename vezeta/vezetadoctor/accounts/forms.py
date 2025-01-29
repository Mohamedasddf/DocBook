from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class SignUp(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='تأكيد كلمة المرور')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise ValidationError("كلمة المرور وتأكيد كلمة المرور يجب أن يكونا متطابقين.")
        return cleaned_data



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='اسم المستخدم')
    password = forms.CharField(widget=forms.PasswordInput(), label='كلمة المرور')

    class Meta:
        model = User
        fields = ('username', 'password')




class UpdateUser(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label='تأكيد كلمة المرور')

    class Meta:
        model = User
        fields = ('username' ,'first_name', 'last_name', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean() 
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("كلمة المرور وتأكيد كلمة المرور يجب أن يكونا متطابقين.") 
        return cleaned_data

