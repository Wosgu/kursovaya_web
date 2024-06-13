from messapp.base.Models.UserModels import UserProfile
from django import forms
from mess.settings import DEFAULT_BACKGROUNDIMAGE, DEFAULT_AVATAR_URL

class ProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(label='Avatar', required=False)

    class Meta:
        model = UserProfile
        fields = ['avatar', 'background_image','description']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:  # Если фото удалено
            return DEFAULT_AVATAR_URL  # Возвращаем путь к дефолтному фото
        return avatar
    
    def clean_background_image(self):
        background_image = self.cleaned_data.get('background_image')
        if not background_image:  # Если фото удалено
            return DEFAULT_BACKGROUNDIMAGE  # Возвращаем путь к дефолтному фото
        return background_image