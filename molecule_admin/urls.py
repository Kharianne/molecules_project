from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("molecules/", views.MoleculeListView.as_view(), name='molecules'),
    path("molecule/<int:pk>", views.MoleculeDetailView.as_view(),
         name='molecule_detail')
]
