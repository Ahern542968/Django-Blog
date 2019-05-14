from django.shortcuts import render


def index(request):
    return render(request, 'blogs/blogs_detail.html')
