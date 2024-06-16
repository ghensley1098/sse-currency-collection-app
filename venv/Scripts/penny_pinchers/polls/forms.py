from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserCreationForm(UserCreationForm):
    fname = forms.CharField(max_length=30, required=True)
    lname = forms.CharField(max_length=30, required=True)
    birth_year = forms.DateField(required=True)
    email = forms.CharField(required=True)
    username = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'fname', 'lname', 'birth_year', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Concatenate initials and birth year to the password
        initials = user.first_name + user.last_name
        birth_year = user.birth_year
        user.set_password((user.password))
        if commit:
            user.save()
        return user