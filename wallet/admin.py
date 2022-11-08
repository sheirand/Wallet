from django.contrib import admin
from wallet.models import Organization, Categories, Transaction

admin.site.register(Organization)
admin.site.register(Categories)
admin.site.register(Transaction)
