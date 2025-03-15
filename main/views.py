from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Subreddit, Post, Comment
from .forms import SignupForm, LoginForm, SubredditForm, PostForm, CommentForm

# Home Page
from django.db.models import Count

def home(request):
    total_users = CustomUser.objects.count()
    if request.user.is_authenticated:
        # Subreddits the user follows, sorted by follower count
        followed_subreddits = request.user.followed_subreddits.annotate(follower_count=Count('followers')).order_by('-follower_count')

        # Fetch 5 most recent posts for each followed subreddit
        subreddit_posts = [
            {
                'subreddit': subreddit,
                'posts': subreddit.posts.order_by('-created_at')[:5]
            }
            for subreddit in followed_subreddits
        ]
    else:
        # Top 10 subreddits sorted by follower count
        top_subreddits = Subreddit.objects.annotate(follower_count=Count('followers')).order_by('-follower_count')[:10]

        # Fetch 5 most recent posts for each top subreddit
        subreddit_posts = [
            {
                'subreddit': subreddit,
                'posts': subreddit.posts.order_by('-created_at')[:5]
            }
            for subreddit in top_subreddits
        ]

    return render(request, 'home.html', {'subreddit_posts': subreddit_posts, "total_users":total_users})


# User Management
def signup(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'  # Handle both GET and POST
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect(next_url)  # Redirect to the URL in 'next' or 'home'
    else:
        form = SignupForm()
    return render(request, 'templates/signup.html', {'form': form})



def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    # next_url = request.GET.get('next') or request.POST.get('next', 'home')  # Handle both GET and POST
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(next_url)  # Redirect to the URL in 'next' or 'home'
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Invalid username or password',
                })
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form}) 


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = Post.objects.filter(author=user)
    return render(request, 'templates/user_profile.html', {'user': user, 'posts': posts})

# @login_required
# def edit_profile(request, username):
#     user = get_object_or_404(CustomUser, username=username)
#     if request.user != user:
#         return redirect('home')
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_profile', username=user.username)
#     else:
#         form = UserProfileForm(instance=user)
#     return render(request, 'templates/edit_profile.html', {'form': form})


@login_required
def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.user != user:
        return redirect('home')
    if request.method == 'POST':    
        user.full_name = request.POST.get('fullname')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone')
        user.mobile = request.POST.get('mobile')
        user.address = request.POST.get('address')
        user.description = request.POST.get('description')
        user.save()
        return redirect('user_profile', username=user.username)
    return render(request, 'templates/edit_profile.html', {'user': user})



# Subreddits
def subreddit_list(request):
    subreddits = Subreddit.objects.all()
    return render(request, 'templates/subreddit_list.html', {'subreddits': subreddits})

@login_required
def create_subreddit(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.moderator = request.user
            subreddit.created_by = request.user
            subreddit.save()
            return redirect('subreddit_detail', subreddit_name=subreddit.name)
    else:
        form = SubredditForm()
    return render(request, 'templates/create_subreddit.html', {'form': form})


# Edit Subreddit View
@login_required
def edit_subreddit(request, subreddit_name):
    subreddit = get_object_or_404(Subreddit, name=subreddit_name)
    
    if request.user != subreddit.owner:
        # Check if the current user is the owner of the subreddit
        return redirect('home')  # or any other page you want to redirect to if not the owner
    
    if request.method == 'POST':
        form = SubredditForm(request.POST, instance=subreddit)
        if form.is_valid():
            form.save()
            return redirect('subreddit_detail', subreddit_id=subreddit.id)
    else:
        form = SubredditForm(instance=subreddit)
    
    return render(request, 'templates/edit_subreddit.html', {'form': form, 'subreddit': subreddit})

def subreddit_detail(request, subreddit_name):
    subreddit = get_object_or_404(Subreddit, name=subreddit_name)
    posts = Post.objects.filter(subreddit=subreddit).order_by('-created_at')
    return render(request, 'templates/community_page.html', {'subreddit': subreddit, 'posts': posts})

@login_required
def follow_subreddit(request, subreddit_name):
    subreddit = get_object_or_404(Subreddit, name=subreddit_name)
    
    if subreddit in request.user.followed_subreddits.all():
        # Unfollow the subreddit if the user is already following it
        request.user.followed_subreddits.remove(subreddit)
    else:
        # Follow the subreddit if not already followed
        request.user.followed_subreddits.add(subreddit)
    
    return redirect('subreddit_detail', subreddit_name=subreddit_name)

@login_required
def unfollow_subreddit(request, subreddit_name):
    subreddit = get_object_or_404(Subreddit, name=subreddit_name)
    request.user.followed_subreddits.remove(subreddit)
    return redirect('subreddit_detail', subreddit_name=subreddit_name)

# Posts
@login_required
def create_post(request, subreddit_name):
    subreddit = get_object_or_404(Subreddit, name=subreddit_name)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.subreddit = subreddit
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'templates/create_post.html', {'form': form, 'subreddit': subreddit})


# Edit Post View
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        # Check if the current user is the author of the post
        return redirect('home')  # or any other page you want to redirect to if not the author
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'templates/edit_post.html', {'form': form, 'post': post})


# Delete Post View
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        # Check if the current user is the author of the post
        return redirect('home')  # or any other page you want to redirect to if not the author
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')  # Redirect to homepage or wherever you like

    return render(request, 'templates/delete_post.html', {'post': post})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(parent_post=post).order_by('-created_at')
    return render(request, 'templates/post_detail.html', {'post': post, 'comments': comments})


@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.toggle_upvote(request.user)
    # return JsonResponse({'status': 'success', 'upvotes': post.upvote_count(), 'downvotes': post.downvote_count(), 'vote_counts':post.vote_counts})
    return redirect('post_detail', post_id=post_id)

@login_required
def downvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.toggle_downvote(request.user)
    # return JsonResponse({'status': 'success', 'upvotes': post.upvote_count(), 'downvotes': post.downvote_count(), 'vote_counts':post.vote_counts})
    return redirect('post_detail', post_id=post_id)

@login_required
def upvote_post_from_community(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.toggle_upvote(request.user)
    # return JsonResponse({'status': 'success', 'upvotes': post.upvote_count(), 'downvotes': post.downvote_count(), 'vote_counts':post.vote_counts})
    return redirect('subreddit_detail', subreddit_name=post.subreddit.name)

@login_required
def downvote_post_from_community(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.toggle_downvote(request.user)
    # return JsonResponse({'status': 'success', 'upvotes': post.upvote_count(), 'downvotes': post.downvote_count(), 'vote_counts':post.vote_counts})
    return redirect('subreddit_detail', subreddit_name=post.subreddit.name)

# Comments
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'templates/add_comment.html', {'form': form})

@login_required
def edit_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Fetch the comment by ID
    
    # Check if the user is the owner of the comment (optional, for security)
    if request.user != comment.author:
        return redirect('post_detail', post_id=comment.parent_post.id)  # Redirect to post if not authorized

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  # Save the edited comment
            return redirect('post_detail', post_id=comment.parent_post.id)  # Redirect to the post's detail page
    else:
        form = CommentForm(instance=comment)  # Pre-populate the form with the current comment text

    return render(request, 'templates/edit_comment.html', {'form': form, 'comment': comment, 'post_id':post_id})

# Reply to Comment View
@login_required
def reply_to_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.parent_post = post
            new_comment.parent_comment = parent_comment  # Associate with the parent comment
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'templates/reply_to_comment.html', {'post': post, 'form': form, 'parent_comment': parent_comment})


def delete_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Find the comment by ID
    
    # Check if the user is the owner of the comment (optional, for security)
    if request.user != comment.author:
        return redirect('post_detail', post_id=comment.parent_post.id)  # Redirect to post if not authorized

    # Delete the comment
    comment.delete()

    # Redirect back to the post detail page
    return redirect('post_detail', post_id=comment.parent_post.id)


@login_required
def upvote_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.toggle_upvote(request.user)
    # return JsonResponse({'status': 'success', 'upvotes': comment.upvotes.count()})
    return redirect('post_detail', post_id=comment.parent_post.id)

@login_required
def downvote_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.toggle_downvote(request.user)
    # return JsonResponse({'status': 'success', 'downvotes': comment.downvotes.count()})
    return redirect('post_detail', post_id=comment.parent_post.id)

# Search
def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(content__icontains=query)
    subreddits = Subreddit.objects.filter(name__icontains=query)
    return render(request, 'templates/search_results.html', {'query': query, 'posts': posts, 'subreddits': subreddits})

# Settings
@login_required
def settings(request):
    return render(request, 'templates/settings.html')
