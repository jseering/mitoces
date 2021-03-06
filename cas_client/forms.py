from django import forms
from models import Module, Outcome, Keyword
from django.contrib.auth.models import User

class ModuleForm(forms.ModelForm):
    
    class Meta:
        model = Module
        fields = ('name', 'description', 'outcomes', 'link', 'keywords')

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ModuleForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(ModuleForm, self).save(commit=False)
        inst.creator = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

class OutcomeForm(forms.ModelForm):
    
    class Meta:
        model = Outcome
        fields = ('name', 'description')

class KeywordForm(forms.ModelForm):
    
    class Meta:
        model = Keyword

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name','last_name','email')
