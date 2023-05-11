from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from apps.blog.forms import SharePornoStarForm
from apps.blog.models import PornoStar


class PornoStarShareView(View):
    template_name = 'blog/share.html'

    def get(self, request, slug: str) -> HttpResponse:
        """
        Get star, clear form.
        RENDERS:
            star, clear form.
        """
        star = get_object_or_404(PornoStar.published, slug=slug)
        form = SharePornoStarForm()
        context = {'star': star, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, slug: str) -> HttpResponse:
        """
        Get star, send mail, create session data( email_to, star_name ).
        IF FROM VALID:
            REDIRECT to list.html with session data.
        RENDERS:
            star, complete form.
        """
        star = get_object_or_404(PornoStar.published, slug=slug)

        if (form := SharePornoStarForm(request.POST)).is_valid():
            cd = form.cleaned_data

            # send message to email
            absolute_url = request.build_absolute_uri(star.get_absolute_url())
            subject = f"{cd['name']} recommends looking at {star.name}"
            message = f"Look at {cd['name']} at {absolute_url}\n\n" \
                      f"{cd['name']}'s message: {cd['text']}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [cd['email_to']])

            # save email and star_name to session and redirect tolist.html page
            request.session['share_success_data'] = {
                'email_to': cd["email_to"],
                'star_name': star.name,
            }
            return redirect(reverse('blog:star_list'))

        context = {'star': star, 'form': form}
        return render(request, self.template_name, context)
