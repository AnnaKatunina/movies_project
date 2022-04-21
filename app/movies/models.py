import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        movie = 'movie', _('movie')
        tv_show = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=8, choices=Type.choices, default=Type.movie)
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    genres = models.ManyToManyField('Genre', verbose_name=_('genres'),
                                    through='GenreFilmwork',
                                    related_name='film_works')
    persons = models.ManyToManyField('Person', verbose_name=_('persons'),
                                     through='PersonFilmwork',
                                     related_name='film_works')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')

    def __str__(self):
        return self.title


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)
    birth_date = models.DateField(_('birth_date'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', verbose_name=_('filmwork'), on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', verbose_name=_('genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('film_work', 'genre'),)
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre-film-work')
        verbose_name_plural = _('genre-film-works')

    def __str__(self):
        return f'{self.film_work.title} - {self.genre.name}'


class PersonFilmwork(UUIDMixin):

    class Role(models.TextChoices):
        director = 'director', _('director')
        screenwriter = 'writer', _('writer')
        actor = 'actor', _('actor')

    film_work = models.ForeignKey('Filmwork', verbose_name=_('filmwork'), on_delete=models.CASCADE)
    person = models.ForeignKey('Person', verbose_name=_('person'), on_delete=models.CASCADE,
                               related_name='person_film_works')
    role = models.CharField(_('role'), max_length=64, choices=Role.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('film_work', 'person', 'role'),)
        db_table = "content\".\"person_film_work"
        verbose_name = _('person-film-work')
        verbose_name_plural = _('person-film-works')

    def __str__(self):
        return f'{self.film_work.title} - {self.person.full_name}'
