from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .forms import ProfileCreationForm, LoginForm, AvatarChangeForm, CustomUserCreationForm, ProfileEditForm, \
    UserEditForm


def register_account(request):
    if request.user.is_authenticated:
        return render(request, 'registration/sucess_register.html')

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileCreationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.owner = user
            profile.save()

            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")

            return redirect('review')

    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileCreationForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm


class MyLogoutView(LogoutView):
    pass


@login_required
def review_account(request):
    return render(request, 'registration/review.html')


def edit_profile(request):
    if request.method == 'POST':
        pass
    else:
        user_form = UserEditForm()
        profile_form = ProfileEditForm()

    return render(request, 'registration/update_profile.html', {'profile_form': profile_form, 'user_form': user_form})


def change_avatar(request, current_view):
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile.avatar = form.cleaned_data['avatar']
            request.user.profile.save()
            messages.success(request, 'Atividade')
    return redirect(current_view)