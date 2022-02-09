import datetime

from django.utils.crypto import get_random_string

CHAT_BUFFER_SIZE = 10


class Member:
    def __init__(self, username):
        self.id = get_random_string(length=32)
        self.username = username


class Message:

    def __init__(self, author, message):
        self.id = get_random_string(length=32)
        self.author = author
        self.message = message
        self.created = datetime.datetime.now()

    def as_dict(self):
        return {
            "username": self.author.username,
            "message": self.message
        }


class Channel:

    def __init__(self):
        self.id = get_random_string(length=32)
        self.history = []
        self.members = []
        self.admin = self.add_member("ADMIN")
        self.add_message(self.admin, "ADMIN STARTED SESSION")

    def __str__(self):
        return f"Chat channel: {self.id}"

    def update_state(self):
        self.state = get_random_string(length=32)

    def add_message(self, sender, message):
        if isinstance(sender, Member):
            member = sender
        else:
            member = self.__get_member_by_uuid(sender)

        if not member:
            return

        self.history = [
            *self.history[-(CHAT_BUFFER_SIZE-1):],
            Message(member, message)
        ]

        self.update_state()

    def get_messages(self):
        messages = map(lambda message: message.as_dict(), self.history)
        return list(messages)

    def add_member(self, username):
        member = Member(username)
        self.members.append(member)
        return member

    def is_chat_member(self, uuid):
        return self.__get_member_by_uuid(uuid) is not None

    def __get_member_by_uuid(self, uuid):
        filter_fn = lambda member: member.id == uuid
        matched = list(filter(filter_fn, self.members))
        return matched[0] if matched else None


class Chat:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'channel'):
            cls.channel = Channel()
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        print("Started with channel", self.channel.id)
