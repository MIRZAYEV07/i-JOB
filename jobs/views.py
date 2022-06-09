from functools import reduce
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from .forms import JobForm, AppliesForm
from .models import Job, JobType, CarrerLevel, Category, Applies


class Home(ListView):
    queryset = Job.objects.filter(status=True, active=True, vacancy__gte=1)
    template_name = 'job/home.html'
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs = super().get_queryset()

        countries = {job.country for job in jobs if job.country}

        context['categories'] = Category.objects.all()
        context['countries'] = countries
        return context


class JobListView(ListView):
    queryset = Job.objects.filter(status=True, active=True, vacancy__gte=1)
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs = super().get_queryset()

        countries = {job.country for job in jobs if job.country}
        cities = {job.city for job in jobs if job.city}

        context['categories'] = Category.objects.all()
        context['job_types'] = JobType.objects.all()
        context['carrer_levels'] = CarrerLevel.objects.all()
        context['countries'] = countries
        context['cities'] = cities
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        data = self.request.GET
        if not data:
            return qs

        keywords = data.get("keywords")
        categories = data.getlist("category")
        countries = data.getlist("countries")
        cities = data.getlist("cities")
        min_exp = data.get("min_exp")
        max_exp = data.get("max_exp")
        job_type = data.getlist("type")
        carrer_levels = data.getlist("carrer_levels")
        salary = data.get("salary")

        if keywords:
            qs = qs.filter(Q(title__icontains=keywords) | Q(description__icontains=keywords))

        if categories:
            qs = qs.filter(categories__in=categories)

        if cities:
            qs = qs.filter(city__in=cities)

        if countries:
            qs = qs.filter(country__in=countries)

        if min_exp:
            qs.filter(min_experience__gte=min_exp)

        if max_exp:
            qs.filter(min_experience__lte=max_exp)

        if job_type:
            qs = qs.filter(job_type__in=job_type)

        if carrer_levels:
            qs = qs.filter(carrer_levels__in=carrer_levels)

        if salary:
            min_salary, max_salary = salary.split('-')

            max_salary = filter(lambda a: a not in '$/ Year', max_salary)
            max_salary = int("".join(list(max_salary)))

            min_salary = filter(lambda a: a not in '$', min_salary)
            min_salary = int("".join(list(min_salary)))
            if min_salary != 750:
                qs = qs.filter(Q(min_salary__gte=min_salary) & Q(max_salary__lte=max_salary))

        return qs


class JobDetailView(DetailView):
    queryset = Job.objects.filter(status=True, active=True, vacancy__gte=1)
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name, email = None, None
        if self.request.user.is_authenticated:
            user = self.request.user
            name = f"{user.first_name} {user.last_name}"
            email = user.email

        data = {'name': name, 'email': email}
        context['form'] = AppliesForm(initial=data)
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm

    def form_invalid(self, form):
        print('*' * 88)
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        print('*' * 88)
        form2 = form.save(commit=False)
        form2.owner = self.request.user
        form2.save()
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm

    def test_func(self):
        return self.get_object().owner == self.request.user


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    context_object_name = 'job'

    def test_func(self):
        return self.get_object().owner == self.request.user

    def get_success_url(self):
        return reverse('job:jobs')


class ApplyJobView(CreateView):
    model = Applies
    http_method_names = ['post', ]
    form_class = AppliesForm

    def get_job(self):
        slug = self.kwargs['slug']
        jobs = Job.objects.filter(status=True, active=True, vacancy__gte=1)
        job = get_object_or_404(jobs, slug=slug)

        return slug, job

    def form_invalid(self, form):
        slug = self.kwargs['slug']
        return redirect('job:job', slug=slug)

    def form_valid(self, form):
        slug, job = self.get_job()
        form2 = form.save(commit=False)
        form2.job = job
        form2.save()
        messages.success(self.request, f"You have successfully applied for the job {job.title}")
        return redirect('job:job', slug=slug)