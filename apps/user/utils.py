def upload_normal_user_avatar_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (instance.user.username, ext)

    return 'avatar/{}'.format(
        new_filename
    )
