from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room, Messages


@login_required
def chat_rooms(request):
    rooms = Room.objects.all()

    return render(request, 'chat/rooms.html', {'rooms': rooms})


@login_required
def chat_room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Messages.objects.filter(room=room)[0:25]
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})
