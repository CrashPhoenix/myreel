from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from myreel.forms import UserForm, UserProfileForm, MovieForm
from django.template import RequestContext
from myreel.models import Person, Character, CrewMember, Genre, Studio, Movie, Poster, Backdrop, Profile, Logo, Reel, UserProfile
from rottentomatoes import RT
import tmdb3
import os

def set_tmdb3_key(function, *kwargs):
    def new_function():
        tmdb3.set_key(os.environ['TMDB_KEY'])
        function(*kwargs)
    return new_function

#@set_tmdb3_key
def index(request):
    tmdb3.set_key(os.environ['TMDB_KEY'])
    context = RequestContext(request)
    user = request.user

    data = { 
        'user': user,
        'showButton': True,
        'width': '180px',
        'height': '267px'
    }

    rt = RT()
    in_theaters = rt.movies('in_theaters')
    movies = []
    for movie in in_theaters:
        if 'alternate_ids' in movie.keys():
            if 'imdb' in movie['alternate_ids'].keys():
                imdb_id = 'tt{0}'.format(movie['alternate_ids']['imdb'])
                tmdb3_movie = tmdb3.Movie.fromIMDB(imdb_id)
                if tmdb3_movie.poster is not None:
                    movie_info = {
                        'tmdb_id': tmdb3_movie.id,
                        'poster': tmdb3_movie.poster.geturl(),
                        'title': tmdb3_movie.title
                    }
                    movies.append(movie_info)
    data['movies'] = movies

    if user.is_authenticated():
        profile = user.profile

        if not profile.reels.filter(name='Favorites').exists():
            _create_user_profile_reel(request, "Favorites")
        if not profile.reels.filter(name='Watch List').exists():
            _create_user_profile_reel(request, "Watch List")

        favorites = profile.reels.get(name='Favorites')
        watchlist = profile.reels.get(name='Watch List')
    else:
        data['showButton'] = False
    
    '''
    rt = RT()
    movies = rt.movies('in_theaters')
    data['movies'] = movies

    for movie in movies:
        movie = _fix_poster_links(movie)

        if user.is_authenticated():
            if favorites.movies.filter(tmdb_id=movie['id']).exists():
                movie['favorite'] = True
            else:
                movie['favorite'] = False
            if watchlist.movies.filter(tmdb_id=movie['id']).exists():
                movie['watchlist'] = True
            else:
                movie['watchlist'] = False
    '''

    return render_to_response('myreel/index.html', data, context)

def movie(request, tmdb_id):
    '''
    context = RequestContext(request)
    rt = RT()
    movie = rt.info(tmdb_id)
    movie = _fix_poster_links(movie)
    data = {
        'movie': movie,
        'form': MovieForm(),
    }
    return render_to_response('myreel/movie.html', data, context)
    '''
    pass

def add_movie(request):
    '''
    user = request.user
    if user.is_authenticated():
        profile = UserProfile.objects.get(user=user)
        
        rt = RT()
        tmdb_id = request.POST['tmdb_id']
        movie = rt.info(tmdb_id)

        # if the Movie exists in our database
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            movie_obj = Movie.objects.get(tmdb_id=tmdb_id)
        else: # otherwise, build the movie and save
            # first, build the movie
            movie_obj = Movie(
                            tmdb_id=movie['id'],
                            title=movie['title'],
                            year=movie['year'],
                            mpaa_rating=movie['mpaa_rating'],
                            runtime=movie['runtime'],
                            release_date=movie['release_dates']['theater'],
                            synopsis=movie['synopsis'],
                            studio=movie['studio']
                        )
            movie_obj.save()

            # next, build the genre object        
            for genre in movie['genres']:
                if Genre.objects.filter(genre=genre).exists():
                    genre_obj = Genre.objects.get(genre=genre)
                else:
                    genre_obj = Genre(genre=genre)
                    genre_obj.save()
                # add genres to movie's genres
                movie_obj.genres.add(genre_obj)

            # save movie
            movie_obj.save()

            # build a ratings model
            ratings_obj = Ratings(
                            critics_rating=movie['ratings']['critics_rating'],
                            critics_score=movie['ratings']['critics_score'],
                            audience_rating=movie['ratings']['audience_rating'],
                            audience_score=movie['ratings']['audience_score']
                        )
            # set to this movie and save
            ratings_obj.movie = movie_obj
            ratings_obj.save()

            # build a posters model
            posters_obj = Posters(
                            thumbnail=movie['posters']['thumbnail'],
                            profile=movie['posters']['original'].replace('tmb', 'pro'),
                            detailed=movie['posters']['original'].replace('tmb', 'det'),
                            original=movie['posters']['original'].replace('tmb', 'org')
                        )
            # set to this movie and save
            posters_obj.movie = movie_obj
            posters_obj.save()

            # one last save...just in case? ;)
            movie_obj.save()

        # update critic's concensus
        movie_obj.critics_consensus = movie['critics_consensus']
        movie_obj.save()

        favorites = profile.reels.get(name=request.POST['reel'])
        if not favorites.movies.filter(tmdb_id=tmdb_id).exists():
            favorites.movies.add(movie_obj)

        if request.POST['ajax']:
            return
        return HttpResponseRedirect('/profile')
    return HttpResponseRedirect('/')
    '''
    pass

def remove_movie(request):
    '''
    user = request.user
    if user.is_authenticated():
        profile = UserProfile.objects.get(user=user)
        tmdb_id = request.POST['tmdb_id']

        movie_obj = Movie.objects.get(tmdb_id=tmdb_id)
        favorites = profile.reels.get(name=request.POST['reel'])
        favorites.movies.remove(movie_obj)
        return HttpResponseRedirect('/profile')
    return HttpResponseRedirect('/')
    '''
    pass

def search(request):
    '''
    context = RequestContext(request)
    user = request.user

    data = { 
        'user': user,
        'showButton': True,
        'width': '180px',
        'height': '267px'
    }

    if user.is_authenticated():
        profile = user.profile

        if not profile.reels.filter(name='Favorites').exists():
            _create_user_profile_reel(request, "Favorites")
        if not profile.reels.filter(name='Watch List').exists():
            _create_user_profile_reel(request, "Watch List")

        favorites = profile.reels.get(name='Favorites')
        watchlist = profile.reels.get(name='Watch List')
    else:
        data['showButton'] = False
        
    
    rt = RT()
    movies = rt.search(request.POST['query'])
    data['movies'] = movies

    for movie in movies:
        movie = _fix_poster_links(movie)

        if user.is_authenticated():
            if favorites.movies.filter(tmdb_id=movie['id']).exists():
                movie['favorite'] = True
            else:
                movie['favorite'] = False
            if watchlist.movies.filter(tmdb_id=movie['id']).exists():
                movie['watchlist'] = True
            else:
                movie['watchlist'] = False

    return render_to_response('myreel/index.html', data, context)
    '''
    pass

def profile(request):
    user = request.user
    if user.is_authenticated():
        context = RequestContext(request)
        profile = user.profile

    else: 
        return HttpResponseRedirect('/')

    favorites = profile.reels.get(name='Favorites')
    watchlist = profile.reels.get(name='Watch List')
    
    data = {
        'user': user,
        'favorites': favorites.movies.all(),
        'watchlist': watchlist.movies.all(),
        'form': MovieForm()
    }
    return render_to_response('myreel/profile.html', data, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

'''
def _fix_poster_links(movie):
    thumbnail = movie['posters']['thumbnail']
    movie['posters']['profile'] = thumbnail.replace('tmb', 'pro')
    movie['posters']['original'] = thumbnail.replace('tmb', 'org')
    movie['posters']['detailed'] = thumbnail.replace('tmb', 'det')
    return movie
'''

def _create_user_profile_reel(request, name):
    user = request.user
    profile = user.profile

    profile.reels.create(
        name=name
    )
    profile.save()
    return