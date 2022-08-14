from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class register_form_auth(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def save(self):
		new_user = super(register_form_auth, self).save(commit=False)
		new_user.email = self.cleaned_data['email']
		new_user.save()
		return new_user
