# -*- encoding: utf8 -*-

from django import forms
from django.conf import settings

from candidate.models import CV, JobType
from utils import DateField

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
    
    def __init__(self, *args, **kwargs):
        super(CVForm, self).__init__(*args, **kwargs)
        self.fields['available_on'] = DateField(
            input_formats   = ('%d/%m/%Y', ), 
            label           = u"Je suis disponible à partir du",
            help_text       = "Format : jj/mm/aaaa")
        if self.instance.id:
            self.fields['available_on'].initial = self.instance.available_on
        
    

class SearchForm(forms.Form):
    job_type        = forms.ModelMultipleChoiceField(
                        queryset = JobType.objects.all(),
                        label = u"Type de poste",
                        required = False
                      )
    
    keywords        = forms.CharField(
                        label = u"Mot-clés",
                        required = False
                      )
    
    available_on    = forms.CharField(
                        label = "Disponibilité",
                        help_text = "Format: jj/mm/aaaa" ,
                        required = False
                      )
    
    name            = forms.CharField(
                        label = "Nom du candidat",
                        required = False
                      )
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['available_on'].widget.attrs = {'class': 'date-range-field', 'autocomplete': 'off'}
        
        keywords = CV.objects.all().values_list('keywords')
        if keywords:
            keyword_choices = []
            for keyword in ",".join(zip(*keywords.distinct())[0]).split(","):
                keyword = keyword.strip().lower()
                if not keyword in keyword_choices:
                    keyword_choices.append( keyword )
            keywords = ",".join( keyword_choices )
        else:
            keywords = ""
        self.fields['keywords'].widget.attrs.update({ 'choices' : keywords })
        
        names = CV.objects.all().values_list('last_name', 'first_name')
        names = ",".join(map(" ".join, names))
        self.fields['name'].widget.attrs.update({ 'choices' : names })
    
    def clean_available_on(self):
        data = self.cleaned_data
        if not data['available_on']: return data['available_on']
        
        available_on = data['available_on'].split(' ')
        return available_on
    
    def clean_keywords(self):
        data = self.cleaned_data
        if not data['keywords']: return data['keywords']
        
        return data['keywords'].split(',')

