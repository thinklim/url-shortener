from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm


class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect("index")

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            return redirect("index")
        else:
            return redirect("login")


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)

        return redirect("login")


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class SignUpView(View):
    template_name = "sign_up.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        form = CustomUserCreationForm(
            data={"email": email, "password1": password1, "password2": password2}
        )

        if form.is_valid():
            form.save()
            messages.success(request, "회원 가입을 축하합니다.")

            return redirect("login")

        return redirect("sign_up")
