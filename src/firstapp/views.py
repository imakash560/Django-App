from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404,render
from django.urls import reverse

from .models import Choice, Question

import datetime
from django.utils import timezone

# Create your views here.

def index(request):
	latest_question_list=Question.objects.order_by('-pub_date')
	#template=loader.get_template('firstapp/index.html')
	context={
		'latest_question_list': latest_question_list,
	}
	return render(request,'firstapp/index.html',context)
def addq(request):
	if request.method == 'POST':
		newq=request.POST.get('new_question')
		q = Question(question_text=newq,pub_date=timezone.now())
		q.save()

		return render(request,'firstapp/addq.html')
	else:	
		return render(request,'firstapp/addq.html')

def detail(request,question_id):
	question=get_object_or_404(Question,pk=question_id)
	return render(request,'firstapp/detail.html',{'question':question})

def results(request,question_id):
	response="You're looking at the results of question %s."
	return render(request,'firstapp/results.html')

def vote(request,question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=int(request.POST['choice']))
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'firstapp/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('firstapp:results', args=(question.id,)))
