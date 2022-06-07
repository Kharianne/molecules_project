from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView

from molecule_admin.forms import CreateNoteForm
from molecule_admin.models import Molecule, Collection, Note


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(molecule=context.get('molecule').pk,
                                               user_id=self.request.user.id)
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = "notes/create_note.html"
    form_class = CreateNoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['molecule'] = self.request.GET.get('molecule')
        return initial

    def get_form(self, form_class=None):
        form = super(NoteCreateView, self).get_form(form_class)
        form.instance.user_id = self.request.user
        return form

    def get_success_url(self):
        return reverse('molecule_detail',
                       kwargs={'pk': self.request.GET.get('molecule')})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "notes/delete_note.html"

    def get_success_url(self):
        return reverse('molecule_detail',
                       kwargs={'pk': self.request.GET.get('molecule')})

    def dispatch(self, request, *args, **kwargs):
        note_user = self.get_object().user_id.pk
        if note_user != self.request.user.id:
            raise PermissionDenied("It seems like you are trying to delete "
                                   "a note that does not belong to you.")
        return super(NoteDeleteView, self).dispatch(request)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = "notes/update_note.html"
    fields = ['note_text']

    def get_success_url(self):
        return reverse('molecule_detail',
                       kwargs={'pk': self.request.GET.get('molecule')})

    def dispatch(self, request, *args, **kwargs):
        note_user = self.get_object().user_id.pk
        if note_user != self.request.user.id:
            raise PermissionDenied("It seems like you are trying to update "
                                   "a note that does not belong to you.")
        return super(NoteUpdateView, self).dispatch(request)
