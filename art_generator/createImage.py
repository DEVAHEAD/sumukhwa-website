import torch
# from diffusers import StableDiffusionPipeline
import os,shutil 
import re
from django.conf import settings
#give GeneratedImages object
#when new generate, give fresh 8 images
#fakeGenerateImage(project, negative_prompt, positive_prompt,projectType)
def generateImage(project_object, np, pp,type="1"):

    command = "python ai/codes/main_exe.py "+np+ " "+pp+" "+type+" "+str(project_object.id)
    os.system(command)

    images=[]
    global saved_once
    if saved_once==False:
        #DONE:media에 유저마다 폴더 있어야함
        #DONE:유저마다 project 만들 시에 generated 폴더 있어야함
        path='..\\ai\\results\\'
        
        #copy destination
        dest_path=os.path.join(settings.MEDIA_ROOT,str(project_object.user.id))
        dest_path=os.path.join(dest_path,str(project_object.id))
        dest_path=os.path.join(dest_path,'generated')

        #dest path is made well
        #print('!!!!!!!!!!!!!!!!!!!destpath:',dest_path)
        for file in os.listdir(path):
            #NEED WORK: latest 8개에 대해서만 실행하기 

            #옮기기
            shutil.copy(os.path.join(path,file), os.path.join(dest_path,file))

            #인스턴스 생성
            image_object=GeneratedImage.objects.create_image(os.path.join(dest_path,file),project_object)
            images.append(image_object)
        #saved_once=True
    
    #print("!!!!!!!!!!!!!!!!test",images[0].image.url)
    return images
