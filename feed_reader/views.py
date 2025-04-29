from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm, FeedAddForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Feed, FeedItem
import subprocess

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed_list')  # Create 'home' route later
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

'''@login_required
def home(request):
    return render(request, 'home.html')  # Create this template later'''

@login_required
def home(request):
    """
    Handle the home view for the RSS reader application.
    This view displays a list of feeds associated with the currently logged-in user
    and provides a form to add new feeds. If a POST request is made with valid form data,
    a new feed is created and associated with the user. After saving the feed, the 
    `update_feed_items` function is called to fetch the latest feed updates for the new feed.
    """
    feeds = Feed.objects.filter(user=request.user)
    form = FeedAddForm()
    if request.method == 'POST':
        form = FeedAddForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = request.user
            feed.save()

            # Fetch and parse the newly added feed
            from .utils import update_feed_items
            update_feed_items(feed)

            return redirect('feed_list')
    return render(request, 'feed_reader/feed_list.html', {'feeds': feeds, 'form': form})

@login_required
def article_list(request, id=None):
    """
    View function to display a list of articles.
    If an `id` is provided, the function retrieves all articles from the feed
    corresponding to the given `id`. Otherwise, it retrieves articles from all
    feeds the currently authenticated user is subscribed to. The articles are
    ordered by their published date in descending order.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about
            the request and the currently authenticated user.
        id (int, optional): The primary key of the feed to filter articles by.
            Defaults to None.
    Returns:
        HttpResponse: A rendered HTML page displaying the list of articles.
    """

    # Get all articles from feeds user subscribes to, order by published date
    if id:
        feed = get_object_or_404(Feed, pk=id)
        items = FeedItem.objects.filter(feed=feed).order_by('-published')
    else:
        items = FeedItem.objects.filter(feed__user=request.user).order_by('-published')

    return render(request, 'feed_reader/article_list.html', {'items': items})
    '''items = FeedItem.objects.filter(feed__user=request.user).order_by('-published')
    return render(request, 'feed_reader/article_list.html', {'items': items})'''

@login_required
def article_detail(request, pk):
    """
    Handles the display of a specific article's details.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        pk (int): The primary key of the FeedItem to retrieve.
    Returns:
        HttpResponse: Renders the 'feed_reader/article_detail.html' template with the specified FeedItem.
    Raises:
        Http404: If the FeedItem with the given primary key does not exist or does not belong to the current user.
    """

    item = get_object_or_404(FeedItem, pk=pk, feed__user=request.user)
    return render(request, 'feed_reader/article_detail.html', {'item': item})

@login_required
def toggle_read_status(request, pk):
    item = get_object_or_404(FeedItem, pk=pk, feed__user=request.user)
    item.read = not item.read
    item.save()
    return HttpResponseRedirect(reverse('article_detail', args=[pk]))

@login_required
def unsubscribe_feed(request, feed_id):
    """
    Handles unsubscribing from a feed.
    Requires POST method and user authentication.
    Only allows removal if the feed belongs to the current user.
    """
    feed = get_object_or_404(Feed, pk=feed_id, user=request.user)
    
    if request.method == 'POST':
        feed.delete()
        messages.success(request, f'Successfully unsubscribed from {feed.title or feed.url}')
        return redirect('feed_list')
    
    return HttpResponseRedirect(reverse('feed_list'))
# Create your views here.
