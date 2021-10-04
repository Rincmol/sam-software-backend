from .views import RegisterView,LoginView, UserView,LogoutView
from django.urls import path
from Sam import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('items', views.items),
    path('itemshow',views.itemshow), 

     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

