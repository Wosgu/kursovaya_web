from django.contrib.auth.models import User
from messapp.base.Models.PersonalChatModels import Message
from django import forms

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'receiver', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'width: 70%;'}),
            'receiver': forms.Select(attrs={'class': 'form-control', 'style': 'display: none;', 'label': ''}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'content': '',
            'receiver': '',
            'attachment': '',
        }

    def __init__(self, sender, receiver=None, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.exclude(id=sender.id)
        if receiver:
            self.fields['receiver'].initial = receiver.id
            self.receiver = receiver  # Добавьте эту строку
        self.sender = sender

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.sender = self.sender
        if commit:
            instance.save()
        return instance
    
