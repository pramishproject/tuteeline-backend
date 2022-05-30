from datetime import date, timedelta
import datetime
from datetime import date

from apps.student.models import StudentApply


def date_wise_filter(id):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    totaldays = 7
    data = {}
    for i, item in enumerate(days):
        now = datetime.datetime.now()
        day = now - timedelta(days=totaldays - i)
        dayformat = day.strftime("%Y-%m-%d %H:%M:%S")
        keyinitialize = datetime.datetime.strptime(dayformat, '%Y-%m-%d %H:%M:%S').weekday()
        applyed = StudentApply.objects.filter(college=id, apply_date__lte=day).count()
        accept = StudentApply.objects.filter(college=id, status=1, apply_date__lte=day).count()
        reject = StudentApply.objects.filter(college=id, status=2, apply_date__lte=day).count()
        pending = StudentApply.objects.filter(college=id, status=3, apply_date__lte=day).count()
        data.update({days[keyinitialize]: [applyed, accept, reject, pending]})
    return data


def application_report_count(cid, day):
    enddate = datetime.datetime.now()
    if day == '0':
        applyed = StudentApply.objects.filter(college=cid, apply_date__lte=enddate).count()
        accept = StudentApply.objects.filter(college=cid, status=1, apply_date__lte=enddate).count()
        reject = StudentApply.objects.filter(college=cid, status=2, apply_date__lte=enddate).count()
        pending = StudentApply.objects.filter(college=cid, status=3, apply_date__lte=enddate).count()

    else:
        startdate = enddate - timedelta(days=int(day))
        applyed = StudentApply.objects.filter(college=cid, apply_date__range=[startdate, enddate]).count()
        accept = StudentApply.objects.filter(college=cid, status=1, apply_date__range=[startdate, enddate]).count()
        reject = StudentApply.objects.filter(college=cid, status=2, apply_date__range=[startdate, enddate]).count()
        pending = StudentApply.objects.filter(college=cid, status=3, apply_date__range=[startdate, enddate]).count()

    data = {'applyed': applyed, 'accept': accept, 'pending': pending, 'reject': reject}
    return data


def count_yeardata(id, year):
    data = {}
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'july', 'aug', 'sep', 'oct', 'nov', 'dec']
    today = date.today()
    # df = pd.DataFrame(list(StudentApply.objects.filter(college=id,apply_date__year=year).values('status',
    # 'apply_date'))) print(df[df.apply_date.dt.month==1][ df.status==1].shape[0])

    for i, item in enumerate(months):
        # data.update({months[i]:[df[df.apply_date.dt.month==i+1].shape[0],df[df.apply_date.dt.month==i+1][
        # df.status=='1'].shape[0],df[df.apply_date.dt.month==i+1][ df.status=='2'].shape[0],
        # df[df.apply_date.dt.month==i+1][ df.status=='3'].shape[0]]})
        applyed = StudentApply.objects.filter(college=id, apply_date__year=year, apply_date__month=i + 1).count()
        accept = StudentApply.objects.filter(college=id, status=2, apply_date__year=year,
                                             apply_date__month=i + 1).count()
        reject = StudentApply.objects.filter(college=id, status=3, apply_date__year=year,
                                             apply_date__month=i + 1).count()
        pending = StudentApply.objects.filter(college=id, status=4, apply_date__year=year,
                                              apply_date__month=i + 1).count()
        data.update({months[i]: [applyed, accept, reject, pending]})
    return data
