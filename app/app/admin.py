from app import models

from django.contrib import admin


admin.site.register(models.Tag)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Profile)
admin.site.register(models.QuestionVote)
admin.site.register(models.AnswerVote)
