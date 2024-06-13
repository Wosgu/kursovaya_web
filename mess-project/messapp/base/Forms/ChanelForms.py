from messapp.base.Models.ChannelModels import Channel, MessageChannel
from django import forms

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'avatar']

class MessageChannelForm(forms.ModelForm):
    class Meta:
        model = MessageChannel
        fields = ['content', 'attachment']

    def __init__(self, user, channel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.channel = channel