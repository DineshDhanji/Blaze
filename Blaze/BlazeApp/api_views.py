from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Post, User, Event
from .serializers import (
    LikeStatusSerializer,
    SavedStatusSerializer,
    FollowStatusSerializer,
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


# LIKE
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
