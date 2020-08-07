from rest_framework import serializers
from .models import Comment


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user_id')

    def get_user_id(self, obj):
        return {'id': obj.user_id.id, 'name': obj.user_id.name}

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'food_id', 'content', 'created_at']
        read_only_fields = ('user_id',)
