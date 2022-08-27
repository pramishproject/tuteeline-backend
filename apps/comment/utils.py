from django.utils.text import slugify
from datetime import datetime, timedelta
import time
def upload_comment_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.user_id), ext)
    dtime = datetime.now() + timedelta(seconds=3)
    unixtime = time.mktime(dtime.timetuple())
    return 'application/comment/'+str(unixtime)+"/"+'{}'.format(
        new_filename
    )