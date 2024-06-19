from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser, mEntry, mCollection, CONTINENT_CHOICES, QUALITY_CHOICES
from django.contrib.auth.models import Group

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
        user.is_staff = True
        group = Group.objects.get(name='NormalUser')
        user.save()
        user.groups.add(group)
        # Concatenate initials and birth year to the password
        # initials = user.first_name + user.last_name
        # birth_year = user.birth_year
        # user.set_password(str(hash(user.password + initials + str(birth_year))))
        # if commit:
        #     user.save()
        return user
    
class mEntryNewModelForm(ModelForm):
    def __init__(self, *args, user=None, collection=None, **kwargs):
        super(mEntryNewModelForm, self).__init__(*args, **kwargs)
        self.user = user
        if collection is not None:
            query = mCollection.objects.filter(cName = collection)
            self.fields['eCollection'].queryset = query
            self.fields['eCollection'].initial = query.first()
            self.fields['eCollection'].empty_label = None

    class Meta:
        model = mEntry
        exclude = ['created_by']

    def save(self, commit=False):
        entry = super().save(False)
        entry.created_by = self.user
        entry.save()
        return entry
        
    
class mEntryModelForm(ModelForm):
    class Meta:
        model = mEntry
        exclude = ['created_by', 'eCollection']

        widgets = [
            {'ePlace': forms.Select(choices = CONTINENT_CHOICES)},
            {'eQuality': forms.Select(choices = QUALITY_CHOICES)}
        ]
