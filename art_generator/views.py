# Create your views here.
from .models import Project, GeneratedImage
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.contrib import messages
from .models import GeneratedImage
from django.http import HttpResponseRedirect
from django.urls import reverse
from UserApp.models import *
from rest_framework.response import Response
import  shutil,os
from django.conf import settings
# OBJECTIVE: projectList 화면에 보낼 프로젝터를 렌더링 하는 뷰 함수
# NEED WORK: user permission 설정 로직 없음, 템플렛 연결 미완,선택 후 이동 없음

saved_once=False #WARNING: fakeGeneratedImage를 만들기 위한 전역변수 

def project_list_view(request):
    
    #DONE!: get user id - request에서 받아와야
    #user_id = '1'  # request.session["user_id"]

    # NEED WORK: filter project by user id
    #user=UserApp.objects.get(id==user_id)
    #projects=Project.objects.get(user==user)
    username=request.session['username']
    user=User.objects.get(username=username)
    print('project_list_view\n!!!!!!!!!!!!!!!!!',username)
    try:
        projects = Project.objects.filter(user=user)
    except:
        projects=None
    
    if request.method == "POST":


        # NEED WORK: reference user uploaded image
        if 'use' in request.POST:
            #선택된 프로젝트 pk를 받아오기 
            project_id = request.POST.get("use")
            request.session['project_id']=project_id 
            
            # imageGenerate 페이지로 가기 
            return HttpResponseRedirect('../../sumukhwa/imageGenerate')
            
        #NEED WORK: 더 이상 스타일 이미지를 자기가 고르지 않으므로 deprecated
        #NEED WORK: 그렇지만 주로 풍경 수묵화에서 비롯한 style transfer를 원하는지 등등이 바뀔 수 있음
        elif 'edit' in request.POST:
            # 선택된 프로젝트 pk를 받아오기 
            project_id = request.POST.get("edit")
            request.session['project_id']=project_id 

            # chooseType로 돌아가기 
            return HttpResponseRedirect(reverse('../../sumukhwa/chooseType', args=[project_id]))
        
        elif 'new_project' in request.POST:
            project = Project.objects.create_project(user)
            project_id=project.pk
            request.session['project_id']=project_id

            return HttpResponseRedirect('../../sumukhwa/chooseType')

            # return HttpResponseRedirect(reverse('/sumukhwa/chooseType',args=[project]))
    return render(request, "projectList.html", {"projects": projects})



# OBJECTIVE: generate 버튼 클릭 시 이미지 생성
# NEED WORK: collect such images
def generateImage(project_object, np, pp):
    images = GeneratedImage.objects.create_images(project_object, np, pp)
    return images


def fakeGenerateImage(project_object, np, pp,type=1):
    images=[]
    global saved_once
    if saved_once==False:
        #NEED WORK:media에 유저마다 폴더 있어야함
        #DONE:유저마다 project 만들 시에 generated 폴더 있어야함
        path='F:\\1DEVAHEAD\\1DEV\\sumukhwa-server\\fake_photos'
        dest_path=os.path.join(settings.MEDIA_ROOT,str(project_object.user.id))
        dest_path=os.path.join(dest_path,str(project_object.id))
        dest_path=os.path.join(dest_path,'generated')

        #dest path is made well
        #print('!!!!!!!!!!!!!!!!!!!destpath:',dest_path)
        for file in os.listdir(path):
            #옮기기
            shutil.copy(os.path.join(path,file), os.path.join(dest_path,file))

            #인스턴스 생성
            image_object=GeneratedImage.objects.create_image(os.path.join(dest_path,file),project_object)
            images.append(image_object)
        #saved_once=True
    
    print("!!!!!!!!!!!!!!!!test",images[0].image.url)
    return images



# NEED WORK: existing project인 경우와 new project인 경우 구분해야함
def image_generate_view(request):

    # test GeneratedImage instances
    project_id=request.session['project_id']
    project=Project.objects.get(id=project_id)
    projectType=project.projectType

    
    #prompt checker
    def prompt_exist(prompt):
        try:
            if prompt=="":
                return False 
            elif prompt.strip()=="":
                return False 
        except:
            print("image_generate_view/prompt was either not a string, or was None",prompt)     
            return False 

        return True
    
    # get project info
    try:
        #웹사이트로부터 정보를 받고
        project_name=request.POST.get('project_name')
        negative_prompt = request.POST.get('negative_prompt')
        positive_prompt = request.POST.get('positive_prompt')

        #project 인스턴스에 정보 업데이트
        #NEED WORK: class 함수를 왜 안씀?
        if project.projectName!=project_name and prompt_exist(project_name):
            project.changeName(project_name)
        if project.negativePrompt!=negative_prompt and prompt_exist(negative_prompt):
            project.negativePrompt=negative_prompt
        if project.positivePrompt!=positive_prompt and prompt_exist(positive_prompt):
            project.positivePrompt=positive_prompt
        project.save() 

    except:
        #WARNING: test prompt used
        if not prompt_exist(project.projectName):
            project.projectName="default_project"
        project.negativePrompt="not a fierce cat"
        project.positivePrompt="is a cute cat"


    #이미 만들어진 이미지가 있었다면 불러오기
    selected_images=[]
    try:
        GeneratedImage.objects.get(project=project)
        generated_images=GeneratedImage.objects.filter(project=project)
    except:
        generated_images=[]
        
    # NEED WORK: 만약 prompt가 존재한다면 clause 없음
    if request.method == 'POST':

        #generate 버튼을 눌러 이미지를 요구했다면
        if 'generate' in request.POST:

            #NEED WORK: 폴더 정리 로직 없음
            #기존의 선택된 이미지들과 새로 generated 된 이미지를 불러온다.
            #generateImage 함수 안에 이미 저장 로직이 있다. 
            try:               
                selected_images = GeneratedImage.objects.filter(project=project, selected=True)
                generated_images = fakeGenerateImage(project, negative_prompt, positive_prompt,projectType)  # NEED WORK
   
            except:
                generated_images = fakeGenerateImage(project, negative_prompt, positive_prompt)  # NEED WORK 
            
         
        elif 'changeProjectName' in request.POST:
            project.projectName=request.POST.get('project_name')
            project.save()
        
        elif 'changePrompt' in request.POST:
            print(project.projectName,"????????????????????")
            negative_prompt = request.POST.get('negative_prompt')
            positive_prompt = request.POST.get('positive_prompt')
            project.negativePrompt=negative_prompt
            project.positivePrompt=positive_prompt
            project.save() 
            #NEED WORK: django web push를 아직 안함

        elif 'export' in request.POST:

            #꼭 할 것
            #1. generated 폴더를 8개 빼고 다 비워두기 
            #2. selected image를 전달하기

            if selected_images:
                request.session['project_id']=project_id 
            
            else:
                #NEED WORK: message that there is no images selected
                print("image_generate_view!!!!!!!!!!!!!!!!!\nNo selected images yet")
                
            return redirect("../../sumukhwa/export")
        
        #지우기와 고르기 
        if request.POST.get('action') == 'toggle_button':
            if request.POST.get('button_type')=='remove':
                token = request.POST.get('csrfmiddlewaretoken')
                id = request.POST.get("id")#image object id 
                GeneratedImage.objects.get(id=id).delete()
                generated_images=GeneratedImage.objects.filter(project=project)
                selected_images=GeneratedImage.objects.filter(project=project,selected=True)
                redirect('art_generator:imageGenerate')

            elif request.POST.get('button_type')=='select':
                token = request.POST.get('csrfmiddlewaretoken')
                id = request.POST.get("id")#image object id 
                GeneratedImage.objects.select_image(id)
                selected_images=GeneratedImage.objects.filter(project=project,selected=True)
                redirect('art_generator:imageGenerate')
    #where to return
    link='imageGenerate.html'
    context={'project':project,'generated_images': generated_images, 'selected_images': selected_images}
    return render(request,link, context=context)      

def export_view(request):
    #export 후 selected 폴더 비우기 
    project_id=request.session['project_id']
    project=Project.objects.get(id=project_id)
    selected_images=GeneratedImage.objects.selected_images(project_id)
    
    if 'Done' in request.POST:

        #NEED WORK:save to user computer
        for image in selected_images:
            pass 

        GeneratedImage.objects.filter(project=project,selected=True).delete() 
        return redirect('../../sumukhwa/imageGenerate.html')
    elif 'Back' in request.POST:
        return redirect('../../sumukhwa/imageGenerate.html')
        
    context={'images':selected_images}
    return render(request,'export.html',context)

def choose_type_view(request):
    project_id=request.session['project_id']
    if request.method == 'POST':
        project=Project.objects.get(id=project_id)
        if '1' in request.POST:#1~3
            project.projectType='1'
            project.save()
            return redirect('art_generator:imageGenerate')
        elif '2' in request.POST:#4~6
            project.projectType='2'
            project.save()
            return redirect('art_generator:imageGenerate')
        elif '3' in request.POST:#5~9
            project.projectType='3'
            project.save()
            return redirect('art_generator:imageGenerate')
    return render(request, 'chooseType.html')

def delete_image_view(request):
    project_id=request.session['project_id']
    project=Project.objects.get(id=project_id)
    image_id=request.session['image_id']
    image=GeneratedImage.objects.get(id=image_id,project=project)
    if 'delete' in request.POST:
        image.delete()
        redirect('art_generator:ImageGenerate')
    context={'image':image}
    return render(request,'deleteImage.html')