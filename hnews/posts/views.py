import json
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView

from .models import Post, Comment
from .forms import CommentForm
# Create your views here.

class CommentCreateView(CreateView):
    template_name = 'posts/create.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        return login_required(super().post)(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['post_json'] = json.dumps(self.post_obj.to_dict(self.request.user))
        kwargs['post'] = self.post_obj
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.post = self.post_obj
        self.object.save()
        return self.render_to_response(self.get_context_data())

class PostListView(ListView):
    template_name = 'posts/list.html'
    model = Post
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['posts'] = json.dumps([
            post.to_dict(self.request.user)
            for post in context['posts']
        ])
        return context

def upvote_view(view):
    @wraps(view)
    @require_POST
    @login_required
    def new_view(request, *args, **kwargs):
        obj = view(request, *args, **kwargs)
        try:
            upvoted = json.loads(request.body.decode('utf-8'))['upvoted']
        except (json.JSONDecodeError, KeyError):
            return HttpResponseBadRequest()
        obj.set_upvoted(request.user, upvoted=upvoted)
        # 204: No content
        return HttpResponse(status=204)
    return new_view

@require_POST
@login_required
def set_upvoted_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        upvoted = json.loads(request.body.decode('utf-8'))['upvoted']
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    post.set_upvoted(request.user, upvoted=upvoted)
    # 204: No content
    return HttpResponse(status=204)


def create_upvote_view(model):
    @require_POST
    @login_required
    def view(request, id):
        obj = get_object_or_404(model, id=id)
        try:
            upvoted = json.loads(request.body.decode('utf-8'))['upvoted']
        except (json.JSONDecodeError, KeyError):
            return HttpResponseBadRequest()
        obj.set_upvoted(request.user, upvoted=upvoted)
        # 204: No content
        return HttpResponse(status=204)
    return view


@upvote_view
def set_upvoted_post(request, post_id):
    return get_object_or_404(Post, id=post_id)


@upvote_view
def set_upvoted_comment(request, comment_id):
    return get_object_or_404(Comment, id=comment_id)


@require_POST
@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    try:
        content = json.loads(request.body.decode('utf-8'))['content']
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    Comment.objects.create(content=content, creator=request.user,
                           post=comment.post, parent=comment)
    return HttpResponse(status=204)
