from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Articles, Comment
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

#

def LikeView(request, pk):
    post = get_object_or_404(Articles, id=request.POST.get('object_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True


    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))

class ArticleListView(ListView):
    model = Articles
    template_name = 'article_list.html'
    ordering = ['-id']



class ArticleDetailView(DetailView):
    model = Articles
    template_name = 'article_detail.html'
    def get_context_data(self, *args, **kwargs):
        # context = Articles.objects.all()
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Articles, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class ArticleUpdateView(UpdateView):
    model = Articles
    fields = ('title', 'summary', 'body', 'photo')
    template_name = 'article_edit.html'


class ArticleDeleteView(DeleteView):
    model = Articles
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

class ArticleCreateView(CreateView):
    model = Articles
    fields = ('title', 'summary', 'body', 'photo')
    template_name = 'article_create.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'article_comment.html'
    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('article_list')