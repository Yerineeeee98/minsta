from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    posts = Post.objects.all()
    
    context = {
        'posts': posts, 
    }
    
    return render(request, 'index.html', context)

@login_required
def create(request):
    
    # 모든 경우의 수
    # -GET :form을 만들어서 html 문서를 사용자에게 리턴
    # -POST : invalid data (데이터 검증 실패)
    # -POST : valid data (데이터 검증 성공)
    
    # new/ - > 빈종이를 보여주는 기능
    # create - >  사용자가 입력한 데이터 저장
    # -------
    # GET create/ => 빈 종이를 보여주는 기능
    # POST create/ => 사용자가 입력한 데이터 저장
  
   # 5. POST 요청(invalid data가 들어올 때) 
   # 10. POST 요청 (valid data가 들어올 때)
    if request.method == 'POST':
        # 6. 사용자가 입력한 데이터  (request.POST)를 form 생성(invalid한 데이터)
        # 7. 사용자가 입력한 데이터  (request.POST)를 form 생성(valid한 데이터)
        form = PostForm(request.POST, request.FILES)
        
        # 7. form의 유효성 검증(실패)
        # 12. form을 검증 (성공)
        if form.is_valid(): # 이상한 데이터인지 아닌지 검증하기(데이터가 유효한지 아닌지)
            # 13. form 저장
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # 14. index로 redirect
            return redirect('posts:index')
    else: # 유효하지 않으면 다시 작성하라고 하기
        form = PostForm()
        
    context = {
        'form': form,
         }
    return render(request, 'create.html', context)
    
    # # 1. GET 요청
    # else: # 빈종이를 보여주는 기능
    #     # 2. 비어있는 form을 만든다.
    #     form = PostForm()
        
    # # 3. context dict에 비어있는 form을 담는다.
    # # 8. context dict에 검증에 실패한 form을 담는다.
    # context = {
    #     'form': form,
            
    #     }
    # # 4. create.html을 랜더링 (주어진 데이터를 화면에 시각적으로 표현하는 과정)
    # # 9. create.html을 랜더링
    # return render(request, 'create.html', context)