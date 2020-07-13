
from django.shortcuts import render


# Create your views here.
def about(request):
    return render(request, "about.html", {})

def profile(request):
    return render(request, "profile.html", {})

def slider(request):
    return render(request, "slider.html", {})

def create(request):
    return render(request, "create.html", {})

def viewresult(request):
    return render(request, "viewresult.html", {})

def delete(request):
    return render(request, "delete.html", {})

def deleted(request):
    return render(request, "deleted.html", {})

def created(request):
    return render(request, "created.html", {})

def download(request):
    return render(request, "download.html", {})

def upload(request):
    return render(request, "upload.html", {})

def finished(request):
    return render(request, "finished.html", {})

def introduccion (request):
    return render(request, "introduccion.html", {})

def slider_q(request):
    return render(request, "slider.html", {})

def start_q(request):
    return render(request, "start_q.html", {})

def sure(request):
    return render(request, "sure.html", {})

def start_r(request):
    return render(request, "start_r.html", {})

def read_r(request):
    return render(request, "start_r.html", {})

def read_r_uploaded(request):
    return render(request, "start_r_uploaded.html", {})

def warning(request):
    return render(request, "warning.html", {})



