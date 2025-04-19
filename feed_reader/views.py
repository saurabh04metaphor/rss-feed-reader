from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm, FeedAddForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Feed, FeedItem

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Create 'home' route later
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

'''@login_required
def home(request):
    return render(request, 'home.html')  # Create this template later'''

@login_required
def home(request):
    feeds = Feed.objects.filter(user=request.user)
    form = FeedAddForm()
    if request.method == 'POST':
        form = FeedAddForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = request.user
            # Optionally, fetch feed title/description later
            feed.save()
            return redirect('home')
    return render(request, 'feed_reader/feed_list.html', {'feeds': feeds, 'form': form})

@login_required
def article_list(request):
    # Get all articles from feeds user subscribes to, order by published date
    items = FeedItem.objects.filter(feed__user=request.user).order_by('-published')
    return render(request, 'feed_reader/article_list.html', {'items': items})

@login_required
def article_detail(request, pk):
    item = get_object_or_404(FeedItem, pk=pk, feed__user=request.user)
    return render(request, 'feed_reader/article_detail.html', {'item': item})

@login_required
def toggle_read_status(request, pk):
    item = get_object_or_404(FeedItem, pk=pk, feed__user=request.user)
    item.read = not item.read
    item.save()
    return HttpResponseRedirect(reverse('article_detail', args=[pk]))
# Create your views here.
