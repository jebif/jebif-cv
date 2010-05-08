# -*- encoding: utf8 -*-

from django.db.models import Q
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, redirect

from jebif_cv.constants import INFO_MSG, SUCCESS_MSG, ERROR_MSG
from candidate.models import CV
from candidate.forms import CVForm, SearchForm

#
# Public views (called from urls)
#

def collection(request):
    if request.method == "GET":
        return _index(request)
    elif request.method == "POST":
        return _create(request)

def entry(request, cv_id):
    cv = get_object_or_404(CV, id = cv_id)
    user_profile = request.user.get_profile()
    if not user_profile.is_employer or not user_profile.cv == cv:
        message = ERROR_MSG%"Vous devez être 'employeur', ou être le propriétaire de ce CV pour le visualiser"
        request.user.message_set.create( message = message)
        return redirect( 'cv_collection' )
    
    if request.method == "GET":
        return _show(request, cv)
    elif request.method == "PUT":
        return _update(request, cv)
    elif request.method == "DELETE":
        return _delete(request, cv)

def new(request):
    return direct_to_template(request, "cv/new.html", {
        'form': CVForm()
    })

def edit(request, cv_id):
    cv = get_object_or_404(CV, id = cv_id)
    return direct_to_template(request, "cv/edit.html", {
        'form': CVForm(instance = cv),
        'cv': cv
    })

def toggle_valid(request, cv_id):
    cv = get_object_or_404(CV, id = cv_id)
    cv.is_valid = not cv.is_valid
    cv.save()
    return redirect( 'user_collection' )

def search(request):
    form = SearchForm( data = request.POST )
    
    filters = {}
    
    if form.is_valid():
        data         = form.cleaned_data
        job_type     = data['job_type']
        keywords     = data['keywords']
        available_on = data['available_on']
        name         = data['name']
        
        # Job type - multiple choices
        if job_type:
            filters.update({ 'job_type__in': job_type })
        
        # Available from / Available before
        if available_on and instance(available_on, list) and len(available_on) == 2:
            filters.update({
                'available_on__gte': available_on[0],
                'available_on__lte': available_on[1]
            })
        
        # Keywords
        if keywords:
            ids = []
            for kw in keywords:
                ids.extend(CV.objects.filter(keywords__icontains = kw).values_list('id', flat = True))
            filters.update({ 'id__in': ids })
        
        if filters:
            cv_list = CV.objects.filter(**filters)
        else:
            cv_list = CV.objects.none()
        
        # First name and Last name
        if name:
            if not cv_list and not filters: cv_list = CV.objects.all()
            
            name = name.split(' ')
            if len(name) == 1:
                cv_list = cv_list.filter( Q(first_name = name[0]) | Q(last_name = name[0]) )
            else:
                cv_list = cv_list.filter( 
                    Q(first_name = name[0]) | Q(last_name = name[1]) |
                    Q(first_name = name[1]) | Q(last_name = name[0])
                )
        
    
    return direct_to_template(request, "cv/index.html", {
        'form': form,
        'cv_list': cv_list
    })


#
# Private views
#

def _index(request):
    return direct_to_template(request, "cv/index.html", {
        'form': SearchForm(),
        'cv_list': CV.objects.filter(is_valid = True)
    })

def _show(request, cv):
    return direct_to_template(request, "cv/show.html", {
        'cv': cv
    })

def _create(request):
    form = CVForm(data = request.POST, files = request.FILES)
    if form.is_valid():
        cv = form.save()
        user_profile = request.user.get_profile()
        user_profile.cv = cv
        user_profile.save()
        message = SUCCESS_MSG%"CV créé avec succès"
        request.user.message_set.create( message = message )
        return redirect( cv.get_absolute_url() )
    else:
        message = ERROR_MSG%"Le formulaire est invalide, veuillez corriger les erreurs suivantes"
        request.user.message_set.create( message = message )
        return direct_to_template(request, "cv/new.html", {
            'form': form
        })
    

def _update(request, cv):
    data = request.PUT.copy()
    data['is_valid'] = cv.is_valid
    
    form = CVForm(instance = cv, data = data, files = request.FILES)
    if form.is_valid():
        form.save()
        message = SUCCESS_MSG%"CV modifié avec succès"
        request.user.message_set.create( message = message )
        return redirect( cv.get_absolute_url() )
    else:
        message = ERROR_MSG%"Le formulaire est invalide, veuillez corriger les erreurs suivantes"
        request.user.message_set.create( message = message )
        return direct_to_template(request, "cv/edit.html", {
            'cv': cv,
            'form': form
        })

def _delete(request, cv_id):
    cv.delete()
    return redirect('cv_collection')
