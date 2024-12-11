from django import forms
from django.core.exceptions import ValidationError
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'image_url', 'start_date', 'end_date', 'race_time']

    def clean(self):
        cleaned_data = super().clean()
        try:
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            
            if start_date and end_date and end_date < start_date:
                raise ValidationError("End date must be after start date.")
        except Exception as e:
            raise ValidationError(f"Error validating dates: {str(e)}")
        
        # Image URL validation
        image_url = cleaned_data.get('image_url')
        if image_url:
            if not any(image_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                raise ValidationError("Image URL must point to a valid image file (jpg, jpeg, png, gif)")

        return cleaned_data