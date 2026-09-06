from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'base/index.html')


def season_list(request):
    """
    Khi vào trang "/" thì tự động redirect về trang danh sách mùa giải
    """
    return redirect('season:season_list')


def healthz(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    return HttpResponse('ok', content_type='text/plain')
