# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from utilitis.firebase import delete_image_from_firebase,upload_image_from_firebase


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']  
            firebase_url = upload_image_from_firebase(image)
            return Response({'firebase_url': firebase_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ImageDeleteView(APIView):
    def delete(self, request):
        image_url = request.query_params.get('image_url')
        if not image_url:
            return Response({"error": "se requiere url para eliminar"}, status=status.HTTP_400_BAD_REQUEST)        
        try:
            delete_image_from_firebase(image_url)
            return Response({"message": "Imagen borrada exitosamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      

