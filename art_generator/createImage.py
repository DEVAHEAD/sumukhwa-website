import torch
from diffusers import StableDiffusionPipeline
import os

#OBJECTIVE: 인공지능 함수를 통해 이미지를 만드는 함수  
#NEED WORK: image generation 아직 안 함
def create_ai_image(np,pp,project=None,limit=10):

    if not project:
        class Project:
            projectName="test_default"
        project=Project()


    # make sure you're logged in with `huggingface-cli login`
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    #use np, pp to create the image
    #1 negative prompt가 적용되는지 확인인
    if np!="" and pp!="":
        images=pipe(pp,negative_prompt=np,num_images_per_prompt=limit).images
    else:
        pp="a photograph of an astronaut riding a horse"
        np="not a red horse"
        images=pipe(pp,negative_prompt=np,num_images_per_prompt=limit).images
    
    #auto generate filename 
    image_paths=[]
    for i,image in enumerate(images):  

        orig_image_path=os.path.join("art_generator\\media\\generatedImages\\",project.projectName+"_"+str(i)+".png")
        '''
        #장고에서 사진 업로드 할 때 쓰는 거라는데... 꼭 이거 써야하는지 모르겟음
        fs = FileSystemStorage()
        filename = fs.save(image_path, image)
        image_path = fs.url(filename)
        image_paths.append(image_path)
        '''
        
        image.save(orig_image_path) 
        image_paths.append(orig_image_path)
    return images,image_paths

if __name__=="__main__":
    create_ai_image("","")