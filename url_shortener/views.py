from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import URL
from .forms import URLForm
import random
import string


class URLListView(LoginRequiredMixin, ListView):
    model = URL
    template_name = 'url_list.html'
    context_object_name = 'urls'

    def get_queryset(self):
        return URL.objects.filter(user=self.request.user)


class URLCreateView(LoginRequiredMixin, CreateView):
    model = URL
    form_class = URLForm
    template_name = 'url_create.html'
    success_url = '/'

    def form_valid(self, form):
        url = form.save(commit=False)
        url.user = self.request.user
        url.short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        url.save()
        return super().form_valid(form)


class URLRedirectView(DetailView):
    model = URL
    slug_field = 'short_url'
    slug_url_kwarg = 'short_url'

    def get(self, request, *args, **kwargs):
        url = self.get_object()
        url.clicks += 1
        url.save()
        return redirect(url.original_url)
