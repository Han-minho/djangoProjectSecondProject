from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('',views.post_list, name='post_list'),
    # path('<int:id>/', views.post_detail, name='post_detail'),
    path(r'<int:year>/<int:month>/<int:day>/<post>/', views.post_detail, name='post_detail'),
]