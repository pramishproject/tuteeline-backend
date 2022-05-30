from django.contrib.auth.base_user import BaseUserManager


class StudentUserManager(BaseUserManager):
    def get_queryset(self):
        return super(StudentUserManager, self).get_queryset().filter(
            user_type='student_user'
        )
    def create(self, email, password=None, **kwargs):
        kwargs.update({
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'student_user',
            'username': email,
        })
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class InstituteUserManager(BaseUserManager):
    def get_queryset(self):
        return super(InstituteUserManager, self).get_queryset().filter(
            user_type='institute_user'
        )
    def create(self, email, password=None, **kwargs):
        kwargs.update({
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'institute_user',
            'username': email,
        })
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

class ConsultancyUserManager(BaseUserManager):
    def get_queryset(self):
        return super(ConsultancyUserManager, self).get_queryset().filter(
            user_type='consultancy_user'
        )

    def create(self, email, password=None, **kwargs):
        kwargs.update({
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'consultancy_user',
            'username': email,
        })
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class PortalUserManager(BaseUserManager):
    def get_queryset(self):
        return super(PortalUserManager, self).get_queryset().filter(
            user_type='portal_user'
        )

    def create(self, email, password=None, **kwargs):
        kwargs.update({
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'portal_user',
            'username': email,
        })
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
