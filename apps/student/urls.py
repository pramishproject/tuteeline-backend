from django.urls import path

from . import views

urlpatterns = [
    path('createaccount/', views.StudentsCreateAccountApi.as_view()),
    path('login/', views.StudentLoginApi.as_view()),
    path('getstudentdata/', views.GetStudentDataApi.as_view()),
    path('academic/', views.AcademicApi.as_view()),
    path('doc/', views.DocumentApi.as_view()),
    path('init/', views.InitApi.as_view()),
    path('eligibility/', views.EligibilityExamApi.as_view()),
    path('apply/', views.ApplyAPI.as_view()),
    path('parents/', views.ParentsView.as_view()),
    path('bookmark/', views.BookmarkApi.as_view()),
    path('getvisitedcollege/', views.VisitCollegeApi.as_view()),
    path('essay/', views.EssayAPI.as_view()),
    path('test/<str:name>/', views.Test.as_view()),
    path('profilepic/', views.ChangeStudentProfile.as_view()),
    # path('sop/',views.SOPAPIViews.as_view()),
    path('citizenship/', views.CitizensipApi.as_view()),
    path('passport/', views.PassportAPI.as_view()),
    path('viewcomment/', views.StudentApplicationComment.as_view()),
    path('studentcouncilor/', views.StudentCouncilorView.as_view()),
    path('lor/', views.StudentLORApi.as_view())

    # path('')
]
