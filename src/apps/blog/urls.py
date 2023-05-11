from django.urls import path

from .views import PornoStarList, PornoStarShareView, DetailView

app_name = 'star'

urlpatterns = [
    path('', PornoStarList.as_view(), name="star_list"),
    path('<slug:tag_slug>', PornoStarList.as_view(), name="star_list_by_tag"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', DetailView.as_view(),
         name="star_detail"),
    path('share/<slug:slug>', PornoStarShareView.as_view(), name="star_share"),
]
