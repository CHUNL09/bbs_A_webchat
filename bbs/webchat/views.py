from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from webchat import models
import queue
import json
import time
import os
# Create your views here.
GLOBAL_MSG_QUEUE={

}

@login_required
def webchat(request):
    return render(request,'webchat/webchat.html')

@login_required
def send_msg(request):
    print(request.POST)
    msg_data=request.POST['data']
    if msg_data:
        msg_data=json.loads(msg_data)
    msg_data['timestamp']=time.time()
    msg_data['from_name']=request.user.userprofile.name
    if msg_data['type']=='single':
        if not GLOBAL_MSG_QUEUE.get(int(msg_data['to'])):
            GLOBAL_MSG_QUEUE[int(msg_data['to'])]=queue.Queue()
        GLOBAL_MSG_QUEUE[int(msg_data['to'])].put(msg_data)
    else:  # group msgs
        print(json.loads(request.POST['data']),"---->")
        msg_dic=json.loads(request.POST['data'])
        group_id=int(msg_dic['to'])
        group_obj=models.WebGroup.objects.filter(id=group_id).first()
        member_objs=group_obj.members.select_related()
        for member in member_objs:
            if not GLOBAL_MSG_QUEUE.get(member.id):
                GLOBAL_MSG_QUEUE[member.id]=queue.Queue()
            if member.id!=request.user.userprofile.id:
                GLOBAL_MSG_QUEUE[member.id].put(msg_data)
    return HttpResponse('---message received--')

@login_required
def file_upload(request):
    print(request.FILES,"------->>>>")
    file_obj=request.FILES['file']
    user_home_dir="statics/upload/%s" %request.user.userprofile.id
    if not os.path.isdir(user_home_dir):
        os.mkdir(user_home_dir)
    new_file_name="%s/%s" %(user_home_dir,file_obj.name)
    with open(new_file_name,"wb") as new_file_obj:
        for chunk in file_obj.chunks():
            new_file_obj.write(chunk)
    return HttpResponse("---uploaded success----")

@login_required
def get_new_msgs(request):
    if request.user.userprofile.id not in GLOBAL_MSG_QUEUE:
        GLOBAL_MSG_QUEUE[request.user.userprofile.id]=queue.Queue()
    q_instance= GLOBAL_MSG_QUEUE[request.user.userprofile.id]
    msg_count=q_instance.qsize()
    msg_list=[]
    if msg_count>0:
        for msg in range(msg_count):
            msg_list.append(q_instance.get())
    else:
        try:
            msg_list.append(q_instance.get(timeout=60))
        except queue.Empty:
            print("no msgs,timeout...")
    return HttpResponse(json.dumps(msg_list))

