from django.db import models
 
# Create your models here.
from django.utils import timezone
# from versions.models import Versionable, VersionedForeignKey
from simple_history.models import HistoricalRecords
from simple_history import register
from django.contrib.auth.models import User, Group
from django.contrib import admin
 
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from svn_manager.models import Repo, SVNManager
from os import path, mkdir
import json, codecs

PRODUCT_CHOICES = (
    ('BETAGO','FIFA Online'),
)

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('m', 'Migrated'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)

repo = Repo()

register(User, inherit=True)
    
class Product(models.Model):
    name = models.CharField(max_length=10, choices=PRODUCT_CHOICES)
    category = models.CharField(max_length=18)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    
    class Meta:
        unique_together = ('name','category')
         
    def __unicode__(self):
        return "{0}_{1}".format(self.name, self.category)
     
    def clean(self):
        '''
        trim whitespace
        '''
        self.category = self.category.strip()
        '''
        replace space with _
        '''
        self.category = self.category.replace(' ', '_')
        '''
        uppercase
        '''
        self.category = self.category.upper()
        pass
    
    def save(self, *args, **kwargs):
        '''
        TODO: Versionable end_date must be same for all, then this enddate time must be provided by user history
        '''
        self.full_clean()
        return super(Product, self).save(*args, **kwargs)
    
    def add2svn(self):
        svnMgr = PRODUCTS["{0}_{1}".format(self.name, self.category)].add2vc(self)
        return svnMgr
    def commit_to_vc(self, username, *args):
        try:
            user = User.objects.get(username=username)
        except (KeyError, User.DoesNotExist):
            '''
            TODO: exception
            '''
            pass
        '''
        Save the table into each respective json string file
        '''
#         db = fabric(self)
        queries = PRODUCTS["{0}_{1}".format(self.name, self.category)].objects.all()
        svnMgr = PRODUCTS["{0}_{1}".format(self.name, self.category)].commit2vc(self, queries, user)
        '''
        Create Commit Log
        '''
        #PRODUCTS["{0}_{1}".format(self.name, self.category)].commit2svn(self, user)
        '''
        Commit only changed json string file
        '''
        return svnMgr
class LanguageStringModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['stringid']
         
    stringid = models.CharField(max_length=200, primary_key=True)
    description1 = models.CharField(max_length=255, default='', blank=True)
    description2 = models.CharField(max_length=255, default='', blank=True)
    
    '''
    Translations
    '''
    Korea = models.TextField()
    Korea_modified_at = models.DateTimeField(default=timezone.now)
    English = models.TextField(null=True, blank=True)
    English_modified_at = models.DateTimeField(default=timezone.now)
    Thailand = models.TextField(null=True, blank=True)
    Thailand_modified_at = models.DateTimeField(default=timezone.now)
    China = models.TextField(null=True, blank=True)
    China_modified_at = models.DateTimeField(default=timezone.now)
    Indonesia = models.TextField(null=True, blank=True)
    Indonesia_modified_at = models.DateTimeField(default=timezone.now)
    Vietnam = models.TextField(null=True, blank=True)
    Vietnam_modified_at = models.DateTimeField(default=timezone.now)
    
    __Korea = None
    __English = None
    __Thailand = None
    __China = None
    __Indonesia = None
    __Vietnam = None
    def __setOriginal(self):
        self.__Korea = self.Korea
        self.__English = self.English
        self.__Thailand = self.Thailand
        self.__China = self.China
        self.__Indonesia = self.Indonesia
        self.__Vietnam = self.Vietnam
    def __init__(self, *args, **kwargs):
        super(LanguageStringModel, self).__init__(*args, **kwargs)
        self.__setOriginal()
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.full_clean()
        self.setTimeStamp()
        super(LanguageStringModel, self).save(force_insert=False, force_update=False, *args, **kwargs)
        self.__setOriginal()
    def setTimeStamp(self):
        if self.Korea != self.__Korea:
            self.Korea_modified_at = timezone.now()
        if self.English != self.__English:
            self.English_modified_at = timezone.now()
        if self.Thailand != self.__Thailand:
            self.Thailand_modified_at = timezone.now()
        if self.China != self.__China:
            self.China_modified_at = timezone.now()
        if self.Indonesia != self.__Indonesia:
            self.Indonesia_modified_at = timezone.now()
        if self.Vietnam != self.__Vietnam:
            self.Vietnam_modified_at = timezone.now()
    def clean(self):
        '''
        Custom validation
        trim whitespace
        '''
        self.stringid = self.stringid.strip()
        '''
        replace space with _
        '''
        self.stringid = self.stringid.replace(' ', '_')
        '''
        uppercase everything
        '''
        self.stringid = self.stringid.upper()
        '''
        if null, set to ""
        '''
        if self.English is None:
            self.English = ""
        if self.Thailand is None:
            self.Thailand = ""
        if self.China is None:
            self.China = ""
        if self.Indonesia is None:
            self.Indonesia = ""
        if self.Vietnam is None:
            self.Vietnam = ""
        
    def __unicode__(self):
        return self.stringid
    @classmethod
    def add2vc(self, product,*args):
        '''
        TODO: store each colum into <itemname>_<languages>.json text file (not json file)
        '''
        #print type(product)
        #print type(queries)
        groups = Group.objects.exclude(name='admin')
        tablename = self._meta.db_table.split('_',2)
        workdir = path.join(repo.workdir, tablename[0].upper())
        changelist = 'Initial Commit -'+timezone.now().strftime("%Y-%m-%d_%H:%M:%S")
        svn = SVNManager(repo, changelist, tablename[0].upper(), tablename[1].upper())
        if not path.exists(workdir):
            mkdir(workdir)
            # New SVN node
            svn.add(workdir)
            svn.commit("Adding_New_Product:"+tablename[0].upper())
            pass
        
        for group in groups:
            # save as text file to vc workdir
            # create template json file
            filename = "{0}_{1}.json".format(tablename[1].upper(), group.name[0:3].upper())
            filepath = path.join(workdir, filename)
            jsonString = "{}"
            with codecs.open(filepath, "w+", encoding="utf-8") as outfile:
                outfile.write(jsonString)
            outfile.close()
            svn.add(filepath)
         
        svn.commit(changelist)
        return svn

    @classmethod
    def commit2vc(self, product, queries, user, *args):
        '''
        TODO: store each colum into <itemname>_<languages>.json text file (not json file)
        '''
        groups = user.groups.exclude(name='admin').exclude(name='manager')
        converted = {}
        for row in queries:
#             print type(row)
            for group in groups:
                if (not group.name in converted.keys()):
                    converted[group.name] = {}
                    pass
#                 if (not row.stringid in converted[group.name].keys()):
#                     converted[group.name][row.stringid] = ""
#                 print row
                converted[group.name][row.stringid] = getattr(row, group.name)
                pass
            pass
         
        tablename = self._meta.db_table.split('_',2)
        workdir = path.join(repo.workdir, tablename[0].upper())
        changelist = user.username+'-'+timezone.now().strftime("%Y-%m-%d_%H:%M:%S")
        svn = SVNManager(repo, changelist, tablename[0].upper(), tablename[1].upper())
        if not path.exists(workdir):
            mkdir(workdir)
            # New SVN node
            svn.add(workdir)
            svn.commit("Adding New Product"+tablename[0].upper())
            pass
        
        for group in groups:
            # save as text file to vc workdir
            # create template json file
            filename = "{0}_{1}.json".format(tablename[1].upper(), group.name[0:3].upper())
            filepath = path.join(workdir, filename)
            jsonString = json.dumps(converted[group.name], sort_keys=True,
                                    ensure_ascii=False, indent=4, separators=(',', ': '))
            with codecs.open(filepath, "w+", encoding="utf-8") as outfile:
                outfile.write(jsonString)
            outfile.close()
            svn.add_to_changelist(filepath)
         
        svn.commit(changelist)
        return svn
    
    @classmethod
    def diff(self):
        return self
    def importJson(self):
        return self
    
 
class LanguageStringResource(resources.ModelResource):
     
#     def get_instance(self, instance_loader, row):
#         return False
    
    stringid = fields.Field(column_name='id', attribute='stringid')
    Korea = fields.Field(column_name='kor', attribute='Korea')
    English = fields.Field(column_name='eng', attribute='English')
    Thailand = fields.Field(column_name='tha', attribute='Thailand')
    China = fields.Field(column_name='chi', attribute='China')
    Indonesia = fields.Field(column_name='ind', attribute='Indonesia')
    Vietnam = fields.Field(column_name='vie', attribute='Vietnam')
     
    class Meta:
        model = LanguageStringModel
        skip_unchanged = True
        import_id_fields = ('stringid',)
        fields = ('stringid','description1','description2')
        ordering = ['stringid',]
         
    def trim_field(self, data, **kwargs):
        cleaned_data = data;
        return cleaned_data;
    
class LanguageStringModelAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = LanguageStringResource
    
    fieldsets = [
        (None, {'fields': [('stringid'), ('description1', 'description2'), ('Korea', 'English', 'Thailand', 'China', 'Indonesia', 'Vietnam',)]}),
    ]
    list_display = ('stringid', 'description1', 'description2', 'Korea', 'Korea_modified_at', 
                    'English', 'English_modified_at', 'China', 'China_modified_at', 
                    'Thailand', 'Thailand_modified_at', 'Indonesia', 'Indonesia_modified_at',
                    'Vietnam','Vietnam_modified_at',)
    ordering = ['stringid','description1', 'description2']
    search_fields = ['stringid', 'description1', 'description2', 'Korea', 'English']
    
def fabricModel(product, baseclass=LanguageStringModel, resourceclass=LanguageStringResource, adminclass=LanguageStringModelAdmin, admin_opts=None):
    '''
    Generating Dynamic Models
    '''
    class MyClassMetaClass(models.base.ModelBase):
        def __unicode__(self):
            return "{0}_{1}".format(product.name, product.category)
 
        def __new__(cls, name, bases, attrs):
            name = "{0}_{1}".format(product.name, product.category)
            return models.base.ModelBase.__new__(cls, name, bases, attrs)
    class MyClass(baseclass):
        __metaclass__ = MyClassMetaClass
        history = HistoricalRecords()
        class Meta:
            db_table = "{0}_{1}".format(product.name, product.category)
            abstract = False
        
    '''
    Register Model to Admin.site
    '''    
    if admin_opts is not None:
        for key, value in admin_opts:
            setattr(adminclass, key, value)
    for reg_model in admin.site._registry.keys():
        if MyClass._meta.db_table == reg_model._meta.db_table:
            del admin.site._registry[reg_model]
     
    class MyClassResource(resourceclass):
        class Meta:
            model = MyClass
     
    class MyClassAdmin(adminclass):
        resource_class = MyClassResource
    # Try the regular approach too, but this may be overdoing it
    try:
        admin.site.unregister(MyClass)
    except:
        pass    
    admin.site.register(MyClass, MyClassAdmin)
    return MyClass

PRODUCTS = {}

try:
    for product in Product.objects.all():
        PRODUCTS["{0}_{1}".format(product.name, product.category)] = fabricModel(product)
except:
    pass
