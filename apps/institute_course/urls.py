from django.urls import path

from apps.institute_course import views

urlpatterns = [
    path(
        '<str:institute_id>/add',
        views.AddInstituteCourse.as_view(),
        name = 'add-gallery'
    ),
    path(
        '<institute_id>/get',
        views.ListInstituteCourse.as_view(),
        name = 'get-institute-course'
    ),
    path(
        '<institute_course_id>/update',
        views.UpdateInstituteCourse.as_view(),
        name = 'update-course'
    ),
    path(
        '<institute_course_id>/delete',
        views.DeleteInstituteCourseView.as_view(),
        name = 'delete-course'
    ),
    path(
        'listfaculty',
        views.ListFacultyView.as_view(),
        name = 'list-faculty'
    ),
    path(
        '<faculty_id>/listcourse',
        views.ListCourseView.as_view(),
        name='list course'
    ),
    path(
        'apply',
        views.ApplyInstituteCourseView.as_view(),
        name = 'apply'
    ),
    path(
        '<apply_id>/application/comment',
        views.AddCommentApplicationView.as_view(),
        name= 'comment-apply'
    ),
    path(
        '<institute_id>/application/list',
        views.ListStudentApplicationView.as_view(),
        name='list-application'
    ),
    path(
        '<consultancy_id>/application/consultancy/list',
        views.ListStudentApplicationForCounsultancy.as_view(),
        name="application-consultancy"
    ),
    path(
        '<apply_id>/application/detail',
        views.GetMyApplicationDetailView.as_view(),
        name="application-detail"
    ),
    path(
        '<apply_id>/application/institute/detail',
        views.GetStudentApplicationDetailForInstitute.as_view(),
        name = "application-detail-for-institute"
    ),
    path(
        '<apply_id>/application/cancel',
        views.CancleStudentApplication.as_view(),
        name='cancel-application'
    ),
    path(
        '<student_id>/student/application/list',
        views.ListMyStudentApplication.as_view(),
        name="std-application"
    ),
    path(
        '<apply_id>/application/comment/list',
        views.GetListCommentApplicationView.as_view(),
        name="list-comment"
    ),
    path(
        '<institute_id>/applicant/dashboard/count',
        views.ApplicantDashboard.as_view(),
        name = 'applicant-count'
    ),

    path(
        '<institute_course_id>/course/compare',
        views.CompareInstituteView.as_view(),
        name="compare-coure"
    )

]
