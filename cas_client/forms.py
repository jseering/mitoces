from django import forms
from models import Module, Outcome, Keyword

class ModuleForm(forms.ModelForm):
    
    class Meta:
        model = Module
        fields = ('name', 'link', 'outcomes', 'keywords')

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