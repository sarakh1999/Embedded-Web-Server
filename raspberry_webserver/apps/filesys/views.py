from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os

from .models import Directory, File
from .forms import FileUploadForm


User = get_user_model()


def get_abs_path(abs_path: str, name: str):
    if abs_path == '/':
        return '/' + name
    else:
        return abs_path + '/' + name


# Checks whether NAME is unique inside CUR_DIR so it can be the name of a new file or directory.
def is_name_unique(request, cur_dir, name):
    files = File.objects.filter(owner=request.user, parent_dir=cur_dir)
    for file in files:
        if file.get_name() == name:
            return False
    dirs = Directory.objects.filter(owner=request.user, parent_dir=cur_dir)
    for dir in dirs:
        if dir.get_name() == name:
            return False
    return True


# Go to root directory
@login_required(login_url='/login/')
def go_to_root(request):
    root_dir = get_object_or_404(Directory, owner=request.user, abs_path='/')
    return redirect('filesys:get-dir', dir_id=root_dir.id)


# Go to Directory
@login_required(login_url='/login/')
def get_dir(request, dir_id):
    dir = get_object_or_404(Directory, pk=dir_id, owner=request.user)
    upload_file_form = FileUploadForm()

    return render(request, 'filesys/panel.html', {'directory': dir, 'upload_file_form': upload_file_form})


# Make directory
@login_required(login_url='/login/')
def make_dir(request, dir_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    cur_dir = get_object_or_404(Directory, pk=dir_id, owner=request.user)
    if not is_name_unique(request, cur_dir, request.POST['dir-name']):
        return HttpResponseBadRequest("Directory name is not unique.")

    new_dir_abs_path = get_abs_path(cur_dir.abs_path, request.POST['dir-name'])
    new_dir = Directory(parent_dir=cur_dir,
                        owner=request.user, abs_path=new_dir_abs_path)
    new_dir.save()

    return redirect('filesys:get-dir', dir_id=dir_id)


# Delete Directory
@login_required(login_url='/login/')
def remove_dir(request, dir_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    cur_dir = get_object_or_404(Directory, pk=dir_id, owner=request.user)
    dir_to_remove = get_object_or_404(
        Directory, pk=request.POST['dir-id'], owner=request.user, parent_dir=cur_dir)
    dir_to_remove.delete()

    return redirect('filesys:get-dir', dir_id=dir_id)


# Upload file
@login_required(login_url='/login/')
def upload_file(request, dir_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    uploaded_file = list(request.FILES.values())[0]
    cur_dir = get_object_or_404(Directory, pk=dir_id, owner=request.user)
    if not is_name_unique(request, cur_dir, uploaded_file.name):
        return HttpResponseBadRequest("File name is not unique.")
    new_file_abs_path = get_abs_path(cur_dir.abs_path, uploaded_file.name)
    new_file = File(parent_dir=cur_dir, owner=request.user,
                    abs_path=new_file_abs_path, file=uploaded_file)
    new_file.save()

    return redirect('filesys:get-dir', dir_id=dir_id)


# Delete file
@login_required(login_url='/login/')
def remove_file(request, dir_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    cur_dir = get_object_or_404(Directory, pk=dir_id, owner=request.user)
    file_to_remove = get_object_or_404(
        File, pk=request.POST['file-id'], owner=request.user, parent_dir=cur_dir)
    file_to_remove_path = './' + os.path.join(
        settings.MEDIA_ROOT, file_to_remove.file.name)
    os.remove(file_to_remove_path)
    file_to_remove.delete()

    return redirect('filesys:get-dir', dir_id=dir_id)


# Download file
@login_required(login_url='/login/')
def get_file(request, file_id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    file = get_object_or_404(File, pk=file_id, owner=request.user)
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
    with open(file_path, 'rb') as f:
        response = HttpResponse(
            f.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + \
            os.path.basename(file_path)
        return response
