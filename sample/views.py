from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import SWOT
from .models import SwotIdeas
import re

def my_view(request):
    context = {
        'name': 'World'
    }
    return render(request, 'index.html', context)

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



# 作成したSWOTを表示するための関数
# def idea_detail(request, id):
#     # SWOTオブジェクトを取得する
#     swot = get_object_or_404(SWOT, pk=id)

#     # SWOTに関連するすべてのswotideasレコードを取得する
#     swotideas = swot.swotideas_set.all()

#     context = {
#         'swot': swot,
#         'swotideas': swotideas,
#     }
#     return render(request, 'idea_detail.html', context)

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


"""
Strengths: 強いな
Weaknesses: 弱いな
Opportunity: 機会だな
Threats: 脅威だな

"""