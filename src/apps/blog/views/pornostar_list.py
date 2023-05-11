import copy

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from taggit.models import Tag

from apps.blog.models import PornoStar


class PornoStarList(View):
    paginate_by = 7
    template_name = 'blog/list.html'

    def get(self, request, tag_slug=None) -> HttpResponse:
        """
        Get pagination using star.
        Get and Pop email, star_name from session.
        RENDERS:
            title, pagination.
        """
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            pornostars = PornoStar.published.filter(tags__in=[tag])
        else:
            pornostars = PornoStar.published.all()

        pornostars = pornostars.prefetch_related(
            Prefetch('tags')
        ).only('name', 'slug', 'content', 'image', 'publish')

        paginator = Paginator(pornostars, self.paginate_by)
        page_number = request.GET.get('page', 1)

        try:
            pornostars_per_page = paginator.page(page_number)
        except EmptyPage:
            pornostars_per_page = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            pornostars_per_page = paginator.page(1)

        context = {'title': 'PornoStars', 'pornostars': pornostars_per_page}

        if share_data := request.session.get("share_success_data"):
            context.setdefault('email_to', copy.copy(share_data['email_to']))
            context.setdefault('star_name', copy.copy(share_data['star_name']))
            request.session.pop('share_success_data')

        return render(request, self.template_name, context)
