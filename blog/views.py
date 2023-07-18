from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator
from django.http import Http404
# Create your views here.


def post_list(request):
    post_list = Post.published.all()
    # 페이지당 3개의 게시물로 페이지네이션
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    posts = paginator.page(page_number)
    return render(request,
                  'blog/post/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    # try:
    #     post = Post.published.get(Post,id=id,status = Post.Status.PUBLISHED)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,'blog/post/detail.html',{'post':post})
