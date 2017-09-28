from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.


#分类
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
#标签
class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

#文章的数据库
class Post(models.Model):
    title=models.CharField(max_length=70)#标题
    body=models.TextField()#正文
    created_time=models.DateTimeField()#创建时间
    modified_time=models.DateTimeField()#最后修改时间
    excerpt=models.CharField(max_length=100,blank=True)#摘要
    category=models.ForeignKey(Category)#外键，分类
    tags=models.ForeignKey(Tag)#外键，标签
    author=models.ForeignKey(User)#外键，用户
    views=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={"pk": self.pk})

    class Meta:
        ordering=["-created_time"]

    def increase_views(self):
        self.views+=1
        self.save(update_fields=["views"])

    def save(self, *args,**kwargs):
        if not self.excerpt:
            md=markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt=strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)