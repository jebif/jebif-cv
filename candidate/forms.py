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
    
    keyword         = forms.CharField(
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
            keywords = ",".join(zip(*keywords.distinct())[0]).replace(", ", ",").replace(" ,", ",")
        else:
            keywords = ""
        self.fields['keyword'].widget.attrs.update({ 'choices' : keywords })
    
