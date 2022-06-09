from django import forms
from .models import Category, Job, Applies
from django_countries.widgets import CountrySelectWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('owner', 'created_at', 'slug', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                'country',
                'city',
            ),
            Fieldset(
                '',
                Div(
                Div('max_salary',css_class='col-md-6',),
                Div('min_salary',css_class='col-md-6',),
                Div('min_experience',css_class='col-md-6',),
                Div('max_experience',css_class='col-md-6',),
                Div('vacancy',css_class='col-md-6',),
                Div('career_level',css_class='col-md-6',),
                Div('job_type',css_class='col-md-6',),
                Div('categories',css_class='col-md-6',),
                Div('image',css_class='col-md-6',),
                Div('published_at',css_class='col-md-6',),
                Div('status',css_class='col-md-6',),
                css_class='row',
            ),
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white mb-3 mt-3')
            )
        )

        self.fields['min_salary'].label = 'Min Salary  $/year'
        self.fields['max_salary'].label = 'Max Salary  $/year'

        widgets = {'country': CountrySelectWidget()}


class AppliesForm(forms.ModelForm):
    class Meta:
        model = Applies
        fields = ['name', 'email', 'portfolio', 'cv', 'coverletter']