from urllib.parse import urlencode
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Articles(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=100)
    time_create = models.DateTimeField(auto_now_add=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    
    def get_absolute_url(self):
        
        query_dict = {
            'id': self.pk
        }
        
        return f"{reverse('theme')}?{urlencode(query_dict)}"
    


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)


class ArticlesContent(models.Model):
    article = models.ForeignKey('Articles', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=2000)
    code = models.CharField(max_length=10000, null=True)
    time_create = models.DateTimeField(auto_now_add=True)