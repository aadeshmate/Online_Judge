from distutils.log import error
import filecmp
import subprocess
import http
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from onlinejudge.models import Problem, Submission, TestCase
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os
# Create your views here.


def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login')
def addproblem(request):
    if(request.method == 'POST'):
        name = request.POST.get('problem_name')
        level = request.POST.get('problem_level')
        desc = request.POST.get('problem_desc')
        new_problem = Problem(
            problem_name=name, problem_level=level, problem_desc=desc)
        new_problem.save()
        messages.success(request, 'Your Message Has been Sent!!!.')
    return render(request, 'problem.html')


@login_required(login_url='/login')
def showproblem(request):
    allProblem = Problem.objects.all()
    return render(request, 'listproblem.html', {'all_posts': allProblem})


@login_required(login_url='/login')
def viewproblem(request, question_id):
    obj = Problem.objects.get(id=question_id)
    return render(request, 'viewproblem.html', {'question': obj})
    # return render(request,'viewproblem.html',question)

@login_required(login_url='/login')
def submitproblem(request,question_id):
    if(request.method == "POST"):
        uploaded_file = request.FILES['usercode']
        with open('onlinejudge/static/solution.cpp','wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)
        test = TestCase.objects.get(problem = question_id)
        # test = TestCases.objects.get(problem = question_id)
        # out_container = open('output.txt' , 'w')
        # subprocess.call(['g++','onlinejudge/static/solution.cpp'],shell=True)
        # subprocess.call(['a.exe'],stdin=test.inp ,stdout='output.txt',shell=True)

        # p1=subprocess.run(['g++','onlinejudge/static/solution.cpp'],shell=True,stdout=subprocess.PIPE,text=True)
        # p2=subprocess.run(['a.exe'],stdin=test.inp,shell=True,text=True)
        # print(p1.stdout) #if not 0 its fine
        # print(p1.stderr)
        p1=subprocess.run(['g++','onlinejudge/static/solution.cpp'], shell=True,capture_output=True)
        # if(p1.returncode!=0):
        #     return HttpResponse("Something went wrong,Please Check your code!!")
        p2=subprocess.run(['a.exe'],input=test.inp,text=True,capture_output=True)
        # print(p2.returncode)
        # if(p2.returncode!=0):
        #     return HttpResponse("Something went wrong,Please Check your code!!")
        a=p2.stdout.strip()
        user_ans=a.encode()
        expected=test.outp
        expected = expected.replace("\r\n", "\n")
        expected_ans=expected.encode()
        solution = Submission()
        if(user_ans==expected_ans):
            solution.verdict=True
            solution.problem = Problem.objects.get(id=question_id)
            solution.submitted_at = timezone.now()
            solution.submittedcode = 'onlinejudge/static/solution.cpp'
            solution.save()
            return HttpResponse("Accepted")
        else:
            solution.verdict=False
            solution.problem = Problem.objects.get(id=question_id)
            solution.submitted_at = timezone.now()
            solution.submittedcode = 'onlinejudge/static/solution.cpp'
            solution.save()
            return HttpResponse("Wrong Answer")
        
    return HttpResponse("Code Submitted")


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameter
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cnfpassword = request.POST['cnfpassword']
        # check for errorneus inputs
        if password != cnfpassword:
            return redirect('/')
        if len(username) > 10:
            return redirect('/')

        if User.objects.filter(username=username).exists():
            return redirect('/')

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.success(request, "Your account is created")
        return redirect('/showproblem')

    else:
        return HttpResponse('You Need To login First')


def handlelogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            return redirect('showproblem')
        else:
            return redirect('/')

    return HttpResponse('You Need To login First')


def handlelogout(request):
    logout(request)
    return redirect('/')