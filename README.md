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
            created_at = models.DateTimeField(auto_now_add=True) # 생성된 날짜
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

    - `{% for post in posts %}`로 `posts` 객체를 반복문으로 순회하면서, 각 post의 내용을 출력해야함함.

```python
{% extends 'base.html' %}

{% block body %}
    {% for post in posts %}
        <p>{{ post.content }}</p>  <!-- 게시글 내용 -->
        <p><img src="{{ post.image.url }}" alt="Post Image"></p>  <!-- 게시글 이미지 -->
    {% endfor %}
{% endblock %}
```
# 8. media 설정
1️⃣ `settings.py`에서 미디어 파일 설정
- ```python
    # 업로드한 사진을 저장한 위치 (실제 폴더 경로)
    MEDIA_ROOT = BASE_DIR / 'image' → 업로드된 파일이 저장될 실제 폴더 경로를 BASE_DIR/image로 설정함.

    # 미디어 경로를 처리할 URL
    MEDIA_URL = '/image/' → 미디어 파일을 불러올 때 사용할 URL 경로를 /image/로 지정함.
                            예를 들어, post.image.url을 사용하면 /image/파일이름.jpg와 같은 URL이 만들어짐.
    ```

2️⃣ `urls.py`에서 미디어 URL 연결
- `insta/urls.py`에서 `MEDIA_URL`과 `MEDIA_ROOT`를 추가하여, 미디어 파일을 브라우저에서 접근할 수 있도록 설정함.

- ``` python
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
    ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # → 개발 환경에서 Django가 MEDIA_URL로 요청된 파일을 MEDIA_ROOT에서 찾아 제공하도록 설정함.
     # (운영 환경에서는 웹 서버(Nginx, Apache)가 이 역할을 대신함.)
  ```

3️⃣ `models.py`에서 `ImageField` 설정 확인
- 이미지 업로드가 가능하도록 `models.py`에서 `ImageField`가 올바르게 설정되어 있어야 함.
- `image = models.ImageField(upload_to='image')`
    - 업로드된 이미지가 image 폴더에 저장됨.

# 9. post read 기능 업데이트
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

# 10. post create 기능 구현
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



# 11. image resize 기능 추가
1️⃣ `posts/models.py`에서 이미지 필드 수정
- 기존 `ImageField`를 `ResizedImageField`로 변경

- 이미지 크기를 500x500으로 조정

- 이미지를 중앙(middle, center)에서 크롭

- upload_to='image/%Y/%m'을 설정해 연/월 단위로 이미지 저장

- ```python

    from django_resized import ResizedImageField

    image = ResizedImageField(
    size=[500, 500],  # 이미지 크기 조정 (500x500)
    crop=['middle', 'center'],  # 중앙에서 크롭
    upload_to='image/%Y/%m'  # 연/월별로 이미지 저장
    )
    ```
2️⃣ `requirements.txt` 업데이트
- `django-bootstrap5==25.1`

- `django-resized==1.0.3`

3️⃣ 필수 패키지 설치 `(pip install)`
- 아래 명령어 실행해서 django-resized 라이브러리 설치
- `pip install django-resized`

4️⃣ `migrations` 적용
- 모델을 수정했으므로 데이터베이스에 반영해야 함
- `python manage.py makemigrations`
- `python manage.py migrate`

---
# 12. accounts app 생성
- `django-admin startapp accounts`

---
# 13. 회원가입 기능 구현
👉 **forms.py**를 만든 이유?
- 회원가입 시 입력을 쉽게 처리하기 위해

- Django 기본 회원가입 폼(`UserCreationForm`)을 가져와 커스텀해서 사용자가 추가 정보를 입력할 수 있도록 만듦.

- 입력된 데이터의 검증 및 유효성 체크

- 사용자가 입력한 데이터가 올바른지 확인하고, 잘못된 데이터를 방지함.

- 폼을 통해 HTML 입력 폼을 자동 생성할 수 있음

- Django의 forms.py를 이용하면 {{ form }}만으로 HTML 입력 폼을 생성할 수 있어 코드가 간결해짐.

**1️⃣** `accounts` 앱 생성
- `accounts` 앱을 생성해서 회원가입 기능을 따로 관리하도록 함.

2️⃣ `forms.py` (회원가입 폼 생성)
- 📌 `accounts/forms.py`
- ```python
    from django.contrib.auth.forms import UserCreationForm  # Django 기본 회원가입 폼 가져옴
    from .models import User  # 사용자 모델 가져옴

    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = User  # User 모델을 기반으로 회원가입 폼 생성
            fields = ('username', 'profile_image',)  # 회원가입 시 받을 정보
    ```
- ✅ 설명
    - `UserCreationForm`: `Django` 기본 회원가입 폼을 상속받아 커스텀한 폼.

    - `model = User`: `User` 모델과 연결하여 회원 정보를 데이터베이스에 저장할 수 있도록 함.

    - `fields = ('username', 'profile_image',)`: 회원가입 시 사용자명과 프로필 이미지를 입력받도록 설정.

3️⃣ `urls.py` (URL 설정)
- 📌 `accounts/urls.py`
- ```python

    from django.urls import path
    from . import views

    app_name = 'accounts'  # URL 네임스페이스 설정

    urlpatterns = [
        path('signup/', views.signup, name='signup'),  # 회원가입 페이지 URL 추가
    ]
    ```    
- ✅ 설명
    - `app_name = 'accounts'`: 다른 앱과 URL 네임스페이스가 겹치지 않도록 설정.

    - `path('signup/', views.signup, name='signup')`: `/accounts/signup/`으로 접근하면 `views.signup` 실행.

4️⃣ `views.py` (회원가입 로직)
- 📌 `accounts/views.py`
- ```python
    from django.shortcuts import render, redirect
    from .forms import CustomUserCreationForm

    def signup(request):
        if request.method == 'POST':  # 회원가입 폼 제출 시
            form = CustomUserCreationForm(request.POST, request.FILES)
            if form.is_valid():  # 입력 데이터 검증
                form.save()  # 회원가입 완료 (DB에 저장)
                return redirect('posts:index')  # 회원가입 후 게시물 리스트 페이지로 이동
    
        else:  # GET 요청 시 (회원가입 폼 띄우기)
            form = CustomUserCreationForm()

        context = {'form': form}  # 폼을 템플릿으로 전달
        return render(request, 'signup.html', context)
- ✅ 설명
    - `if request.method == 'POST'`: 사용자가 회원가입 정보를 입력한 후 제출했을 때 실행.

    - `form = CustomUserCreationForm(request.POST, request.FILES)`: 사용자가 입력한 데이터로 폼 생성.

    - `if form.is_valid()`: 데이터가 유효하면 저장.

    - `form.save()`: 입력받은 회원 정보를 DB에 저장.

    - `return redirect('posts:index')`: 회원가입 후 게시물 리스트 페이지(/posts/)로 이동.

    - `else`: `GET` 요청일 경우 빈 회원가입 폼을 띄움.

    - `context = {'form': form}`: 폼을 `signup.html` 템플릿으로 전달.

5️⃣ `insta/urls.py` (전체 URL 연결)
- 📌 `insta/urls.py`
- ```python
    from django.urls import path, include
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        path('accounts/', include('accounts.urls')),  # accounts 앱의 URL 포함
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 미디어 파일 URL 설정
    ```
- ✅ 설명
    - `path('accounts/', include('accounts.urls'))`: `/accounts/`로 시작하는 요청을 `accounts/urls.py`에서 처리하도록 설정.

    - `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`: 사용자가 업로드한 미디어 파일을 처리할 수 있도록 설정.

6️⃣ `signup.html` (회원가입 템플릿)
- 📌 `accounts/templates/signup.html`
- ```html
    {% extends 'base.html' %}
    {% load django_bootstrap5 %}

    {% block body %}

    <form action="" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {% bootstrap_form form %}
        <input type="submit" class="btn btn-primary">
    </form>

    {% endblock %}
  ```
- ✅ 설명
    - `{% extends 'base.html' %}`: `base.html` 레이아웃을 확장하여 사용.

    - `{% load django_bootstrap5 %}`: Django Bootstrap5 기능을 로드하여 폼을 부트스트랩 스타일로 적용.

    - `action=""`: 현재 페이지에서 폼을 제출.

    - `method="POST"`: 데이터를 서버에 전송.

    - `enctype="multipart/form-data"`: 이미지 업로드를 위해 설정.

    - `{% csrf_token %}`: 보안 토큰 추가.

    - `{% bootstrap_form form %}`: 폼을 부트스트랩 스타일로 출력.

    - `<input type="submit" class="btn btn-primary">`: 제출 버튼 생성.

- 📌 전체 과정 요약
    - accounts 앱 생성

        - 회원가입 기능을 따로 관리하기 위해 새로운 앱을 생성.

    - 회원가입 폼 (forms.py)

        - Django 기본 회원가입 폼(UserCreationForm)을 상속받아 커스텀함.

        - username과 profile_image 필드를 입력받도록 설정.

    - URL 설정 (accounts/urls.py)

        - /accounts/signup/으로 접근하면 views.signup이 실행되도록 설정.

    - 회원가입 로직 (views.py)

        - POST 요청 시: 입력한 데이터가 유효하면 회원가입 처리 후 게시물 리스트 페이지(/posts/)로 이동.

        - GET 요청 시: 빈 회원가입 폼을 보여줌.

    - 프로젝트 URL 설정 (insta/urls.py)

        - accounts 앱의 URL을 프로젝트에 포함.

        - static() 설정을 추가해 업로드한 미디어 파일을 처리할 수 있도록 설정.

    - 회원가입 템플릿 (signup.html)

        - base.html을 확장하여 부트스트랩 스타일을 적용한 회원가입 폼 생성.

---
# 14. 로그인 기능 구현
1️⃣ 로그인 폼 생성 – `accounts/forms.py`
- ```python
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

    class CustomAuthenticationForm(AuthenticationForm):
    pass
    ```
    - 💡 설명:
        - `AuthenticationForm`: `Django`에서 기본 제공하는 로그인 폼 클래스

        - `CustomAuthenticationForm`: 기본 로그인 폼을 그대로 사용할 거지만, 커스터마이징할 준비를 위해 클래스를 따로 만들어줌

2️⃣ 로그인 URL 연결 – `accounts/urls.py`
- ```python
    from django.urls import path
    from . import views

    app_name = 'accounts'

    urlpatterns = [
        path('signup/', views.signup, name='signup'),
        path('login/', views.login, name='login'),  # 로그인 URL 추가!
    ]
    ```
    - 💡 설명:
        - `path('login/', views.login, name='login')`: `/accounts/login/`으로 접속하면 `login 뷰 함수`가 실행.

3️⃣ 로그인 뷰 함수 – `accounts/views.py`
- ```python
    from .forms import CustomUserCreationForm, CustomAuthenticationForm
    from django.contrib.auth import login as auth_login 
    from django.shortcuts import render, redirect

    def login(request):
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, request.POST)  # 사용자 입력 데이터 받기
            if form.is_valid():  # 입력된 데이터가 유효하다면
                user = form.get_user()  # 로그인할 사용자 객체 가져옴
                auth_login(request, user)  # 로그인 처리 (세션에 사용자 정보 저장)
            return redirect('posts:index')  # 로그인 후 게시물 목록으로 이동
        else:
            form = CustomAuthenticationForm()  # GET 요청일 경우, 빈 로그인 폼 생성

        context = {
            'form': form,
        }

        return render(request, 'login.html', context)  # 로그인 템플릿 렌더링
    ```
    - 💡 설명 요약:
        - `auth_login(request, user)`: `Django` 내부에서 세션을 생성하고 로그인 상태로 만들어주는 함수

        - `request, request.POST`: 로그인 폼은 인증 관련 보안 처리를 위해 `request` 객체도 같이 넘겨줘야 함.

    - `form.get_user()`: 인증이 완료된 사용자 객체를 가져오는 메서드.

4️⃣ 로그인 템플릿 – `accounts/templates/login.html`
- ```html
    {% load django_bootstrap5 %}

    {% block body %}
        <form action="" method ="POST">
            {% csrf_token %}
            {% bootstrap_form form %}
            <input type="submit" value="💛 login" 
               style="background-color: #fff8b5; 
                      color: black;
                      border: none;  테두리 없음
                      border-radius: 50px; 둥글게 
                      padding: 10px 20px; 위아래 양옆 여백
                      font-size: 16px;
                      font-weight: bold; 두껍게
                      cursor: pointer;"> 마우스 커서를 갖다대면 클릭모양으로 바뀌게
        </form>
     
    {% endblock %}
    ```
    - 💡 설명:
        - `{% csrf_token %}`: 보안 토큰은 필수, 안 넣으면 POST 요청에서 에러가 남.

        - `{% bootstrap_form form %}`: 부트스트랩으로 자동 스타일링된 폼 출력.

        - `<input type="submit">`: 로그인 버튼을 예쁘게 스타일링해준 부분

✅ 요약 흐름
- 1️⃣	CustomAuthenticationForm 폼으로 사용자 입력을 받을 준비를 함
- 2️⃣	/accounts/login/ URL 설정
- 3️⃣	로그인 뷰 함수에서 로그인 처리 (auth_login)
- 4️⃣	템플릿에서 로그인 폼 보여주고 버튼 누르면 POST로 처리


---
# 15. 로그아웃 기능 구현
1️⃣ 로그아웃 URL 설정
- 📌 `accounts/urls.py`

- ```python
    from django.urls import path
    from . import views

    app_name = 'accounts'

    urlpatterns = [
        path('signup/', views.signup, name='signup'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),  # 🔥 로그아웃 추가
    ]
    ```
    - ✅ 설명

        - `path('logout/', views.logout, name='logout')`: `/accounts/logout/`으로 접근하면 로그아웃 처리.

2️⃣ 로그아웃 로직
- 📌 `accounts/views.py`

- ```python
    from django.contrib.auth import logout as auth_logout

    def logout(request):
        auth_logout(request)  # 세션 종료 → 로그아웃 처리
        return redirect('posts:index')  # 로그아웃 후 메인 페이지로 이동
  ```  
    - ✅ 설명

        - ` auth_logout(request)`: `Django` 내부 세션 삭제 → 로그아웃 완료.

        - `redirect('posts:index')`: 로그아웃 후 게시물 목록 페이지`(/posts/)`로 이동.

3️⃣ 내비게이션 바에 표시
- 📌 `templates/_nav.html`

- ```html
    {% if user.is_authenticated %}
        <a class="nav-link" href="{% url 'posts:create' %}">Create</a>
        <a class="nav-link" href="{% url 'accounts:logout' %}">logout</a>
        <a class="nav-link disabled" href="">{{ user }}</a>
    {% else %}
        <a class="nav-link" href="{% url 'accounts:signup' %}">Signup</a>
        <a class="nav-link" href="{% url 'accounts:login' %}">login</a>
    {% endif %}
    ```
    - ✅ 설명

        - `user.is_authenticated`: 로그인 상태인지 판별.

        - 로그인 상태면 → Create, logout, 사용자명 표시.

        - 로그아웃 상태면 → Signup, login 링크 표시.

- 📌 전체 과정 요약
    - ✅ 1. 로그아웃 URL 연결 (accounts/urls.py)
        - /accounts/logout/ 경로에 로그아웃 뷰 연결.

    - ✅ 2. 로그아웃 로직 (views.py)
        - 세션 종료 → 사용자 로그아웃 → 게시글 페이지로 이동.

    - ✅ 3. 로그인 상태에 따른 메뉴 표시 (_nav.html)
        - 로그인 되어 있으면 Create, logout, 사용자 이름 표시.

        - 로그인 안 되어 있으면 Signup, login 버튼만 표시.

# 16. post create/read 기능 업데이트
1️⃣ PostForm 필드 수정
- 📌 `posts/forms.py`

- ```python
    from django import forms
    from .models import Post

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ('content', 'image', )  # ✅ 필요한 필드만 지정
  ```  
    - ✅ 설명

        - 원래는 `fields = '__all__'`로 모든 필드를 다 폼에 포함시켰지만, `user` 필드는 사용자 입력이 아닌, `view`에서 자동으로 지정해야 하므로 제외해야 함.

        - 그래서 명시적으로 `('content', 'image')`만 폼에 포함시킴.

2️⃣ 사용자 정보 출력
- 📌 `posts/templates/_card.html`

- ```html
    <img class="rounded-circle" src="{{ post.user.profile_image.url }}" alt="" width="30px">
    <a href="">{{ post.user.username }}</a>
    ```
    - ✅ 설명

        - 게시글 카드에 작성자 프로필 사진과 유저 이름을 표시.

        - `post.user.profile_image.url`: 유저의 프로필 이미지 경로.

        - `post.user.username`: 유저 이름.

3️⃣ 게시글 작성 뷰 수정
- 📌 `posts/views.py`

- ```python
    from django.contrib.auth.decorators import login_required
    from .forms import PostForm

    @login_required  # 로그인한 유저만 접근 가능
    def create(request):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)  # ✅ 저장을 잠시 멈춤
                post.user = request.user       # ✅ 작성자 정보 추가
                post.save()                    # ✅ 최종 저장
                return redirect('posts:index')
        else:
            form = PostForm()

        context = {
            'form': form,
            }
        return render(request, 'posts/form.html', context)
    ```
    - ✅ 설명

        - `@login_required`: 로그인하지 않으면 `/accounts/login/`으로 리다이렉트됨.

        - `form.save(commit=False)`: DB에 저장하지 않고 객체만 생성.

        - `post.user = request.user`: 현재 로그인한 유저를 post 작성자로 설정.

        - `post.save()`: 작성자 정보를 포함한 post를 DB에 저장.

📌 전체 요약
- ✅ 1. 폼 필드 제한 (forms.py)
    - 사용자가 입력해야 할 필드만 명확하게 설정 (content, image).
    - 자동으로 설정될 필드(user)는 제외.

- ✅ 2. 카드 템플릿에 작성자 표시 (_card.html)
    - 게시물 목록에 작성자 이름과 프로필 사진 추가.

- ✅ 3. 게시글 작성 로직 개선 (views.py)
    - 로그인한 사용자만 글 작성 가능.

    - 작성자 정보(post.user)를 자동으로 설정.


