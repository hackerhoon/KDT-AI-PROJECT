from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Coffee
from .forms import CoffeeForm
# Create your views here.
def index(request):
    #return HttpResponse("<h1>Hello World!<h1>")
    nums = [1,2,3,4,5]
    return render(request , 'index.html', {"my_list" : nums})

def introduce(request):
    #return HttpResponse("<h1>Hello World!<h1>")
    context = {
        'name': '한지훈',
        'intro' : '현재 1학기만 남은 휴학생입니다.',
        'major' : '''사이버보안을 전공하였고 학부연구생으로 연구를 참여하며\n
          악성 패킷과 정상 패킷을 구분하면서 인공지능을 접하였습니다.''',
    }
    return render(request , 'introduce.html', context)

def coffee_view(request):
    coffee_all = Coffee.objects.all()
    # 만약 requset가 POST 라면:
        # POST를 바탕으로 Form을 완성하고
        # Form이 유효하면 - > 저장!
    if request.method == "POST":
        form = CoffeeForm(request.POST) # 완성된 Form
        if form.is_valid(): # 채워진 Form이 유효하다면
            form.save() # 이 Form 내용을 Model에 저장

    form = CoffeeForm()
    return render(request, 'coffee.html', {"coffee_list": coffee_all, 'coffee_form': form})

def add_coffee(request):
    coffee_all = Coffee.objects.all()

    if request.method == "POST":
        form = CoffeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/coffee')
    form = CoffeeForm()
    return render(request, 'coffees.html', {"coffee_list": coffee_all, 'coffee_form': form})

def update_coffee(request, pk):
    coffee = get_object_or_404(Coffee, pk=pk)
    if request.method == 'POST':
        form = CoffeeForm(request.POST, instance=coffee)
        if form.is_valid():
            form.save()
            return redirect('/coffee')
    form = CoffeeForm()
    return render(request, 'update_coffee.html', {'coffee_form': form})

def delete_coffee(request, pk):
    coffee = get_object_or_404(Coffee, pk=pk)
    if request.method == 'POST':
        coffee.delete()
        return redirect('/coffee')
    form = CoffeeForm()
    return render(request, 'delete_coffee.html', {'coffee_form': form})