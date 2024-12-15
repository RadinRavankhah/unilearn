from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Subreddit, Post, Comment
from django.contrib.auth import authenticate


# User Signup Form
class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'preferences']

# User Login Form
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username or password.")
        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user

# Subreddit Creation Form
class SubredditForm(forms.ModelForm):
    class Meta:
        model = Subreddit
        fields = ['name', 'description']

# Post Creation Form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

# Comment Creation Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'preferences']
