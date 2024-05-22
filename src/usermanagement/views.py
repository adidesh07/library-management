from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Account, AccountType
from .forms import UserRegistrationForm, AccountAuthenticationForm
from .utils import get_single_error_from_form
from decorators import capture_exception_logs


@capture_exception_logs
def register(request):
    if request.user.is_authenticated:
        return redirect("bookmanagement:home")

    context = {}
    if request.method == "POST":
        form_data = request.POST.dict()
        print(form_data)
        form = UserRegistrationForm(form_data)

        if not form.is_valid():
            context["error"] = get_single_error_from_form(form)
            return render(request, "usermanagement/register.html", context)

        user = form.save(commit=False)
        if form_data.get("type") == "librarian":
            user.type = AccountType.LIBRARIAN
        else:
            user.type = AccountType.END_USER
        user.save()

        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        acc = authenticate(email=email, password=raw_password)
        login(request, acc)
        return redirect("bookmanagement:home")

    return render(request, "usermanagement/register.html", context)


@capture_exception_logs
def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("bookmanagement:home")

    if request.method == "POST":
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.authenticated_user
            login(request, user)
            return redirect("bookmanagement:home")

        context["error"] = get_single_error_from_form(form)
    return render(request, "usermanagement/login.html", context)


@login_required(login_url="login")
@capture_exception_logs
def logout_view(request):
    logout(request)
    return redirect("login")
