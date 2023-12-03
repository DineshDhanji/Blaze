from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from .models import Post, User, Event, Answer, User, Reply, Notification
from .serializers import (
    LikeStatusSerializer,
    SavedStatusSerializer,
    FollowStatusSerializer,
    AnswerSerializer,
    UserSerializer,
    ReplySerializer,
    NotificationSerializer
)


# LIKE FOR EVENT
@api_view(["GET"])
def event_like_or_unlike(request, event_id):
    try:
        # Try to get the event object, return 404 if not found
        event = get_object_or_404(Event, pk=event_id)
    except Http404:
        # Event does not exist, return JsonResponse with appropriate message
        return Response(
            {"like_status": False, "error": "No such event exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if the user has already liked the event
    if request.user.liked_events.filter(pk=event_id).exists():
        # User has liked the event, remove the like
        request.user.liked_events.remove(event)
        like_status = False
    else:
        # User hasn't liked the event, add the like
        request.user.liked_events.add(event)
        like_status = True

    # Serialize the response data
    serializer = LikeStatusSerializer({"like_status": like_status, "error": None})

    # Return the serialized data as JSON response
    return Response(serializer.data)


@api_view(["GET"])
def event_check_like_or_unlike(request, event_id):
    try:
        # Try to get the event object, return 404 if not found
        event = get_object_or_404(Event, pk=event_id)
    except Http404:
        # Event does not exist, return JsonResponse with appropriate message
        return Response(
            {"like_status": False, "error": "No such event exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the response data
    serializer = LikeStatusSerializer(
        {"like_status": request.user.liked_events.filter(pk=event_id).exists()}
    )

    # Return the serialized data as JSON response
    return Response(serializer.data)


# LIKE FOR POST
@api_view(["GET"])
def like_or_unlike(request, post_id):
    try:
        # Try to get the post object, return 404 if not found
        post = get_object_or_404(Post, pk=post_id)
    except Http404:
        # Post does not exist, return JsonResponse with appropriate message
        return Response(
            {"like_status": False, "error": "No such post exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if the user has already liked the post
    if request.user.liked_post.filter(pk=post_id).exists():
        # User has liked the post, remove the like
        request.user.liked_post.remove(post)
        like_status = False
    else:
        # User hasn't liked the post, add the like
        request.user.liked_post.add(post)
        like_status = True

    # Serialize the response data
    serializer = LikeStatusSerializer({"like_status": like_status, "error": None})

    # Return the serialized data as JSON response
    return Response(serializer.data)


@api_view(["GET"])
def check_like_or_unlike(request, post_id):
    try:
        # Try to get the post object, return 404 if not found
        post = get_object_or_404(Post, pk=post_id)
    except Http404:
        # Post does not exist, return JsonResponse with appropriate message
        return Response(
            {"like_status": False, "error": "No such post exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the response data
    serializer = LikeStatusSerializer(
        {"like_status": request.user.liked_post.filter(pk=post_id).exists()}
    )

    # Return the serialized data as JSON response
    return Response(serializer.data)


# SAVED
@api_view(["GET"])
def save_or_unsave(request, post_id):
    try:
        # Try to get the post object, return 404 if not found
        post = get_object_or_404(Post, pk=post_id)
    except Http404:
        # Post does not exist, return JsonResponse with appropriate message
        return Response(
            {"saved_status": False, "error": "No such post exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if the user has already liked the post
    if request.user.saved_post.filter(pk=post_id).exists():
        # User has liked the post, remove the like
        request.user.saved_post.remove(post)
        saved_status = False
    else:
        # User hasn't liked the post, add the like
        request.user.saved_post.add(post)
        saved_status = True

    # Serialize the response data
    serializer = SavedStatusSerializer({"saved_status": saved_status, "error": None})

    # Return the serialized data as JSON response
    return Response(serializer.data)


@api_view(["GET"])
def check_save_or_unsave(request, post_id):
    try:
        # Try to get the post object, return 404 if not found
        post = get_object_or_404(Post, pk=post_id)
    except Http404:
        # Post does not exist, return JsonResponse with appropriate message
        return Response(
            {"saved_status": False, "error": "No such post exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the response data
    serializer = SavedStatusSerializer(
        {"saved_status": request.user.saved_post.filter(pk=post_id).exists()}
    )

    # Return the serialized data as JSON response
    return Response(serializer.data)


# FOLLOW
@api_view(["GET"])
def check_follow_or_unfollow(request, user_id):
    try:
        # Try to get the user object, return 404 if not found
        user = get_object_or_404(User, pk=user_id)
    except Http404:
        # User does not exist, return JsonResponse with appropriate message
        return Response(
            {"follow_status": False, "error": "No such user exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )
    if user == request.user:
        return Response(
            {"follow_status": False, "error": "user entity can not follow itself."}
        )
    # Serialize the response data
    serializer = FollowStatusSerializer(
        {"follow_status": request.user.follow.filter(pk=user_id).exists()}
    )

    # Return the serialized data as JSON response
    return Response(serializer.data)


@api_view(["GET"])
def follow_or_unfollow(request, user_id):
    try:
        # Try to get the user object, return 404 if not found
        user = get_object_or_404(User, pk=user_id)
    except Http404:
        # User does not exist, return JsonResponse with appropriate message
        return Response(
            {"follow_status": False, "error": "No such user exists in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if user == request.user:
        return Response(
            {"follow_status": False, "error": "user entity can not follow itself."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if the requested user is already following the user
    if request.user.follow.filter(pk=user.pk).exists():
        # User follows the requested user, remove the follow
        request.user.follow.remove(user)
        saved_status = False
    else:
        # User does not follow the requested user, add the follow
        request.user.follow.add(user)
        saved_status = True

    # Serialize the response data
    serializer = FollowStatusSerializer(
        {"follow_status": request.user.follow.filter(pk=user_id).exists()}
    )

    # Return the serialized data as JSON response
    return Response(serializer.data)


# ANSWER
@api_view(["GET"])
def get_answer(request, aid):
    try:
        # Try to get the answer object, return 404 if not found
        answer = get_object_or_404(Answer, pk=aid)
    except Http404:
        # Answer does not exist, return JsonResponse with appropriate message
        return Response(
            {
                "data": None,
                "error": "No such answer exists in the database.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the response data
    serializer = AnswerSerializer(answer)
    # Return the serialized data as JSON response with success status
    return Response(
        {
            "data": serializer.data,
            "error": None,
            "status": "success",
        },
        status=status.HTTP_200_OK,
    )


# REPLY
@api_view(["GET"])
def create_reply(request, aid, new_reply):
    try:
        # Try to get the answer object, return 404 if not found
        answer = get_object_or_404(Answer, pk=aid)
    except Http404:
        # Answer does not exist, return JsonResponse with appropriate message
        return Response(
            {
                "data": None,
                "error": "No such answer exists in the database.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    reply = Reply.objects.create(aid=answer, uid=request.user, content=new_reply)
    reply.save()

    # Serialize the response data
    serializer = ReplySerializer(reply)

    # Return the serialized data as JSON response with success status
    return Response(
        {
            "data": serializer.data,
            "error": None,
            "status": "success",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_reply(request, rid):
    try:
        # Try to get the reply object, return 404 if not found
        reply = get_object_or_404(Reply, pk=rid)
    except Http404:
        # Reply does not exist, return JsonResponse with appropriate message
        return Response(
            {
                "data": None,
                "error": "No such answer exists in the database.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the response data
    serializer = ReplySerializer(reply)

    # Return the serialized data as JSON response with success status
    return Response(
        {
            "data": serializer.data,
            "error": None,
            "status": "success",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def delete_reply(request, rid):
    try:
        # Try to get the reply object, return 404 if not found
        reply = get_object_or_404(Reply, pk=rid)
    except Http404:
        # Reply does not exist, return JsonResponse with appropriate message
        return Response(
            {
                "data": None,
                "error": "No such answer exists in the database.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Serialize the response data
    if request.user.pk == reply.uid.pk:
        reply.delete()
        return redirect("BlazeApp:redirecting_page")
    else:
        # Reply does not exist, return JsonResponse with appropriate message
        return Response(
            {
                "data": None,
                "error": "No such answer exists in the database.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )


# NOTIFICATION
@api_view(["GET"])
def noti_read(request, nid):
    try:
        # Try to get the notification object, return 404 if not found
        noti = get_object_or_404(Notification, pk=nid)
    except Http404:
        # Notification does not exist, return JsonResponse with appropriate message
        return Response(
            {
                "error": "No such notification exists in the database.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    if noti.user == request.user:
        noti.is_read = True
        noti.save()
    else:
        return Response(
            {
                "error": "No such notification exists in the database.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(
        {
            "error": None,
            "status": status.HTTP_200_OK,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def notification_heart_beat(request):
    # Assuming you have a Notification model and want to get notifications for the current user
    notifications = request.user.notifications.all()

    # Serialize the response data using NotificationSerializer
    serializer = NotificationSerializer(notifications, many=True)

    # Return the serialized data as JSON response with success status
    return Response(
        {
            "data": serializer.data,
            "error": None,
            "status": "success",
        },
        status=status.HTTP_200_OK,
    )
