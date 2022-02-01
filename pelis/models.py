from django.db import models

from wagtail.core.models import Page 
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.snippets.models import register_snippet

# Create your models here.

## Page que mostrará el index de las películas
## Hereda solo de Home y no descendientes

## Modelo para películas


class Pelicula(models.Model):
    title = models.CharField('título', max_length=250)
    #slug = models.SlugField()
    rating = models.DecimalField(max_digits=6, decimal_places=4)
    link = models.URLField()
    place = models.IntegerField()
    year = models.IntegerField()
    imagen = models.URLField()
    cast = models.CharField(max_length = 250, 
        help_text='Introduzca nombres separados por comas')

    panels = [
        FieldPanel('title'),
        FieldPanel('rating'),
        FieldPanel('link'),
        FieldPanel('place'),
        FieldPanel('year'),
        FieldPanel('imagen'),
        FieldPanel('cast')
    ]
    def __str__(self):
        return f'{self.title} ({self.year})'

class PelisIndexPage(Page):
    introduccion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduccion', classname="full")
    ]


    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(Pelicula.objects.all().order_by('-rating'), 20)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that  is used to populate the
    # template
    def get_context(self, request):
        context = super(PelisIndexPage, self).get_context(request)

        # BreadPage objects (get_breads) are passed through pagination
        peliculas = self.paginate(request)

        context['peliculas'] = peliculas

        return context

    