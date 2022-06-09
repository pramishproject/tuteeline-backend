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
        '<apply_id>/application/cancle',
        views.CancleStudentApplication.as_view(),
        name='cancle-application'
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
    # path(
    #     '<student_id>/<institute_course_id>/document_tracker',
    #     views.StudentMarkToSendView.as_view(),
    #     name="document_tracker"
    # ),
    path(
        '<institute_course_id>/course/compare',
        views.CompareInstituteView.as_view(),
        name="compare-coure"
    ),
    path(
        'access',
        views.StudentAccessDetail.as_view(),
        name="response"
    )

]
