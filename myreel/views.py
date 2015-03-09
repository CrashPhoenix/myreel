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

def set_tmdb3_key(function):
    def new_function(request, **kwargs):
        tmdb3.set_key(os.environ['TMDB_KEY'])
        return function(request, **kwargs)
    return new_function

@set_tmdb3_key
def index(request):
    #tmdb3.set_key(os.environ['TMDB_KEY'])
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

@set_tmdb3_key
def movie(request, tmdb_id):
    context = RequestContext(request)
    '''
    rt = RT()
    movie = rt.info(tmdb_id)
    movie = _fix_poster_links(movie)
    '''
    movie = tmdb3.Movie(tmdb_id)
    data = {
        'movie': movie,
        'poster': movie.poster.geturl(),
        'form': MovieForm(),
    }
    return render_to_response('myreel/movie.html', data, context)

def add_movie(request):
    user = request.user
    if user.is_authenticated():
        profile = UserProfile.objects.get(user=user)
        
        tmdb_id = request.POST['tmdb_id']
        movie = tmdb3.Movie(tmdb_id)

        # if the Movie exists in our database
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            movie_obj = Movie.objects.get(tmdb_id=tmdb_id)
        else: # otherwise, build the movie and save
            # first, build the movie
            movie_obj = Movie(
                            tmdb_id=movie.id,
                            imdb_id=movie.imdb,
                            title=movie.title,
                            overview=movie.overview,
                            release_date=movie.releasedate,
                            popularity=movie.popularity,
                            user_rating=movie.userrating,
                            votes=movie.votes,
                            adult=movie.adult
                        )
            movie_obj.save()

            # next, build the genre object        
            for genre in movie.genres:
                if Genre.objects.filter(tmdb_id=genre.id).exists():
                    genre_obj = Genre.objects.get(tmdb_id=genre.id)
                else:
                    genre_obj = Genre(
                                    tmdb_id=genre.id,
                                    genre=genre.name
                                )
                    genre_obj.save()
                # add genres to movie's genres
                movie_obj.genres.add(genre_obj)

            # save movie
            movie_obj.save()

            # build poster models
            for poster in movie.posters:
                posters_obj = Posters()
                if 'w92' in poster.sizes():
                    posters_obj.w92 = poster.geturl('w92')
                if 'w154' in poster.sizes():
                    posters_obj.w154 = poster.geturl('w154')
                if 'w185' in poster.sizes():
                    posters_obj.w185 = poster.geturl('w185')
                if 'w342' in poster.sizes():
                    posters_obj.w342 = poster.geturl('w342')
                if 'w500' in poster.sizes():
                    posters_obj.w500 = poster.geturl('w500')
                if 'w780' in poster.sizes():
                    posters_obj.w780 = poster.geturl('w780')
                if 'original' in poster.sizes():
                    posters_obj.original = poster.geturl('original')
                # set to this movie and save
                posters_obj.movie = movie_obj
                posters_obj.save()

            # build backdrop models
            for backdrop in movie.backdrops:
                backdrop_obj = Backdrop()
                if 'w300' in backdrop.sizes():
                    backdrop_obj.w300 = backdrop.geturl('w300')
                if 'w780' in backdrop.sizes():
                    backdrop_obj.w780 = backdrop.geturl('w780')
                if 'w1280' in backdrop.sizes():
                    backdrop_obj.w1280 = backdrop.geturl('w1280')
                if 'original' in backdrop.sizes():
                    backdrop_obj.original = backdrop.geturl('original')
                # set to this movie and save
                backdrop_obj.movie = movie_obj
                backdrop_obj.save()

            # build studio models
            for studio in movie.studios:
                if Studio.objects.filter(tmdb_id=studio.id).exists():
                    studio_obj = Studio.objects.get(tmdb_id=studio.id)
                else:
                    studio_obj = Studio(
                                    tmdb_id=studio.id,
                                    studio=studio.name,
                                    description=studio.description
                                )
                    if studio.logo:
                        logo_obj = Logo()
                        if 'w45' in studio.logo.sizes():
                            logo_obj.w45 = studio.logo.geturl('w45')
                        if 'w92' in studio.logo.sizes():
                            logo_obj.w92 = studio.logo.geturl('w92')
                        if 'w154' in studio.logo.sizes():
                            logo_obj.w154 = studio.logo.geturl('w154')
                        if 'w185' in studio.logo.sizes():
                            logo_obj.w185 = studio.logo.geturl('w185')
                        if 'w300' in studio.logo.sizes():
                            logo_obj.w300 = studio.logo.geturl('w300')
                        if 'w500' in studio.logo.sizes():
                            logo_obj.w500 = studio.logo.geturl('w500')
                        if 'original' in studio.logo.sizes():
                            logo_obj.original = studio.logo.geturl('original')
                        # set to this studio and save
                        logo_obj.studio = studio_obj
                        logo_obj.save()
                studio_obj.save()
                # add studio to movie's studios
                movie_obj.studios.add(studio_obj)

            # build cast models
            for actor in movie.cast:
                if Person.objects.filter(tmdb_id=actor.id).exists():
                    person_obj = Person.objects.get(tmdb_id=actor.id)
                else:
                    person_obj = Person(
                                tmdb_id=actor.id,
                                name=actor.name,
                                biography=actor.biography
                            )
                    if actor.dayofbirth:
                        person_obj.dayofbirth = actor.dayofbirth
                    person_obj.save()
                character_obj = Character(
                                character=actor.character
                            )
                character_obj.person = person
                character_obj.save()
                # add actor to movie's cast
                movie_obj.cast.add(character_obj)

            # build crew models
            for crewMember in movie.crew:
                if Person.objects.filter(tmdb_id=crewMember.id).exists():
                    person_obj = Person.objects.get(tmdb_id=crewMember.id)
                else:
                    person_obj = Person(
                                tmdb_id=crewMember.id,
                                name=crewMember.name,
                                biography=crewMember.biography
                            )
                    if crewMember.dayofbirth:
                        person_obj.dayofbirth = crewMember.dayofbirth
                    person_obj.save()
                crewMember_obj = CrewMember(
                                job=crewMember.job
                            )
                crewMember_obj.person = person
                crewMember_obj.save()
                # add actor to movie's crew
                movie_obj.crew.add(crewMember_obj)

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