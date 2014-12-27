from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from myreel.forms import UserForm, UserProfileForm, MovieForm
from django.template import RequestContext
from myreel.models import Reel, Movie, Ratings, Posters, Actor, AbridgedCast, Director, AbridgedDirectors, Studio, Links, Genre, UserProfile
from rottentomatoes import RT
import os

def index(request):
    data = { 
        'user': request.user,
        'width': '180px',
        'height': '267px'
    }

    rt = RT()
    movies = rt.movies('in_theaters')
    data['movies'] = movies

    for movie in movies:
        movie = _fix_poster_links(movie)

    return render_to_response('myreel/index.html', data)

def movie(request, rt_id):
    context = RequestContext(request)
    rt = RT()
    movie = rt.info(rt_id)
    movie = _fix_poster_links(movie)
    data = {
        'movie': movie,
        'form': MovieForm(),
    }
    return render_to_response('myreel/movie.html', data, context)

def add_movie(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    
    rt = RT()
    rt_id = request.POST['rt_id']
    movie = rt.info(rt_id)

    # if the Movie exists in our database
    if Movie.objects.filter(rt_id=rt_id).exists():
        movie_obj = Movie.objects.get(rt_id=rt_id)
    else: # otherwise, build the movie and save
        # first, build the movie
        movie_obj = Movie(
                        rt_id=movie['id'],
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


    favorites = profile.reels.get(name='Favorites')
    favorites.movies.add(movie_obj)
    return HttpResponseRedirect('/profile')

def remove_movie(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    rt_id = request.POST['rt_id']

    movie_obj = Movie.objects.get(rt_id=rt_id)
    favorites = profile.reels.get(name='Favorites')
    favorites.movies.remove(movie_obj)
    return HttpResponseRedirect('/profile')

def profile(request):
    context = RequestContext(request)
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if not user.is_authenticated(): 
        return HttpResponseRedirect('/')

    favorites = profile.reels.get(name='Favorites')
    
    data = {
        'user': user,
        'favorites': favorites.movies.all(),
        'form': MovieForm()
    }
    return render_to_response('myreel/profile.html', data, context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the form is valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile.reels.create(
                name="Favorites"
            )
            profile.save()


            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
            #    profile.picture = request.FILES['picture']

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'myreel/register.html',
            {'user_form': user_form, 'profile_form': profile_form,
            'registered': registered}, context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('registration/login.html', {}, context)

    # Use the login_required() decorator to ensure only those logged in can access the view.

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def _fix_poster_links(movie):
    thumbnail = movie['posters']['thumbnail']
    movie['posters']['profile'] = thumbnail.replace('tmb', 'pro')
    movie['posters']['original'] = thumbnail.replace('tmb', 'org')
    movie['posters']['detailed'] = thumbnail.replace('tmb', 'det')
    return movie