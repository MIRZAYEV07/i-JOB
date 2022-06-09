from django.conf.urls import include
from django.urls import path
from  .views import ProfileView, CVCreateView, JobList, JobApplicants, ChangeApplyStatus


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cv/', CVCreateView.as_view(), name='cv'),
    path('dashboard/jobs/', JobList.as_view(), name='jobs_list_edit'),
    path('jobs/<slug:slug>/appliers/', JobApplicants.as_view(), name='job_applicants_list'),
    path('jobs/<int:id>/appliers/<int:is_accepted>/', ChangeApplyStatus.as_view(), name='change_apply_status'),
]