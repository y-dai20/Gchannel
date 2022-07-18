from dataclasses import field
from django import forms
from django.contrib.auth import get_user_model
from base.models import Post, ReplyPost, ReplyReply
from base.models.room_models import Room
 
 
class UserCreationForm(forms.ModelForm):
    password = forms.CharField()
 
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', )
 
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'text', 'img')

class ReplyPostForm(forms.ModelForm):
    
    class Meta:
        model = ReplyPost
        fields = ('text','type', 'url', 'img')

class ReplyReplyForm(forms.ModelForm):
    
    class Meta:
        model = ReplyReply
        fields = ('text',)

class CreateRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('title', 'subtitle', 'img')