from rest_framework import serializers

from blog.models import Blog
from user.models import User


class CreateBlogSerializer(serializers.ModelSerializer):
  author_id = serializers.UUIDField()
  class Meta:
    model = Blog
    fields = ['title', 'text', 'thumbnail', 'author_id']

  def validate_author_id(self, value):
    user = User.objects.get(id=value)
    if user:
      return value
    raise ValueError("user not in databae")

  def create(self, validated_data):
    blog = Blog.objects.create(
      title=validated_data.get('title'),
      text=validated_data.get('text'),
      thumbnail=validated_data.get('thumbnail'),
      author_id=validated_data.get('author_id')
    )
    return blog


class ReadBlogPreviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Blog
    fields = ['id', 'title', 'thumbnail', 'last_modified']


class ReadBlogDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Blog
    fields = '__all__'