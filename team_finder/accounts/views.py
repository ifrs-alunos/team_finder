from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from tinder.forms import get_skill_level_formset
from .forms import ProfileCreationForm, LoginForm, CustomUserCreationForm, ProfileEditForm, \
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

            return redirect('edit_profile')

    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileCreationForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.first_name:
            return super(MyLoginView, self).get_success_url()
        return reverse('edit_profile')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile)
        skill_formset = get_skill_level_formset()(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid() and skill_formset.is_valid():
            user_form.save()
            profile_form.save()
            skill_formset.save()
            return redirect('tinder:main_menu')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        skill_formset = get_skill_level_formset()(instance=request.user.profile)
    
    skill_names = {skill.id: skill.name for skill in request.user.profile.get_skills()}

    context = {
        'skill_names': skill_names,
        'profile_form': profile_form,
        'user_form': user_form,
        'skill_formset': skill_formset
    }
    return render(request, 'registration/update_profile.html', context)
