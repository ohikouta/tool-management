from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import SWOT
from .models import SwotIdeas
import re
from django.http import HttpResponseForbidden
from .forms import FourPAnalysisForm, SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # 登録後、トップページへリダイレクトする例
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_profile(request):
    # request.userにログイン中のユーザー情報が入っている
    return render(request, 'profile.html', {'user': request.user})

def hello_view(request):
    context = {
        'name': 'World'
    }
    return render(request, 'hello.html', context)

# SWOTへの導線
def to_swot(request):
    swots = SWOT.objects.all()
    context = {
        'swots': swots
    }
    return render(request, 'swot.html', context)

def four_p(request):
    if request.method == 'POST':
        form = FourPAnalysisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('four_p_display')  # 送信後のリダイレクト先（例）
    else:
        form = FourPAnalysisForm()
    
    context = {
        'form': form,
    }
    return render(request, 'four_p.html', context)

# SWOTの保存処理: add_swot1つ目これは修正したい
def add_swot(request):
    if request.method == 'POST':
        print(f'requestの内容を確認しよう -> {request.POST.keys()}')
        # SWOTテーブル
        title = request.POST.get('title')
        swot_instance = SWOT.objects.create(title=title)

        # 4象限のデータ取得
        strengths = request.POST.get('strengths')
        print(strengths)
        weaknesses = request.POST.get('weaknesses')
        opportunities = request.POST.get('opportunities')
        threats = request.POST.get('threats')

        # swotideasテーブル
        SwotIdeas.objects.create(
            category='strengths',
            content=strengths,
            swot = swot_instance
        )
        SwotIdeas.objects.create(
            category='weaknesses',
            content=weaknesses,
            swot = swot_instance
        )
        SwotIdeas.objects.create(
            category='opportunity',
            content=opportunities,
            swot = swot_instance
        )
        SwotIdeas.objects.create(
            category='threats',
            content=threats,
            swot = swot_instance
        )

        # リダイレクトではなく同じページを再度レンダリングする
        swot_data = SWOT.objects.all()
        return render(request, 'swot.html', {'swot_data': swot_data, 'success_message': 'SWOTが正常に追加されました'})
    return render(request, 'swot.html')



def add_swot(request):
    if request.method == 'POST':
        # SWOTテーブル
        title = request.POST.get('title')
        swot_instance = SWOT.objects.create(title=title)

        # 正規表現パターンをコンパイル
        pattern = re.compile(r'^(strengths|weaknesses|opportunities|threats)(_)?(\d+)?$')

        # POSTデータのキーと値を走査
        for key, value in request.POST.items():
            # キーが正規表現パターンに一致する場合のみ処理
            if pattern.match(key):
                base_key = pattern.match(key).group(1)
                SwotIdeas.objects.create(
                    category=base_key.capitalize(),
                    content=value,
                    swot=swot_instance
                )

        # リダイレクトではなく同じページを再度レンダリングする
        swot_data = SWOT.objects.all()
        return render(request, 'swot.html', {'swot_data': swot_data, 'success_message': 'SWOTが正常に追加されました'})
    return render(request, 'swot.html')





def idea_detail(request, id):
    # SWOTオブジェクトを取得する
    swot = get_object_or_404(SWOT, pk=id)

    # SWOTに関連するすべてのswotideasレコードを取得する
    swot_ideas = {
        'Strength': swot.swotideas_set.filter(category='Strengths'),
        'Weakness': swot.swotideas_set.filter(category='Weaknesses'),
        'Opportunity': swot.swotideas_set.filter(category='Opportunity'),
        'Threat': swot.swotideas_set.filter(category='Threats'),
    }

    context = {
        'swot': swot,
        'swot_ideas': swot_ideas,
    }
    return render(request, 'idea_detail.html', context)

# swotの削除
def delete_swot(request, id):
    if request.method == 'POST':
        swot = get_object_or_404(SWOT, id=id)
        swot.delete()
        return redirect('swot_list')
    return HttpResponseForbidden()

"""
Strengths: 強いな
Weaknesses: 弱いな
Opportunity: 機会だな
Threats: 脅威だな

"""