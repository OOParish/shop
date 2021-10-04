from django.shortcuts import render

# Create your views here.
def zz(request):
    return render(
        request,'account/main.html')