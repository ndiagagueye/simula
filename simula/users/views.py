from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import datetime


from django.db.models import Q
from .models import *
from .forms import *

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage



# Create your views here.



def connexion(request):
    marques =Marque.objects.all()
    categories =Categorie.objects.all()
    nombre_p = nombre_prod(request)
    error = False
    form = ConnexionForm(request.POST or None)
    connect = False

    if form.is_valid():
        username = form.cleaned_data['username']
        password= form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            client = Userclient.objects.get(user=user)
            connect = True
            __move_session_cart_to_database_cart(request, client)
            login(request, user)  
            error=False
            if request.GET.get('next', False):
                return redirect(request.GET['next'])
            else:
                return redirect(accueil)
        else:
           error = True
    return render(request, 'compte/connexion.html', locals())

  


def inscription(request):
    nombre_p = nombre_prod(request)
    inscri = False
    marques =Marque.objects.all()
    categories =Categorie.objects.all()

    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = InscriptionForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    probleme = False
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        users = User.objects.all()
        #Nous allons vérifier si le nom d'utilisateur existe déja
        for user in users:
            if user.username in username and username in user.username:
                probleme = True

        if probleme:
            envoi = False
        else:

            user = User.objects.create_user(username , email , password)
            client = Userclient()
            client.user = user
            client.save()
            inscri = True
            __move_session_cart_to_database_cart(request, client)
            login(request, user)        

    
       

            # Nous pourrions ici envoyer l'e-mail grâce aux données 
            # que nous venons de récupérer
            envoi = True
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'compte/inscription.html', locals())
	
