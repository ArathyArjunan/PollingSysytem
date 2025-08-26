
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
import csv
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny

from .models import Polls, Question, Choice, Vote
from .serializers import PollSerializer, VoteSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class PollListView(generics.ListAPIView):
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        q=Polls.objects.all()
        return q

class PollDetailView(generics.RetrieveAPIView):
    queryset = Polls.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]

class VoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, poll_id):
        poll = get_object_or_404(Polls, pk=poll_id)
        question_id = request.data.get("question")
        choice_id = request.data.get("choice")

        question = get_object_or_404(Question, id=question_id, poll=poll)
        choice = get_object_or_404(Choice, id=choice_id, question=question)

        if Vote.objects.filter(user=request.user, question=question).exists():
            return Response({"error": "Already voted."}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(user=request.user, poll=poll, question=question, choice=choice)

        # Build results like WhatsApp
        results = []
        choices = question.choices.annotate(votes_count=Count("votes"))
        total = sum(c.votes_count for c in choices)
        for c in choices:
            pct = (c.votes_count / total * 100) if total else 0
            results.append({
                "choice_id": c.id,
                "choice": c.text,
                "votes": c.votes_count,
                "pct": round(pct, 2)
            })

        return Response({
            "poll": poll.title,
            "question": question.text,
            "total_votes": total,
            "results": results
        }, status=status.HTTP_201_CREATED)

class PollResultsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, poll_id):
        poll = get_object_or_404(Polls, pk=poll_id)
        data = []
        for q in poll.questions.all():
            choices = q.choices.annotate(votes_count=Count("votes"))
            total = sum(c.votes_count for c in choices)
            results = []
            for c in choices:
                pct = (c.votes_count / total * 100) if total else 0
                results.append({
                    "choice": c.text,
                    "votes": c.votes_count,
                    "pct": round(pct, 2)
                })
            data.append({
                "question": q.text,
                "total_votes": total,
                "results": results
            })
        return Response({"poll": poll.title, "results": data})

class PollExportView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, poll_id):
        poll = get_object_or_404(Polls, pk=poll_id)
        votes = Vote.objects.filter(poll=poll).select_related("user", "question", "choice")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename=poll_{poll.id}_votes.csv"
        writer = csv.writer(response)
        writer.writerow(["poll_id", "poll_title", "question", "choice", "user", "voted_at"])

        for v in votes:
            writer.writerow([poll.id, poll.title, v.question.text, v.choice.text, v.user.username, v.voted_at])
        return response


from django.shortcuts import render

def frontend_index(request):
    return render(request, "index.html")

def frontend_poll(request):
    return render(request, "poll.html")

def frontend_results(request):
    return render(request, "results.html")


@api_view(["POST"])
@permission_classes([AllowAny])  
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_staff
    })

# Admin-only: poll results
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def poll_results(request, poll_id):
    if not request.user.is_staff:
        return Response({"error": "Unauthorized"}, status=403)

    results = (
        Vote.objects.filter(poll_id=poll_id)
        .values("choice__text")
        .annotate(total=Count("id"))
    )
    return Response(list(results))

class MyVotesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        votes = Vote.objects.filter(user=request.user)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)