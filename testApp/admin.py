from django.contrib import admin
# 同じフォルダにあるmodels.pyから、管理したいPostモデルをインポート
from .models import Post
# 「Postモデルを、この管理サイトで扱えるように登録します」という命令
admin.site.register(Post)