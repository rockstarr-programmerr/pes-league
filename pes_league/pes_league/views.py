from django.shortcuts import render, redirect


def index(request):
    return render(request, 'base/index.html')


def season_list(request):
    """
    Khi vào trang "/" thì tự động redirect về trang danh sách mùa giải
    """
    return redirect('season:season_list')
