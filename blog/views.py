from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from cloudinary import uploader

from blog.models import Blog
from blog.serializers import ReadBlogPreviewSerializer, CreateBlogSerializer, ReadBlogDetailsSerializer


class BlogDetailsView(GenericAPIView):
  def get_object(self, id):
    blog = Blog.objects.get(pk=id)
    return blog

  def validate_params(self, params):
    if not params.get('id'):
      return False
    return True

  def get(self, request, format=None):
    params = request.query_params
    if not self.validate_params(params):
      return Response(status=status.HTTP_400_BAD_REQUEST)
    blog = self.get_object(params.get('id'))
    serializer = ReadBlogDetailsSerializer(blog)
    return Response(serializer.data, status=status.HTTP_200_OK)


class BlogCrudView(GenericAPIView):
  def get_permissions(self):
    if self.request.method.lower() == 'post':
      return [permissions.IsAdminUser()]
    else:
      return [permissions.AllowAny()]

  def get(self, request, format=None):
    params = request.query_params
    if params.get('id') == 'all':
      blogs = Blog.objects.all().order_by('-last_modified')
      serializer = ReadBlogPreviewSerializer(blogs, many=True)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
      blog = Blog.objects.get(id=params.get('id'))
      if blog is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
      serializer = ReadBlogDetailsSerializer(blog)
      return Response(data=serializer.data, status=status.HTTP_200_OK)


  def post(self, request, format=None):
    def upload_image(file):
      response = uploader.upload(file, folder='images', resource_type='image')
      return response.get('url')

    data = request.data
    files = request.FILES
    thumbnail = files.get('thumbnail')
    # Upload images and thumbnail
    if thumbnail:
      thumbnail = upload_image(thumbnail)
    
    image_urls = []
    for file in files:
      if file.startswith('img'):
        image_urls.append(upload_image(files.get(file)))

    # Embeded image urls to blog text
    text = []
    for value in data.get('text').split('<BR>'):
      if value == "<IMG>":
        text.append("<IMG>"+image_urls.pop(0))
      else:
        text.append(value)

    serializer = CreateBlogSerializer(
      data={'title': data.get('title'), 'text': '<BR>'.join(text), 'author_id': request.user.id, 'thumbnail': thumbnail}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)