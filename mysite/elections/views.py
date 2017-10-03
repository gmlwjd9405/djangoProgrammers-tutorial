from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

# Create your views here.
def index(request):
    # Candidate로 저장된 모든 DB의 내용을 불러와 확인
    candidates = Candidate.objects.all()

    return render(request, 'elections/index.html')

