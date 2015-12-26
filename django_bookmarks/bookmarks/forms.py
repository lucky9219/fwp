import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
class RegistrationForm(forms.Form):
	username=forms.CharField(label='username',max_length=200,widget=forms.TextInput(attrs={'size':26}))
	email=forms.EmailField(label='Email',widget=forms.TextInput(attrs={'size':30}))
	password1=forms.CharField(
		label='Password',
		widget=forms.PasswordInput(attrs={'size':26}),
	)
	password2=forms.CharField(
		label='Retype Password',
		widget=forms.PasswordInput(attrs={'size':20})
			)

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1=self.cleaned_data['password1']
			password2=self.cleaned_data['password2']
			if password1==password2:
				return password2
			raise forms.ValidationError('passwords do not match')

	def clean_username(self):
		username=self.cleaned_data['username']
		if not re.search(r'^\w+$',username):
			raise forms.ValidationError('Username can only contain alphanumeric character and the Underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username is already existed!')

	def clean_email(self):
		if 'email' in self.cleaned_data:
			email=self.cleaned_data['email']
		try:
			User.objects.get(email=email)
		except ObjectDoesNotExist:
			return email
		raise forms.ValidationError('email is already existed')

class BookmarkSaveForm(forms.Form):
	url=forms.URLField(
		label='URL',
		widget=forms.TextInput(attrs={'size':64},
			)
		)
	title=forms.CharField(
		label='TITLE',
		widget=forms.TextInput(attrs={'size':64})
		)
	tags=forms.CharField(
		label='TAGS',
		required=False,
		widget=forms.TextInput(attrs={'size':64})
		)
		
	share=forms.BooleanField(
		label='Share on main page',
		required=False
		)
	
class SearchForm(forms.Form):
	query=forms.CharField(
		label='Enter The Search Item',
		widget=forms.TextInput(attrs={'size':32})
		)
