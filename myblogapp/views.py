from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from taggit.models import Tag
from .forms import EmailPostForm,CommentForm,SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count, Q

# Create your views here.

def post_search(request):
    form = SearchForm()
    query = None
    
    results = []

    if ('query' in request.GET):
        form = SearchForm(request.GET)
        if(form.is_valid()):
            query = form.cleaned_data['query']
            results = Post.published.filter(Q(title__icontains=query) | Q(body__icontains=query))
            
    return render(request,'blog/post/search.html',{'form': form,'query':query,'results': results})

def post_list(request, tag_slug = None):
    post_list = Post.published.all()
    tag = None
    if(tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    middle_page = (paginator.num_pages) // 2

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, "blog/post/list.html", {"posts": posts,'middle_page': middle_page})


def post_detail(request, post, year, month, day):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED,
    )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    
    return render(request, "blog/post/detail.html", {"post": post,'comments': comments,'form':form,'similar_posts':similar_posts})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id, status=Post.Status.PUBLISHED)
    comment = None

    comments = post.comments.filter(active=True)
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    form = CommentForm(data=request.POST)
    if(form.is_valid()):
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request,'blog/post/detail.html',{'post': post,'form':form,'comments':comments,'similar_posts':similar_posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


# def post_share(request, post_id):

#     post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
#     sent = False
#     if request.method == "POST":

#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = (
#                 f"{cd['name']} ({cd['email']})" f"recomends you to read {post.title}"
#             )
#             message = (
#                 f"Read { post.title} at {post_url}\n\n"
#                 f"{cd['name']}'s comments: {cd['comments']}"
#             )
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=None,
#                 recipient_list=[cd["to"]],
#             )
#             sent = True
#     else:
#         form = EmailPostForm()

#     return render(request, "blog/post/share.html", {"post": post, "form": form})
