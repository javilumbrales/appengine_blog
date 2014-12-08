from django.views.generic import ListView
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.decorators.cache import cache_page

from filetransfers.api import serve_file
from filetransfers.api import prepare_upload

from blog.models import Article
from blog.forms import ArticleForm


class BlogList(ListView):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Article.objects.all().order_by("created")
        return Article.objects.filter(status=1).order_by("created")



@login_required
def add(request):
    if request.method == 'POST':
        formData = ArticleForm(request.POST, request.FILES)
        if formData.is_valid():
            edited = formData.save(commit=False)
            edited.user = request.user
            edited.save()
        return redirect("list")

    view_url = reverse("add")
    upload_url, upload_data = prepare_upload(request, view_url)

    return render(request, "add.html", {"form": ArticleForm, "action": "Add new", 'upload_url': upload_url, 'upload_data': upload_data})


@login_required
def edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(instance=article)

    if request.method == 'POST':
        formData = ArticleForm(request.POST, request.FILES, instance=article)
        if formData.is_valid():
            edited = formData.save(commit=False)
            edited.user = request.user
            edited.save()
        return redirect("list")

    view_url = reverse("edit", kwargs={"pk":pk})
    upload_url, upload_data = prepare_upload(request, view_url)

    return render_to_response("add.html", {"form": form, "action": "Edit", 'upload_url': upload_url, 'upload_data': upload_data})


@login_required
def delete(request, pk):
    Article.objects.filter(pk=pk).delete()
    return redirect("list")

@cache_page(60 * 15)
def download_handler(request, pk):
    article = get_object_or_404(Article, id=pk)
    if article.file:
        return serve_file(request, article.file)
    raise Http404