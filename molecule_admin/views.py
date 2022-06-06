from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView

from molecule_admin.models import Molecule, Collection


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
