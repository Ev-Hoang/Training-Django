from rest_framework import serializers
from .models import Post

class PostQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    limit = serializers.IntegerField(required=False, default=10)
    offset = serializers.IntegerField(required=False, default=0)

class PostSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("You must have a title.")
        if len(value) > 200:
            raise serializers.ValidationError("Title must be shorter than 200 characters.")
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("content must exceeded 10 characters.")
        return value

    def validate_author(self, value):
        if not value:
            raise serializers.ValidationError("You must have an author.")
        return value