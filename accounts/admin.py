from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client, Model, Applicant, Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'approved')
    list_filter = ('approved',)
    actions = ['approve_agents']

    def approve_agents(self, request, queryset):
        queryset.update(approved=True)
    approve_agents.short_description = "Approve selected agents"

admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Model)
admin.site.register(Applicant)
admin.site.register(Agent, AgentAdmin)