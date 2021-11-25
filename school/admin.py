# from django.contrib import admin
# from .models import *

# # Register your models here.
# admin.site.register(User)
# admin.site.register(Principal)
# admin.site.register(AcademicYear)
# admin.site.register(Classes)
# admin.site.register(Teacher)
# admin.site.register(Subjects)
# admin.site.register(Student)
# admin.site.register(Results)
# admin.site.register(report)
# admin.site.register(Fees)



from django.apps import apps
from django.contrib import admin

# Register your models here.
# all other models


class ListAdminMixin(object):
    def _init_(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        self.list_per_page = 10
        super(ListAdminMixin, self)._init_(model, admin_site)


models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass