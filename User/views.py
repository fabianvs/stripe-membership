#Python imports
import os
#Django imports
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.db.models import Q
#Forms imports
from .forms import SignupForm, StudentForm, ProfesorForm, UserUpdateForm, DocumentForm, Post_fileForm
#Models imports
from .models import Student, Profesor, Pay_method, Document, Post_file

def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            return render (request,'user/login.html', {'error': 'invalid user of password'})

    return render (request,'user/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(
        request=request,
        template_name='user/signup.html',
        context={'form': form}
    )

@login_required
def logout_view(request):
    logout(request)
    
    return redirect('login')


class Choise_roll(LoginRequiredMixin,TemplateView):
    template_name = "user/roll.html"


@login_required
def home_view(request):
    return render(request,'home.html')

@login_required
def student_create(request, Student_ID=None, **kwargs):

    user= request.user
    student = Student()

    try:
        user.student
    except ObjectDoesNotExist:
        pk= user.pk
        student.user_id = pk
        student.save()
    
    if request.method == 'POST': 
        stu_ints = Student.objects.last()

        form = StudentForm(request.POST, request.FILES, instance=stu_ints)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = StudentForm(instance=student)

    return render(
        request=request,
        template_name='user/new_student.html',
        context={
            'form': form,
            'user': request.user,
        }
    )

@login_required
def profesor_create(request, Profesor_ID=None, **kwargs):

    profesor = Profesor()
    user= request.user

    try:
        user.profesor
    except ObjectDoesNotExist:
        pk= user.pk
        profesor.user_id = pk
        profesor.save()

    if request.method == 'POST':
        pro_ints = Profesor.objects.last()
        form = ProfesorForm(request.POST, request.FILES, instance=pro_ints)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ProfesorForm(instance=profesor)

    return render(
        request=request,
        template_name='user/new_profesor.html',
        context={
            'form': form,
            'user': request.user,
        }
    )


@login_required
def profile(request):
    
    user = request.user
    pk = user.pk    

    try:
        user.student
    except ObjectDoesNotExist:
        print('user is not a student')
        pass
    else:
        profile = Student.objects.get(user=pk)

    try:
        user.profesor
    except ObjectDoesNotExist:
        print('user is not a profesor')
    else:
        profile = Profesor.objects.get(user=pk)
    finally:   
        context = {
            'profile': profile,
        }
    return render(request,"user/profile.html", context)


@login_required
def profile_update(request, pk):

    user_init= User.objects.get(pk=pk)
    form = []
    user_form = []

    if request.method == 'GET':

        try:
            user_init.student
        except ObjectDoesNotExist:
            print('user is not a student')
            pass
        else:
            profile = Student.objects.get(user=pk)
            form = StudentForm(instance=profile)
            user_form = UserUpdateForm(instance=user_init)

        try:
            user_init.profesor
        except ObjectDoesNotExist:
            print('user is not a profesor')
        else:
            profile = Profesor.objects.get(user=pk)
            form = ProfesorForm(instance=profile)
            user_form = UserUpdateForm(instance=user_init)
        finally:   
            context = {
                'profile': profile,
            }

    elif request.method == 'POST':

        try:
            user_init.student
        except ObjectDoesNotExist:
            print('user is not a student')
            pass
        else:
            profile = Student.objects.get(user=pk)
            form = StudentForm(request.POST, request.FILES,instance=profile)
            user_form = UserUpdateForm(request.POST, instance=user_init)

            if form.is_valid() and user_form.is_valid():
                form.save()
                user_form.save()
            return redirect('profile')   

        try:
            user_init.profesor
        except ObjectDoesNotExist:
            print('user is not a profesor')
        else:
            profile = Profesor.objects.get(user=pk)
            form = ProfesorForm(request.POST, request.FILES,instance=profile)
            user_form = UserUpdateForm(request.POST, instance=user_init)

            if form.is_valid() and user_form.is_valid():
                form.save()
                user_form.save()
            return redirect('profile')
  
    else:
        form = ()
        user_form = UserUpdateForm(instance=user_init)
    
    context = {
        'form': form,
        'user_form': user_form,
    }
    
    return render(request,"user/profile_update.html", context)


@login_required
def search_profesor(request):
    queryset = request.GET.get("buscar")
    profesors = Profesor.objects.filter(visibility=True)

    if queryset:
        profesors = Profesor.objects.filter(
            Q(visibility=True) &
            Q(carrer = queryset) |
            Q(university =queryset)
        )
    return render(request, "user/list_profesor.html", {'profesors' : profesors})


@login_required
def upload_document(request):

    user = request.user
    if request.method == 'POST':
        form= DocumentForm(request.POST, request.FILES)
        
        #import pdb; pdb.set_trace()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.stu_rel = request.user
            instance.save()
            return redirect('doc_list')
    else:
        form=DocumentForm()

    context = {
        'user': user,
        'form': form,
    }
    return render(request,'user/file_upload.html', context)


@login_required
def document_list(request):

    user=request.user
    documents = Document.objects.filter(stu_rel=user)
    queryset = request.GET.get("buscar")

    if queryset:
        documents = Document.objects.filter(
            Q(stu_rel=user) &
            Q(file_name__icontains=queryset)
        )
    return render(request, "user/file_list.html", {'documents' : documents})


@login_required
def post_file(request):

    if request.method == 'POST':
        form = Post_fileForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_rel = request.user
            instance.save()
            return redirect('post_list')
            
        else:
            print(form.errors)
    else:
        form = Post_fileForm()

    context = {
        'form': form,
    }
    return render(request,'user/post_file.html', context)


@login_required
def post_list(request):
    items = Post_file.objects.all()
    queryset = request.GET.get("buscar")
    #import pdb; pdb.set_trace()
    if queryset:
        items = Post_file.objects.filter(
            Q(is_active=True) &
            Q(post_title__icontains=queryset)
        )
    return render(request, "user/post_list.html", {'items' : items})


class DocumentUpdateView(LoginRequiredMixin,UpdateView):
    model = Document
    template_name = "user/file_upload.html"
    form_class = DocumentForm
    success_url = reverse_lazy('doc_list')



class Post_fileUpdateView(LoginRequiredMixin,UpdateView):
    model = Post_file
    template_name = "user/post_file.html"
    form_class = Post_fileForm
    success_url = reverse_lazy('post_list')


class DocumentDeleteView(LoginRequiredMixin,DeleteView):
    model = Document
    template_name = "user/delete_confirm.html"
    success_url = reverse_lazy('doc_list')


class Post_fileDeleteView(LoginRequiredMixin,DeleteView):
    model = Post_file
    template_name = "user/delete_confirm.html"
    success_url = reverse_lazy('post_list')
