from django.conf.urls import url, include
from django.contrib import admin

from microblog import views as mb_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/(?P<username>\w{0,50})/$', mb_views.view_posts),
    url(r'^make-post/$', mb_views.make_post),
    # url(r'', include('actable.urls', namespace='actable')),
]
