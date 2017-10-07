from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.db.models import Sum
from .models import Candidate, Poll, Choice

import datetime

# Create your views here.
def index(request):
    # Candidate로 저장된 모든 DB의 내용을 불러와 확인
    candidates = Candidate.objects.all()
    # dictionary 구조로 DB에 있는 내용을 가져온다.
    context = {'candidates': candidates}

    # context로 html에 모든 후보에 대한 정보를 전달
    return render(request, 'elections/index.html', context)

def candidates(request, name):
    candidate = get_object_or_404(Candidate, name=name)
    # try:
    #     candidate = Candidate.object.get(name=name)
    # except:
    #     # return HttpResponseNotFound("없는 페이지 입니다.")
    #     raise Http404
    return HttpResponse(candidate.name)

def areas(request, area):
    # 현재 시간
    today = datetime.datetime.now()
    print("############", today)

    # 현재 진행 중인 Poll을 확인
    try:
        # get에 인자로 조건을 전달
        poll = Poll.objects.get(area=area, start_date__lte=today, end_date__gte=today)
        # Candidate의 area(앞)와 매개변수 area(뒤)가 같은 객체만 불러오기
        candidates = Candidate.objects.filter(area=area)
    except:
        poll = None
        candidates = None

    context = {'candidates': candidates, 'area': area, 'poll': poll}
    print("############", context)

    return render(request, 'elections/area.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    # 사용자가 입력한 것을 받아온다. (area.html에서 name="choice"의 value 받아온다)
    selection = request.POST['choice']
    print("############", poll_id)
    try:
        # (Choice의 poll_id)와 객체 poll의 id값이 같고, (Choice의 candidate_id)와 사용자가 입력한 selection이 같은 객체를 불러오기
        choice = Choice.objects.get(poll_id=poll.id, candidate_id=selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성한다.
        choice = Choice(poll_id=poll.id, candidate_id=selection, votes=1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area=area)
    polls = Poll.objects.filter(area=area) # 여러 개의 여론조사가 있음
    poll_results = [] # list

    for poll in polls:
        result = {} # dictionary
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date

        # poll.id에 해당하는 전체 투표수
        total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes')) # dictionary
        result['total_votes'] = total_votes['votes__sum']

        rates = [] # 지지율
        for candidate in candidates:
            # choice가 하나도 없는 경우 - 예외처리로 0을 append
            try:
                choice = Choice.objects.get(poll=poll, candidate=candidate)
                rates.append(
                    round(choice.votes * 100 / result['total_votes'], 1) # 소수점 첫 번째 자리까지만 넘겨준다
                    )
            except :
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates': candidates, 'area': area, 'poll_results': poll_results}
    return render(request, 'elections/result.html', context)