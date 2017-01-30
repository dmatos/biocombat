from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator


class CardForm(forms.Form):
    
    hp = forms.IntegerField(error_messages={'required': 'Set a value'},
                                      label='Health Points',
                                      min_value=0,
                                      max_value=5,
                                      required=True)
    name = forms.CharField(max_length=40,
                           min_length=2,
                           label='Card Name',
                           error_messages={'required': 'Set a name'},
                           validators=[MinLengthValidator(2),
                                       MaxLengthValidator(40)],
                           required=True)
    structure = forms.CharField(max_length=45,
                                label='Structure',
                                min_length=2,
                                validators=[MinLengthValidator(3),
                                             MaxLengthValidator(45)],
                                required=True)
    image = forms.ImageField(label='Image')
    info = forms.CharField(widget=forms.Textarea,
                           max_length=330,
                           label='Info',
                           validators=[MinLengthValidator(2),
                                       MaxLengthValidator(330)],
                           required=True)
    atk = forms.IntegerField(label='Attack',
                                 error_messages={'required': 'Set the damage inflicted by the card'},
                                 min_value=0,
                                 max_value=5,
                                 required=True)
    
    
    CHOICES= [(0,'Defense Mechanism'),(1, 'Bacteria'), (2,'Other Mechanisms')]    
    cardType = forms.ChoiceField(choices=CHOICES, label='Card Type')
