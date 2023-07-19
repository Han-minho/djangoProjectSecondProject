# from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from blog.models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from blog.forms import EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
    queryset = Post.published.all()
    context_obejct_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# Create your views here.
def post_share(request,post_id):
    # id로 글 검색
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    # 추가
    sent = False
    if request.method == 'POST':
        # 폼이 제출되었습니다.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 폴 필드가 유효한 경우
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}님이 {post.title}을(를) 추천합니다."
            message = f"{post.title}을(를) {post.url}에서 읽어보세요\n\n"\
                      f"{cd['name']}의 의견: {cd['comments']}"
            send_mail(subject,message,'hihi6024@gmail.com',[cd['to']])
            sent = True
            # ... 이메일 전송
        else:
            form = EmailPostForm()
        return render(request,'blog/post/share.html',
                      {'post':post,'form':form,'sent':sent})


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