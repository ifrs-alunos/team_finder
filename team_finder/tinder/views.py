from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupForm
from .models.groups import Group
from .models.skill_levels import SkillLevel
from .models.skills import Skill

#erro: manyrelatedmanager is not iterable na linha 12
def my_menu(request):
	pass
"""	
	profile = request.user.profile
	groups_i_rule, groups_i_belong = [], []

	for group in profile.group_list:
		if group.leader == profile:
			groups_i_rule.append(group)
		else:
			groups_i_belong.append(group)

	context = {'profile':profile, 'leader':groups_i_rule, 'member':groups_i_belong}
	return render(request, 'tinder/grupos.html', context)
"""
def create_group(request):
	message = ''
	if request.method == 'POST':
		form = GroupForm(request.POST)
		if form.is_valid():
			form.save()
			message = "GRUPO SALVO COM SUCESSO"
	else:
		form = GroupForm()

	context = {
		'form': form,
		'message':message,
		}

	return render(request, 'core/home.html', context)

def search_my_groups(request, name):
	profile = request.user.profile
	mygroups = profile.group_list
	results = mygroups.filter(name__contains=name)
	context = {'results':results}
	return render(requets, 'core/home.html', context)

def search_group(request, name):
	results = Group.objects.filter(name__contains=name).exclude(private = True)
	context = {'results':results}
	return render(request, 'core/home.html' , context)

def search_person(request, parameter, term):	
	results = Profile.objects.filter(**{'parameter': term})
	context = {'results':results}
	return redner(request, 'core/home.html', context)

def match_ingroup(request, group, skill, level):
	group_members = Profile.objects.filter(group_list=group)
	results = group_members.filter(skilllevel_set__skill=skill, skilllevel_set__level = level)
	context = {'results':results}
	return redner(request, 'core/home.html', context)

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
	if userpass == group.passwd:
		group.members.add(request.user.profile)

def rmv_fromgroup(request, group_id, userpass, member):
	#tirar algm de um grupo ou a si mesmo
	message = ''
	group = get_object_or_404(Group, pk=group_id)
	if (userpass == group.passwd) and (member in group.members):
		group.members.delete(member)
		message = 'REMOÇÃO BEM-SUCEDIDA.'
	else:
		message = 'IMPOSSÍVEL REALIZAR A OPERAÇÃO SOLICITADA'

	context = {'message':message}
	return render(request, 'core/home.html', context)

