from django.contrib import admin
from models import Repo
from json import dumps
# Register your models here.

class RepoAdmin(admin.ModelAdmin):
    list_display = ['protocol','workdir','repodir']
    ordering = ['repodir','workdir']
    actions = ['checkout','commit']
    
    def checkout(self, request, queryset):
        output = []
        for obj in queryset:
            output.append(obj.checkout())
        rows_updated = len(output)
        if rows_updated == 1:
            message_bit = "1 table was"
        else:
            message_bit = "%s tables were" % rows_updated
        self.message_user(request, "%s successfully checked out.\n %s" % (message_bit, dumps(output)))
    checkout.short_description = "Checkout selected repos"
    
    def commit(self, request, queryset):
        output = []
        for obj in queryset:
            output.append(obj.commit())
        rows_updated = len(output)
        if rows_updated == 1:
            message_bit = "1 table was"
        else:
            message_bit = "%s tables were" % rows_updated
        self.message_user(request, "%s successfully committed working directories." % (message_bit, dumps(output)))
    commit.short_description = "Commit selected working directories."
    
admin.site.register(Repo, RepoAdmin)