from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.timezone import now
from PIL import Image

User = get_user_model()


def image_upload(instance, filename):
    _, extension = filename.split('.')
    return f"jobs/{instance.id}.{extension}"


STATUS_CHOICES = [
    (True, 'Active'),
    (False, 'Deactive'),
]


class JobType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.name)


class CarrerLevel(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.name)


exp_choices = [(x, x) for x in range(26)]


class Job(models.Model):
    owner = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    categories = models.ManyToManyField('Category', related_name='jobs', blank=True)
    image = models.ImageField(upload_to=image_upload, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    min_salary = models.IntegerField(default=0, null=True, blank=True)
    max_salary = models.IntegerField(default=0, null=True, blank=True)

    vacancy = models.IntegerField(default=1)

    min_experience = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(25)])
    max_experience = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(25)])

    career_level = models.ManyToManyField(CarrerLevel, blank=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, blank=True)

    published_at = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    status = models.BooleanField(default=True, choices=STATUS_CHOICES)  # For Users
    active = models.BooleanField(default=True, choices=STATUS_CHOICES,
                                 help_text="for admins only if you want deactive job")  # For Admins


    class Meta:
        ordering = ['-published_at']

    def __init__(self, *args, **kwargs):
        self.check_job_type_and_carrer_level()
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('job:job', kwargs={'slug': self.slug})

    def check_job_type_and_carrer_level(self):
        JobType.objects.get_or_create(name='full time')
        JobType.objects.get_or_create(name='part time')
        JobType.objects.get_or_create(name='internship')
        JobType.objects.get_or_create(name='free lancer')
        JobType.objects.get_or_create(name='work from home')

        CarrerLevel.objects.get_or_create(name='student')
        CarrerLevel.objects.get_or_create(name='entry-level')
        CarrerLevel.objects.get_or_create(name='intermediate')
        CarrerLevel.objects.get_or_create(name='mid-leve')
        CarrerLevel.objects.get_or_create(name='senior')

        return

    def save(self, *args, **kwargs):
        if not self.pk:
            post_slug = slugify(self.title)
            slug_count = len(Job.objects.filter(slug=post_slug))

            if slug_count > 0:
                post_slug = f"{post_slug}-{slug_count}"

            self.slug = post_slug


        if self.pk is None and self.image:
            image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = image

        super().save(*args, **kwargs)

        # Resize a image
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 800 or img.height > 800:
                img.thumbnail((800, 800))
                img.save(self.image.path)


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """ Make category name lower case """
        self.name = str(self.name).lower()
        return super().save(*args, **kwargs)


apply_status_choices = [
    (True, 'Accepted'),
    (False, 'Refused'),
]


class Applies(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applies')
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    portfolio = models.URLField(null=True, blank=True)
    cv = models.FileField(upload_to='applies/cvs/')
    apply_status = models.BooleanField(null=True, blank=True, choices=apply_status_choices)
    coverletter = models.TextField(max_length=400, null=True, blank=True)
    applied_to = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)