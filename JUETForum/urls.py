from django.contrib import admin
from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from users.views import menu,not_logged_in
from users.views import signup,activate
from users.views import about
from django.conf import settings
from django.conf.urls.static import static
from main.views import index_forum
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',menu,name='menu'),
    path('home/',index_forum.as_view(),name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('not_logged_in/',not_logged_in,name='not_logged_in'),
    path('about/',about,name='about'),
    path('forum/',include('main.urls')),
    path('signup/',signup, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)