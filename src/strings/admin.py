from django.contrib import admin

# Register your models here.
from strings.models import Product, fabricModel, PRODUCTS
from json import dumps
from subprocess import Popen, PIPE

PYTHON = '/usr/local/bin/python'
SUPERVISOR = '/usr/bin/supervisorctl'
KILL = '/bin/kill'
WORKDIR = '/opt/webapp'

def run_migrate(product):
    result = {}
    result[product.pk] = {}
    # makemigration
    result[product.pk]['makemigrations'] = {}
    cmd = [PYTHON, 'manage.py', 'makemigrations', 'strings']
    print "Makemigration: " + "{0}_{1}".format(product.name, product.category)
    p = Popen(cmd, cwd=WORKDIR, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (raw, err) = p.communicate()
    print ''.join(raw)
    print ''.join(err)
    result[product.pk]['makemigrations']['output'] = ''.join(raw)
    result[product.pk]['makemigrations']['error'] = ''.join(err)
    # migrate
    result[product.pk]['migrate'] = {}
    cmd = [PYTHON, 'manage.py', 'migrate', 'strings']
    print "Migrate: " + "{0}_{1}".format(product.name, product.category)
    p = Popen(cmd, cwd=WORKDIR, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (raw, err) = p.communicate()
    print ''.join(raw)
    print ''.join(err)
    result[product.pk]['migrate']['output'] = ''.join(raw)
    result[product.pk]['migrate']['error'] = ''.join(err)
    # restart django gunicorn
    result[product.pk]['restart_gunicorn'] = {}
#     cmd = [KILL, '-HUP', "`cat /var/run/gunicorn.pid`"]
    cmd = [KILL, '-HUP', "1"]
    print "Restart Gunicorn: " + "{0}_{1}".format(product.name, product.category)
    p = Popen(cmd, cwd=WORKDIR, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (raw, err) = p.communicate()
    print ''.join(raw)
    print ''.join(err)
    result[product.pk]['restart_gunicorn']['output'] = ''.join(raw)
    result[product.pk]['restart_gunicorn']['error'] = ''.join(err)
    return result

def run_withdraw(product):
    result = {}
    result[product.pk] = {}
    # makemigration
    result[product.pk]['makemigrations'] = {}
    cmd = [PYTHON, 'manage.py', 'makemigrations', 'strings']
    print "Makemigration: " + "{0}_{1}".format(product.name, product.category)
    p = Popen(cmd, cwd=WORKDIR, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (raw, err) = p.communicate()
    print ''.join(raw)
    print ''.join(err)
    result[product.pk]['makemigrations']['output'] = ''.join(raw)
    result[product.pk]['makemigrations']['error'] = ''.join(err)
    # migrate
    result[product.pk]['migrate'] = {}
    cmd = [PYTHON, 'manage.py', 'migrate', 'strings']
    print "Migrate: " + "{0}_{1}".format(product.name, product.category)
    p = Popen(cmd, cwd=WORKDIR, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (raw, err) = p.communicate()
    print ''.join(raw)
    print ''.join(err)
    result[product.pk]['migrate']['output'] = ''.join(raw)
    result[product.pk]['migrate']['error'] = ''.join(err)
    # restart django gunicorn
    result[product.pk]['restart_gunicorn'] = {}
#     cmd = [KILL, '-HUP', "`cat /var/run/gunicorn.pid`"]
    cmd = [KILL, '-HUP', "1"]
    print "Restart Gunicorn: " + "{0}_{1}".format(product.name, product.category)
    p = Popen(cmd, cwd=WORKDIR, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (raw, err) = p.communicate()
    print ''.join(raw)
    print ''.join(err)
    result[product.pk]['restart_gunicorn']['output'] = ''.join(raw)
    result[product.pk]['restart_gunicorn']['error'] = ''.join(err)
    return result
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','status']
    ordering = ['name','category']
    readonly_fields = ['status']
    actions = ['migrate', 'publish', 'withdraw']
    
    def publish(self, request, queryset):
        '''
        Run python manage.py makemigrations && python manage.py withdraw table
        '''
        output = []
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "1 table was"
        else:
            message_bit = "%s tables were" % rows_updated
        self.message_user(request, "%s successfully marked as migrated.\n%s" % (message_bit, dumps(output)))
        
    publish.short_description = "Published selected table for translation."
    
    def migrate(self, request, queryset):
        '''
        Run python manage.py makemigrations && python manage.py migrate
        '''
        output = []
        for obj in queryset:
            output.append(run_migrate(obj))
            PRODUCTS["{0}_{1}".format(obj.name, obj.category)] = fabricModel(obj)
            PRODUCTS["{0}_{1}".format(obj.name, obj.category)].add2vc(obj)
        rows_updated = queryset.update(status='m')
        if rows_updated == 1:
            message_bit = "1 table was"
        else:
            message_bit = "%s tables were" % rows_updated
        self.message_user(request, "%s successfully marked as migrated.\n%s" % (message_bit, dumps(output)))
    migrate.short_description = "Migrate selected table to prepare for input."    
    
    # TODO: This action must be part of delete process
    def withdraw(self, request, queryset):
        '''
        Run python manage.py makemigrations && python manage.py withdraw table
        '''
        output = []
#         for obj in queryset:
#             output.append(run_withdraw(obj))
            
        rows_updated = queryset.update(status='w')
        if rows_updated == 1:
            message_bit = "1 table was"
        else:
            message_bit = "%s tables were" % rows_updated
        self.message_user(request, "%s successfully marked as migrated.\n%s" % (message_bit, dumps(output)))
    withdraw.short_description = "Withdraw selected table to prepare for input."    
admin.site.register(Product, ProductAdmin)
