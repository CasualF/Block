from rest_framework import serializers
from .models import Post, PostImages
from category.models import Category
from like.serializers import LikeSerializer

class PostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category', 'preview', 'owner_username', 'category_name')


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    images = PostImagesSerializer(many=True, required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        print(images_data)

        for image in images_data:
            PostImages.objects.create(image=image, post=post)

        return post

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images')


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImagesSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        data = super(PostDetailSerializer, self).to_representation(instance)
        data['likes'] = LikeSerializer(instance.likes.all(), many=True, required=False).data
        data['like_count'] = len(data['likes'])
        return data
