from django.urls import include, path
from . import views
from .search.views import SearchCollege
from .User.utils.refrace_token import refresh_token_view
from .filtering.views import CollegeFilteringApi
from .search.views import SearchListApi, SearchApplicationForm

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('college/<int:id>/',views.CollegeApiViews.as_view()),
    path('collegeinfo/<page>/', views.CollegePageApi.as_view()),
    path('myinstituteOperation/', views.CollegeApiViews.as_view()),
    path('addCourse/', views.AddCourse.as_view()),
    path('courselist/<cid>/<fid>/', views.CollegeCourceListAPI.as_view()),
    path('course_detail/<cid>/<courceId>/', views.CourseDetailApi.as_view()),
    path('availablecourse/<fid>/', views.CollegeCourse.as_view()),
    path('availableFaculty/', views.CollegeFaculty.as_view()),
    # path('chooseDocument/', views.DocumentApi.as_view()),
    path('chooseFacility/', views.FacilityAPI.as_view()),
    path('add_facility/', views.AddFacilityApi.as_view()),
    path('detail/', views.CollegeDetailAPI.as_view()),
    path('college/login/', views.Login.as_view()),
    path('college/refrace_token/', refresh_token_view),
    path('college/create_account/', views.UserRegisterApi.as_view()),
    path('college/search/', SearchCollege.as_view()),
    path('college/filtering/', CollegeFilteringApi.as_view()),
    path('college/searchlist/', SearchListApi.as_view()),
    path('college/gallery/', views.GallaryAPI.as_view()),
    path('college/statistics/', views.StatisticsApi.as_view()),
    path('college/application/', views.StudentApplication.as_view()),
    path('college/chart/', views.ChartApi.as_view()),
    path('college/student_detail/', views.ViewedStudentDetails.as_view()),
    path('college/notacceptablecountry/', views.NotAcceptableCountry.as_view()),
    path('locationupdate/', views.LocationAPI.as_view()),
    path('college/enrolled/', views.EnrolledStudentApi.as_view()),
    path('college/studentapplicationsearch/', SearchApplicationForm.as_view()),
    path('college/form/', views.FormOpen.as_view()),
    path('college/counselor/', views.CounselorAPI.as_view()),
    path('college/accomodation/', views.AccomodationApi.as_view()),
    path('college/canteen/', views.CanteenApi.as_view()),
    path('college/laboratory/', views.LaboratoryApi.as_view()),
    path('college/comment/', views.CommentApplication.as_view()),
    path('college/library/', views.Library.as_view())
]
# http://127.0.0.1:8000/college/application/
# http://127.0.0.1:8000/college/application/
# http://127.0.0.1:8000/college/student_detail/?sid=b41aa823-e41b-4ec1-902d-b8548ebb1162&&id=13
