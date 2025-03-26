from django.urls import path
from.import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path ('login/', views.loginpage, name = 'login'),
    path ('signup/', views.signuppage, name = 'signup'),
    path('logout/', views.logoutpage, name = "logout"),
    path('upload/', views.upload_photos, name='upload'),
    path('update/<int:photo_id>/', views.update_photo, name='update'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete'),
    path('like-photo/<int:photo_id>/', views.like_photo, name='like_photo'),
    path('dislike-photo/<int:photo_id>/', views.dislike_photo, name='dislike_photo'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path ('forgotpassword/', views.forgotpassword, name = 'forgotpassword'),
    path ('resetpassword/<str:user>/', views.resetpassword, name = 'resetpassword'),
    path ('contact_us/', views.contact_us, name = 'contact_us'),

] 