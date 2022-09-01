from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.PollListVIew.as_view(), name='poll-list'),
    path('create', views.PollCreateView.as_view(), name='poll-create'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
]
