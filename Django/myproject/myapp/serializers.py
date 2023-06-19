from rest_framework import serializers
from .models import Barang, Album, Track

class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id','title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album
    
    def update(self, instance, validated_data):
        tracks_data = validated_data.pop('tracks', [])
        instance = super().update(instance, validated_data)
        
        for track_data in tracks_data:
            track_id = track_data.get('id')
            if track_id:
                track = instance.tracks.filter(id=track_id).first()
                if track:
                    track.title = track_data.get('title', track.title)
                    track.duration = track_data.get('duration', track.duration)
                    track.save()
            else:
                instance.tracks.create(title=track_data['title'], duration=track_data['duration'])

        return instance
    