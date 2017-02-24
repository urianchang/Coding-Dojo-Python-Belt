from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.

# Render the login & registration page
def index(request):
    print "** LOGIN/REG **"
    if 'user_id' not in request.session:
        request.session['user_id'] = -1
    return render(request, 'belt/index.html')

# When user attempts to log in
def login(request):
    if request.method == 'GET':
        print "** Login is POST-only **"
        return redirect('/')
    print "** Log in requested **"
    login_info = User.userManager.login(**request.POST)
    if login_info['valid']:
        print "** Login info is valid **"
        request.session['user_id'] = login_info['user_id']
        return redirect('/travels')
    else:
        print "** Something went wrong **"
        for msg in login_info['messages']:
            messages.warning(request, msg)
        return redirect('/')

# When user attempts to register
def register(request):
    if request.method == 'GET':
        print "** Registration is POST-only **"
        return redirect('/')
    print "** Registration requested **"
    status_info = User.userManager.register(**request.POST)
    if status_info['valid']:
        print "** Registration information is valid **"
        for msg in status_info['messages']:
            messages.success(request, msg)
    else:
        print "** Something went wrong **"
        for msg in status_info['messages']:
            messages.error(request, msg)
    return redirect('/')

# Render the success/welcome page
def welcome(request):
    if 'user_id' not in request.session or request.session['user_id'] == -1:
        print "Nuh-uh. You can't see this page yet."
        request.session['user_id'] = -1
        messages.warning(request, 'Please sign-in or register.')
        return redirect('/')
    else:
        print "** Welcome back, user! **"
        context = {
            'user': User.userManager.get(id=request.session['user_id']),
            'users': User.userManager.all()
        }
        return render(request, 'belt/travels.html', context)

# When user logs out
def logout(request):
    if request.method == "GET":
        print "Logging out should be a POST request"
        return redirect('/')
    print "** Logging out **"
    request.session.pop('user_id')
    return redirect('/')

# # Delete a user
# def delete(request):
#     if request.method == 'GET':
#         print "Delete is POST-only"
#         return redirect('/')
#     User.userManager.get(id=request.POST['id']).delete()
#     return redirect('/success')

# If user accesses a URL route that's not supported...
def any(request):
    return redirect('/')
