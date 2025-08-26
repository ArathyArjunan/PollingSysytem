from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Polls, Question, Choice, Vote


class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)


    class Meta:
        model = Choice
        fields = ["id", "text", "votes_count"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)


    class Meta:
        model = Question
        fields = ["id", "text", "choices"]


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    is_active = serializers.BooleanField(read_only=True)


    class Meta:
        model = Polls
        fields = ["id", "title", "description", "start_date", "end_date", "is_active", "questions"]


class VoteSerializer(serializers.ModelSerializer):
    poll_title = serializers.CharField(source="poll.title", read_only=True)
    question_text = serializers.CharField(source="question.text", read_only=True)
    choice_text = serializers.CharField(source="choice.text", read_only=True)

    class Meta:
        model = Vote
        fields = ["id", "poll", "poll_title", "question", "question_text", "choice", "choice_text", "voted_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]



class ChoiceSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text"]

class QuestionSerializerList(serializers.ModelSerializer):
    choices = ChoiceSerializerList(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "choices"]

class PollSerializerList(serializers.ModelSerializer):
    questions = QuestionSerializerList(many=True, read_only=True)

    class Meta:
        model = Polls
        fields = ["id", "title", "description", "questions"]