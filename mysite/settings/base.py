"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import psycopg2
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  #引用了相关静态文件的库
    'ckeditor',  #富文本编辑器
    'ckeditor_uploader',#添加图片上传功能
    "myblog.apps.MyblogConfig",
    "read_statistics.apps.ReadStatisticsConfig",
    "comment.apps.CommentConfig",
    "likes.apps.LikesConfig",
    "user.apps.UserConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR
                         ,'templates'),
        ],
        'APP_DIRS': True,  #true的意思是app里面的templates都是有效的，可以访问
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.login_modal_form'
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

#数据库采用外接数据库postgresql
DATABASE_PASSWORD=os.environ['DATABASE_PASSWORD']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myblog',
        'USER': 'postgres',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  #设置页面为中文界面

TIME_ZONE = 'Asia/Shanghai'  #设置时区为北京时间

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR
                 , 'static'),
]

#MEDIA
MEDIA_URL ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')


#配置ckeditor
CKEDITOR_UPLOAD_PATH='UPLOAD/'
CKEDITOR_CONFIGS={
    'default':{
        'language':'zh-cn',
                # 编辑器的宽高请根据你的页面自行设置
                'width':'730px',
                'height':'150px',
                'image_previewText':' ',
                'tabSpaces': 4,
                'toolbar': 'Custom',
                # 添加按钮在这里
                'toolbar_Custom': [
                    ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
                    ["TextColor", "BGColor", "RemoveFormat"],
                    ["NumberedList", "BulletecList"],
                    ["Link", "Unlink"],
                    ["Smiley", "SpecialChar", "Blockquote", 'CodeSnippet'],
                ],
                # 插件
                'extraPlugins': ','.join(['codesnippet','uploadimage','prism','widget','lineutils',]),


    },
    'comment_ckeditor':{
        'toolbar':'custom',  #定义工具栏名称
        'toolbar_custom':[
            ['Bold','Italic','Underline','Strike','Subscript','Superscript'],
            ["TextColor","BGColor","RemoveFormat"],
            ["NumberedList","BulletecList"],
            ["Link","Unlink"],
            ["Smiley","SpecialChar","Blockquote",'CodeSnippet'],
        ],
        'width': 'auto',
        'height': '180',
        'tabSpaces':4,
        'removePlugins':'elementspath',
        'resize_enabled':False,
        # 添加按钮在这里
       # 插件
        'extraPlugins': ','.join(['codesnippet','widget','lineutils',]),
    }

}



# 自定义的参数
BLOGS_NUM_OF_EACH_PAGE = 4   #规定每一页有多少个博客

#缓存设置
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.db.DatabaseCache',
        'LOCATION':'my_cache_table'
    }
}


