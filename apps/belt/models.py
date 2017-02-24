from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def login(self, **kwargs):
        print "** User manager activated **"
        print "** Checking login info **"
        status = {}
        messages = []
        email = kwargs['mail'][0]
        password = kwargs['password'][0]
        print email, password
        if len(email) < 1 or len(password) < 1:
            messages.append("Login fields cannot be blank.")
        else:
            userinfo = User.userManager.filter(email=email)
            if not userinfo:
                messages.append("Unable to find user. Please register.")
            elif not bcrypt.checkpw(password.encode(), userinfo[0].password.encode()):
                messages.append("Incorrect password.")
        if not messages:
            valid = True
            status.update({'user_id': userinfo[0].id})
        else:
            valid = False
            status.update({'messages': messages})
        status.update({'valid': valid})
        return status

    def register(self, **kwargs):
        print "** User manager activated **"
        print "** Checking registration form **"
        status = {}
        messages = []
        fname = kwargs['first_name'][0]
        lname = kwargs['last_name'][0]
        email = kwargs['mail'][0]
        pword = kwargs['pword'][0]
        cpword = kwargs['c-pword'][0]
        birthday = kwargs['birthday'][0]
        if len(fname) < 1:
            messages.append('First name is required.')
        elif len(fname) < 3:
            messages.append('First name has to be at least 3 characters.')
        elif not NAME_REGEX.match(fname):
            messages.append('First name can only contain letters.')
        if len(lname) < 1:
            messages.append('Last name is required.')
        elif len(lname) < 3:
            messages.append('Last name has to be at least 3 characters.')
        elif not NAME_REGEX.match(lname):
            messages.append('Last name can only contain letters.')
        if len(email) < 1:
            messages.append('E-mail is required.')
        elif not EMAIL_REGEX.match(email):
            messages.append('Invalid e-mail format.')
        elif len(User.userManager.filter(email=email)) > 0:
            messages.append('User already exists.')
        if len(pword) < 1:
            messages.append('Password is required.')
        elif len(pword) < 8:
            messages.append('Password should be at least 8 characters.')
        elif pword != cpword:
            messages.append('Password fields do not match.')
        if not re.search(r'^[0-9][0-9][0-9][0-9][\-][0-9][0-9][\-][0-9][0-9]', birthday):
            messages.append('Invalid birthday format. Should be YYYY-MM-DD format.')
        elif birthday > time.strftime("%Y-%m-%d"):
            messages.append('Invalid birthday! Need to be from the past.')
        if not messages:
            valid = True
            messages.append('Thank you for registering! Please sign in.')
            pw_hash = bcrypt.hashpw(pword.encode(), bcrypt.gensalt())
            User.userManager.create(first_name = fname, last_name = lname, email = email, password = pw_hash, birthday = birthday)
        else:
            valid = False
        status.update({'valid': valid, 'messages': messages})
        return status

class TripManager(models.Manager):
    def addTrip(self, user_id, postData):
        print "** Trip Manager activated **"
        print "** Checking trip form **"
        messages = []
        print postData['startdate']
        print postData['enddate']
        if len(postData['destination']) < 1:
            messages.append("Destination is required.")
        if len(postData['description']) < 1:
            messages.append("Description is required.")
        if not re.search(r'^[0-9][0-9][0-9][0-9][\-][0-9][0-9][\-][0-9][0-9]', postData['startdate']):
            messages.append("Invalid start date format. Should be YYYY-MM-DD format.")
        elif postData['startdate'] < time.strftime("%Y-%m-%d"):
            messages.append("Invalid start date. Travel has to be future dated.")
        if not re.search(r'^[0-9][0-9][0-9][0-9][\-][0-9][0-9][\-][0-9][0-9]', postData['enddate']):
            messages.append("Invalid end date format. Should be YYYY-MM-DD format.")
        elif postData['startdate'] > postData['enddate']:
            messages.append("Invalid end date. End date of travel should not be before start date.")
        if not messages:
            messages.append('Thank you for adding your new trip.')
            Trip.tripMan.create(destination=postData['destination'], description=postData['description'], start=postData['startdate'], stop=postData['enddate'], user=User.userManager.get(id=user_id))
            return {'valid': True, 'msg': messages}
        else:
            print "** Something went wrong **"
            return {'valid': False, 'msg': messages}

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField(auto_now = False, auto_now_add = False, default="9999-11-29")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateField(auto_now=False, auto_now_add=False)
    stop = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(User, related_name="trips")
    plan = models.ManyToManyField(User, related_name="groups")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    tripMan = TripManager()
