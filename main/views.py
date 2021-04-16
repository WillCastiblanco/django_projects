from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):   
    
    return render (request,'index.html')

def register(request):    
    if request.method == 'POST':        
        errors=User.objects.registration_validator(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect ('/')
        hash_pw = bcrypt.hashpw(request.POST['password'].encode() ,bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_pw
        )
        
        request.session['logged_user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")

        return redirect ('/success')
    return redirect ('/')


def login(request):    

    if not User.objects.credentials_validator(request.POST['email'],request.POST['password']):
            messages.error(request,'wrong credentials')
            return redirect('/')

    if request.method == 'POST':
        
        user = User.objects.filter(email=request.POST['email'])        

        if user:
            logged_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
                request.session['logged_user_id']=logged_user.id
                
                messages.success(request, "You have successfully logged in!")
                return redirect('/success')
        
        request.session['incorrect']='either login or password are incorrect'


    return redirect ('/')
    



def output(request):

    if 'logged_user' not in request.session:
        return redirect('/')

    context={
        'logged_user':User.objects.get(id=request.session['logged_user_id'])
    }    
    return render(request,'output.html',context)


def logout(request):
    request.session.flush()
    return redirect('/')


def catch_all(request, url):
    return redirect ('/')

# Create your views here.
