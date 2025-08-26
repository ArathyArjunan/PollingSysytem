from django.contrib import admin
from .models import Polls, Question, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Polls)
class PollsAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "created_at", "is_active")
    search_fields = ("title",)
    list_filter = ("start_date", "end_date")
    inlines = [QuestionInline]

    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "poll")
    search_fields = ("text",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question")
    search_fields = ("text",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "poll", "question", "choice", "voted_at")
    list_filter = ("poll", "question")
    search_fields = ("user__username", "poll__title", "choice__text")
