from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from theblog.models import Post, Category, Comment
from theblog.forms import PostForm, EditForm, CommentForm


# def home(request):
#     return render(request, 'home.html', {})


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    cats = Category.objects.all()
    ordering = ['-date_posted']
    paginate_by = 5  # Numărul de postări pe pagină

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu

        post_list = Post.objects.all().order_by('-date_posted')
        paginator = Paginator(post_list, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if self.request.method == 'POST':
            form = PostForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = self.request.user
                new_post.save()
                return redirect('blog-home')
        else:
            form = PostForm()

        is_paginated = paginator.num_pages > 1

        context.update({
            'form': form,
            'page_obj': page_obj,
            'is_paginated': is_paginated,
        })
        return context


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' ')).order_by('-date_posted')
    per_page = 5

    paginator = Paginator(category_posts, per_page)
    page = request.GET.get('page', 1)

    try:
        category_posts = paginator.page(page)
    except PageNotAnInteger:
        # Dacă parametrul page nu este un întreg, returnăm prima pagină.
        category_posts = paginator.page(1)
    except EmptyPage:
        # Dacă parametrul page este în afara intervalului de pagini, returnăm ultima pagină.
        category_posts = paginator.page(paginator.num_pages)

    return render(request, 'categories.html',
                  {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(**kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['cat_menu'] = cat_menu
        context['total_like'] = total_likes
        context['liked'] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.object.pk})

    # fields = '__all__'
    # fields = ['title', 'body']


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddCommentView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})


class AddCategoryView(CreateView):
    model = Category

    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'

    # fields = ['title', 'title_tag', 'body']

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.object.pk})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
        liked = False
    else:
        post.likes.add(request.user.id)
        liked = True

    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class EditCommentView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'edit_comment.html'

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.object.post.pk})


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'delete_comment.html'

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.object.post.pk})


def user_posts(request, user_id):
    # Obține obiectul utilizatorului sau aruncă o eroare 404 dacă utilizatorul nu există
    user = get_object_or_404(User, id=user_id)

    # Obține toate postările asociate cu utilizatorul dat
    user_posts = Post.objects.filter(author_id=user_id)

    # Paginare - specifică numărul de postări pe pagină
    paginator = Paginator(user_posts, 10)  # Schimbă 10 cu numărul dorit de postări pe pagină

    # Obține numărul paginii din parametrul de query
    page_number = request.GET.get('page')

    try:
        # Obține pagina specifică
        user_posts_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        # Dacă numărul paginii nu este un întreg, afișează prima pagină
        user_posts_paginated = paginator.page(1)
    except EmptyPage:
        # Dacă numărul paginii este mai mare decât numărul total de pagini, afișează ultima pagină
        user_posts_paginated = paginator.page(paginator.num_pages)

    # Trimite numele utilizatorului și postările paginate către șablonul HTML
    return render(request, 'user_posts.html', {'user': user, 'user_posts': user_posts_paginated})
