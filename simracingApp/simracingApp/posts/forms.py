from django import forms
from simracingApp.posts.models import Post, Comment


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image_url']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control post-input',
                    'rows': '1',
                    'placeholder': 'Share your racing experience...',
                    'required': True
                }
            ),
            'image_url': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Add an image URL (optional)',
                    'required': False
                }
            )
        }

    def clean_image_url(self):
        image_url = self.cleaned_data.get('image_url')
        if image_url == '':
            return None
        return image_url


class PostAddForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['content', 'image_url']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control post-input',
                    'rows': '3',
                    'placeholder': 'Edit your post...'
                }
            ),
            'image_url': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Edit image URL (optional)'
                }
            )
        }


class PostDeleteForm(PostBaseForm):
    pass


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control comment-input',
                    'rows': '1',
                    'placeholder': 'Write a comment...'
                }
            )
        }