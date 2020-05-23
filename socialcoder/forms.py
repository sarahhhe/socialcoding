from django import forms
from django.contrib.auth.models import User
from .models import Post, Response, Category
from ckeditor.widgets import CKEditorWidget

class ResponseForm(forms.ModelForm):
    code = forms.CharField(widget=CKEditorWidget(config_name='special'), label='')

    class Meta:
        model = Response
        fields = ['code']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','image', 'description']

class PostForm(forms.ModelForm):
    code = forms.CharField(widget=CKEditorWidget(config_name='special'), label=' ')

    class Meta:
        model = Post
        fields = ['category','title','code']

class UserForm(forms.ModelForm):
    confirm_pw = forms.CharField(widget=forms.PasswordInput(), label='Re-enter password')
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_pw = cleaned_data.get("confirm_pw")

        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError("Email address already in use, please try a different one.")
        if password != confirm_pw:
            raise forms.ValidationError("Passwords do not match, try again.")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
