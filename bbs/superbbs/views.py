from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from superbbs import models
from django.contrib.auth import authenticate,login,logout
from superbbs import comment_handler
from superbbs import myform
import json
# Create your views here.
category_obj=models.Category.objects.filter(top_display=True).order_by('priority')


def index(request):
    article_list=models.Article.objects.filter(priority__gte=1,status='published').all()
    return render(request,'superbbs/index.html',{'category_list':category_obj,'article_list':article_list})

def category(request,cate_id):
    article_list=models.Article.objects.filter(priority__gte=1,status='published').all()
    category_res = models.Category.objects.get(id=cate_id)
    articles=models.Article.objects.filter(category=category_res.id,status='published').all()
    return render(request,'superbbs/index.html',{'category_list':category_obj,'article_list':articles,
                                                 'current_category':category_res})

def view_article(request,article_id):
    article_res=models.Article.objects.get(id=article_id)
    return render(request,'superbbs/article.html',{'category_list':category_obj,
                                                 'article':article_res})

def add_comment(request):
    if request.method=='POST':
        # print("------>",request.POST)
        new_comment_obj = models.Comment(
            article_id = request.POST.get('article_id'),
            parent_comment_id = request.POST.get('comment_pid') or None,
            comment_type = int(request.POST.get("comment_type")),
            user_id = request.user.userprofile.id,
            comment = request.POST.get('comment')
        )
        new_comment_obj.save()
        return HttpResponseRedirect('/bbs/article/%s' %request.POST.get('article_id'))
    else:
        article_obj = models.Article.objects.get(id=int(request.GET.get('article_id')))
        comment_list = comment_handler.build_tree(article_obj.comment_set.select_related().filter(comment_type=1))
        test_comment=models.Comment.objects.get(id=4)
        test=test_comment.children
        # test=test_comment.comment_set.select_related()
        # print(test_comment,test,test.count())
        # print('-----comment_list----',comment_list)
        new_list=[]
        # for item in comment_list:
        #     print(item)

        return HttpResponse(json.dumps(comment_list))

def mylogin(request):
    article_list=models.Article.objects.filter(priority__gte=1,status='published').all()
    if request.method=='POST':
        login_user=authenticate(username=request.POST['username'],
                                password=request.POST['password'])
        if login_user is not None:
            login(request,login_user)
            return render(request,'superbbs/index.html',{'category_list':category_obj,'article_list':article_list})
        else:
            print("username and password were incorrect.")
            err_msg='Login Failed! ' \
                    'username and password were incorrect.'
            return render(request,'superbbs/error.html',{'errors':err_msg,'category_list':category_obj})
    else:
        return render(request,'superbbs/login.html',{'category_list':category_obj})

def mylogout(request):
    logout(request)
    msg='Logout Success!'
    return render(request,'superbbs/logout.html',{'messages':msg,'category_list':category_obj})

def add_article(request): #未完成
    if request.method=='GET':
        article_obj=myform.ArticleForm()
        return render(request,'superbbs/addarticle.html',{'category_list':category_obj,'article_obj':article_obj})
    else:
        print(request.POST)
        new_article=models.Article(
            title = request.POST.get('title'),
            brief = request.POST.get('brief'),
            category_id = request.POST.get('category'),
            content = request.POST.get('content'),
            author_id = request.POST.get('author'),
            pub_date = request.POST.get('pub_date'),
            status = request.POST.get('status'),
            priority = request.POST.get('priority'),
            tag_img = request.FILES['tag_img'],
        )
        # print("-------->",request.FILES['tag_img'])
        new_article.save()
        # new_article.tag_img
        return HttpResponseRedirect('/bbs')