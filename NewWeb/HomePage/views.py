from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import login,authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.generic.base import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from HomePage.forms import LoginForm,RegisterForm
from HomePage.models import Category,Best,Article,Comment,UserProfile
from HomePage.forms import CommentForm
# Create your views here.

#@login_required,该装饰器用于告诉程序，使用这个方法是要求用户登录的。
def index(request):
    cates = Category.objects.all().order_by("-id") #分类列表

    todaynew_big = Best.objects.filter(select_reason="今日新闻")[0].select_article  #取出一篇今日新闻作为大标题
    todaynew = Best.objects.filter(select_reason="今日新闻")[1:4]
    todaynew_top3 = [i.select_article for i in todaynew]          #取出三篇今日新闻

    hot_recommend = Best.objects.filter(select_reason="热点要闻")[:5]
    hot_recommendlist = [i.select_article for i in hot_recommend]   #取出五篇热点要闻

    read_recommendtop3 = Best.objects.filter(select_reason="推荐阅读")[:3]
    read_recommendtop3list = [i.select_article for i in read_recommendtop3]  #取出三篇推荐阅读作为大标题

    read_recommend = Best.objects.filter(select_reason="推荐阅读")[3:10]
    read_recommendlist = [i.select_article for i in read_recommend]     #再取出七篇推荐阅读

    article_list = Article.objects.all().order_by("-publish_time")  #取出所有文章
    pagerobot = Paginator(article_list,5)                           #创建分页器，每页限定五篇文章
    page_num = request.GET.get("page",1)                            #取到当前页数

    try:
        article_list = pagerobot.page(page_num)                   #返回当前页码下的文章
    except EmptyPage:
        article_list = pagerobot.page(pagerobot.num_pages)        #如果不存在该页，返回最后一页
    except PageNotAnInteger:
        article_list = pagerobot.page(1)                          #如果页码不是一个整数，返回第一页

    context={
      "cates":cates,
      "todaynew_big":todaynew_big,
      "todaynew_top3":todaynew_top3,
      "hot_recommendlist":hot_recommendlist,
      "article_list":article_list,
      "read_recommendtop3list":read_recommendtop3list,
      "read_recommendlist":read_recommendlist,
    }
    return render(request, 'index.html', context=context)      #模板渲染

def detail(request,article_id):
    cates = Category.objects.all().order_by("-id")  #分类列表

    read_recommendtop3 = Best.objects.filter(select_reason="推荐阅读")[:3]
    read_recommendtop3list = [i.select_article for i in read_recommendtop3]     #取出三篇编辑推荐作为大标题

    read_recommend = Best.objects.filter(select_reason="推荐阅读")[3:10]
    read_recommendlist = [i.select_article for i in read_recommend]     #再取出七篇编辑推荐

    article = Article.objects.get(id=article_id)

    comments = Comment.objects.filter(belong_article=article)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():                             #是否合法
            words = form.cleaned_data.get("comment")
            comment = Comment(belong_user=request.user,words=words,belong_article=Article.objects.get(id=article_id))
            comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    context ={
       "cates":cates,
       "read_recommendtop3list":read_recommendtop3list,
       "read_recommendlist":read_recommendlist,
       "article":article,
       "comments":comments,
       "form":form
    }
    return render(request,'detail.html',context=context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(to='index')       #登录成功,重定向到首页
            else:
                return HttpResponse('用户名不存在或用户名密码错误')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context=context)

class LogoutView(View):

    def get(self,request):
        logout(request)
        return redirect(reverse("index"))    #返回首页

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()                      # 保存创建的用户
            userprofile = UserProfile(belong_to=user, avatar='avatar/avatar.png')
            userprofile.save()               # 保存创建该用户的资料
            return redirect(to='login')        #进入登录界面
    else:
        form = RegisterForm()

    context={'form':form}
    return render(request, 'register.html', context=context)
