from .chat import Chat
import time
import json

def is_authenticated(request):
    return Chat().channel.is_chat_member(
        get_member_id(request)
    )

def authenticate(response, member):
    response.set_cookie("uuid", member.id)

def get_member_id(request):
    return request.COOKIES.get("uuid", "")

def get_sse_message(data: dict):
    return "data: %s\nretry:1000\n\n" % json.dumps(data)

def messages_generator():
    chat = Chat()
    prev_state = None

    while(True):
        if chat.channel.state != prev_state:
            prev_state = chat.channel.state
            messages = chat.channel.get_messages()
            yield get_sse_message(messages)
        time.sleep(.1)
