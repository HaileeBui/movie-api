from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = '__all__'
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    #watchlist = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        #fields = ['id', 'name', 'description', 'active']
        #exclude = ['active']
        
        
"""
add new field with SerializerMethodField
len_name = serializers.SerializerMethodField()
def get_len_name(self, obj):
        return len(obj.name)
        
   
def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name must be at least 2 characters long")

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    description = serializers.CharField()
    active = serializers.BooleanField()
    
    def create(seld, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    def validate(self, data):
        if data['description'] == data['name']:
            raise serializers.ValidationError("Title and name cannot be the same")
        else:
            return data
"""