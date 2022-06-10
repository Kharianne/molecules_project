#from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
#from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

from molecule_admin.forms import RegisterUserForm, UserForm
from molecule_admin.models import Molecule, Collection, Profile, User


class IndexView(TemplateView):
    template_name = "index.html"


class MoleculeListView(LoginRequiredMixin, ListView):
    paginate_by = 32
    model = Molecule
    template_name = "molecules/molecule_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collections'] = Collection.objects.all().order_by('name')
        search_query = self.request.GET.get('search')
        context['search'] = search_query
        return context

    def get_queryset(self):
        filter_collection = self.request.GET.getlist('collection')
        search_query = self.request.GET.get('search')
        if filter_collection and search_query:
            return Molecule.objects.filter(collection__in=filter_collection,
                                           name__icontains=search_query)\
                .order_by('name')
        elif filter_collection:
            return Molecule.objects.filter(collection__in=filter_collection)\
                .order_by('name')
        elif search_query:
            return Molecule.objects.filter(name__icontains=search_query)\
                .order_by('name')
        else:
            return Molecule.objects.all().order_by('name')


class MoleculeDetailView(LoginRequiredMixin, DetailView):
    model = Molecule
    template_name = "molecules/molecule_detail.html"


class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("profile_update")
    success_message = "User was created successfully."

    def get_object(self, queryset=None):
        return self.request.user.profile


    def post(self, request, *args, **kwargs):
        user = super().post()
        return user


class ProfileLoginView(TemplateView, LoginRequiredMixin):
    model = User
    template_name = "registration/login.html"
    fields = ["name", "password"]
    success_url = reverse_lazy("index")


class ProfileUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    form_class = UserForm
    #fields = ["name", "surname", "institution"]
    template_name = "profiles/profile_update.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return self.request.user.profile
