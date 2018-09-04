from django.urls import path
from HomePage import views

# Django将 URL 和视图关联起来，URLconf 将 URL 模式映射到视图。
urlpatterns = [
    path('', views.index, name='index'),     # name参数为你的 URL 取名能使你在 Django 的任意地方唯一地引用它，尤其是在模板中。这个有用的特性允许你只改一个文件就能全局地修改某个 URL 模式。
    path('detail/<int:article_id>', views.detail, name='detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),      #通用视图
    path('register/', views.register, name='register'),
]