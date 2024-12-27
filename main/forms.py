from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Subreddit, Post, Comment
from django.contrib.auth import authenticate
from .models import CustomUser  # Import your custom user model



# User Signup Form
class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-field',
                'placeholder': 'Email',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Confirm Password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email








# class SignupForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'input-field',
#                 'placeholder': 'Username',
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'input-field',
#                 'placeholder': 'Email',
#             }),
#             'password1': forms.PasswordInput(attrs={
#                 'class': 'input-field',
#                 'placeholder': 'Password',
#             }),
#             'password2': forms.PasswordInput(attrs={
#                 'class': 'input-field',
#                 'placeholder': 'Confirm Password',
#             }),
#         }

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if CustomUser.objects.filter(email=email).exists():
#             raise forms.ValidationError("This email is already in use.")
#         return email





# class SignupForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2', 'bio', 'preferences']

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
        widgets = {
            'title': forms.TextInput(attrs={'class': 'titleOfPost', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'contentOfPost', 'placeholder': 'Enter post content'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''  # Remove label

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
