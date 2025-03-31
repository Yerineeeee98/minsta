# 1. 가상환경 활성화
- `python -m venv venv`
- `source venv/Scripts/activate`
- `pip install django`
# 2. .gitignore 설정
# 3. startproject/ startapp
- `django-admin startproject insta .`
- `django-admin startapp posts`
- pjt `settings.py`에 앱 등록하기
# 4. 'base.html' 구조 잡기
- 프로젝트와 앱 외부에 templates 폴더 생성
- pjt `settings.py`에 `'DIRS': [BASE_DIR / 'templates'],` 등록하기
- `{% block body %}`
    `{% endblock %}`의 의미 : 템플릿에서 원하는 내용으로 변경할 수 있는 부분을 만든다는 의미
    - 다른 템플릿에서 이 부분을 원하는 대로 채울 수 있음
# 5. Post modeling/migration
- post의 `models.py`에
    - ```python
        class Post(models.Model): # Django 모델 정의
            content = models.TextField() # 게시글 내용용
            created_at = models.DateTimeField(auto_now_add=True) # 생성된 날짜짜
             image = models.ImageField(upload_to='image') # 이미지 업로드
      ```
- models.py에서 POST클래스를 정의한 이유는 장고의 데이터베이스 모델을 만들기 위해서 이 모델을 기반으로 데이터베이스 테이블이 생성되고, 다른 곳에서 불러와 사용할 수 있음
- 이 클래스느 데이터베이스의 posts_post 테이블로 변환
- 다른곳(views.py, .html 등)에서 post 객체를 불러와 사용할 수 있음
- ✨ Post 모델 사용
    - 1. 모델을 만든 다음 디비에 적용해야됨
        - `python manage.py makemigrations`
        -  `python manage.py migrate`
        - 위에 명령어를 실행하면 장고가 post모델을 테이블로 만들어줌
# 6. admin에 POST모델등록
- posts 앱의 admin.py에 `admin.site.register(Post)` 추가하고 `python manage.py createsuperuser`로 계정생성해주기
# 7. post read 기능 구현하기
- 1️⃣ 프로젝트의  `urls.py`에 `posts` 앱 연결
`insta/urls.py` 파일에서 `path('posts/', include('posts.urls'))` 코드를 추가한 이유는:

    - posts/ 경로로 들어오는 요청을 posts 앱의 URL로 넘겨주기 위해서. 즉, posts 앱에서 정의한 URL 패턴을 사용하게 되는 것.

```python
from django.urls import path, include

urlpatterns = [
    path('posts/', include('posts.urls')),  # posts 앱의 URL 패턴을 연결
]
```
- 2️⃣ posts 앱의 urls.py 파일에 경로 정의
    - `posts/urls.py` 파일에서 `path('', views.index, name="index")` 코드를 작성한 이유는:

    - 빈 경로('')로 들어오는 요청에 대해 `views.index` 함수가 실행되도록 연결한 것. 즉, `posts/` 경로로 들어오면 `index` 함수가 호출되어 그에 해당하는 내용을 반환하게 되는 거지.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),  # 빈 경로로 index 뷰 연결
]
```
- 3️⃣ views.py에서 index 함수 작성
    - **views.py**에서 index 함수를 작성한 이유는:

        - `Post` 모델을 사용해서 모든 게시글을 쿼리하여 `index.html` 템플릿에 데이터를 전달하는 역할. `Post.objects.all()`로 게시글을 모두 가져오고, 이를 `context` 딕셔너리로 `index.html`에 전달하는 거야.

```python
from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all()  # 모든 게시글을 가져옴
    
    context = {
        'posts': posts,  # 템플릿에 전달할 데이터
    }
    
    return render(request, 'index.html', context)  # 템플릿을 렌더링하고 context 전달
```
- 4️⃣ index.html에서 게시글 표시
    - index.html 파일에서 게시글을 표시하려면:

    - `{% for post in posts %}`로 `posts` 객체를 반복문으로 순회하면서, 각 post의 내용을 출력해야 해.

```python
{% extends 'base.html' %}

{% block body %}
    {% for post in posts %}
        <p>{{ post.content }}</p>  <!-- 게시글 내용 -->
        <p><img src="{{ post.image.url }}" alt="Post Image"></p>  <!-- 게시글 이미지 -->
    {% endfor %}
{% endblock %}
```