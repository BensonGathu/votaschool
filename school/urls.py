from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from. import views

urlpatterns =[
    path("",views.home,name="home"),
    path("hodhome/",views.hodhome,name="hodhome"),
    path("teachhome/",views.teachhome,name="teachhome"),
    path("studhome/",views.studhome,name="studhome"),
    # path('register/',views.register,name="register"),
    # path('teacherregister',views.registerteacher.as_view(),name="teacherregister"),
    # path('studentregister',views.registerstudent.as_view(),name="studentregister"),
    path('registerprincipal/',views.principal_registration,name="registerprincipal"),
    path('registerteacher/',views.teacher_registration,name="registerteacher"),
    path('registerstudent/',views.student_registration,name="registerstudent"),
    path('profile/',views.profile,name="profile"),
    path('accounts/login/',views.loginPage,name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('allstudents/<int:id>',views.allstudents,name="allstudents"),
    path('allteachers/',views.allteachers,name="allteachers"),
    path('addclasses/',views.addclasses,name="addclasses"),
    path('addacademicyear/',views.addacademicyear,name="addacademicyear"),   
    path("editprofile/<int:id>",views.editprofile,name="editprofile"),
    path("admineditprofile/<int:id>",views.admineditprofile,name="admineditprofile"),
    path("delprofile/<int:id>",views.delprofile,name="delprofile"),
    path("addfees/<int:id>/",views.fees,name="addfees"),
    path("pcomment/<int:id>/",views.principal_comment,name="principal_comment"),
    path("tcomment/<int:id>/",views.teacherComment,name="teacher_comment"),
    path("addinformation",views.addinformation,name="addinformation"),
    path("classDone/<int:id>",views.donewithclass,name="classdone"),
    # path("addteacher",views.addTeacher,name="addteacher"),
    # path("addstudent",views.addStudent,name="addstudent"),
    path("addsubject",views.addSubject,name="addsubject"), 
    path("allclasses/",views.classes,name="allclasses"),
    path("addresults/",views.addresults,name="addresults"),
    path("getposition/<int:id>/",views.student_positions,name="getposition"),
    path("getsubjectposition/<int:id>/",views.student_subject_positions,name="studentsubjectpositions"),
    # path("subjectdetails/<int:id>/",views.subjectdetails,name="subjectdetails"),
    # path("create-user/",views.UserCreateView.as_view(),name="createuser"),
    # path("create-student/<int:id>/",views.StudentView.as_view(),name="create-student"),
    # path("create-teacher/<int:id>/",views.TeacherView.as_view(),name="create-teacher"),
    # path("create-principal/<int:id>/",views.PrincipalView.as_view(),name="create-principal"),
    path("ajax/load-subjects/",views.load_subjects,name='ajax_load_subjects'),
    path("teacher",views.teacher,name="teacher"),
    path("students/<int:id>",views.Students,name="students"),
    path("addmarks/<int:id>/",views.addmarks,name="addmarks"),
    path("editmarks/<int:id>/",views.editmarks,name="editmarks"),
    path("studentsperfomancelist/",views.studentsperfomancelist,name="studentperfomancelist"),
    path("admineditprofile/<int:id>/",views.admineditprofile,name="admineditprofile"),
    path("allteachers/", views.allteachers, name="allteachers"),

    #student urls
    path("studentinfo/",views.studentInfo,name="studentinfo"),
    path("reportform/", views.reportform, name="reportform"),


    #timetable
    # path('createtimetable',views.CreateTimetable,name="createtimetable"),
    # path('createtimetableitems',views.CreateTimetableItems,name="createtimetableitems"),




]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)