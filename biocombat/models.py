from django.core.validators import MinValueValidator, MaxValueValidator, \
    MaxLengthValidator, MinLengthValidator
from django.db import models
import os


def renameImage(instance, filename):
    path = BioCard.path_to_images()
    ext = filename.split('.')[-1]
    return os.path.join(path,instance.pk.replace(" ", "_")+'.'+ext)


class BioCard(models.Model):
    
    hp = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],
                                                blank=False)
    name = models.CharField(max_length=40,
                             validators=[MinLengthValidator(2),MaxLengthValidator(40)],
                              blank=False,
                              primary_key=True)
    structure = models.CharField(max_length=45,
                                  validators=[MinLengthValidator(3),MaxLengthValidator(45)],
                                   blank=False)
    image = models.ImageField(upload_to=renameImage)
    info = models.CharField(max_length=330,
                             validators=[MinLengthValidator(2),MaxLengthValidator(330)],
                              blank=False)
    atk = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],
                                          blank=False)
    CHOICES= [(0,'Defense Mechanism'),(1, 'Bacteria'), (2,'Other Mechanisms')]  
    cardType = models.IntegerField(choices=CHOICES)   
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def path_to_images():
        return '/var/www/biocombat/static/cards'
    
    @staticmethod
    def card_types(language='en'):
        if language == 'pt-br':
            return ['Mecanismo de Defesa', 'Bacteria', 'Outros Mecanismos'] 
        if language == 'en':
            return ['Defense Mechanism', 'Bacteria', 'Other Mechanisms']
        
    @staticmethod
    def card_colors():
        return ['lightblue','gold','crimson']
        
    
