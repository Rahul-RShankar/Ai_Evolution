# civilization/protocol.py

class Message:

    def __init__(self, sender, receiver, intent, content):

        self.sender = sender
        self.receiver = receiver
        self.intent = intent
        self.content = content

    def to_dict(self):
        return {
            "from": self.sender,
            "to": self.receiver,
            "intent": self.intent,
            "content": self.content
        }
