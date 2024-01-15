from django.contrib import admin
from django.urls import path
from myapp.views import admin_reject_user, admin_approve_user, admin_dashboard, verifyOTP,add, update, profile, index, login, signup, signout, delete_profile

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('logout/', signout),
    path('profile/', profile, name="profile"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:profile_id>/', delete_profile, name="delete"),
    path('add', add, name="add"),
    path('verify/',verifyOTP,name = "verify"),
 path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
  path('admin_approve_user/<int:user_id>/', admin_approve_user, name='admin_approve_user'),
    path('admin_reject_user/<int:user_id>/', admin_reject_user, name='admin_reject_user'),

]
# urlpatterns += [
#     path('admin/', admin.site.urls),
# ]