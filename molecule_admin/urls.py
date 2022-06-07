from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("molecules/", views.MoleculeListView.as_view(), name='molecules'),
    path("molecule/<int:pk>", views.MoleculeDetailView.as_view(),
         name='molecule_detail'),
    path("note/create", views.NoteCreateView.as_view(), name='create_note'),
    path("note/delete/<int:pk>", views.NoteDeleteView.as_view(),
         name='delete_note'),
    path("note/update/<int:pk>", views.NoteUpdateView.as_view(),
         name='update_note')
]
