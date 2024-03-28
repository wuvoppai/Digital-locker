from django.shortcuts import render, redirect
from MyApp.models import Customer, Upload
import os

msg = None
status = {'username':None,
          'logged':False,
          'userdata':None,
          'filedata':None,
          'error':None,
          'memory_status':0}

def index(request):
    global msg
    return render(request,'Index.html',{'msg':msg})

def register(request):
    return render(request,'Register.html')

def registration(request):
    name = request.POST['name']
    age = request.POST['age']
    gender = request.POST['gender']
    email = request.POST['email']
    mobile = request.POST['mobile']
    profile = request.FILES.get('profile',False)
    username = request.POST['username']
    password = request.POST['password']
    if Customer.objects.filter(username=username):
            
            return render(request,"Index.html")
        
    if Customer.objects.filter(email=email):
            
            return render(request,"Index.html")
    customer = Customer(name=name,age=age,gender=gender,email=email,mobile=mobile,profile=profile,username=username,password=password)

    customer.save()
    global msg
    msg = 'User Created Successfully'
    return redirect('/')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    global status
    user = Customer.objects.all().filter(username=username)
    if user is not None:
        for i in user:
            if i.password==password:
                status['username']=i.username
                status['logged']=True
                break
    if status['logged']:
        return redirect('/Home')
    else:
        return render(request,'Index.html',{'msg':'Invalid Login Credentials'})
    

def home(request):
    global status
    data=Customer.objects.get(username=status['username'])
    status['filedata']=Upload.objects.all().filter(username=status['username'],storage='Memory').order_by('-id')
    status['memory_status']=round(data.memory/data.total_memory*100,2)
    return render(request,'Dashboard.html',status)

def logout(request):
    global status
    global msg
    msg = 'You have been logged out'
    status['logged']=False
    return redirect('/')

def upload(request):
    global status
    files = request.FILES.getlist('pic')
    for i in files:
        data = Customer.objects.get(username=status['username'])
        if data.total_memory-data.memory >= i.size:
            file = Upload(username=status['username'],file_name=i.name,storage='Memory',file=i)
            file.save()
            data.memory = data.memory + i.size
            data.save()
        else:
            status['error']='Insufficient Space'
            return redirect('/Home')
    status['error']='Uploaded Successfully'
    return redirect('/Home')

def delete(request):
    ids = request.POST['id']
    data = Upload.objects.get(id=ids)
    data.storage = 'Bin'
    data.save()
    global status
    status['error']='Deleted Successfully'
    return redirect('/Home')

def bin(request):
    global status
    data=Customer.objects.get(username=status['username'])
    status['filedata']=Upload.objects.all().filter(username=status['username'],storage='Bin').order_by('-id')
    status['memory_status']=round(data.memory/data.total_memory*100,2)
    return render(request,'Bin.html',status)

def restore(request):
    ids = request.POST['documentid']
    data = Upload.objects.get(id=ids)
    data.storage = 'Memory'
    data.save()
    global status
    status['error']='Restored Successfully'
    return redirect('/Bin')

def deleteforever(request):
    global status
    data=Customer.objects.get(username=status['username'])
    ids = request.POST['id']
    data1 = Upload.objects.get(id=ids)
    data.memory = data.memory-data1.file.size
    data.save()
    data1.delete()
    status['error']='Deleted Forever'
    return redirect('/Bin')

def rename(request):
    newname = request.POST['newname']
    id = request.POST['id']
    data = Upload.objects.get(id=id)
    os.rename(data.file.path,'media/'+newname)
    data.file.name = newname
    data.file_name = newname
    data.save()
    status['error']='File Renamed Successfully'
    return redirect('/Home')

def profile(request):
    global status
    status['userdata']=Customer.objects.get(username=status['username'])
    return render(request,'Profile.html',status)

def updateprofile(request):
    global status
    status['userdata']=Customer.objects.get(username=status['username'])
    profile = request.FILES['pic']
    status['userdata'].delete()
    status['userdata'].profile = profile
    status['userdata'].save()
    status['error']='Profile pic updated'
    return redirect('/Profile')

def changepassword(request):
    global status
    status['userdata']=Customer.objects.get(username=status['username'])
    password = request.POST['pass']
    status['userdata'].password = password
    status['userdata'].save()
    global msg
    msg = 'Password Changed Successfully'
    return redirect('/Logout')

def updatedetails(request):
    global status
    status['userdata']=Customer.objects.get(username=status['username'])
    email = request.POST['email']
    mobile = request.POST['mobile']
    status['userdata'].email = email
    status['userdata'].mobile = mobile
    status['userdata'].save()
    status['error']='Contact Details Updated'
    return redirect('/Profile')

def about(request):
    return render(request,'About.html')
