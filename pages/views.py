# views.py
import requests
from django.shortcuts import render

def mainpage(request):
    # API 요청을 보내 데이터 받아오기
    api_key = '5868b084'
    # 추천 영화 데이터 가져오기
    recommended_url = f'http://www.omdbapi.com/?s=Batman&apikey={api_key}'
    recommended_response = requests.get(recommended_url)
    recommended_movies = recommended_response.json().get('Search', [])
    # 검색된 영화 데이터 가져오기
    query = request.GET.get('query', '')
    sort = request.GET.get('sort', 'desc')
    movies_url = f'http://www.omdbapi.com/?s={query}&apikey={api_key}'
    movies_response = requests.get(movies_url)
    movies = movies_response.json().get('Search', [])
    # 정렬
    movies.sort(key=lambda movie: int(movie['Year']), reverse=(sort == 'desc'))
    # 기존의 코드를 유지하면서, 추가로 recommended_movies와 movies를 context로 전달합니다.
    return render(request, 'pages/mainpage.html', {'recommended_movies': recommended_movies, 'movies': movies})

def company(request):
    return render(request, 'pages/company_info.html')

def movie_detail(request, movie_id):
    api_key = '5868b084'
    url = f'http://www.omdbapi.com/?i={movie_id}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if 'Response' in data and data['Response'] == 'True':
        return render(request, 'pages/movie_detail.html', {'movie': data})
    else:
        return JsonResponse({'error': 'Unable to fetch data'}, status=500)
