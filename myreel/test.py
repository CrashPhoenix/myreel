import datetime

from django.utils import timezone
from django.test import TestCase

from myreel.models import Movie
from myreel.views import add_movie_to_db

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import svm
import tmdb3, os

class RecommenderTests(TestCase):

    def setUp(self):
        add_movie_to_db(11)
        add_movie_to_db(190859)

    def test_test_svm(self):
        """
        Asserts the correctness of svm
        """
        tmdb3.set_key(os.environ['TMDB_KEY'])
        movie = Movie.objects.get(tmdb_id=11)
        self.assertEqual(movie.title, 'Star Wars: Episode IV - A New Hope')

        movies = []
        movies.append(movie)
        movie = Movie.objects.get(tmdb_id=190859)
        movies.append(movie)

        print "*" * 20

        X = []
        y = []
        x = {}
        for movie in movies:
            for genre in movie.genres.all():
                if genre.genre not in x:
                    x[genre.genre] = 1
                else:
                    x[genre.genre] += 1
            for person in movie.cast.all():
                if person.person.name not in x:
                    x[person.person.name] = 1
                else:
                    x[person.person.name] += 1
            for person in movie.crew.all():
                if person.person.name not in x:
                    x[person.person.name] = 1
                else:
                    x[person.person.name] += 1

        for key in x.keys():
            x[key] = 1 - (1/x[key])

        new_movie = add_movie_to_db(207703) # Kingsman
        new_x = {}
        for genre in new_movie.genres.all():
            if genre.genre not in new_x:
                new_x[genre.genre] = 1
            else:
                new_x[genre.genre] += 1
        for person in new_movie.cast.all():
            if person.person.name not in new_x:
                new_x[person.person.name] = 1
            else:
                new_x[person.person.name] += 1
        for person in new_movie.crew.all():
            if person.person.name not in new_x:
                new_x[person.person.name] = 1
            else:
                new_x[person.person.name] += 1

        X.append(x)
        X.append(new_x)
        #y.append(1)

        vec = DictVectorizer()
        X = vec.fit_transform(X).toarray()
        x = vec.fit_transform(x).toarray()
        new_x = vec.fit_transform(new_x).toarray()

        print "*" * 20
        print 
        score = cosine_similarity(X[0], X[1]).astype(float)
        print score
        #print self.assertIsInstance(float(str(score.item)), float)
        print score.item(0,0)
        self.assertGreater(score.item(0,0), 0.9)
        print score.dtype

        #clf = svm.SVC()

        #print len(X)
        #print len(y)
        #clf.fit(X, y)

        # Get movie vector
        #movie = add_movie_to_db(tmdb_id)


        pass