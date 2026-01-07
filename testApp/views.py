import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from rest_framework import generics
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer
from django.http import JsonResponse



def timeline(request):
    query = request.GET.get('q')
    
    if query:
        posts = (
            Post.objects
            .select_related('author')
            .filter(content__icontains=query)
            .order_by('-created_at')
        )
    else:
        posts = (
            Post.objects
            .select_related('author')
            .order_by('-created_at')
        )
    
    context = {
        'posts': posts,
        'query': query,
    }
    
    return render(request, 'timeline.html', context)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

# Create your views here.
@login_required
def post_create(request):
    # 1. POSTリクエスト（送信ボタン押下時）の処理
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('timeline')
        # (POSTで無効だった場合は、下の 'return render' に進む)
    # 2. GETリクエスト（ページ初回表示時）の処理
    else:
        form = PostForm()  # 空のフォームを作成
    
    # 3. GETリクエスト、または POSTが失敗した場合
    return render(request, 'post_create.html', {'form': form})

def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk) # 権限チェック：投稿者とログインユーザーが一致しない場合はリダイレクト
  if request.user != post.author:
     return redirect('post_detail', pk=pk)
  if request.method == 'POST':
     # 既存のインスタンスを渡してフォームを生成
     form = PostForm(request.POST, instance=post)
     if form.is_valid():
        form.save()
        return redirect('post_detail', pk=pk)
  else:
    # 既存のインスタンスを渡してフォームを生成（初期表示）
    form = PostForm(instance=post)
  return render(request, 'post_edit.html', {'form': form, 'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
         return redirect('post_detail', pk=pk)
    if request.method == 'POST':
       post.delete() # データを削除
       return redirect('timeline') # タイムラインにリダイレクト
    return render(request, 'post_confirm_delete.html', {'post': post})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required
def post_create(request):
    if request.method == 'POST':               
        form = PostForm(request.POST)
        if form.is_valid():                    
            post = form.save(commit=False)   
            post.author = request.user        
            post.save()                       
            return redirect('timeline')        
    else:
        form = PostForm()                      
    
    return render(request, 'post_create.html', {'form': form})

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def weather(request):
    locations = {
        'Kanazawa': {'lat': 36.59, 'lon': 136.60},
        'Tokyo': {'lat': 35.68, 'lon': 139.76},
        'Osaka': {'lat': 34.69, 'lon': 135.50},
        'Sapporo': {'lat': 43.06, 'lon': 141.35},
        'Naha': {'lat': 26.21, 'lon': 127.68},
        'HokurikuUniversity': {'lat': 36.54, 'lon': 136.68},
    }
    
    city_name = 'Kanazawa'
    if request.GET.get('city') and request.GET.get('city') in locations:
        city_name = request.GET.get('city')
    
    lat = locations[city_name]['lat']
    lon = locations[city_name]['lon']
    
    api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
    
    response = requests.get(api_url)
    data = response.json()
    
    context = {
        'city': city_name,
        'temperature': data['current_weather']['temperature'],
        'windspeed': data['current_weather']['windspeed'],
        'weathercode': data['current_weather']['weathercode'],
    }
    
    return render(request, 'weather.html', context)



def chat_view(request):
    return render(request, "chat.html")
def ask_gemini(request):
    if request.method == "POST":
        user_input = request.POST.get("question", "")
        if not user_input:
            return JsonResponse({"error": "質問を入力してください"}, status=400)

        API_KEY = "AIzaSyBs8rzZXome00OT23tQL5hrVVwOCwjnJNg"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

        payload = {
            "contents": [{"parts": [{"text": user_input}]}]
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()
            reply = (
                data.get("candidates", [{}])[0]
                   .get("content", {})
                   .get("parts", [{}])[0]
                   .get("text", "回答がありません")
            )
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    
    return JsonResponse({"error": "このエンドポイントは POST リクエストのみ対応しています"}, status=400)