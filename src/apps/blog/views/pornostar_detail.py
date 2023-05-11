from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, Count, Subquery
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.blog.forms import CommentForm, CommentUserForm
from apps.blog.models import PornoStar, Comment


class StarCommentsGetterMixin:
    @staticmethod
    def get_queries(year: int, month: int, day: int,
                    slug: str) -> tuple[QuerySet, ...]:
        """
        Realize queries such as ( star, comments, recommendations ).
        RETURNS:
            star, comments, recommendations.
        """
        star = get_object_or_404(
            PornoStar.published.select_related('author')
            .only('name', 'slug', 'content', 'publish', 'image',
                  'author__username', 'tags__name'),
            slug=slug, publish__year=year,
            publish__month=month, publish__day=day
        )
        comments = Comment.published.filter(pornostar_id=star.id) \
            .select_related('comment_user') \
            .only('comment_user__name', 'content', 'created')

        recommendations = PornoStar.published.filter(
            tags__in=Subquery(star.tags.values_list('id', flat=True))
        ).exclude(pk=star.pk).alias(same_tags=Count('tags'))\
            .order_by('-same_tags', 'publish')\
            .only('name', 'content', 'image', 'slug', 'publish')[:7]

        return star, comments, recommendations


class DetailView(StarCommentsGetterMixin, View):
    template_name: str = 'blog/detail.html'

    def get(self, request: WSGIRequest, year: int, month: int,
            day: int, slug: str) -> HttpResponse:
        """
        Get star, comments, recommendations.
        RENDERS:
            star, comments, recommendations, clear forms.
        """
        queries = self.get_queries(year, month, day, slug)
        star, comments, recommendations = queries

        comment_user_form = CommentUserForm()
        comment_form = CommentForm()

        context = {
            'star': star,
            'comments': comments,
            'recommendations': recommendations,
            'comment_user_form': comment_user_form,
            'comment_form': comment_form,
        }

        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest, year: int, month: int,
             day: int, slug: str) -> HttpResponse:
        """
        Get star, comments, recommendations and validate form data.
        RENDERS:
            star, comments, recommendations,
            clear or complete forms,
            open_comment_form = True - always open form.
        """
        queries = self.get_queries(year, month, day, slug)
        star, comments, recommendations = queries

        post = request.POST
        comment_user_form = CommentUserForm(data={
            'name': post.get('name'),
            'email': post.get('email')
        })
        comment_form = CommentForm({'content': post.get('content')})

        if comment_user_form.is_valid() and comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.pornostar = star
            comment_form.comment_user = comment_user_form.save()
            comment_form.save()

            comment_user_form = CommentUserForm()
            comment_form = CommentForm()

        context = {
            'star': star,
            'comments': comments,
            'recommendations': recommendations,
            'comment_user_form': comment_user_form,
            'comment_form': comment_form,
            'open_comment_form': True,
        }

        return render(request, self.template_name, context)
