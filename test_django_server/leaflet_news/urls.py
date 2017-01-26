from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from leaflet_news.models import NewsPost
from . import views


#urlpatterns = [# rest of urls
#              url(r'^$', MainPageView.as_view()),]

urlpatterns = [
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=NewsPost, properties=('title','city', 'tags','link', 'created_date', 'popupContent',)), name='data'),
	url(r'^test$',views.mainpage, name='mainpage')
]