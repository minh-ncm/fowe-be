import io
import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from django.http import FileResponse
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class VisionCrudView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        model_name = data.get('model')
        image = Image.open(request.FILES['image'])
        image.thumbnail((1000, 1000))
        image_color = np.mean(np.array(image), axis=0)
        image_color = np.mean(image_color, axis=0)
        min_chanel = np.argmin(image_color)
        if min_chanel == 0:
            color = (255, 0, 0)
        elif min_chanel == 1:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('vision/static/vision/BeVietnamPro-Regular.ttf', size=20)
        
        if model_name == 'yolo':
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            pred = model(image)
            df = pred.pandas().xyxy[0]
            for value in df.values:
                xmin, ymin, xmax, ymax, confi, _, name = value
                draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=color, width=2)
                draw.text((xmin, ymin - font.getsize('foo')[1] - 5), name, color, font)
        byte_image = io.BytesIO()
        image.save(byte_image, format='JPEG')
        
        return FileResponse(ContentFile(byte_image.getvalue()))
