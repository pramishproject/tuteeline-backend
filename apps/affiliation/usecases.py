from apps.affiliation.models import Affiliation
from apps.core.usecases import BaseUseCase
from apps.affiliation.exceptions import UniqueKeyError, UniversityIsNotAffiliated, CollegeIsNotAffiliated, \
    MultipleUniversityError, TypeValidationError
from django.db import IntegrityError

from apps.institute.models import Institute
from apps.institute_course.models import InstituteApply


class AddAffiliationUseCase(BaseUseCase):
    def __init__(self,institute:Institute,serializer):
        self._institute = institute
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            if self._institute.category == "University":
                raise UniversityIsNotAffiliated

            if self._data.get("university").category == "College":
                raise CollegeIsNotAffiliated

            # if self._data.get("course")['type'] == None:
            #     raise CollegeIsNotAffiliated
            if self._data.get("course").get("type") == None:
                raise TypeValidationError
            affiliation = Affiliation.objects.filter(institute = self._institute)
            if len(affiliation)>0:
                for i in affiliation:
                    if i.course.get('type')=="ALL":
                        raise MultipleUniversityError
                    else:
                        self.affCourse = i.course.get("course")
                        self.courseData = self._data.get("course").get("course")
                        if self.affCourse ==None or self.courseData == None:
                            continue
                        if self.compare_listDate():
                            raise MultipleUniversityError

            Affiliation.objects.create(
                institute = self._institute,
                **self._data,
            )
        except IntegrityError:
            raise UniqueKeyError

    def compare_listDate(self):

        for i in self.affCourse:
            for j in self.courseData:
                if i["id"] == j["id"]:
                    return True
        return False

class ListAffiliation(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self.affiliation

    def _factory(self):
        self.affiliation = Affiliation.objects.filter(institute=self._institute).select_related("institute","university")

class ForwardApplicationUseCase(BaseUseCase):
    def __init__(self,university,institute):
        self._university = university
        self._institute = institute

    def execute(self):
        self._factory()

    def _factory(self):
        InstituteApply.objects.filter(institute=self._institute).update()