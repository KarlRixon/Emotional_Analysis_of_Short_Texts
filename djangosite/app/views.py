from django.shortcuts import render
from django.http import HttpResponse
from mongoengine.queryset.visitor import Q
from .models import comment
# import os

# Create your views here.
def welcome(request):
	return HttpResponse("<h1>Welcome to my tiny Django site!</h1>")

def index(request, catergory=0, page=1):
	count=0
	query = None

	# load model predicted result


	# catergory
	if (catergory > 5) or (catergory < 0):
		catergory = 0
	if catergory == 0:
		query = comment.objects.all()
	elif catergory == 1:
		query = comment.objects((Q(comment_con__contains='大小')|Q(comment_con__contains='合适'))&Q(comment_star__gt=3))
	elif catergory == 2:
		query = comment.objects((Q(comment_con__contains='颜色')|Q(comment_con__contains='好看'))&Q(comment_star__gt=3))
	elif catergory == 3:
		query = comment.objects((Q(comment_con__contains='穿着')|Q(comment_con__contains='舒服'))&Q(comment_star__gt=3))
	elif catergory == 4:
		query = comment.objects((Q(comment_con__contains='物流')|Q(comment_con__contains='很快'))&Q(comment_star__gt=3))
	elif catergory == 5:
		query = comment.objects(Q(comment_con__contains='掉色')|Q(comment_con__contains='严重'))

	# page
	count = query.count()
	totalpage = (int(count/10)+1)
	pages = [page-1, page, page+1, totalpage]
	if pages[1] <= 1:
		pages[1] = 1
		pages[0] = 1
		pages[2] = 2
	if pages[1] >= totalpage:
		pages[1] = totalpage
		pages[2] = totalpage
		pages[0] = (totalpage-1)
	
	# result
	result = query.values_list('comment_star', 'comment_con', 'comment_time')[(page-1)*10: page*10]
	# print(result)

	context = {'catergory':catergory, 'pages':pages, 'comment': result}
	return render(request, 'app/index.html', context)