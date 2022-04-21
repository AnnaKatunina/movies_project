from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        genres = ArrayAgg('genres__name', distinct=True)
        actors = ArrayAgg('persons__full_name',
                          filter=Q(persons__person_film_works__role=PersonFilmwork.Role.actor),
                          distinct=True)
        directors = ArrayAgg('persons__full_name',
                             filter=Q(persons__person_film_works__role=PersonFilmwork.Role.director),
                             distinct=True)
        writers = ArrayAgg('persons__full_name',
                           filter=Q(persons__person_film_works__role=PersonFilmwork.Role.screenwriter),
                           distinct=True)
        queryset = self.model.objects.prefetch_related('genres', 'persons').values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(genres=genres, actors=actors, directors=directors, writers=writers)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):

    paginate_by = 50
    ordering = ['-rating']

    def get_queryset(self):
        queryset = super(MoviesListApi, self).get_queryset()

        genre_name = self.request.GET.get('genre')
        if genre_name:
            queryset = queryset.filter(genres__contains=[genre_name])

        movie_title = self.request.GET.get('title')
        if movie_title:
            queryset = queryset.filter(title__icontains=movie_title)

        return queryset.order_by(*self.ordering)

    def get_context_data(self, *, object_list=None, **kwargs):

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )

        prev_page = page.previous_page_number() if page.has_previous() else None
        next_page = page.next_page_number() if page.has_next() else None

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': prev_page,
            'next': next_page,
            'results': list(queryset)
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        obj = self.get_object(queryset=self.get_queryset())
        return obj
