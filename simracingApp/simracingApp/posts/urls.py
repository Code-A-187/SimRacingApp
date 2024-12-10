# simracingApp/posts/urls.py
from django.urls import path, include

from simracingApp.posts import views

urlpatterns = (
    path('add/', views.PostAddView.as_view(), name='post-add'),
    path('author/<int:pk>/', views.AuthorPostListView.as_view(), name='author-posts'),
    path('<int:pk>/', include([
        path('', views.PostDetailsView.as_view(), name='post-details'),
        path('edit/', views.PostEditView.as_view(), name='post-edit'),
        path('delete/', views.post_delete, name='post-delete'),
        path('comment/', views.add_comment, name='add-comment'),
        path('like/', views.toggle_like, name='toggle-like'),
    ])),
)