from django.urls import path
from .views import JobListView, JobDetailView, JobCreateView, ApplyJobView, JobUpdateView, JobDeleteView, Home

app_name = 'job'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('jobs/', JobListView.as_view(), name='jobs'),
    path('jobs/apply/<slug:slug>/', ApplyJobView.as_view(), name='apply_job'),
    path('jobs/create/', JobCreateView.as_view(), name='create_job'),
    path('jobs/<slug:slug>/', JobDetailView.as_view(), name='job'),
    path('jobs/<slug:slug>/update/', JobUpdateView.as_view(), name='update_job'),
    path('jobs/<slug:slug>/delete/', JobDeleteView.as_view(), name='delete_job'),
]