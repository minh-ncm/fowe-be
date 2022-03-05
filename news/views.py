import requests
import numpy as np
from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated




class NewsView(GenericAPIView):
  __params = {
    'nyt': {'api-key': settings.NYT_KEY},
    }
  __sources = {
    'nyt': 'https://api.nytimes.com/svc/topstories/v2/world.json'
  }

  def __clean_data(self, data, source):
    if source == 'nyt':
      articles = data.get('results')
      results = []
      for article in articles:
        media = article.get('multimedia')
        try:
          media = media[0]
        except Exception:
          image = {
            "url": "",
            "caption": "Not available",
            "alt": ""
          }
        else:
          image = { 
          'url': media.get('url'),
          'caption': media.get('caption'),
          'alt': media.get('subtype'),
          }

        results.append({
          "id": article.get('uri'),
          "title": article.get('title'),
          "headline": article.get('abstract'),
          "url": article.get('url'),
          'image': image,
          "published_date": article.get('published_date'),
          "source": "new york times",
          "logo": "https://developer.nytimes.com/files/poweredby_nytimes_30a.png"
        })

    return results


  def __fetch_data(self, source):
    if source != "all":
      response = requests.get(
        url=self.__sources.get(source), 
        params=self.__params.get(source)
      )

      response_status = response.status_code
      response_data = self.__clean_data(response.json(), source)      
    else:
      response_data = []

      for src in self.__sources.keys():
        params = self.__params.get(src)
        response = requests.get(
          url=self.__sources.get(src), 
          params=params
        )

        response_status = response.status_code
        if response_status != 200:
          break
        
        response_data.append(self.__clean_data(response.json(), src))
        response_data = np.concatenate(response_data, axis=0)
    return response_data, response_status
    

  def get(self, request, format=None):
    query_params = request.query_params
    source = query_params.get("source")
    if len(list(query_params)) == 0:
      source = "all" 
      if source not in self.__sources.keys():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
      fetch_data, fetch_status = self.__fetch_data(source)
      return Response(fetch_data, status=fetch_status)
