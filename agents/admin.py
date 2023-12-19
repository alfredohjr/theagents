from django.contrib import admin

from .models import (
    Agent, 
    Prompt, 
    BudgedMonth, 
    Data,
    Chat,
    ChatExtraInformation,
)

# Register your models here.

admin.site.register(Agent)
admin.site.register(Prompt)
admin.site.register(BudgedMonth)
admin.site.register(Data)
admin.site.register(Chat)
admin.site.register(ChatExtraInformation)