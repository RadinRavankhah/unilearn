from django.contrib import admin
from .models import Subreddit, Post, Comment, Vote
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to display in the list view
    list_display = ('username', 'email', 'karma', 'date_joined', 'last_online')
    search_fields = ('username', 'email')

    # Exclude non-editable fields from the form
    readonly_fields = ('date_joined', 'last_online')

    # Fieldsets for organizing admin form sections
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('bio', 'karma', 'preferences')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('date_joined', 'last_online')}),
    )

    # Fields to include when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description', 'created_by__username')
    list_filter = ('created_at',)
    filter_horizontal = ('moderators',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subreddit', 'votes', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username', 'subreddit__name')
    list_filter = ('subreddit', 'created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'parent_post', 'parent_comment', 'votes', 'created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'parent_post__title')
    list_filter = ('created_at', 'updated_at')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content_id', 'vote_type', 'created_at')
    search_fields = ('user__username', 'content_type', 'content_id')
    list_filter = ('vote_type', 'content_type', 'created_at')
