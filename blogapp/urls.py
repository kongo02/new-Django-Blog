from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import registration_view, login_view

urlpatterns = [

    path('', views.index, name='index'),
    path('post/<str:pk>', views.getPost, name='post_detail'),
    path('post/<str:pk>/delete/', views.deletePost, name='post_delete'),
    path('create_post/', views.createPost, name='create_post'),
    path('post/<str:pk>/edit/', views.updatePost, name="post_update"),
    path('register/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout, name="logout"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
