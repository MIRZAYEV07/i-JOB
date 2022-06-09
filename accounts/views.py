from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, ListView
from .forms import UserUpdateForm, UserCVForm
from .models import UserCV
from jobs.models import Applies, Job


class ProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = UserUpdateForm(instance=user)

        CV_form = UserCVForm()
        return render(request, self.template_name, {'form': form, 'CV_form': CV_form})

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, instance=self.request.user, files=request.FILES)
        if form.is_valid():
            form.save()
        form = UserUpdateForm(instance=self.request.user)
        return self.get(request, *args, **kwargs)


class CVCreateView(LoginRequiredMixin, View):
    template_name = 'account/user_cv_form.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        cv = UserCV.objects.filter(user=user)

        form = UserCVForm()

        if cv.exists():
            form = UserCVForm(instance=cv.first())

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        cv = UserCV.objects.filter(user=user)

        form = UserCVForm(request.POST, files=request.FILES)

        if cv.exists():
            form = UserCVForm(request.POST, instance=cv.first(), files=request.FILES)

        if form.is_valid():
            form2 = form.save(commit=False)
            form2.user = user
            form2.save()

        return self.get(request, *args, **kwargs)


class JobList(LoginRequiredMixin, ListView):
    model = Job
    context_object_name = 'jobs'
    template_name = 'account/job_list.html'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class JobApplicants(LoginRequiredMixin, ListView):
    model = Applies
    context_object_name = 'appliers'
    template_name = 'account/job_applicants_list.html'

    def get_queryset(self):
        job = get_object_or_404(Job.objects.filter(owner=self.request.user), slug=self.kwargs['slug'])
        return self.model.objects.filter(job=job)


class ChangeApplyStatus(LoginRequiredMixin, UserPassesTestMixin, View):

    def get_apply(self):
        appliers = Applies.objects.all()
        return get_object_or_404(appliers, id=self.kwargs['id'])

    def test_func(self):
        apply = self.get_apply()
        job_owner = apply.job.owner

        return self.request.user == job_owner

    def post(self, request, id, is_accepted=None, *args, **kwargs):
        apply = self.get_apply()
        apply.apply_status = bool(is_accepted)

        if not apply.apply_status:
            apply.save()
        else:
            job = apply.job
            if job.vacancy > 0:
                apply.save()

        if apply.apply_status:
            job = apply.job
            job.vacancy -= 1
            job.save()

        return redirect('job_applicants_list', slug=apply.job.slug)
