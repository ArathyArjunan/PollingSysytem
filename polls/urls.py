from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MyVotesView, PollListView, PollDetailView, VoteView, PollResultsView, PollExportView, current_user, frontend_index, frontend_poll, frontend_results, poll_results,register

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("polls/", PollListView.as_view(), name="poll-list"),
    path("polls/<int:pk>/", PollDetailView.as_view(), name="poll-detail"),
    path("polls/<int:poll_id>/vote/", VoteView.as_view(), name="poll-vote"),
    # path("polls/<int:poll_id>/results/", PollResultsView.as_view(), name="poll-results"),
    path("polls/<int:poll_id>/export/", PollExportView.as_view(), name="poll-export"),
     path("", frontend_index, name="frontend-index"),
    path("polls-frontend/poll.html", frontend_poll, name="frontend-poll"),
    path("polls-frontend/results.html", frontend_results, name="frontend-results"),
    path("register/", register, name="register"),
    path("my-votes/", MyVotesView.as_view()),
    path("current-user/", current_user),
    path("polls/<int:poll_id>/results/", poll_results),
]
