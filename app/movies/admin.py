from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date')


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    raw_id_fields = ('genre', )


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    raw_id_fields = ('person',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres')
    list_filter = ('type', 'genres__name')
    search_fields = ('title', 'description', 'id')
    list_prefetch_related = ('genres', 'persons')

    def get_queryset(self, request):
        queryset = (
            super(FilmworkAdmin, self).get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('genres')
