from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed

import json

from accounts.models import Profile
from .forms import GroupForm, PasswordForm
from .models import Group, Skill, SkillLevel



def my_menu(request):
    search_term = request.GET.get('search')
    user_profile = request.user.profile

    leading = user_profile.leading.all()
    member = user_profile.group_list.all()

    if search_term:
        leading = leading.filter(name__contains=search_term)
        member = member.filter(name__contains=search_term)

    return render(request, 'tinder/main_menu.html', {'leading': leading, 'member': member})


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.leader = request.user.profile
            group.save()
            messages.success(request, "GRUPO SALVO COM SUCESSO")
            return redirect('tinder:main_menu')
    else:
        form = GroupForm(initial={'leader': request.user.profile})

    print('erro', form.errors)
    context = {
        'form': form,
    }

    return render(request, 'tinder/create_groups.html', context)


@login_required
def search_group(request):
    search_term = request.GET.get('search')
    groups = Group.objects.all().exclude(private=True)

    if search_term:
        groups = groups.filter(name__contains=search_term)

    context = {'groups': groups}
    return render(request, 'tinder/search_group.html', context)


@login_required
def search_person(request, parameter, term):
    results = Profile.objects.filter(**{str(parameter): term})
    context = {'results': results}
    return render(request, 'core/home.html', context)


# não abrir a jaula!
@login_required  # precisa proteger p/ usuario não acessar grupos que não faz parte
def match_withlist(request, group_id):
    skills = json.loads(request.GET.get('skills'))
    skills = {int(k): int(v) for k, v in skills.items()}

    profile_skills_levels = request.user.profile.skilllevel_set.all()

    for skill_level in profile_skills_levels:
        skill = skill_level.skill
        level = skill_level.level
        if skill.id in skills and level >= skills[skill.id]:
            del skills[skill.id]

    group = Group.objects.get(id=group_id)
    members = list(group.members.exclude(id=request.user.profile.id))
    for member in members:
        member.points = 0

    for member in members:
        for skill_level in member.skilllevel_set.all():
            skill = skill_level.skill
            level = skill_level.level
            if (skill.id in skills and level >= skills[skill.id]):
                member.points += level - skills[skill.id] + 10

    best_groups = sorted(members, key=lambda x: x.points, reverse=True)

    return render(request, 'tinder/group_matches.html', {'best_groups': best_groups, 'group': group})


@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if group.leader == request.user.profile:
        if request.method == 'POST':
            form = GroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                return redirect('tinder:main_menu')
        else:
            form = GroupForm(instance=group)
    else:
        return HttpResponseNotAllowed()

    return render(request, 'tinder/create_groups.html', {'form': form})


""" USERS relations inside groups """
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    access = False
    if request.method == 'POST':
        if group.private:
            form = PasswordForm()
            if form.is_valid():
                userpass = form.cleaned_data['password']
                if userpass != group.password:
                    access = True
        else:
            access = True

        if access:
            group.members.add(request.user.profile)
            messages.success(request, 'Bem-vindo ao grupo')
            return redirect('tinder:detail_group', pk=group_id)
        else:
            messages.error(request, 'Informe a senha correta para acessar o grupo')
    # Form is only used if the group is private (verified in template)
    return render(request, 'tinder/join_confirmation.html', {'form': PasswordForm(), 'group': group})
@login_required
def rmv_fromgroup(request, group_id, userpass, member):
    # tirar algm de um grupo ou a si mesmo
    message = ''
    group = get_object_or_404(Group, pk=group_id)
    if (user.profile == group.leader) and (userpass == group.passwd) and (member in group.members):
        group.members.delete(member)
        message = 'REMOÇÃO BEM-SUCEDIDA.'
    else:
        message = 'IMPOSSÍVEL REALIZAR A OPERAÇÃO SOLICITADA'

    context = {'message': message}
    return render(request, 'core/home.html', context)


class DetailGroup(DetailView):
    model = Group


def activity_group_match(request, pk):
    group = get_object_or_404(Group, id=pk)
    skills = Skill.objects.all()
    levels = SkillLevel.SKLEVEL
    return render(request, 'tinder/activity.html', {'group': group, 'skills': skills, 'levels': levels})


class DeleteGroup(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('tinder:main_menu')
    success_message = 'Grupo deletado!'

    def test_func(self):
        if self.get_object().leader != self.request.user.profile:
            return False
        return True

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super(DeleteGroup, self).delete(request, *args, **kwargs)
