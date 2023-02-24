from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class PostListView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        posts = Post.objects.filter(author__profile__followers__in=[request.user.id])
        c_form = CommentForm()
        form = PostForm()
        share_form = ShareForm()
        
        context = {
            'post_list':posts,
            "c_form":c_form,
            'form':form,
            'shareform':share_form,
        }
        return render(request,'social/post_list.html',context)
    
    def post(self,request,*args,**kwargs):
        posts = Post.objects.filter(author__profile__followers__in=[request.user.id])
        form = PostForm(request.POST,request.FILES)
        c_form = CommentForm(request.POST)
        share_form = ShareForm()
        files = request.FILES.getlist("image")
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()        
            
            instance.create_tags()
            
            for f in files:
                img = Image(image=f)
                img.save()
                instance.image.add(img)
            
            instance.save()
               
            return redirect("post-list")
        context = {
            "post_list":posts,
            "form":form,
            "c_form":c_form,
            'shareform':share_form,
        }
        
        return render(request,'social/post_list.html',context)
    
class SharePostView(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST)
        
        if form.is_valid():
            instance = Post(
                body = post.body,
                author = post.author,
                created_on = post.created_on,
                shared_user = request.user,
                shared_on = timezone.now(),
            )
            
            instance.save()
        
        
            for img in post.image.all():
                instance.image.add(img)
        
            instance.save()

        return redirect("post-list")
            
class PostDetailView(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        
        context = {
            'post':post,
            'form':form          
        }
        
        return render(request,'social/post_detail.html',context)
    
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.author = request.user
            instance.save()        
            instance.create_tags()
            Notification.objects.create(notification_type=2,from_user=request.user,to_user=instance.post.author,post=instance.post)
            return redirect("post-detail",post.pk)
               
        context = {
            'post':post,
            'form':form
        }
        
        
        return render(request,'social/post_detail.html',context)
    
    
class CommentFormPost(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        form = CommentForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = Post.objects.get(id=request.POST.get("post_pk"))
            instance.author = request.user
            instance.save()     
            instance.create_tags()   
            Notification.objects.create(notification_type=2,from_user=request.user,to_user=instance.post.author,post=instance.post)
            return redirect("post-list")
        

class CommentReplyView(LoginRequiredMixin,View):
    def post(self,request,post_pk,pk,*args,**kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.post = post
            instance.parent = parent_comment
            instance.create_tags()
            instance.save() 
                   
        return redirect("post-detail",post.pk)

class PostEditView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['body']        
    template_name = "social/post_edit.html"
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("post-detail",kwargs={"pk":pk})

@login_required(login_url="account_login")
def CommentDelete(request,pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return redirect("post-detail",comment.post.pk)

@login_required(login_url="account_login")
def post_delete(request,pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("post-list")


class ProfileView(View):
    def get(self,request,pk,*args,**kwargs):
        profile = Profile.objects.get(pk=pk)
        user = request.user
        posts = Post.objects.filter(author=profile.user).order_by('-created_on')
        
        context = {
            'profile':profile,
            'user':user,
            'posts':posts,
        }
        
        return render(request,'social/profile.html',context)
    
class UpdateProfile(LoginRequiredMixin,UpdateView):
    model = Profile
    fields = ['bio','location','picture']
    template_name = "social/profile_update.html"
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("profile",kwargs={"pk":pk})
    
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    
def search(request):
    search = request.GET.get("query")
    profiles = Profile.objects.filter(Q(user__username__icontains=search))
    context = { 'profiles':profiles}
    return render(request,'social/search.html',context)

@login_required(login_url="account_login")
def AddFollower(request,pk):
    profile = Profile.objects.get(pk=pk)
    profile.followers.add(request.user)
    
    Notification.objects.create(notification_type=3,from_user=request.user,to_user=profile.user)
    return redirect('profile', pk=profile.pk)
        
@login_required(login_url="account_login")
def RemoveFollower(request,pk):
    profile = Profile.objects.get(pk=pk)
    profile.followers.remove(request.user)
    
    return redirect('profile', pk=profile.pk)

@login_required(login_url="account_login")
def add_like(request,pk):
    post = Post.objects.get(pk=pk)
    post.likes.add(request.user)
    Notification.objects.create(notification_type=1,from_user=request.user,to_user=post.author,post=post)
    return redirect('post-detail',pk=pk)

@login_required(login_url="account_login")
def remove_like(request,pk):
    post = Post.objects.get(pk=pk)
    post.likes.remove(request.user)
    return redirect('post-detail',pk=pk)

@login_required(login_url="account_login")
def add_comment_like(request,pk):
    comment = Comment.objects.get(pk=pk)
    comment.likes.add(request.user)
    Notification.objects.create(notification_type=1,from_user=request.user,to_user=comment.author,comment=comment)
    return redirect('post-detail',pk=comment.post.pk)

@login_required(login_url="account_login")
def remove_comment_like(request,pk):
    comment = Comment.objects.get(pk=pk)
    comment.likes.remove(request.user)
    return redirect('post-detail',pk=comment.post.pk)

class ListFollowers(View):
    def get(self,request,pk):
        profile = Profile.objects.get(pk=pk)
        followers = profile.followers.all()
        
        context = {
            'followers':followers,
            'profile':profile,
        }
        return render(request,'social/followers.html',context)
        
class Notifications(LoginRequiredMixin,View):
    def get(self,request):
        notifications = Notification.objects.filter(to_user=request.user).order_by('-date')
        context = { 'notifications':notifications}
        return render(request,'social/notifications.html',context)
    
@login_required(login_url="account_login")
def notification_delete(request,pk):
    notification = Notification.objects.get(pk=pk)
    notification.delete()
    return redirect('notifications')

class ListThreads(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        
        context = { 'threads':threads}
        return render(request,'social/inbox.html',context)
        
class CreateThread(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form = ThreadForm()
        
        context = {'form':form}
        return render(request,'social/create_thread.html',context)
    
    def post(self,request,*args,**kwargs):
        form = ThreadForm(request.POST)
        
        username = request.POST.get("username")
        
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user,receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user,receiver=receiver)[0]
                return redirect('thread',pk=thread.pk)
            elif ThreadModel.objects.filter(receiver=request.user,user=receiver).exists():
                thread = ThreadModel.objects.filter(receiver=request.user,user=receiver)[0]
                return redirect('thread',pk=thread.pk)
            
            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()
                return redirect('thread',pk=thread.pk)
        except:
            return redirect("create-thread")
        
class ThreadView(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        
        context = { 'thread':thread,'form':form,'message_list':message_list}
        return render(request,'social/thread.html',context)
        
class CreateMessage(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
            
        message = MessageModel(
            thread=thread,
            receiver_user=receiver,
            sender_user=request.user,
            image=request.FILES.get('image'),
            body=request.POST.get("body"),
        )
        Notification.objects.create(notification_type=4,from_user=request.user,to_user=receiver,thread=thread)

        
        message.save()
        return redirect('thread',pk=pk)
    
@login_required(login_url='account_login')
def get_tag(request,pk):
    tag = Tag.objects.get(pk=pk)
    post = Post.objects.filter(tags=tag)
    comments = Comment.objects.filter(tags=tag)
    context = {'tag': tag, 'posts': post,"comments":comments}
    return render(request, 'social/tags.html',context)