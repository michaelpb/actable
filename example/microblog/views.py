from django.shortcuts import render, redirect

from microblog.models import MicroPost, Author, Follow
from microblog.forms import MicroPostForm, AuthorForm, FollowForm

from actable.helpers import EventDictPaginator

def index(request):
    return render(request, 'index.html', {
        'author_form': AuthorForm(),
        'follow_form': FollowForm(),
        'micro_post_form': MicroPostForm(),
        'authors': Author.objects.all(),
    })

def new_author(request):
    AuthorForm(request.POST).save()
    return redirect('/')

def new_post(request):
    inst = MicroPostForm(request.POST).save()
    return redirect('/posts/%s/' % inst.author.name)

def new_follow(request):
    FollowForm(request.POST).save()
    return redirect('/')

def view_posts(request, username):
    author = Author.objects.get(name=username)
    if request.method == 'POST':
        AuthorForm(request.POST, instance=author).save()
        return redirect(author.get_absolute_url())
    return render(request, 'posts.html', {
        'activities': EventDictPaginator(author, 100).page(1),
        'form': AuthorForm(instance=author),
        'posts': MicroPost.objects.filter(author__name=username),
        'micro_post_form': MicroPostForm(initial={'author': author}),
        'username': username,
    })
