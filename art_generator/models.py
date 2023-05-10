
# Create your models here.
from django.db import models
# from datetime
import datetime
from UserApp.models import *
import os
from django.conf import settings
from django.core.files.base import ContentFile

# [주의]
# 사용자에 대한 구분을 하고 있지 않음

# NEED WORK: 사진 조회
class ProjectManager(models.Manager):

    def create_project(self,user, projectName="default"):
        if projectName == "default":
            projectName = datetime.date.today().strftime('%Y-%m-%d')+" project"

        project = self.create(user=user,projectName=projectName)
        
        # make folders
        try:
            dest_dir=os.path.join(os.path.join(settings.MEDIA_ROOT,str(user.id)))
            os.mkdir(dest_dir)  
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!making user dir failed')
        try:
            dest_dir=os.path.join(dest_dir,str(project.id))
            os.mkdir(dest_dir)     
        except:
            print('!!!!!!!!!!!!!!!!!!!making project dir failed',os.path.join(dest_dir,str(project.id))) 
        try:
            dest_dir=os.path.join(dest_dir,"generated")
            os.mkdir(dest_dir)
        except:
            print('!!!!!!!!!!!!!!!!!!!!!making generated dir failed')

        return project

    def delete_all_project(self):
        self.all().delete()

    def bring_styleTransfer(self, project_id):
        project = Project.objects.filter(id=project_id)
        stPath = project.styleTranferPath

        # NEED WORK: 모델 불러오기
        model = None

        return model


# NEED wORK: 알고리즘 경로 attribute
class Project(models.Model):
    # PK
    id = models.BigAutoField(auto_created=True, primary_key=True)
    created = models.DateField(auto_now=True)
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    
    # 소속 이미지 파일명에 쓰일 projectName
    projectName = models.CharField(max_length=100, default="devahead")

    # Prompt
    negativePrompt = models.CharField(default="", max_length=100)
    positivePrompt = models.CharField(default="", max_length=100)

    # 풍경(landscape), 인물(human), 정물(object) 중 택1
    projectType = models.CharField(default="1", max_length=100)

    # 프로젝트 관리자
    objects = ProjectManager()

    # for update

    def changeName(self, name):
        self.projectName = name

    def changeNegativePrompt(self, prompt):
        self.negativePrompt = prompt

    def changePositivePrompt(self, prompt):
        self.positivePrompt = prompt

    def __str__(self):
        return f"{self.projectName}"

    class Meta:
        get_latest_by = ["created"]


# OBJECTIVE: CREATE, UPDATE, DELETE INSTANCES
class GeneratedImageManager(models.Manager):
   
    def create_image(self,image_path,project):
        with open(image_path,'rb') as f:
            data=f.read()
            #print("!!!!!!!!!!image making: read data:",data) #it exists
            GeneratedImage.objects.create(project=project)
            image_object=GeneratedImage.objects.filter(project=project).latest('created')
            upload_path=os.path.join(os.path.join(str(project.user.id) ,str(project.id)), "generated")
            image_object.image.save(upload_path,ContentFile(data))
            image_object.save()
            return image_object


    def select_image(self, id):
        imageInstance = GeneratedImage.objects.get(id=id)
        imageInstance.select()
        imageInstance.save(force_update=True)

        # NEED WORK: save files to selected
        # 고민점: 인스턴스를 지우지 않는 한 계속 있을텐데 굳이 따로
        #        저장을 할 필요가 있는가. 근데 분리를 하면 generated image 폴더를
        #        정리하기는 좋을 것...

    def selected_images(self, project_id):
        project=Project.objects.get(id=project_id)
        imageInstances = GeneratedImage.objects.filter(
            project=project, selected=True)
        return imageInstances


class GeneratedImage(models.Model):

    # 하나의 이미지에 대한 정보
    id = models.BigAutoField(auto_created=True, primary_key=True)
    created = models.DateField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    image = models.ImageField(upload_to='uploads/',
                              default="generated/test1.jpg")

    # 여러 이미지에 대한 처리
    objects = GeneratedImageManager()

    def select(self):
        self.selected = True

    def __str__(self):
        return f"{self.image.url}"
