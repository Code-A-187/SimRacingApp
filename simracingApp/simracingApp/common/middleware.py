from django.utils.html import escape
from django.core.exceptions import ValidationError

class ContentSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            # Sanitize POST data to prevent XSS attacks
            post_data = request.POST.copy()
            for key in post_data:
                if isinstance(post_data[key], str):
                    post_data[key] = escape(post_data[key].strip())
            request.POST = post_data

        response = self.get_response(request)
        return response 