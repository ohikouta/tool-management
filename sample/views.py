from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import SWOT
from .models import SwotIdeas

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

# SWOTの保存処理
def add_swot(request):
    if request.method == 'POST':
        # SWOTテーブル
        title = request.POST.get('title')
        swot_instance = SWOT.objects.create(title=title)

        # 4象限のデータ取得
        strengths = request.POST.get('strengths')
        weaknesses = request.POST.get('weaknesses')
        opportunities = request.POST.get('opportunities')
        threats = request.POST.get('threats')

        # swotideasテーブル
        SwotIdeas.objects.create(
            category='Strengths',
            content=strengths,
            swot = swot_instance
        )
        SwotIdeas.objects.create(
            category='Weaknesses',
            content=weaknesses,
            swot = swot_instance
        )
        SwotIdeas.objects.create(
            category='Opportunity',
            content=opportunities,
            swot = swot_instance
        )
        SwotIdeas.objects.create(
            category='Threats',
            content=threats,
            swot = swot_instance
        )

        # リダイレクトではなく同じページを再度レンダリングする
        swot_data = SWOT.objects.all()
        return render(request, 'swot.html', {'swot_data': swot_data, 'success_message': 'SWOTが正常に追加されました'})
    return render(request, 'swot.html')

# 作成したSWOTを表示するための関数
def idea_detail(request, id):
    # SWOTオブジェクトを取得する
    swot = get_object_or_404(SWOT, pk=id)

    # SWOTに関連するすべてのswotideasレコードを取得する
    swotideas = swot.swotideas_set.all()

    context = {
        'swot': swot,
        'swotideas': swotideas,
    }
    return render(request, 'idea_detail.html', context)

"""
Strengths: 強いな
Weaknesses: 弱いな
Opportunity: 機会だな
Threats: 脅威だな

"""