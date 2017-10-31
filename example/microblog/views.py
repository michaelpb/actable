from django.shortcuts import render, redirect

from microblog.models import MicroPost

def view_posts(request, username):
    return render(request, 'posts.html', {
        'posts': MicroPost.objects.filter(user__username=username),
        'username': username,
    })


def make_post(request, username):
    MicroPost.objects.create(
        body=request.POST.get('body'),
        title=request.POST.get('title'),
        user=request.user,
    )
    return redirect('/')

