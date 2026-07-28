from django.shortcuts import render, redirect
from .models import Room, Message

# Create your views here.
def home(request):
    if request.method == "POST":
        username= request.POST['username']
        request.session['username'] = username
        room_name= request.POST['room_name']
        room, created = Room.objects.get_or_create(room_name=room_name)
        return redirect('room', room_name=room_name)
    return render(request, 'home.html')
def room(request, room_name):
    room = Room.objects.get(room_name=room_name)

    if request.method == "POST":
        sender_name = request.session['username']
        message_detail = request.POST['message_detail']

        message = Message.objects.create(
            sender_name = sender_name,
            message_detail = message_detail,
            room = room
        )

        return redirect('room', room_name=room_name)
    
    messages = Message.objects.filter(room=room).order_by('created_time')
    return render(request, 'room.html', {
        'room': room,
        'messages' : messages,
        'username' : request.session['username']
        })