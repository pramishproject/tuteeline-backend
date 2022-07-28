from django.db.models import Count
from django.db.models.functions import TruncDay

from apps.institute_course.models import InstituteApply


def get_student_application_status(student_id):
    application=InstituteApply.objects.filter(
        student=student_id
        # created_at__range=["2021-12-01", "2022-01-31"]
    ).annotate(date=TruncDay('created_at')).values("date", "action"). \
        annotate(action_count=Count('action'))

    print(application)
    return application

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None