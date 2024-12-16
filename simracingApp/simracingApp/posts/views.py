from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ValidationError

from .forms import PostAddForm, PostCommentForm, PostEditForm
from .models import Post

UserModel = get_user_model()


class PostAddView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostAddForm
    template_name = 'posts/post-add-page.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.object.pk})


class PostDetailsView(LoginRequiredMixin, DetailView):
    """
    Display detailed view of a post.
    Handles post information display and user interactions.
    """
    model = Post
    template_name = 'posts/post-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'comment_form': PostCommentForm()}


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'posts/post-edit.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.object.pk})


class AuthorPostListView(ListView):
    template_name = 'posts/author-posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.author = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return Post.objects.filter(author=self.author).order_by('-created_at')

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'author': self.author,
            'comment_form': PostCommentForm()
        }


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post-details', pk=pk)
        
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post successfully deleted.")
        return redirect('home-page')
        
    return render(request, 'common/delete.html', {
        'object_type': 'Post',
        'object_name': post.content[:50] + '...' if len(post.content) > 50 else post.content,
        'cancel_url': reverse_lazy('post-details', kwargs={'pk': post.pk})
    })


@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        # Rate limiting check
        cache_key = f'user_{request.user.pk}_comment_timeout'
        if cache.get(cache_key):
            messages.error(request, 'Please wait before commenting again.')
            return redirect(request.META.get('HTTP_REFERER', 'home-page'))

        post = get_object_or_404(Post, pk=pk)
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Set rate limit - one comment per 30 seconds
            cache.set(cache_key, True, 30)
            
    return redirect(request.META.get('HTTP_REFERER', 'home-page'))


@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_liked = user in post.likes.all()
    if request.method == 'POST':
        cache_key = f'user_{request.user.pk}_like_timeout'
        if cache.get(cache_key):
            return JsonResponse({'error': 'Please wait before liking again'}, status=429)
            
        if is_liked:
            post.likes.remove(user)
        else:
            post.likes.add(user)
            
        # Set rate limit - one like per 5 seconds
        cache.set(cache_key, True, 5)
            
        return JsonResponse({
            'liked': is_liked,
            'likes_count': post.likes.count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)