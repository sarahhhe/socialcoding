from django.contrib import admin
from django.db import models
from .models import Post, Vote, Response, Category, ResponseVote, UserCategory

from. import models as demo_models
from mdeditor.widgets import MDEditorWidget

class CodeSnippetAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }

# Register your models here.
admin.site.register(Post)
admin.site.register(Response)
admin.site.register(Vote)
admin.site.register(Category)
admin.site.register(UserCategory)
admin.site.register(ResponseVote)
