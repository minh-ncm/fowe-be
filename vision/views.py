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
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        if model_name == 'yolo':
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            pred = model(image)
            df = pred.pandas().xyxy[0]
            print(df)
            for value in df.values:
                xmin, ymin, xmax, ymax, confi, _, name = value
                if confi >= 0.5:
                    draw.rectangle([(xmin, ymin), (xmax, ymax)], outline='green')
                    draw.text((xmin, ymin - font.getsize('foo')[1]), f'{name} - {confi*100:.1f}%', 'green', font)
        byte_image = io.BytesIO()
        image.save(byte_image, format='JPEG')
        
        return FileResponse(ContentFile(byte_image.getvalue()))
