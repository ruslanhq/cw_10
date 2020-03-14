from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from webapp.forms import SearchForm, FileForm
from webapp.models import File


class IndexView(ListView):
    model = File
    template_name = 'index.html'
    paginate_by = 10
    paginate_orphans = 1
    ordering = '-created_at'

    def get_queryset(self):
        query = self.request.GET.get('form')
        if query:
            return File.objects.filter(name__contains=query)
        else:
            return File.objects.all()


class FileCreate(CreateView):
    model = File
    template_name = 'create_file.html'
    form_class = FileForm

    def get_success_url(self):
        return reverse('webapp:index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user.is_authenticated:
            self.object.author = self.request.user
            self.object.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class FileUpdate(UserPassesTestMixin, UpdateView):
    form_class = FileForm
    template_name = 'update_file.html'
    model = File
    context_object_name = 'file'

    def test_func(self):
        file = File.objects.filter(author__username=self.request.user, pk=self.kwargs['pk'])
        if file or self.request.user.has_perm('webapp.change_file'):
            return True

    def get_success_url(self):
        return reverse('webapp:file_detail', kwargs={'pk': self.object.pk})


class DetailFile(DetailView):
    pk_url_kwarg = 'pk'
    model = File
    template_name = 'file.html'
    context_object_name = 'file'


class FileDelete(UserPassesTestMixin, DeleteView):
    model = File
    context_object_name = 'file'
    template_name = 'delete_file.html'
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        file = File.objects.filter(author__username=self.request.user, pk=self.kwargs['pk'])
        if file or self.request.user.has_perm('webapp.delete_file'):
            return True

