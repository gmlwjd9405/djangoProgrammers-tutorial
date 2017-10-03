from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate, Poll, Choice

import datetime

# Create your views here.
def index(request):
    # Candidate로 저장된 모든 DB의 내용을 불러와 확인
    candidates = Candidate.objects.all()
    # dictionary 구조로 DB에 있는 내용을 가져온다.
    context = {'candidates' : candidates}

    # context로 html에 모든 후보에 대한 정보를 전달
    return render(request, 'elections/index.html', context)

def areas(request, area):
    # 현재 시
    today = datetime.datetime.now()

    # 현재 진행 중인 Poll을 확인
    try:
        # get에 인자로 조건을 전달
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte = today)
        # Candidate의 area(앞)와 매개변수 area(뒤)가 같은 객체만 불러오기
        candidates = Candidate.objects.filter(area = area)
    except:
        poll = None
        candidates = None

    context = {'candidates': candidates, 'area': area, 'poll': poll}

    return render(request, 'elections/area.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)
    # 사용자가 입력한 것을 받아온다. (area.html에서 name="choice"의 value 받아온다)
    selection = request.POST['choice']

    try:
        # (Choice의 poll_id)와 객체 poll의 id값이 같고, (Choice의 candidate_id)와 사용자가 입력한 selection이 같은 객체를 불러오기
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성한다.
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    return HttpResponse("finish")