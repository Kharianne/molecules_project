from django.urls import include, path


from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("molecules/", views.MoleculeListView.as_view(), name='molecules'),
    path("molecule/<int:pk>", views.MoleculeDetailView.as_view(),
         name='molecule_detail'),
    path("login/", views.ProfileLoginView.as_view(), name='login'),
    path("profile-update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path('register/', views.RegisterView.as_view(), name='register'),
]
