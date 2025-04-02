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
# 8. post read 기능 업데이트
1️⃣ `settings.py`에서 미디어 파일 설정
- 업로드한 사진을 저장할 위치를 설정하기 위해 `MEDIA_ROOT`와 `MEDIA_URL`을 추가함.

- ```python
    # 업로드한 사진을 저장할 위치 (실제 폴더 경로)
    MEDIA_ROOT = BASE_DIR / 'media'

    # 미디어 경로를 처리할 URL
    MEDIA_URL = '/media/'
    ```
이렇게 설정하면, Django가 업로드된 미디어 파일을 media/ 폴더에 저장하고, MEDIA_URL을 통해 접근할 수 있게 됨.

2️⃣ `templates/` 폴더에 `_card.html` 파일 생성
게시글을 카드 형식으로 보기 위해 `posts/templates/` 폴더에 `_card.html`을 만듦.

- ```html

    <div class="card my-3" style="width: 18rem;">
     <div class="card-header">
         <p>username</p>
     </div>
     <img src="{{ post.image.url }}" class="" alt="..."> 
        # post.image.url → 업로드된 이미지의 경로를 불러옴.
     <div class="card-body">
       <!-- <h5 class="card-title">Card title</h5> -->
       <p class="card-text">{{ post.content }}</p>
       # post.content → 게시글 내용을 표시함.
       <p class="card-text">{{ post.created_at }}</p>
       # post.created_at → 게시글이 작성된 날짜를 표시함.
       <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
     </div>
 </div>
        ```

3️⃣ `index.html`에서 `_card.html` 포함
-  `_card.html`을 재사용하기 위해 index.html에서 {% include '_card.html' %}을 추가함.

- ```python
     {% extends 'base.html' %}

     {% block body %}
        {% for post in posts %} # 모든 게시글을 반복해서 _card.html을 사용함.
            {% include '_card.html' %}
                 # _card.html 템플릿을 포함하여 게시글을 카드 형태로 표시함.
        {% endfor %}
    {% endblock %}


4️⃣ `base.html`에서 컨테이너 추가
- `base.html`에서 `<div class="container">`를 추가하여 템플릿 구조를 정리함.

- ```html

    <div class="container">
        # container 클래스를 사용하여 페이지의 전체적인 여백을 조정함.
        {% block body %}
        {% endblock %}
        # {% block body %}{% endblock %}을 감싸서 모든 페이지에서 적용되도록 설정함.
    </div>
    ```

# 9. post create 기능 구현
1️⃣ `INSTALLED_APPS`에 `django_bootstrap5` 추가
- `settings.py`에서 `INSTALLED_APPS`에 `'django_bootstrap5'`를 추가하여 Bootstrap을 활용한 폼 스타일을 사용할 수 있도록 설정함.
- `pip install django-bootstrap5` 명령어 실행 
-   ```python

    INSTALLED_APPS = [
    ...
    'django_bootstrap5',
    ]
    ```
2️⃣ `posts/urls.py`에 `create` 경로 추가
- 게시글을 생성할 페이지`(create/)`를 위한 URL을 `posts/urls.py`에 추가함.

- ``` python

    urlpatterns = [
    path('create/', views.create, name='create'),
    ]
    path('create/', views.create, name='create')
  ```  


3️⃣ `forms.py`에서 `PostForm` 생성
- 게시글을 생성할 때 사용할 폼을 `forms.py`에 작성함.

- ``` python

    from django.forms import ModelForm
    from .models import Post

    class PostForm(ModelForm):
        class Meta:
            model = Post
            fields = '__all__'
    #ModelForm을 사용하여 Post 모델을 기반으로 입력 폼을 생성함.
    ```


4️⃣ `views.py`에서 `create` 함수 작성
사용자가 글을 작성하고 저장할 수 있도록 `create` 함수를 작성함.

- ```python
    from django.shortcuts import render, redirect
    from .forms import PostForm

    def create(request):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect('posts:index')
            else:
                form = PostForm()
    
            context = {
            'form': form,
            }
        return render(request, 'create.html', context)
    # 동작 과정
    #GET 요청 → 비어있는 폼을 생성해서 create.html에 전달함.

    #POST 요청

    #사용자가 입력한 데이터로 PostForm 객체를 생성함.

    #form.is_valid()로 데이터 검증을 수행함.

    #유효한 데이터면 form.save()로 저장하고, index 페이지로 이동함.

    #유효하지 않으면 다시 폼을 보여줌.

5️⃣ `create.html` 생성
- `posts/templates/` 폴더에 `create.html`을 만들어 폼을 렌더링함.

- ```html
    {% extends 'base.html' %}
    {% load django_bootstrap5 %}

    {% block body %}
    <form action="" method="POST" enctype="multipart/form-data">
        {% csrf_token %} → 보안상 필요한 CSRF 토큰을 추가함.

        {% bootstrap_form form %}
        <input type="submit" value="💛" style="background-color: #FFFACD; color: black; border: 1px solid #FFD700; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
    </form>
    {% endblock %}
    ```

6️⃣  `nav.html` 생성 (네비게이션 바 추가)
- `templates/` 폴더에 `nav.html`을 생성하여 상단 네비게이션 바를 만듦.

- ```html
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'posts:index' %}">insta</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <a class="nav-link" href="{% url 'posts:create' %}">Create</a>
          <a class="nav-link" href="#">Signup</a>
          <a class="nav-link" href="#">Login</a>
        </div>
      </div>
    </div>
    </nav>
    ```




