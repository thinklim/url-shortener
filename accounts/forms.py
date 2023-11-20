from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


PASSWORD_MIN_LENGTH = 8


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmtion", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
        ]

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < PASSWORD_MIN_LENGTH:
            raise ValidationError(f"비밀번호는 {PASSWORD_MIN_LENGTH}글자 이상입니다.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 다릅니다")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["password", "is_active", "is_admin"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
