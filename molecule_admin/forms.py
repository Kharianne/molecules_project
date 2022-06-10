from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, ModelForm
from molecule_admin.models import Profile

class RegisterUserForm(UserCreationForm):
    username = CharField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class UserForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'institution')
