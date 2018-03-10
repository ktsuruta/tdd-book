from django.shortcuts import render, redirect
from lists.models import Item, List
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html',{'list':list_ })

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    redirect_url = '/lists/' + str(list_.id) + '/'
    return redirect(redirect_url)

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    redirect_url = '/lists/' + str(list_.id) + '/'
    return redirect(redirect_url)
