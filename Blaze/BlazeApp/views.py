import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, PostForm, CommentForm, ShareForm, EventForm
from .models import Post, Comment, Share, User, Student, Faculty, Society, Event

from BlazeAdministration.views import page_not_found_404


# Account Related Views
# Login & Logout
def user_login(request):
    splineCanva_data = [
        {
            "script": '<script type="module" src="https://unpkg.com/@splinetool/viewer@0.9.490/build/spline-viewer.js"></script><spline-viewer hint loading-anim url="https://prod.spline.design/vadsFcx7VebdH1Fd/scene.splinecode"></spline-viewer>',
            "bg_color": "#EBBBB1",
        },
        {
            "script": '<script type="module" src="https://unpkg.com/@splinetool/viewer@0.9.490/build/spline-viewer.js"></script><spline-viewer hint loading-anim url="https://prod.spline.design/iAXW7NWl805UGgLf/scene.splinecode"></spline-viewer>',
            "bg_color": "#B2AFE5",
        },
        {
            "script": '<script type="module" src="https://unpkg.com/@splinetool/viewer@0.9.490/build/spline-viewer.js"></script><spline-viewer hint loading-anim url="https://prod.spline.design/QByHTO9vEfxeIVKP/scene.splinecode"></spline-viewer>',
            "bg_color": "#C2E1B9",
        },
    ]

    # Add more splineCanva data as needed
    selected_data = random.choice(splineCanva_data)

    if request.method == "POST":
        login_form = UserLoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_superuser:
                login(request, user)
                return redirect("BlazeApp:newsfeed")
            else:
                messages.error(request, "Invalid username and/or password.")
                return render(
                    request,
                    "BlazeApp/account/login.html",
                    {
                        "login_form": login_form,
                        "splineCanva": selected_data["script"],
                        "splineCanvaBgColor": selected_data["bg_color"],
                    },
                )

        else:
            messages.error(request, "Invalid email and/or password or submission.")
            return render(
                request,
                "BlazeApp/account/login.html",
                {
                    "login_form": login_form,
                    "splineCanva": selected_data["script"],
                    "splineCanvaBgColor": selected_data["bg_color"],
                },
            )
    else:
        if request.user.is_authenticated:
            if request.user.is_staff:
                logout(request)
                return redirect("BlazeAdministration:administration_login")
            else:
                return redirect("BlazeApp:newsfeed")
        else:
            return render(
                request,
                "BlazeApp/account/login.html",
                {
                    "login_form": UserLoginForm(),
                    "splineCanva": selected_data["script"],
                    "splineCanvaBgColor": selected_data["bg_color"],
                },
            )


def user_logout(request):
    logout(request)
    return redirect("BlazeApp:user_login")


# Settings
def settings(request):
    return render(request, "BlazeApp/account/settings.html")


# Others Views
def newsfeed(request):
    # Fetching posts from both the current user and the users they follow
    follows_users = request.user.follow.all()
    newsfeed_posts = Post.objects.filter(
        poster__in=follows_users
    ) | Post.objects.filter(poster=request.user)
    newsfeed_posts = newsfeed_posts.order_by("-timestamp").all()

    # Fetching event from followed societies
    upcoming_events = Event.objects.filter(poster__in=follows_users)

    post_form = PostForm()

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            # Upon valid data, we will save the post
            new_post = post_form.save(
                commit=False
            )  # Create but don't save to the database yet
            new_post.poster = (
                request.user
            )  # Assuming you have a User associated with the post
            new_post.save()
            post_form = PostForm()
            return redirect("BlazeApp:redirecting_page")
            # return redirect("BlazeApp:profile")
        else:
            messages.error(request, "Invalid post submission.")

    content = {
        "post_form": post_form,
        "newsfeed_posts": newsfeed_posts,
        "upcoming_events": upcoming_events,
    }
    return render(request, "BlazeApp/newsfeed.html", content)


def events(request):
    event_instances = Event.objects.all()
    content = {"event_instances": event_instances}
    return render(request, "BlazeApp/events.html", content)


def society(request):
    society_instances = Society.objects.all()
    content = {"society_instances": society_instances}
    return render(request, "BlazeApp/society.html", content)


def profile(request, uid):
    try:
        # Try to get the post object, return 404 if not found
        user_instance = get_object_or_404(User, pk=uid)
    except Http404:
        # User does not exist, return JsonResponse with appropriate message
        return page_not_found_404(
            request, exception=404, message="Got wrong address bro."
        )
    user_type = user_instance.get_user_type
    if user_type == "student":
        user_instance = Student.objects.get(user=user_instance)
    elif user_type == "faculty":
        user_instance = Faculty.objects.get(user=user_instance)
    elif user_type == "society":
        user_instance = Society.objects.get(user=user_instance)

    content = {
        "instance": user_instance,
        "instance_posts": Post.objects.filter(poster=user_instance.user).order_by(
            "-timestamp"
        ),
        "instance_saved_posts": user_instance.user.saved_post.all().order_by(
            "-timestamp"
        )
        if user_instance.user == request.user
        else None,
    }
    return render(request, "BlazeApp/profile.html", content)


def view_post(request, post_id):
    comment_form = CommentForm()

    try:
        # Try to get the post object, return 404 if not found
        post = get_object_or_404(Post, pk=post_id)
    except Http404:
        # Post does not exist, return JsonResponse with appropriate message
        return page_not_found_404(
            request, exception=404, message="You just lost my trust."
        )

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Upon valid data, we will save the comment
            new_comment = comment_form.save(
                commit=False
            )  # Create but don't save to the database yet
            new_comment.object_type = "post"
            new_comment.object_id = post_id
            new_comment.user = (
                request.user
            )  # Assuming you have a User associated with the post
            new_comment.save()
            # Redirect user to redirecting page to clear cache
            return redirect("BlazeApp:redirecting_page")
        else:
            messages.error(request, "Invalid comment submission.")

    content = {
        "post": post,
        "comments": Comment.objects.filter(
            object_id=post_id, object_type="post"
        ).order_by("-timestamp"),
        "comment_form": comment_form,
    }
    return render(request, "BlazeApp/post.html", content)


def delete_post(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        try:
            # Try to get the post object, return 404 if not found
            post = get_object_or_404(Post, pk=post_id)
            if post.poster == request.user:
                post.delete()
            else:
                return page_not_found_404(
                    request, exception=404, message="Just how low you will go?"
                )

        except Http404:
            # Post does not exist, return JsonResponse with appropriate message
            return page_not_found_404(
                request, exception=404, message="You just lost my trust."
            )
        return redirect("BlazeApp:newsfeed")
    return page_not_found_404(
        request, exception=404, message="Mama not gonna be proud of you."
    )


def share_post(request, post_id):
    try:
        # Try to get the post object, return 404 if not found
        post = get_object_or_404(Post, pk=post_id)

    except Http404:
        # Post does not exist, return JsonResponse with appropriate message
        return page_not_found_404(
            request, exception=404, message="Why are you the way your are?"
        )

    share_post_form = ShareForm(shared_post_id=post_id)
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        share_post_form = ShareForm(request.POST, shared_post_id=post_id)
        if share_post_form.is_valid():
            # Creating new instance of share
            share_instance = Share.objects.create(pid=post, uid=request.user)

            # Creating new instance of post
            new_post_instance = Post.objects.create(
                picture=share_post_form.cleaned_data["picture"],
                content=share_post_form.cleaned_data["content"],
                poster=request.user,
                original_post=post,
            )

            return redirect("BlazeApp:newsfeed")

    content = {
        "share_post_form": share_post_form,
        "post": post,
    }
    return render(request, "BlazeApp/share_post.html", content)


def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST["comment_id"]
        try:
            # Try to get the post object, return 404 if not found
            comment_instance = get_object_or_404(Comment, pk=comment_id)
            if comment_instance.user == request.user:
                comment_instance.delete()
            else:
                return page_not_found_404(
                    request, exception=404, message="Go home and take a rest."
                )

        except Http404:
            # Post does not exist, return JsonResponse with appropriate message
            return page_not_found_404(
                request,
                exception=404,
                message="Earth will be amazing without invansions.",
            )
        # Redirect the user to the previous view
        previous_view = request.META.get("HTTP_REFERER")
        return redirect(previous_view)

    return page_not_found_404(request, exception=404, message="Get a life already man.")


def create_event(request):
    # If the requesting user is not society instance then we won't
    # allow them to access this page.
    if not request.user.is_society:
        return page_not_found_404(
            request,
            exception=404,
            message="Instead of events try to make humanity in yourself.",
        )
    event_form = EventForm()
    if request.method == "POST":
        # Retrieving data from post request
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            # Upon valid data, we will save the event
            new_event = event_form.save(
                commit=False
            )  # Create but don't save it to the database yet
            new_event.poster = (
                # Associating user with the event
                request.user
            )
            new_event.save()
            return redirect(
                reverse("BlazeApp:view_event", kwargs={"event_id": new_event.pk})
            )
        else:
            messages.error(request, "Invalid event submission.")

    content = {"event_form": event_form}
    return render(request, "BlazeApp/create_event.html", content)


def view_event(request, event_id):
    try:
        # Try to get the event object, return 404 if not found
        event_instance = get_object_or_404(Event, pk=event_id)
    except Http404:
        # Event does not exist, return JsonResponse with appropriate message
        return page_not_found_404(
            request,
            exception=404,
            message="May God gift you amazing event soon (●'◡'●)",
        )

    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Upon valid data, we will save the comment
            new_comment = comment_form.save(
                commit=False
            )  # Create but don't save to the database yet
            new_comment.object_type = "event"
            new_comment.object_id = event_id
            new_comment.user = (
                request.user
            )  # Assuming you have a User associated with the post
            new_comment.save()
            # Redirect user to redirecting page to clear cache
            return redirect("BlazeApp:redirecting_page")
        else:
            messages.error(request, "Invalid comment submission.")

    content = {
        "event_instance": event_instance,
        "comments": Comment.objects.filter(
            object_id=event_id, object_type="event"
        ).order_by("-timestamp"),
        "comment_form": comment_form,
    }
    return render(request, "BlazeApp/view_event.html", content)


def redirecting_page(request):
    # Redirect user to redirecting page to clear cache
    previous_view = request.META.get("HTTP_REFERER")

    if previous_view:
        return redirect(previous_view)
    else:
        return redirect("BlazeApp:newsfeed")
