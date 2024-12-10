from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm
from django.contrib import messages

class EventListView(ListView):
    model = Event
    template_name = 'events/event-list.html'
    context_object_name = 'events'
    paginate_by = 6

class EventDetailsView(DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-add-page.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class EventEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-edit.html'

    def handle_no_permission(self):
        return redirect('event-details', pk=self.kwargs['pk'])

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.pk})

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'common/delete.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        return redirect('event-details', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Event',
            'object_name': self.object.title,
            'cancel_url': reverse_lazy('event-details', kwargs={'pk': self.object.pk})
        })
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event successfully deleted.")
        return super().delete(request, *args, **kwargs)

@login_required
def toggle_subscribe(request, pk):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=pk)
        if request.user in event.subscribers.all():
            event.subscribers.remove(request.user)
        else:
            event.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home-page'))
