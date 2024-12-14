from django.shortcuts import render
from .forms import UserRegister
from .models import *
from django.core.paginator import Paginator


# Create your views here.
def platform(request):
    return render(request, 'platform.html')


def games(request):
    games = Game.objects.all()
    context = {
        "games": games
    }
    return render(request, 'games.html', context)


def cart(request):
    return render(request, 'cart.html')


info = dict()


def check_data_func( username, password, repeat_password, age):
    is_user = Buyer.objects.filter(name=username)
    if password != repeat_password:
        return {'error': 'Пароли не совпадают'}
    elif age < 18:
        return {'error': 'Вы должны быть старше 18'}
    elif is_user:
        return {'error': 'Пользователь уже существует'}
    if password == repeat_password and age >= 18 and not is_user:
        Buyer.objects.create(name=username, balance=1000, age=age)
        return {'success': f'Приветствуем, {username}!'}


def sign_up_by_django(request):
    if request.method == "POST":
        form = UserRegister(request.POST)
        info.clear()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = int(form.cleaned_data['age'])

            info.update({'form': form})
            info.update(check_data_func(username, password, repeat_password, age))

            return render(request, 'registration_page.html', info)

    else:
        return render(request, 'registration_page.html', info)


def sign_up_by_html(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))
        info.clear()
        info.update({'username': username, 'password': password, 'repeat_password': repeat_password,
                     'age': age})

        info.update(check_data_func(username, password, repeat_password, age))

        return render(request, 'registration_page.html', info)

    else:
        return render(request, 'registration_page.html', info)


def news(request):
    news = News.objects.all().order_by('-date')
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'news': page_obj})
