# from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from blog.models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


class PostListView(ListView):
    queryset = Post.published.all()
    context_obejct_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# Create your views here.
def post_list(request):
    per_page = request.GET.get('per_page', 3)
    page_number = request.GET.get('page', 1)
    post_list = Post.published.all()
    paginator = Paginator(post_list, per_page, orphans=1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request,year,month,day,post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post Found.")
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})