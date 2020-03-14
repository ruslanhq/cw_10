from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from webapp.forms import SearchForm, FileForm, FileFormForCommon
from webapp.models import File


class IndexView(ListView):
    model = File
    template_name = 'index.html'
    paginate_by = 10
    paginate_orphans = 1
    ordering = '-created_at'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.filter(general_access='common')

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class FileCreate(CreateView):
    model = File
    template_name = 'create_file.html'
    # form_class = FileForm

    def get_success_url(self):
        return reverse('webapp:index')

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return FileForm
        else:
            return FileFormForCommon

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user.is_authenticated:
            self.object.author = self.request.user
            self.object.save()
        else:
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


class DetailFile(UserPassesTestMixin, DetailView):
    pk_url_kwarg = 'pk'
    model = File
    template_name = 'file.html'
    context_object_name = 'file'

    def test_func(self):
        file = self.get_object()
        user = self.request.user
        if (file.general_access == 'private' and user in file.users_private.all()) or file.author == user or\
                file.general_access == 'common':
            return True


class FileDelete(UserPassesTestMixin, DeleteView):
    model = File
    context_object_name = 'file'
    template_name = 'delete_file.html'
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        file = File.objects.filter(author__username=self.request.user, pk=self.kwargs['pk'])
        if file or self.request.user.has_perm('webapp.delete_file'):
            return True

