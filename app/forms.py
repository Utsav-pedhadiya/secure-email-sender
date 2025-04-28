from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': 'You need to enter a password.'
        }
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': 'You need to confirm your password.'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        error_messages = {
            'username': {
                'required': 'You need to enter a username.',
                'unique': 'This username is already taken. Please choose another one.'
            },
            'email': {
                'required': 'You need to enter an email address.',
                'invalid': 'Enter a valid email address.'
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Confirm password does not match the entered password.")

        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EmailForm(forms.Form):
    recipient_email = forms.EmailField(
        label="Recipient Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipient email'})
    )
    subject = forms.CharField(
        label="Subject",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'})
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your message'})
    )
