from django.contrib import admin

# Register your models here.
from settings.models.cloud_secret import Cloud_Secret
from settings.models.zone import Zone
from settings.models.qywx_robot import QywxRobot

class AdminCloud_Secret(admin.ModelAdmin):
    # fields = '__all__'
    list_display = ('name', 'secretid', 'secretkey', 'comment', 'created_by')
admin.site.register(Cloud_Secret, AdminCloud_Secret)

class adminZone(admin.ModelAdmin):
    # fields = '__all__'
    list_display = ('name', 'byname', 'cloud', 'created_by')

admin.site.register(Zone, adminZone)

class adminQywxRobot(admin.ModelAdmin):
    # fields = '__all__'
    list_display = ('name', 'byname', 'key', 'created_by')

admin.site.register(QywxRobot, adminQywxRobot)


