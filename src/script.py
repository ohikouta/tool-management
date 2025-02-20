from django.contrib.auth.models import User
from app.models import Project

user = User.objects.get(username="test2")

# 例: プロジェクト名が 'サンプルプロジェクト' という場合
project = Project.objects.get(name="小松商店街支援")
print(project.members.all())  # ここに <User: test1> が含まれているか？

projects = Project.objects.filter(members__in=[user])
print(projects)  # ここで該当のプロジェクトが出てくるか？