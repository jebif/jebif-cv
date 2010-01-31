# -*- encoding: utf8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

SEEKING_CHOICES = (
    (1, "Oui"),
    (2, "Pourquoi pas!"),
    (3, "Non")
)

JOB_TYPE_CHOICES = (
    (1, "CDI"),
    (2, "CDD"),
    (3, "Postdoc"),
    (4, "Thèse"),
    (5, "Stage")
)

def cv_repository_path(instance, filename):
    return "files/cv/%s_%s.pdf"%(instance.first_name, instance.last_name)
    
def picture_repository_path(instance, filename):
    return "files/pictures/%s_%s.jpg"%(instance.first_name, instance.last_name)

class JobType(models.Model):
    title = models.CharField("Titre", max_length = 20)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name, verbose_name_plural = "Type de poste", "Types de poste"

class CV(models.Model):
    is_valid      = models.BooleanField(u"Valide ?", default=False)
    first_name    = models.CharField(u"Prénom", max_length = 80)
    last_name     = models.CharField(u"Nom", max_length = 80)
    picture       = models.FileField(u"Photo", upload_to = picture_repository_path, null = True, blank = True)
    description   = models.CharField(u"Phrase courte d'introduction",
                        help_text = "Exemple: Je suis développeur d'applications web.",
                        null = True, blank = True, max_length=100)
    
    seeking_a_job = models.IntegerField("Je recherche un poste", choices = SEEKING_CHOICES)
    available_on  = models.DateField("Je suis disponible à partir du",
                        help_text = "Format: jj/mm/aaaa",
                        null=True, blank=True)
    job_type      = models.ManyToManyField(JobType, verbose_name = "Type de poste recherché")
    keywords      = models.TextField("Mots-clés", 
                        help_text = "Veuillez séparer les mots-clés par des \
                        virgules pour que la recherche soit ensuite efficace.",
                        null = True, blank = True
                    )
    paper_version = models.BooleanField("Je veux faire diffuser une version papier", default = False)
    cover_letter  = models.TextField("Lettre de motivation", 
                        help_text = "100 caractères maximum",
                        max_length = 100,
                        null = True, blank = True
                    )
    pdf = models.FileField(upload_to = cv_repository_path)
    
    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = "CV", "CVs"
    
    def __unicode__(self):
        return u"%s %s"%(self.first_name, self.last_name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('cv_entry', [self.id])
