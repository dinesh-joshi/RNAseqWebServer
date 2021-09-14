from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from dataUpload.models import Task
import os
import tarfile
import scanpy as sc


# PATH = "/media/dinesh/New Volume/thesis/RnaSeq/media"


def fileUpload(request):

    if request.method == "POST":
        # request.Files is a dictionary type object containing all files with key = file name mentioned in the html input tag
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
            newtask = Task(file=request_file)
            newtask.save()
            filename = newtask.file.name
            # generate_adata(extract(filename))
            newtask.path_to_tar = newtask.extract(filename)
            adata = newtask.generate_adata()
            newtask.save()
            # here the requestion session key-value is added
            request.session['file_id'] = newtask.file_id

    return render(request, 'dataUpload/dataUpload.html')
