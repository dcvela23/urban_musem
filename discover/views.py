from django.shortcuts import render, get_object_or_404
from museums.models import Museum
from django.contrib.auth.models import User
# Search
from itertools import chain
#Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.

def paginator(request, get_discover, num_per_page):

    paginator = Paginator(get_discover, num_per_page)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return results



def get_discover(request):
    latest_places = Museum.objects.all().order_by('-created_date')
    latest_places_limited = paginator(request, latest_places, 6)
    most_viewed = Museum.objects.all().order_by('-views')
    most_viewed_limited = paginator(request, most_viewed,8)
    args = {'latest_places': latest_places_limited, 'most_viewed': most_viewed_limited}
    return render (request, 'discover_home.html', args)

def get_result(request):
    keyword = request.POST["searchy"]

    #search for places: City and Country (show one format of result: list of museums

    country_list = Museum.objects.filter(country__icontains=keyword)
    city_list = Museum.objects.filter(city__contains=keyword)
    title_list = Museum.objects.filter(title__contains=keyword)
    place_list = list(chain(country_list, city_list, title_list))
    place_list = list(set(place_list))
    place_list_limited = paginator(request, place_list, 5)

    #search for Users(show one format of result: list of museums

    username_list = User.objects.filter(username__icontains=keyword)
    username_list = list(chain(username_list))
    username_list_limited = paginator(request, username_list, 5)
    args = {'results_place': place_list_limited, 'results_username':username_list_limited}
    return render(request, 'result_discover.html', args)

def latest_places(request):
    latest_places = Museum.objects.all().order_by('-created_date')
    latest_places_limited = paginator(request, latest_places, 5)
    return render(request, 'latest_places.html', {'latest_places': latest_places_limited})

def most_viewed(request):
    most_viewed = Museum.objects.all().order_by('-views')
    most_viewed_limited = paginator(request, most_viewed, 5)
    return render(request, 'most_viewed.html', {'most_viewed': most_viewed_limited})


def museum_user(request, id):
    user = get_object_or_404(User, pk=id)
    user_museums = Museum.objects.filter(author=user)
    args = {'user':user, 'user_museums':user_museums}
    return render(request, "user_museum.html", args)

