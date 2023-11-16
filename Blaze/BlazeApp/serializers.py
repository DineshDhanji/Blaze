from rest_framework import serializers


class LikeStatusSerializer(serializers.Serializer):
    like_status = serializers.BooleanField()
    error = serializers.CharField(allow_blank=True, required=False)


class SavedStatusSerializer(serializers.Serializer):
    saved_status = serializers.BooleanField()
    error = serializers.CharField(allow_blank=True, required=False)
