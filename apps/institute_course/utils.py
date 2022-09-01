from django.db.models import Count
from django.db.models.functions import TruncDay

# from apps.institute_course.models import InstituteApply
from datetime import datetime
from django.utils.formats import get_format
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa

from django.core.exceptions import ValidationError
from django.utils.datetime_safe import datetime
from django.utils.text import slugify


def upload_voucher_file(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.apply), ext)

    return 'institute/voucher/{}'.format(
        new_filename
    )

def ImageAndPdfValidator(value):
    value = str(value).lower()
    print(value.endswith('.jpg'))
    if value.endswith('.pdf') != True and value.endswith(".jpg") != True and\
            value.endswith('png') != True and value.endswith('jpeg') != True :
        raise ValidationError("Only PDF and image can be uploaded")
    else:
        return value
# def get_student_application_status(student_id):
#     application=InstituteApply.objects.filter(
#         student=student_id
#         # created_at__range=["2021-12-01", "2022-01-31"]
#     ).annotate(date=TruncDay('created_at')).values("date", "action"). \
#         annotate(action_count=Count('action'))
#
#     print(application)
#     return application



# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     # if not pdf.err:
     #     return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None



def parse_date(date_str):
    """Parse date from string by DATE_INPUT_FORMATS of current language"""
    for item in get_format('DATE_INPUT_FORMATS'):
        try:
            return datetime.strptime(date_str, item).date()
        except (ValueError, TypeError):
            continue

    return None