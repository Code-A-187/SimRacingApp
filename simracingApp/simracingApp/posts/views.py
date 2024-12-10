from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth import get_user_model

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
        return redirect('home-page')
        
    return render(request, 'posts/post-delete.html', {'post': post})


@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'home-page'))


@login_required
def toggle_like(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home-page'))