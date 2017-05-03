from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)


User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self,*args,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		# user = authenticate(username=username,password=password)
		if username and password:
			user_qs = User.objects.filter(username=username)
			if user_qs.count() == 1:
				user = user_qs.first()
			else:
				raise forms.ValidationError("This user doesn't Exist !")

			if not user.check_password(password):
				raise forms.ValidationError("Password is incorrect")

			if not user.is_active:
				raise forms.ValidationError("this user is not active")
			return super(UserLoginForm,self).clean(*args,**kwargs)


class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField(label='Email')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]

	def clean(self,*args,**kwargs):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError('Email dont match')
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError('This email already exists')
		return super(UserRegistrationForm,self).clean(*args,**kwargs)

	# def clean_email2(self):
	# 	email = self.cleaned_data.get('email')
	# 	email2 = self.cleaned_data.get('email2')
	# 	if email != email2:
	# 		raise forms.ValidationError('Email dont match')
	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError('This email already exists')
	# 	return email  # THis is an alterenative way to do email validation














