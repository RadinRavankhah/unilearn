from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Username, email, password are inherited from AbstractUser
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    # first_name = models.CharField(max_length=30, blank=True, null=True, default=" ___/")
    # last_name = models.CharField(max_length=30, blank=True, null=True, default="___ ")
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    karma = models.IntegerField(default=0)  # Tracks user's overall karma
    date_joined = models.DateTimeField(auto_now_add=True)  # When the user created the account
    last_online = models.DateTimeField(null=True, blank=True)  # Last time the user was online
    followed_subreddits = models.ManyToManyField('Subreddit', related_name='followers', blank=True)
    # favorite_topics = models.CharField(max_length=1000, blank=True, null=True) # Favorite topics
    # preferences = models.JSONField(default=dict, blank=True)  # To store topic preferences as a JSON object

    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True, 
        default='profile_pictures/default_profile_picture.png'
    )
    website = models.URLField(max_length=200, blank=True, null=True, default='http://website.com')
    github = models.URLField(max_length=200, blank=True, null=True, default='http://github.com')
    twitter = models.URLField(max_length=200, blank=True, null=True, default='http://x.com')
    linkedin = models.URLField(max_length=200, blank=True, null=True, default='http://linkedin.com')
    instagram = models.URLField(max_length=200, blank=True, null=True, default='http://instagram.com')
    facebook = models.URLField(max_length=200, blank=True, null=True, default='http://facebook.com')
    


    def __str__(self):
        return self.username


class Subreddit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_subreddits")
    created_at = models.DateTimeField(auto_now_add=True)
    moderators = models.ManyToManyField(CustomUser, related_name="moderated_subreddits")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE, related_name="posts")
    upvotes = models.ManyToManyField(CustomUser, related_name="post_upvotes", blank=True)
    downvotes = models.ManyToManyField(CustomUser, related_name="post_downvotes", blank=True)
    votes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toggle_upvote(self, user):
        """
        Toggles upvote for a given user.
        If the user already upvoted, remove the upvote.
        If the user downvoted, remove the downvote and add the upvote.
        """
        if user in self.upvotes.all():
            self.upvotes.remove(user)
        else:
            self.upvotes.add(user)
            self.downvotes.remove(user)  # Ensure user can't upvote and downvote simultaneously

    def toggle_downvote(self, user):
        """
        Toggles downvote for a given user.
        If the user already downvoted, remove the downvote.
        If the user upvoted, remove the upvote and add the downvote.
        """
        if user in self.downvotes.all():
            self.downvotes.remove(user)
        else:
            self.downvotes.add(user)
            self.upvotes.remove(user)  # Ensure user can't upvote and downvote simultaneously

    def upvote_count(self):
        """Returns the number of upvotes."""
        return self.upvotes.count()

    def downvote_count(self):
        """Returns the number of downvotes."""
        return self.downvotes.count()

    @property
    def vote_counts(self):
        """
        Dynamically calculates the net vote count as upvotes - downvotes.
        """
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    upvotes = models.ManyToManyField(CustomUser, related_name="comment_upvotes", blank=True)
    downvotes = models.ManyToManyField(CustomUser, related_name="comment_downvotes", blank=True)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toggle_upvote(self, user):
        """
        Toggles upvote for a given user.
        If the user already upvoted, remove the upvote.
        If the user downvoted, remove the downvote and add the upvote.
        """
        if user in self.upvotes.all():
            self.upvotes.remove(user)
        else:
            self.upvotes.add(user)
            self.downvotes.remove(user)  # Ensure user can't upvote and downvote simultaneously

    def toggle_downvote(self, user):
        """
        Toggles downvote for a given user.
        If the user already downvoted, remove the downvote.
        If the user upvoted, remove the upvote and add the downvote.
        """
        if user in self.downvotes.all():
            self.downvotes.remove(user)
        else:
            self.downvotes.add(user)
            self.upvotes.remove(user)  # Ensure user can't upvote and downvote simultaneously

    def upvote_count(self):
        """Returns the number of upvotes."""
        return self.upvotes.count()

    def downvote_count(self):
        """Returns the number of downvotes."""
        return self.downvotes.count()

    @property
    def vote_counts(self):
        """
        Dynamically calculates the net vote count as upvotes - downvotes.
        """
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return f"Comment by {self.author.username} on {self.parent_post.title}"


class Vote(models.Model):
    VOTE_CHOICES = [
        ("upvote", "Upvote"),
        ("downvote", "Downvote"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="votes")
    content_type = models.CharField(max_length=10, choices=[("post", "Post"), ("comment", "Comment")])
    content_id = models.IntegerField()
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vote_type} by {self.user.username}"
