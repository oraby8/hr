from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from. import video2text
from. import extract_skills

 
 
def read_pdf(path):
    text=''
    path=os.path.join(settings.MEDIA_ROOT, path)
    path=video2text.Converter(path)
    text=video2text.get_large_audio_transcription(path)
    return(text)


#module_dir = os.path.dirname(__file__)


def home(request):
	return render(request,'base.html')



# Create your views here.
def new_search(request):
    output=[]
    #Get Data
    try:
        new_search = request.POST.get('search')
        dis = request.POST.get('dis')
        pdf=request.FILES['pdf'] if 'pdf' in  request.FILES else None
        if pdf:
            pdf=request.FILES['pdf']
            file=FileSystemStorage()
            fs=file.save(pdf.name,pdf)
            new_search=read_pdf(pdf.name)
    except:
        new_search=None
        dis=None

    #output=resume_scane.scan(str(dis),str(new_search))
    print('text:',new_search)
    a1=extract_skills.extract_name(new_search)
    print('name: ',a1)
    a2=extract_skills.extract_skilles(new_search)
    print('skill: ',a2)
    name=str(a1)
    skills=str(a2)
    name=str(a1)
    output='0'



    

    allout={'out':output,'name':name,'skills':skills,}
    #delete file after finsh
    '''
    if pdf != None:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, pdf.name))
        except:
            pass
    '''
    return render(request,'new_search.html',allout)
