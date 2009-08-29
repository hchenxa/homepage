#:coding=utf8:
from django.views.generic.list_detail import object_list

from lifestream.models import Item
from lifestream.util.decorators import allow_methods
from blog.models import Post
from tagging.views import tagged_object_list

@allow_methods('GET')
def main_page(request):
  # Get latest English and Japanese post.
  try:
      en_post = Post.objects.published().filter(locale="en").latest("pub_date")
  except Post.DoesNotExist:
      en_post = None
  try:
      jp_post = Post.objects.published().filter(locale="jp").latest("pub_date")
  except Post.DoesNotExist:
      jp_post = None

  return object_list(request, 
      queryset = Item.objects.published(), 
      template_name = "lifestream/main.html",
      extra_context = {
          "jp_post": jp_post,
          "en_post": en_post,
      }
  )

@allow_methods('GET')
def main_page(request):
    return object_list(request, 
        queryset = Item.objects.published(),
    )

@allow_methods('GET')
def domain_page(request, domain):
    return object_list(
        request,
        queryset=Item.objects.published().filter(feed__domain=domain),
    )

@allow_methods('GET', 'POST')
def item_page(request, item_id):
    return object_detail(
        request,
        queryset=Item.objects.published(),
        object_id=item_id,    
    )

@allow_methods('GET')
def tag_page(request, tag):
    return tagged_object_list(
        request,
        queryset_or_model=Item.objects.published(),
        tag=tag,
    )