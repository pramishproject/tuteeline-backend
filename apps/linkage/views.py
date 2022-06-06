from apps.core import generics

# Create your views here.

class LinkageInstituteAndConsultancy(generics.CreateWithMessageAPIView): #TODO create linkage
    pass

class GetLinkageConsultancy(generics.ListAPIView): #TODO list linkage
    pass

class LinkageGrantedByAdmin(generics.UpdateWithMessageAPIView): #TODO status change
    pass