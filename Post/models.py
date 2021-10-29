from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
# from mptt.models import MPTTModel, TreeForeignKey
from treebeard.mp_tree import MP_Node 
from core.models import Extensions
import uuid


User  = get_user_model()

def content_path(filename):
    return 'pdfs/{}'.format(filename)

class Category(MP_Node):
    name = models.CharField(max_length=255, blank=False)
    node_order_by = ['name']

    def __str__(self):
        return 'Category: {}'.format(self.name)

# Create your models here.

# class Category(MPTTModel):
#     name = models.CharField(max_length=255, blank=False)
#     icon = models.ImageField(upload_to="icons/", blank=True)
#     parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)

#     class MPTTMeta:
#         order_insertion_by = ['name']
#         verbose_name_plural = "Categories"

#     def __str__(self):
#         return self.name

class Material(Extensions):

    owner = models.ForeignKey(User, related_name='owner_material', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, related_name='material_category', on_delete=models.CASCADE)

    title = models.CharField(max_length=126, blank=False)
    content = models.FileField(blank=False, upload_to='pdfs/')
    vote_up = models.IntegerField(blank=False, default=0)
    vote_down = models.IntegerField(blank=False, default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return str(self.uuid)
