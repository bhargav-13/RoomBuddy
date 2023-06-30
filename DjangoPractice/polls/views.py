from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def home(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )


    topic = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = { 'rooms' : rooms, 'topics' : topic, 'room_count' : room_count, 'room_messages' : room_messages }
    return render(request, 'polls/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        msg = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room': room, 'room_messages' : messages, 'participants':  participants}
    return render(request, 'polls/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    return render(request, 'polls/profile.html', {
        "user" : user,
        "rooms" : rooms,
        "room_messages" : room_messages,
        "topics" : topics,
    })

@login_required(login_url= '/login')
def Createroom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'polls/room_forn.html', context)

@login_required(login_url= '/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("<h1>You are not Allowed Here!!</h1>")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'polls/room_forn.html', context)

@login_required(login_url= '/login')
def DeleteRoom(request, pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse("<h1>Only user can delete this!!</h1>")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'polls/delete.html', {'obj' : room})

def LoginPage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, "User Doesn't Exist")

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is invalid')

    context = {'page' : page}
    return render(request, 'polls/login_register.html', context)

def logoutUser(request):

    logout(request)

    return redirect('home')

def RegisterPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An Error During Registration")

    return render(request, 'polls/login_register.html', {'form' : form})


@login_required(login_url= '/login')
def DeleteMsg(request, pk):
    message = Message.objects.get(id = pk)

    if request.user != message.user:
        return HttpResponse("<h1>Only user can delete this!!</h1>")

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'polls/delete.html', {'obj' : message})

