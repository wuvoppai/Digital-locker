from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='Index'),
    path('Register/',views.register,name='Register'),
    path('CompleteRegistration/',views.registration,name='Registration'),
    path('Login/',views.login,name='Login'),
    path('Home/',views.home,name='Dashboard'),
    path('Logout/',views.logout,name='Logout'),
    path('Upload/',views.upload,name='Upload'),
    path('Delete/',views.delete,name='Delete'),
    path('Bin/',views.bin,name='Bin'),
    path('Restore/',views.restore,name='Restore'),
    path('DeleteForever/',views.deleteforever,name='DeleteForever'),
    path('Rename/',views.rename,name='Rename'),
    path('Profile/',views.profile,name='Profile'),
    path('UpdateProfile/',views.updateprofile,name='UpdateProfile'),
    path('ChangePassword/',views.changepassword,name='ChangePassword'),
    path('UpdateDetails/',views.updatedetails,name='UpdateDetails'),
    path('About/',views.about,name='About'),
]
