from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import render
from django.template import Context, loader
from django.utils.datastructures import MultiValueDictKeyError
import os
import re
import sys
import time

from biocombat.forms import CardForm
from biocombat.models import BioCard

def log(message):
	timestamp = str(time.strftime("%Y/%m%d")) + "-" + str(time.strftime("%H:%M:%S"))
	logfile = open("/var/www/biocombat/log/logfile","a")
	logfile.write(timestamp+": "+message+'\n')
	logfile.close()

def handle_uploaded_image(img, img_nome='card00'):
    path = BioCard.path_to_images()
    with open(path + img_nome, 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk)

def uploadCard(request):
    
    errors = []
    pop_errors = False
    
    form = CardForm(request.POST, request.FILES)

    if True:        
        
        try:
            up_energiaVital = request.POST['hp']
            up_nome = request.POST['name'] 
            up_estrutura = request.POST['structure']
            up_imagem = request.FILES.get('image', default=None)
            up_info = request.POST['info']
            up_ataque = request.POST['atk']  
            up_card_type = request.POST['cardType']
            
            re.sub(' +', ' ',up_info)
            re.sub(' +', ' ', up_nome)
            re.sub(' +', ' ', up_estrutura)            
            
            if len(up_nome) < 2:
                errors.append(form['name'].label + " must contain at least 2 characters")
                pop_errors = True      
                
            try:
                    temp = BioCard.objects.get(pk=up_nome)
                    errors.append(up_nome +" already in use")
                    pop_errors = True
            except:
                pass               
            
            if len(up_estrutura) < 3:
                errors.append(form['structure'].label + " must contain at least 3 characters")
                pop_errors = True
            if len(up_energiaVital) == 0:
                errors.append(form['hp'].label + " must be a value between 0 and 5")
                pop_errors = True   
            if len(up_ataque) == 0:
                errors.append(form['atk'].label + " must be a value between 0 and 5")
                pop_errors = True    
            if len(up_info) < 3:
                errors.append(form['info'].label +" must contain at least 3 characters")
                pop_errors = True 
                
            if up_imagem == None:
                errors.append("A picture must be set to the card")
                pop_errors = True
            
            if pop_errors:                
                return render(request, 'biocombat/createCard.html', {'form': form, 'errors':errors})
            
            else:		
                up_card = BioCard.objects.create(hp=up_energiaVital,
                                  name=up_nome.replace(" ", "_"),
                                  structure=up_estrutura,
                                  image=up_imagem,
                                  info = up_info,
                                  atk=up_ataque,
                                  cardType = up_card_type)        
                up_card.save()    
                return index(request)
        except MultiValueDictKeyError as err:
            log("MultiValueDictError: "+ str(err.message))
            print err.errno
            print err.strerror
        except AttributeError as att:
            log("AttributeError: "+ str(sys.exc_info()))
        except:
            log("Unexpected error:"+str( sys.exc_info()))
            form = CardForm(request.POST, request.FILES)
	    return render(request, 'biocombat/createCard.html', {'form':form, 'errors':errors})
    return render(request, 'biocombat/createCard.html', {'form':form, 'errors':errors})
    
def createCard(request, errors=[], form = None, language='en'):
    #print form
    if form == None:
        form = CardForm()
    return render(request, 'biocombat/createCard.html',
                   {'form': form, 'errors':errors})

def removeCard(request, form = None):
    cardName = request.POST['cardName']
    card = BioCard.objects.get(pk=cardName)
    if(card == None):
       return index(request)
    card.delete()
    path = BioCard.path_to_images()
    for filename in os.listdir(path):
       if filename.find(cardName) > -1:
           os.remove(path + "/" + filename)
    return index(request)

        

def openCard(request):
    print request.path
    
    
    cardName = request.path.split("/")[-1] 
    
    try:
        card = BioCard.objects.get(pk=cardName)    

	if card == None:
		return render(request, 'biocombat/openCard.html', {'errors':[cardName+'not found']})
        
	card_name = card.name.replace("_", " ")

        ext = str(card.image).split('.')[-1]
        relative_path = os.path.join('cards',card.name+'.'+ext)        
        
        card_type = card.cardType
        color = BioCard.card_colors()[card_type]
        
        c = Context({'card':card,
		     'card_name':card_name,
                     'path': relative_path,
                     'color': color})
        t = loader.get_template('biocombat/openCard.html')
        return HttpResponse(t.render(c))    
        
    except:
        print "Erro desonhecido em views.openCard"
        print sys.exc_info()
    errors = [cardName+" not found", sys.exc_info()] 
    return render(request, 'biocombat/openCard.html', {'errors':errors})

def removeCardView(request):
    return render(request, 'biocombat/removeCard.html')

def index(request): 
    
    #dict filename : full path
    cartasCriadas = {}
    path = BioCard.path_to_images()
    
    for filename in os.listdir(path):
        #print filename
        ext = filename.split('.')[-1]
        fn = filename[0:-(len(ext)+1)]
        card = BioCard.objects.get(pk=fn)
        cartasCriadas[fn] = os.path.join('cards',filename)
        
    
    t = loader.get_template('biocombat/index.html')
    c = Context({'cards': cartasCriadas})
    return HttpResponse(t.render(c))    
