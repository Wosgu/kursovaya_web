from django.contrib.auth.models import User
from messapp.base.Models.GroupChatModels import MessageGroup, GroupChat
from django import forms
from messapp.base.Models.managers import get_friends

class MessageGroupForm(forms.ModelForm):
    class Meta:
        model = MessageGroup
        fields = ['content', 'group_chat', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'label': ''}),
            'group_chat': forms.Select(attrs={'class': 'form-control', 'style': 'display: none;', 'label': ''}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'content': '',
            'group_chat': '',
            'attachment': '',
        }

    def __init__(self, user, group_chat, *args, **kwargs):
        super(MessageGroupForm, self).__init__(*args, **kwargs)
        self.fields['group_chat'].queryset = GroupChat.objects.filter(members=user)
        self.user = user
        self.initial['group_chat'] = group_chat.pk

    def save(self, commit=True):
        instance = super(MessageGroupForm, self).save(commit=False)
        instance.sender = self.user
        if commit:
            instance.save()
        return instance

class GroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ['name', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, friends, *args, **kwargs):
        super(GroupChatForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = friends.exclude(id=user.id)