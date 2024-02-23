from django import forms
from .models import Admin

# class AdminForm(forms.ModelForm):
#     class Meta:
#         model = Admin
#         fields = ['a_username', 'a_password', 'a_img']
#         widgets = {
#             'a_password': forms.PasswordInput(),
#         }
#         labels = {
#             'a_username': 'Username',
#             'a_password': 'Password',
#             'a_img': 'Profile Image',
#         }

#     def __init__(self, *args, **kwargs):
#         super(AdminForm, self).__init__(*args, **kwargs)
#         self.fields['a_username'].required = True
#         self.fields['a_password'].required = True

# # class LoginForm(forms.Form):
# #     username = forms.CharField(max_length=20)
# #     password = forms.CharField(widget=forms.PasswordInput)

# class RateForm(forms.ModelForm):
#     class Meta:
#         model = Rate
#         fields = ['rtid', 'r_rate', 'r_cdate', 'r_udate']
class AdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'password', 'a_img']
        widgets = {
            'password': forms.PasswordInput(),  # Render password input as password field
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Encrypt the password
        if commit:
            user.save()
        return user

		
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')