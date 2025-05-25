from django.contrib import admin
from .models import Mushroom, SourdoughStep, BoardgameTrivia

admin.site.register(Mushroom)
admin.site.register(SourdoughStep)
admin.site.register(BoardgameTrivia)

# Register your models here.
