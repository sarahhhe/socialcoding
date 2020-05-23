import datetime
from datetime import timedelta
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Post, Response, Vote, Category, ResponseVote, UserCategory
from users.models import Profile
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .filters import UserFilter
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import utc

from django.views.generic.edit import FormMixin
import numpy as np
from scipy.stats import beta
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from socialcoder.forms import PostForm, ResponseForm, CategoryForm
from tabulate import tabulate

# Create your views here.
@csrf_exempt
def acceptResponse(request, pk, id):
    responses = Response.objects.values_list('best',flat=True)
    if request.method == 'PUT':
        response = Response.objects.get(id=id)
        bestResponse = Response.objects.filter(best=True, post=response.post)
        bestResponseExists = Response.objects.filter(id=id, best=True, post=response.post)
        if bestResponse.exists():
            bestResponse.update(best=False)
        if bestResponseExists.exists():
            bestResponseExists.update(best=False)
        Response.objects.filter(id=id).update(best=True)
    return JsonResponse(list(responses), safe=False)

@csrf_exempt
def followCategory(request, pk, id):
    category = Category.objects.get(id=id)
    if request.method == 'PUT':
        followCategory = UserCategory.objects.filter(user=request.user, category=category)
        if followCategory.exists():
            followCategory.delete()
        else:
            uc = UserCategory(user=request.user, category=category)
            uc.save()
    userCategories = UserCategory.objects.values_list(flat=True)
    return JsonResponse(list(userCategories), safe=False)

class SearchResultsView(ListView):
    model = Post
    template_name = 'socialcoder/search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(code__icontains=query)
        )
        return object_list

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    success_url = '/'
    fields = ['category','title','code']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.instance.creator = request.user
            category_item = form.save(commit=False)
            category_item.save()
            return redirect('/')
    else:
        form = CategoryForm()
    return render(request, 'socialcoder/category_form.html', {'form': form})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            post_item = form.save(commit=False)
            post_item.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'socialcoder/post_form.html', {'form': form})

@csrf_exempt
def downvote_response(request, pk, id, rid):
    vote_response = Response.objects.get(id=rid)
    downvote = ResponseVote.objects.filter(user=request.user, response=vote_response, type="downvote")
    upvote = ResponseVote.objects.filter(user=request.user, response=vote_response, type="upvote")

    # unclick downvote
    if downvote.exists():
        vote_response.votes = vote_response.votes+1
        vote_response.save()
        ResponseVote.objects.filter(user=request.user, response=vote_response, type="downvote").delete()
        print("response by "+ vote_response.author.username + " deleted")

    # downvote and override current upvote object
    elif upvote.exists():
        upvote.delete()
        print("response by "+ vote_response.author.username + " deleted")
        vote_response.votes = vote_response.votes-2
        vote_response.save()
        v = ResponseVote(user=request.user, response=vote_response, type="downvote")
        v.save()

    # create new downvote object
    else:
        vote_response.votes = vote_response.votes-1
        vote_response.save()
        v = ResponseVote(user=request.user, response=vote_response, type="downvote")
        v.save()
        print("response by "+ vote_response.author.username + " created")
    response = {
        'votes' : vote_response.votes,
        }
    return JsonResponse(response, safe=False)

@csrf_exempt
def upvote_response(request, pk, id, rid):
    if request.method == 'PUT':
        vote_response = Response.objects.get(id=rid)
        downvote = ResponseVote.objects.filter(user=request.user, response=vote_response, type="downvote")
        upvote = ResponseVote.objects.filter(user=request.user, response=vote_response, type="upvote")

        # unclick upvote
        if upvote.exists():
            vote_response.votes = vote_response.votes-1
            vote_response.save()
            upvote.delete()
            print("response by "+ vote_response.author.username + " deleted")

        # upvote and override current downvote object
        elif downvote.exists():
            downvote.delete()
            print("response by "+ vote_response.author.username + " deleted")
            vote_response.votes = vote_response.votes+2
            vote_response.save()
            v = ResponseVote(user=request.user, response=vote_response, type="upvote")
            v.save()

        # create new upvote object
        else:
            vote_response.votes = vote_response.votes+1
            vote_response.save()
            v = ResponseVote(user=request.user, response=vote_response, type="upvote")
            v.save()
            print("response by "+ vote_response.author.username + " created")
        response = {
            'votes' : vote_response.votes,
            }
        return JsonResponse(response, safe=False)

@csrf_exempt
def upvote(request, pk, id):
    if request.method == 'PUT':
        vote_post = Post.objects.get(id=id)
        downvote = Vote.objects.filter(user=request.user, post=vote_post, type="downvote")
        upvote = Vote.objects.filter(user=request.user, post=vote_post, type="upvote")

        # unclick upvote
        if upvote.exists():
            vote_post.votes = vote_post.votes-1
            vote_post.save()
            upvote.delete()
            print(vote_post.title + " deleted")

        # upvote and override current downvote object
        elif downvote.exists():
            downvote.delete()
            print(vote_post.title + " deleted")
            vote_post.votes = vote_post.votes+2
            vote_post.save()
            v = Vote(user=request.user, post=vote_post, type="upvote")
            v.save()

        # create new upvote object
        else:
            vote_post.votes = vote_post.votes+1
            vote_post.save()
            v = Vote(user=request.user, post=vote_post, type="upvote")
            v.save()
            print(vote_post.title + " created")
        response = {
            'votes' : vote_post.votes,
            }
        return JsonResponse(response, safe=False)

@csrf_exempt
def downvote(request, pk, id):
    vote_post = Post.objects.get(id=id)
    downvote = Vote.objects.filter(user=request.user, post=vote_post, type="downvote")
    upvote = Vote.objects.filter(user=request.user, post=vote_post, type="upvote")

    # unclick downvote
    if downvote.exists():
        vote_post.votes = vote_post.votes+1
        vote_post.save()
        Vote.objects.filter(user=request.user, post=vote_post, type="downvote").delete()
        print(vote_post.title + " deleted")

    # downvote and override current upvote object
    elif upvote.exists():
        upvote.delete()
        print(vote_post.title + " deleted")
        vote_post.votes = vote_post.votes-2
        vote_post.save()
        v = Vote(user=request.user, post=vote_post, type="downvote")
        v.save()

    # create new downvote object
    else:
        vote_post.votes = vote_post.votes-1
        vote_post.save()
        v = Vote(user=request.user, post=vote_post, type="downvote")
        v.save()
    response = {
        'votes' : vote_post.votes,
        }
    return JsonResponse(response, safe=False)

@csrf_exempt
def add_comment(request, pk):
    code = request.POST['response_editor']
    post = Post.objects.get(id=pk)
    comment = Response(code = code, author = request.user, post = post)
    comment.save()

    print("COMMENT: " + comment.code)

    return JsonResponse({
        'id' : comment.id,
        'code' : comment.code,
        'author' : comment.author.username,
        'post' : comment.post.title
    })

def search_terms(request):
    usernames = User.objects.values_list('username',flat=True)
    post_titles = Post.objects.values_list('title',flat=True)
    return JsonResponse({"search_terms": list(usernames+post_titles)})

def all_usernames(request):
    usernames = User.objects.values_list('username',flat=True)
    return JsonResponse({"usernames": list(usernames)})

def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'socialcoder/user_list.html', {'filter': user_filter})

class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-date_posted')
        context['socialCoders'] = Profile.objects.all().order_by('-score')
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = ResponseForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['responses'] = Response.objects.all().order_by('-date_posted')
        context['socialCoders'] = Profile.objects.all().order_by('-score')
        context['form'] = ResponseForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = self.object
            response_item = form.save(commit=False)
            response_item.save()
            pk = str(self.object.id)
            print(pk)
            response = redirect('/post/'+pk)
            return response
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)

def userprofile(request):
    user = request.user
    user_posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    template = 'socialcoder/profile.html'
    return render(request, template, {'user_posts':user_posts,'user': user})

def to_seconds(dt_time):
    now = datetime.utcnow().replace(tzinfo=utc)
    timediff = now - dt_time
    total_secs = timediff.total_seconds()
    return total_secs

def prior_of_beta(request, arr, date, post):
    for i in range(len(arr)):
        if request.user.is_authenticated:
            if UserCategory.objects.filter(user=request.user, category=post.category).exists():
                return 3
        if date>=0 and date<=np.percentile(arr, 25):
            return 3
        if date>np.percentile(arr, 25) and date<=np.percentile(arr, 50):
            return 6
        if date>np.percentile(arr, 50) and date<=np.percentile(arr, 75):
            return 9
        if date>np.percentile(arr, 75) and date<=np.percentile(arr, 100):
            return 12
        else:
            return 12

def feed(request):
    dates = []
    posts = Post.objects.all()
    table = [["Prior of Beta","Category","Upvotes","Downvotes","Date","Rank Value"]]
    for d in posts:
        dates.append(to_seconds(d.date_posted))
    for p in posts:
        prior = prior_of_beta(request, dates, to_seconds(p.date_posted), p)
        ranking = beta.ppf(0.05,
            prior+Vote.objects.filter(post=p, type="upvote").count(),
            prior+Vote.objects.filter(post=p, type="downvote").count())
        Post.objects.filter(id=p.id).update(ranking=int(ranking*1000000))

        table.append([prior,
            p.category,
            Vote.objects.filter(post=p, type="upvote").count(),
            Vote.objects.filter(post=p, type="downvote").count(),
            p.date_posted, ranking])
    print(tabulate(table))

    context = {
        'posts': posts.order_by('-ranking'),
        'socialCoders': Profile.objects.all().order_by('-score'),
    }
    return render(request, 'socialcoder/feed.html', context, {'title': 'socialCoding'})

def leaderboard(request):
    socialCoders = User.objects.all()
    user_table = [["User","No. of posts","No. of times voted","No. of comments posted","No. of best answers"]]
    rankings_table = [["User","Posts rank value", "Comments rank value", "Votes rank value",  "Best answers rank value","Total Ranking Value"]]
    for s in socialCoders:
        no_of_posts = Post.objects.filter(author=s).count()
        no_of_posted_comments = Response.objects.filter(author=s).count()
        Profile.objects.filter(id=s.id).update(comments=no_of_posted_comments)
        no_of_best_answers = Response.objects.filter(author=s, best=True).count()
        no_of_votes_given = Vote.objects.filter(user=s).count()

        user_table.append([s,
            no_of_posts,
            no_of_votes_given,
            no_of_posted_comments,
            no_of_best_answers
            ])

        rankings_table.append([s,
        beta.ppf(0.05,1+(no_of_posts*0.25),1+(no_of_posts*0.75)),
        beta.ppf(0.05,1+(no_of_posted_comments*0.5),1+(no_of_posted_comments*0.5)),
        beta.ppf(0.05,1+(no_of_best_answers*0.75),1+(no_of_best_answers*0.25)),
        beta.ppf(0.05,1+(no_of_votes_given*1),1+(no_of_votes_given*0)),

        beta.ppf(0.05,1+(no_of_posts*0.25),1+(no_of_posts*0.75))+
        beta.ppf(0.05,1+(no_of_posted_comments*0.5),1+(no_of_posted_comments*0.5))+
        beta.ppf(0.05,1+(no_of_best_answers*0.75),1+(no_of_best_answers*0.25))+
        beta.ppf(0.05,1+(no_of_votes_given*1),1+(no_of_votes_given*0))
        ])
        score = beta.ppf(0.05,1+(no_of_posts*0.25),1+(no_of_posts*0.75))+beta.ppf(0.05,1+(no_of_posted_comments*0.5),1+(no_of_posted_comments*0.5))+beta.ppf(0.05,1+(no_of_best_answers*0.75),1+(no_of_best_answers*0.25))+beta.ppf(0.05,1+(no_of_votes_given*1),1+(no_of_votes_given*0))
        Profile.objects.filter(id=s.id).update(score=int(score*1000000))
    print(tabulate(user_table))
    print(tabulate(rankings_table))

    context = {
        'socialCoders': Profile.objects.all().order_by('-score'),
        'categories': Category.objects.all()
    }
    return render(request, 'socialcoder/leaderboard.html', context, {'title': "Today's Top socialCoders!"})
