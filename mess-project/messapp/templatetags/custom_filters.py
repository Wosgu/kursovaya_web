# chat/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def is_image(file_url):
    return file_url.endswith(('.jpg', '.jpeg', '.png', '.gif'))

@register.filter
def is_video(file_url):
    return file_url.endswith('.mp4')

@register.filter
def is_audio(file_url):
    return file_url.endswith('.mp3')

@register.filter
def is_pdf(file_url):
    return file_url.endswith('.pdf')

@register.filter
def is_docx(file_url):
    return file_url.endswith('.docx')

@register.filter
def is_zip(file_url):
    return file_url.endswith('.zip')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')