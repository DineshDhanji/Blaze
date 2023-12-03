from rest_framework import serializers
from .models import User, Answer, Reply


class LikeStatusSerializer(serializers.Serializer):
    like_status = serializers.BooleanField()
    error = serializers.CharField(allow_blank=True, required=False)


class SavedStatusSerializer(serializers.Serializer):
    saved_status = serializers.BooleanField()
    error = serializers.CharField(allow_blank=True, required=False)


class FollowStatusSerializer(serializers.Serializer):
    follow_status = serializers.BooleanField()
    error = serializers.CharField(allow_blank=True, required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "profile_picture",
            "ring_color",
        ]


class ReplySerializer(serializers.ModelSerializer):
    # aid = AnswerSerializer()
    uid = UserSerializer()

    class Meta:
        model = Reply
        fields = [
            "id",
            "aid",
            "uid",
            "content",
            "timestamp",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    poster = UserSerializer()
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id",
            "poster",
            # 'question',
            "content",
            "timestamp",
            "replies",
        ]
