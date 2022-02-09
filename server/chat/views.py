from django.shortcuts import redirect, render
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseForbidden

from .services import (
    is_authenticated,
    authenticate,
    get_member_id,
    messages_generator
)
from .chat import Chat

def index(request):
    if not is_authenticated(request):
        return render(request, "lobby.html")
    return render(request, "room.html")


def get_messages(request):
    if not is_authenticated(request):
        return HttpResponseForbidden()

    return StreamingHttpResponse(
        messages_generator(),
        content_type='text/event-stream'
    )

def post_message(request):
    if not is_authenticated(request):
        return redirect("index")

    message = request.POST.get("message", "-- empty --")
    Chat().channel.add_message(
        get_member_id(request),
        message
    )
    return HttpResponse()

def join_room(request):
    username = request.POST.get("username", "Incognito")
    member = Chat().channel.add_member(username)
    response = redirect("index")
    authenticate(response, member)
    return response