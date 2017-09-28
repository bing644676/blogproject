from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Post,Category
import markdown #代码高亮
from comments.forms import CommentForm
# Create your views here.

#首页
def index(request):
    post_list=Post.objects.all()
    return render(request,"blog/index.html",context={"post_list":post_list})
#归档
def archives(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month)
    return render(request,"blog/index.html",context={"post_list":post_list})
#分类
def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={"post_list":post_list})
def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)#相当于id
   #阅读量加+
    post.increase_views()

    post.body=markdown.markdown(post.body,
                                extensions=[
                                    "markdown.extensions.extra",
                                    "markdown.extensions.codehilite",
                                    "markdown.extensions.toc",
                                ])
    form=CommentForm()
    comment_list=post.comment_set.all()
    context={'post':post,'form':form,'comment_list':comment_list}
    return render(request,"blog/detail.html",context=context)

