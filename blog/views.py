from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.http import Http404
# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request,'blog/post/list.html',{'posts':posts})


def post_detail(request,id):
    # try:
    #     post = Post.published.get(Post,id=id,status = Post.Status.PUBLISHED)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request,'blog/post/detail.html',{'post':post})
