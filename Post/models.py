<<<<<<< HEAD
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
# from mptt.models import MPTTModel, TreeForeignKey
from treebeard.mp_tree import MP_Node 
from core.models import Extensions
import uuid


from django.contrib.contenttypes.fields import GenericRelation

from activities.models import Activity

User  = get_user_model()

def content_path(instance, filename):
    return 'pdfs/{}/{}/{}'.format(instance.category.get_parent().name, instance.category.name, filename)

class Category(MP_Node):
    name = models.CharField(max_length=255, blank=False)
    node_order_by = ['name']

    def __str__(self):
        return 'Category: {}'.format(self.name)

# Create your models here.

class Material(Extensions):
    
    owner = models.ForeignKey(User, related_name='owner_material', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, related_name='material_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=126, blank=False)
    content = models.FileField(blank=False, upload_to=content_path)
    up_vote = GenericRelation(Activity, related_query_name="material")
    down_vote = GenericRelation(Activity,  related_query_name="material")
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return str(self.uuid)

=======
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
# from mptt.models import MPTTModel, TreeForeignKey
from treebeard.mp_tree import MP_Node 
from core.models import Extensions
import uuid


from django.contrib.contenttypes.fields import GenericRelation

from activities.models import Activity

User  = get_user_model()

def content_path(instance, filename):
    return 'pdfs/{}/{}/{}'.format(instance.category.get_parent().name, instance.category.name, filename)

class Category(MP_Node):
    name = models.CharField(max_length=255, blank=False)
    node_order_by = ['name']

    def __str__(self):
        return 'Category: {}'.format(self.name)

# Create your models here.

class Material(Extensions):
    
    owner = models.ForeignKey(User, related_name='owner_material', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, related_name='material_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=126, blank=False)
    content = models.FileField(blank=False, upload_to=content_path)
    vote_up = GenericRelation(Activity, related_query_name="material")
    vote_down = GenericRelation(Activity,  related_query_name="material")
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return str(self.uuid)

>>>>>>> chat
