from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from accounts.models import Profile
from .forms import GroupForm
from .models.groups import Group
from .models.skills import Skill
from django.contrib import messages


def my_menu(request):
	search_term = request.GET.get('search')
	user_profile = request.user.profile

	leading = user_profile.leading.all()
	member = user_profile.group_list.all()

	if search_term:
		leading = leading.filter(name__contains=search_term)
		member = member.filter(name__contains=search_term)

	return render(request, 'tinder/main_menu.html', {'leading': leading, 'member': member})


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


def search_group(request, name):
	results = Group.objects.filter(name__contains=name).exclude(private = True)
	context = {'results':results}
	return render(request, 'core/home.html' , context)


def search_person(request, parameter, term):	
	results = Profile.objects.filter(**{'parameter': term})
	context = {'results': results}
	return render(request, 'core/home.html', context)


#não abrir a jaula!
def match_withlist(request):
	group_id = request.GET.get('group_id')
	skills_list = request.GET.get('skills').split(',')
	skills_dict = {int(data.split(":")[0]): int(data.split(":")[1]) for data in skills_list}

	necessary_skills = Skill.objects.filter(pk__in=skills_dict)
	really_necessary_skills = {}
	profile_skillslevels = request.user.profile.skilllevel_set
	profile_skills = request.user.profile.skills.all()

	for skill in necessary_skills:
		if skill in profile_skills:
			if profile_skillslevels.get(skill=skill) < necessary_skills[skill]:
				really_necessary_skills[skill] = necessary_skills[skill]

	group = Group.objects.get(id=group_id)
	members = list(group.members.all())
	for member in members:
		member.points = 0

	for member in members:
		for skilllevel in member.skilllevel_set.all():
			if (skilllevel.skill.id in really_necessary_skills) and skilllevel.level >= really_necessary_skills[skilllevel.skill.id]:
				member.points += 1

	best_groups = sorted(members, key=lambda x: x.points)

	return render(request, 'tinder/grupos.html', {'best_groups': best_groups})


def join_group(request, group_id, userpass):
	#verificando se o 
	message = 'A operação não pode ser concluída. Confira os dados informados'
	group = get_object_or_404(Group, pk=group_id)
	if userpass == group.password:
		group.members.add(request.user.profile)


def rmv_fromgroup(request, group_id, userpass, member):
	#tirar algm de um grupo ou a si mesmo
	message = ''
	group = get_object_or_404(Group, pk=group_id)
	if (userpass == group.password) and (member in group.members):
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
	return render(request, 'tinder/activity.html', {'group': group})