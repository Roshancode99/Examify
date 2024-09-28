from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StrategyName)
admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(Test)
admin.site.register(Clients)
admin.site.register(TestsQuestionsRelation)
admin.site.register(QuestionAttempt)
admin.site.register(TestInvitation)
admin.site.register(TestAttempt)
admin.site.register(TabSwitchActivity)
admin.site.register(WindowSwitchActivity)
admin.site.register(CopyPasteActivity)
admin.site.register(TestPing)
admin.site.register(McqOptions)