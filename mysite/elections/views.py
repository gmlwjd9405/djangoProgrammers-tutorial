from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

# Create your views here.
def index(request):
    # Candidate로 저장된 모든 DB의 내용을 불러와 확인
    candidates = Candidate.objects.all()
    # dictionary 구조로 DB에 있는 내용을 가져온다.
    context = {'candidates' : candidates}

    # context로 html에 모든 후보에 대한 정보를 전달
    return render(request, 'elections/index.html', context)

