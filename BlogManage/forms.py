# coding=utf-8

from django import forms
from django.contrib import auth
from BlogManage.models import UserFilmRank


class RankForm(forms.ModelForm):
    class Meta:
        model = UserFilmRank
        # fields = ['name','text','author']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.TextInput(attrs={'class':'form-control'}),

        }
        exclude = ['author']
    
    def __init__(self, *args, **kwargs):
        super(RankForm, self).__init__(*args, **kwargs)
        self.fields['name'].label= u'名 称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['text'].label= u'评 分'
        self.fields['text'].error_messages={'required':u'请输入分数'}



class nameForm(forms.Form):
    name1 = forms.CharField()
