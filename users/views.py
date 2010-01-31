# -*- encoding: utf8 -*-
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm

from jebif_cv.constants import INFO_MSG, SUCCESS_MSG, ERROR_MSG
from users.forms import UserForm

#
# Public views (called from urls)
#

def collection(request):
    if request.method == "GET":
        return _index(request)
    elif request.method == "POST":
        return _create(request)

def entry(request, user_id):
    user = get_object_or_404(User, id = user_id)
    if request.method == "GET":
        return _show(request, user)
    elif request.method == "PUT":
        return _update(request, user)
    elif request.method == "DELETE":
        return _delete(request, user)

def new(request):
    return direct_to_template(request, "users/new.html", {
        'form': UserCreationForm()
    })

def edit(request, user_id):
    user = get_object_or_404(User, id = user_id)
    return direct_to_template(request, "users/edit.html", {
        'form': UserForm(instance = user),
        'user_edit': user
    })

def delete(request, user_id):
    user = get_object_or_404(User, id = user_id)
    return _delete(request, user)

def change_password(request, user_id):
    user = get_object_or_404(User, id = user_id)
    
    if not user == request.user and not request.user.is_superuser:
        message = ERROR_MSG % "Vous n'êtes pas autorisé à modifier le mot de passe de cet utilisateur."
        request.user.message_set.create(message = message)
        return redirect( request.user.get_absolute_url() )
    
    if request.method == 'GET':
        if user == request.user:
            message = INFO_MSG % "Veuillez entrer votre ancien mot de passe, \
pour des raisons de sécurité, et saisissez ensuite deux fois votre nouveau mot \
de passe pour que nous puissions vérifier que vous l'avez entrer correctement"
            request.user.message_set.create( message = message )
            form = PasswordChangeForm(user)
        else:
            form = SetPasswordForm(user)
    elif request.method == 'PUT':
        data = request.PUT
        if user == request.user:
            form = PasswordChangeForm( user, data = data )
        else:
            form = SetPasswordForm( user, data = data )
        if form.is_valid():
            form.save()
            message = SUCCESS_MSG % 'Nouveau mot de passe enregistré.'
            request.user.message_set.create( message = message )
            return redirect( user.get_absolute_url() )
        else:
            message = ERROR_MSG % 'Le formulaire est invalide, veuillez corriger les erreurs suivantes.'
            request.user.message_set.create( message = message )
    
    return direct_to_template(request, 'users/change_password.html', {
        'user_edit': user,
        'password_form': form
    })

#
# Private views
#

def _index(request):
    return direct_to_template(request, "users/index.html", {
        'users': User.objects.all()
    })

def _show(request, user):
    return direct_to_template(request, "users/show.html", {
        'user': user
    })

def _create(request):
    form = UserCreationForm(data = request.POST, files = request.FILES)
    if form.is_valid():
        user = form.save()
        message = SUCCESS_MSG % "Utilisateur créé avec succès. Vous pouvez maintenant éditer son profil."
        request.user.message_set.create( message = message )
        return redirect( 'user_edit', user_id = user.id )
    else:
        message = ERROR_MSG % 'Le formulaire est invalide, veuillez corriger les erreurs suivantes.'
        request.user.message_set.create( message = message )
        return direct_to_template(request, "users/new.html", {
            'form': form
        })
    

def _update(request, user):
    was_superuser = user.is_superuser
    
    form = UserForm(instance = user, data = request.PUT)
    if form.is_valid():
        user = form.save()
        
        # Check if modified user is the last superuser in which case
        # his super-user status must remain True
        if was_superuser \
        and not user.is_superuser \
        and not User.objects.filter(is_superuser = True):
            message = INFO_MSG%"Au moins un utilisateur doit être super-utilisateur."
            request.user.message_set.create( message = message )
            user.is_superuser = True
            user.save()
        
        # Changes have been made.
        message = SUCCESS_MSG % "Modification effectuée avec succès."
        request.user.message_set.create( message = message )
        if request.user.is_superuser:
            return redirect( 'user_collection' )
        else:
            return redirect( 'user_edit', request.user.id )
    else:
        message = ERROR_MSG % 'Le formulaire est invalide, veuillez corriger les erreurs suivantes.'
        request.user.message_set.create( message = message )
        return direct_to_template(request, "users/edit.html", {
            'user': user,
            'form': form
        })
    

def _delete(request, user):
    if User.objects.all().count() == 1:
        message = "Au moins un utilisateur est requis"
        user.message_set.create( message = message )
    elif User.objects.filter(is_superuser = True).count() == 1 and user.is_superuser:
        message = "Au moins un super-utilisateur est requis"
        user.message_set.create( message = message )
    else:        
        user_profile = user.get_profile()
        if user_profile.cv and user_profile.cv.pdf:
            user_profile.cv.pdf.delete()
        user.delete()
    
    return redirect('user_collection')

