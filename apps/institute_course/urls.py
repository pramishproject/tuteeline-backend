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
      '<institute_course_id>/detail',
      views.CourseDetailView.as_view(),
      name = 'institute-course-detail'
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
      '<doc_type>/<apply_doc_id>/check/doc/delete',
      views.DeleteCheckDocument.as_view(),
      name='delete-check-doc'
    ),
    path(
        '<doc_type>/<apply_doc_id>/<apply_id>/add',
        views.AddCheckDocument.as_view(),
        name="add-check-document"
    ),
    path(
        '<institute_staff_id>/institute_staff/assign/application/list',
        views.AssignInstituteStaffApplicationView.as_view(),
        name ="assign list",
    ),
    path(
      '<str:apply_id>/assign/institute/staff' ,
      views.AssignApplicationToInstituteStaff.as_view(),
      name = "assign application"
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
        views.CancelStudentApplication.as_view(),
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
        '<apply_id>/institute/application/action',
        views.ActionByInstitute.as_view(),
        name="institute-action"
    ),
    path(
        '<apply_id>/consultancy/application/action',
        views.ActionByConsultancy.as_view(),
        name="consultancy-application action"
    ),
    path(
        '<institute_id>/applicant/dashboard/count',
        views.ApplicantDashboard.as_view(),
        name = 'applicant-count'
    ),
    path(
        '<institute_id>/application/count',
        views.CountApplicationStatus.as_view(),
        name="count-application"
    ),
    path(
        '<institute_course_id>/course/compare',
        views.CompareInstituteView.as_view(),
        name="compare-coure"
    ),
    path(
        '<apply_id>/action/history',
        views.ListInstituteActionHistoryView.as_view(),
        name="history-action"
    ),
    path(
        '<str:application_id>/application_detail/pdf',
        views.DownloadStudentApplication.as_view()
    ),
    path(
        'csv',
        views.ApplicationCsv.as_view(),
        name="csv"
    ),
    path(
        'getCurrency',
        views.GetCurrency.as_view(),
        name="get currency"
    ),
    path(
        '<str:institute_id>/<str:date_to>/<str:date_from>/chart',
        views.InstituteChart.as_view(),
        name="institute-chart"
    ),
    path(
        '<str:apply_id>/request/application/fee',
        views.RequestForApplicationFeeView.as_view(),
        name="application-request-fee"
    ),
    path(
        '<str:apply_id>/approve/application/fee',
        views.ApproveApplicationVoucher.as_view(),
        name="approve-voucher"
    ),
    path(
        '<str:apply_id>/voucher/add',
        views.AddVoucherFile.as_view(),
        name= "add-voucher"
    ),
    path(
        '<str:voucher_id>/voucher/delete',
        views.DeleteVoucherFile.as_view(),
        name="delete-voucher"
    )
]
