from django.shortcuts import render
import os
from importantapps.settings import IMAGEKIT_PRIVATE_KEY, IMAGEKIT_PUBLIC_KEY, URL_ENDPOINT, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_NAME
# Create your views here.
from .serializers import Category, CategorySerializer, Product, ProductSerializer

from rest_framework import viewsets, filters, views, serializers
from rest_framework.response import Response
import uuid
import json
from rest_framework.parsers import MultiPartParser

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# class ProductModalViewset(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['designation']

from imagekitio import ImageKit
imagekit = ImageKit(
    private_key=IMAGEKIT_PRIVATE_KEY,
    public_key=IMAGEKIT_PUBLIC_KEY,
    url_endpoint=URL_ENDPOINT
)

import cloudinary

cloudinary.config( 
  cloud_name = CLOUDINARY_NAME, 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET,
  secure = True
)


import cloudinary.uploader
import cloudinary.api 

class ImageSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())

class ProductModalViewset(views.APIView):
    # queryset = Product.objects.all()
    parser_classes = [MultiPartParser]
    def post(self, request):
        data = request.data 
        payload = request.data['payload']
        images = data['images']  
        url_list = [] 
        serializer  = ImageSerializer(data=request.data)
        upload_data = ''
        payload  = json.loads(request.data['payload']) 
        product = ''

        print(payload) 
        if serializer.is_valid():
            images = serializer.validated_data.get('images')
            for file in images:
                path = default_storage.save('temp.png', ContentFile(file.read()))
                print(path)
                # print(open(path, 'rb'))
                # binary = open(path, 'rb')
                # convert = base64.b64encode(binary.read())

                upload_data = cloudinary.uploader.upload(path, 
                    # asset_folder = "pets", 
                    public_id =str(uuid.uuid4()) ,
                    overwrite = True,  
                    ) 
                url_list.append(upload_data['url'])
                os.remove(path)

                # result = imagekit.upload_file(
                #     file=path, 
                #     file_name=str(uuid.uuid4())
                # ) 
            image_urls = json.dumps(url_list)
            payload["images"] = image_urls
            product_serializer  = ProductSerializer(data=payload)
            
            if product_serializer.is_valid():
                print("ITS VALID")
                product = product_serializer.save()
                print(product)
                return Response({'message': 'Images uploaded successfully', 'data':str(product), 'id':product.id})
            else:
                print(product_serializer.errors)

            # designation 
            return Response(serializer.errors, status=400)   
            # return Response({'message': 'Images uploaded successfully', 'data':str(product), 'id':product.id})
        else:
            return Response(serializer.errors, status=400)   
    

    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

class CategoryModalViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['designation'] 