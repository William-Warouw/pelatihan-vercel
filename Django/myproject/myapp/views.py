from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from .models import Barang, Album, Track
from .serializers import BarangSerializer, TrackSerializer, AlbumSerializer
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from django.http import HttpResponse

def index(request):
        now = datetime.now()
        html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
        return HttpResponse(html)


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author is None:
            return True
        return obj.author == request.user
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method == 'POST' and request.user.is_authenticated:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            album_pk = view.kwargs.get('album_pk')
            track_pk = view.kwargs.get('track_pk')
            try:
                album = Album.objects.get(pk=album_pk)
                track = album.tracks.get(pk=track_pk)
                if track.author is None or track.author == request.user:
                    return True
            except (Album.DoesNotExist, Track.DoesNotExist):
                return False
        return False


class MyAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                item = Barang.objects.get(pk=pk)
            except Barang.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = BarangSerializer(item)
            return Response(serializer.data)
        
        else:
            items = Barang.objects.all()
            serializer = BarangSerializer(items, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = BarangSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            barang = Barang.objects.get(pk=pk)
        except Barang.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BarangSerializer(barang, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    def delete(self, request, pk):
        try:
            barang = Barang.objects.get(pk=pk)
        except Barang.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)       

        barang.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlbumView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404
    def get(self, request, pk=None, format=None):
        if pk is not None:
            # Retrieve a single album
            try:
                album = Album.objects.get(pk=pk)
                serializer = AlbumSerializer(album)
                return Response(serializer.data)
            except Album.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve multiple albums
            albums = Album.objects.all()
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TrackView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def get_album(self, album_pk):
        try:
            return Album.objects.get(pk=album_pk)
        except Album.DoesNotExist:
            raise Http404

    def get_track(self, album, track_pk):
        try:
            return album.tracks.get(pk=track_pk)
        except Track.DoesNotExist:
            raise Http404

    def get(self, request, album_pk, track_pk, format=None):
        album = self.get_album(album_pk)
        track = self.get_track(album, track_pk)
        serializer = TrackSerializer(track)
        return Response(serializer.data)

    def post(self, request, album_pk, track_pk, format=None):
        album = self.get_album(album_pk)
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(album=album)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, album_pk, track_pk, format=None):
        album = self.get_album(album_pk)
        track = self.get_track(album, track_pk)
        if not self.check_object_permissions(request.user, track):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TrackSerializer(track, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, album_pk, track_pk, format=None):
        album = self.get_album(album_pk)
        track = self.get_track(album, track_pk)
        if not self.check_object_permissions(request.user, track):
            return Response(status=status.HTTP_403_FORBIDDEN)
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_track(self, album, track_pk):
        try:
            return album.tracks.get(pk=track_pk)
        except Track.DoesNotExist:
            raise Http404
        
    def check_object_permissions(self, user, obj):
        # Allow if the user is the author of the track or the track has no author assigned
        if obj.author is None or obj.author == user:
            return True
        return False

