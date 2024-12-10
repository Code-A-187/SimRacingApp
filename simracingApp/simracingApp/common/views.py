from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib import messages
from simracingApp.posts.models import Post
from simracingApp.events.models import Event
from simracingApp.posts.forms import PostAddForm, PostCommentForm


class HomeView(ListView):
    model = Post
    paginate_by = 6
    context_object_name = 'posts'
    
    def get_template_names(self):
        return ['common/dashboard.html'] if self.request.user.is_authenticated else ['common/home.html']

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return super().get_context_data(**kwargs)
            
        # Get the latest 5 events
        latest_events = Event.objects.all()[:5]
        
        return {
            **super().get_context_data(**kwargs),
            'form': PostAddForm(),
            'comment_form': PostCommentForm(),
            'latest_events': latest_events,
            'dashboard': True
        }

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login-page')
            
        content = request.POST.get('content', '').strip()
        if not content:
            messages.error(request, 'Post content cannot be empty.')
            return redirect('home-page')

        Post.objects.create(
            author=request.user,
            content=content,
            image_url=request.POST.get('image_url', '')
        )
        return redirect('home-page')
