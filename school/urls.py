from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from. import views

urlpatterns =[
    path("",views.home,name="home"),
    path('register/',views.register,name="register"),
    path('teacherregister',views.registerteacher.as_view(),name="teacherregister"),
    path('studentregister',views.registerstudent.as_view(),name="studentregister"),
    path('headregister',views.registerheadteacher.as_view(),name="headregister"),
    path('allstudents',views.allstudents,name="allstudents"),    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)