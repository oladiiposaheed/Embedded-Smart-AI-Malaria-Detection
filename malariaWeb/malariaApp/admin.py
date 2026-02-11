from django.contrib import admin
from malariaApp.models import PredictionModel
# Register your models here.

@admin.register(PredictionModel)
class PredictionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'result', 'created_at')
    readonly_fields = ('created_at',)
