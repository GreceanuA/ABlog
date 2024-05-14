from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from theblog.models import Profile
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        profile = (
            'bio', 'profile_pic', 'website_url', 'facebook_url', 'linkedin_url', 'github_url', 'instagram_url',
            'twitter_url', 'tiktok_url', 'snapchat_url')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            # 'profile_pic': forms.TextInput(attrs={'class': 'form-control'}),
            'website_url': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
            'github_url': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
            'tiktok_url': forms.TextInput(attrs={'class': 'form-control'}),
            'snapchat_url': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    # is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    # is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    # date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password',)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'linkedin_url', 'github_url', 'twitter_url',
                  'instagram_url']

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        # Aplicarea claselor Bootstrap
        self.fields['bio'].widget.attrs['class'] = 'form-control'
        self.fields['profile_pic'].widget.attrs['class'] = 'form-control-file'
        self.fields['website_url'].widget.attrs['class'] = 'form-control'
        self.fields['facebook_url'].widget.attrs['class'] = 'form-control'
        self.fields['linkedin_url'].widget.attrs['class'] = 'form-control'
        self.fields['github_url'].widget.attrs['class'] = 'form-control'
        self.fields['twitter_url'].widget.attrs['class'] = 'form-control'
        self.fields['instagram_url'].widget.attrs['class'] = 'form-control'


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'TYPE': 'password'}))
    new_password1 = forms.CharField(label='New Password',max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'TYPE': 'password'}))
    new_password2 = forms.CharField(label='Retype Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'TYPE': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class MyPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        """
        Verifică dacă adresa de e-mail introdusă aparține unui utilizator activ în sistem.
        """
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('There is no active account associated with this email address.')
        return email

    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html', use_https=False,
             token_generator=default_token_generator, from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Suprascrie metoda save pentru a trimite e-mailul de resetare a parolei către adresa specificată.
        """

        return super().save(domain_override, subject_template_name, email_template_name, use_https, token_generator,
                            from_email, request, html_email_template_name, extra_email_context)
