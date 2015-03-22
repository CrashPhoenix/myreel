import datetime

from django.utils import timezone
from django.test import TestCase

from myreel.models import Movie
from myreel.views import add_movie_to_db

from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
import tmdb3, os

class RecommenderTests(TestCase):

    def setUp(self):
        add_movie_to_db(11)

    def test_test_svm(self):
        """
        Asserts the correctness of svm
        """
        tmdb3.set_key(os.environ['TMDB_KEY'])
        movie = Movie.objects.get(tmdb_id=11)
        self.assertEqual(movie.title, 'Star Wars: Episode IV - A New Hope')

        movies = []
        movies.append(movie)

        X = []
        y = []
        for movie in movies:
            x = {}
            for genre in movie.genres.all():
                x[genre.genre] = 1
            for person in movie.cast.all():
                x[person.person.name] = 1
            for person in movie.crew.all():
                x[person.person.name] = 1

        X.append(x)
        y.append(1)

        vec = DictVectorizer()
        X = vec.fit_transform(X).toarray()

        clf = svm.SVC()

        print len(X)
        print len(y)
        clf.fit(X, y)

        # Get movie vector
        #movie = add_movie_to_db(tmdb_id)


        pass