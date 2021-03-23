from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


def login(request):

	if request.method == 'POST':
		try:
			m = User.objects.get(username=request.POST['username'])
			request.session['user_id'] = m.id
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					return HttpResponseRedirect('/')
				else:
					status = True
					info = "Обратитесь к администратору! Ваш логин не активен."
					return render(request, "login/start-page.html", {"info": info, "status": status})
		except User.DoesNotExist:
			status = True
			info = "Обратитесь к администратору! Вы не имеете доступа к приложению."
			return render(request, "login/start-page.html", {"info": info, "status": status})

	return render(request, "login/start-page.html")


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/login')

