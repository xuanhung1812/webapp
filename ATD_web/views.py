from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, get_user_model, logout
from django.contrib.auth.models import User
from django.contrib.auth import login as login1, logout as logout1
from . models import Don_Nghi_Phep
import pandas as pd
# Create your views here.


def Login(request):
	if request.user.is_staff or request.user.is_superuser:

		return HttpResponseRedirect("dash")

	user = request.POST.get("user")
	password = request.POST.get("password")
	print(user, password)

	user = authenticate(request, username=user, password=password)
	if user:
		if user.is_active:
			login1(request, user)
			return HttpResponseRedirect('dash')
	return render(request, 'login.html')


def Home1(request):
	if request.user.is_staff or request.user.is_superuser:
		Username = request.user.username
		return render(request, 'home1.html', {'username': Username})
	else:
		return HttpResponseRedirect('login')


def Forms(request):
	Username = request.user.username
	name_hs = request.POST.get("name_hs")
	id_hs = request.POST.get("id_hs")
	name_ph = request.POST.get("name_ph")
	reason = request.POST.get("reason")
	tg_nghi_from = request.POST.get("tg_nghi_from")
	tg_nghi_to = request.POST.get("tg_nghi_to")
	print(name_hs, id_hs, name_ph, reason)
	try:
		don_nghi_phep = Don_Nghi_Phep.objects.create(name_hs=name_hs, id_hs=id_hs, name_ph=name_ph,
	reason=reason, tg_nghi=str(tg_nghi_from)+' to '+str(tg_nghi_to))
	except:
		pass
	return render(request, 'forms.html', {'username': Username})


def Forms_gv(request):
	Username = request.user.username
	don_nghi_phep = Don_Nghi_Phep.objects.all()
	tim_hs = request.GET.get("tim_hs")
	if tim_hs:
		don_nghi_phep = don_nghi_phep.filter(name_hs=tim_hs)
	return render(request, 'forms_gv.html',{'username':Username, 'don_nghi_phep':don_nghi_phep})

def Charts(request):
	Username = request.user.username
	return render(request, 'chart.html',{'username':Username})

def File_csv(request):
	Username = request.user.username
	# l = []
	file_atd = pd.read_csv('C:/Users/LENOVO/Desktop/Attendance/pyfile/myData.csv',encoding = 'utf-8')
	for i in file_atd['stt']:
		stt = file_atd.iloc[i-1]
		# l.append(stt)
	return render(request, 'file_csv.html',{'username':Username,  'stt':stt})

def Don_view(request,slug = None):
	Username = request.user.username
	intance = Don_Nghi_Phep.objects.get(slug = slug)
	print(intance)
	context = {

	'name_hs':intance.name_hs,
	'id_hs':intance.id_hs,
	'name_ph':intance.name_ph,
	'reason': intance.reason,
	'slug': slug,
	'username':Username

	}
	return render(request, 'doc.html',context)
def Logout(request):
	logout1(request)
	return HttpResponseRedirect('login')