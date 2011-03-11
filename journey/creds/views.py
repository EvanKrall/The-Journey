from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def user_login(request):
    if request.POST:
        # login form was submitted
        next = request.POST.get('next', '/booth/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return render_to_response('login.html', {'error': 'Your account has been disabled'})
        else:
            return render_to_response('login.html', {'error': 'incorrect password/username combination'})
    else:

        # login form was requested
        c = {}
        c.update(csrf(request))
        c['next'] = request.GET.get('next','/booth/')
        return render_to_response('login.html', c)

import urllib

def error_query_string(error):
    error = {'error': error}
    error = urllib.urlencode(error)
    return '?'+error

def register(request):
    if request.POST:
        # registration form was submitted
        username = request.POST['username']
        
        if username.count('@yelp') != 1:
            return HttpResponseRedirect('/register/' + error_query_string('Yelp accounts only'))

        password = request.POST['password']
        repeat = request.POST['repeat']
        if password != repeat:
            return HttpResponseRedirect('/register/' + error_query_string('passwords must be the same'))
        try:
            user = User.objects.create(username, password)
        except User.AlreadyExistis:
            return HttpResponseRedirect('/register/' + error_query_string('username already exists, try another one'))
            
        return user_login(request)
    else:
        # registration form was asked for
        c = {}
        c.update(csrf(request))
        if request.GET:
            c['error'] = request.GET.get('error', None)
        return render_to_response('registration.html', c)

@login_required
def logout_user(request):
  logout(request)
  return HttpResponseRedirect('/login/')



