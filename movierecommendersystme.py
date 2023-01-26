# -*- coding: utf-8 -*-
"""MovieRecommenderSystme.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FcRWYI_eQc3Reo60D2vrpIFjTeTwaw6z

## Objective:
The rapid growth of data collection has led to a new era of information.Data is being used to create more efficient systems and this is where Recommendation Systems come into play. Recommendation Systems are a type of **information filtering systems** as they improve the quality of search results and provides items that are more relevant to the search item or are realted to the search history of the user.



There are basically three types of recommender systems:-

- **Demographic Filtering** - They offered generalized recommendations to every user, based on movies popularity and/or genre. The Systems recommends the same movies to users with similar demographic features. Since each user is different, this approach is considered to be too simple. The basic idea behind this system is that movies that are more popular and critically acclaimed will have higher probability of being liked by the average audience.

- **Content Based Filtering** - They suggest similar items based on a particular item. This system used items metadata, such as genre, director, description, actors, etc. for movies, to make these recommendations. The general idea behind these recommender systems is that if a person liked a partical item, he or she will also like an ite, that is similar to it.

- **Collaborative Filtering** - This system matches persons with similar interests and provides recommendations based on this matching. Collaborative filters do not require items metadata like its content-based counterparts.

In this project we'll be building two types of   Movie Recommendation System (`Content Based Filtering` and `Collaborative Filtering`) using `Moviedatalens`. 

Let's load data and build the systems.

### Import Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

plt.style.use('fivethirtyeight')

"""### Loading Data Files"""

# Loading both ratings and movies dataset
ratings = pd.read_csv("/content/ratings.csv")
movies = pd.read_csv("/content/movies.csv")

"""#### Movie Dataset"""

# To know about movies dataset
movies.info()

"""From above table we can conclude that there is no null values present in the movie dataset."""

# Preview the data
movies.sample(5)

"""- In the title column year is mentioned with the movie name.We will remove the year because the user usually don't type the year, they only search by movie name. 

- In the genres columns, most of the moves consists od diferent genres.
"""

#Look into the total number of rows and columns
print("Total number of rows is : ",movies.shape[0])
print("Total number of columns is : ",movies.shape[1])

"""Let's check number of unique movies and unique genres."""

# Number of moviesId
print("The movies dataset has ", movies["movieId"].nunique(), "unique movies")

# Number of title
print("The movies dataset has", movies["title"].nunique(), "unique title")

# Number of genres
genres = []
for genre in movies.genres:
  x = genre.split("|")
  for i in x:
    if i not in genres:
      genres.append(str(i))
print("The movies dataset has", len(genres), "unique genres" )

# To look into different genres
genres

"""I think there 2 duplicates movie id are there.Let's figure out and remove these."""

# For finding the duplicates title
movies.groupby("title")["movieId"].count().sort_values(ascending=False).head()

"""Here we found `Men with Guns (1997)` and `War of the Worlds (2005)` are present twice. Let's drop it. First we need to find the index and then we will delete the item.




"""

# Search the movie index number so we can drop it
movies[movies.title=="Men with Guns (1997)"]

movies[movies.title=="War of the Worlds (2005)"]

#Let's drop the above two movies
movies.drop(index=[1403,6662],inplace=True)

"""The next task is remove the year from movie name."""

movies[["title","title2"]] = movies["title"].str.split("(", n = 1, expand = True)

movies.drop(["title2"],axis=1,inplace=True)
movies["title"] = movies["title"].str.rstrip()

#Review the updated dataset
movies.head()

"""##### Visulization"""

genres = []
for genre in movies.genres:
  x = genre.split("|")
  for i in x:
    if i not in genres:
      genres.append(str(i))

genres = str(genres)

movie_title = []
for title in movies.title:
  movie_title.append(title)
movies_title = str(movie_title)

wordcloud_genre = WordCloud(width=1500,height=800,background_color="black",min_font_size=2,
                            min_word_length=3).generate(genres)

wordcloud_title = WordCloud(width=1500,height=800,background_color="cyan",min_font_size=2,
                            min_word_length=3).generate(movies_title)

plt.figure(figsize=(30,10))
plt.axis("off")
plt.title("WORDCLOUD for Movies Genre", fontsize=30)
plt.imshow(wordcloud_genre)

plt.figure(figsize=(30,10))
plt.axis("off")
plt.title("WORDCLOUD for Movies Title", fontsize=30)
plt.imshow(wordcloud_title)

"""Now we have done with movies dataset. It's time to explore the ratings dataset.

#### Ratings Dataset
"""

# Take a look at the data
ratings.head()

"""There are four columns in the ratings dataset, userID, movieID, rating, and timestamp."""

# To know about ratings dataset
ratings.info()

"""The dataset has over 100k records, and there is no missing data."""

#Statistical analysis
ratings.describe()

"""From the above table we can conclude that: 
- The average rating is 3.5 and minimum and maximum rating is 0.5 and 5 respectively.
- There are 668 user who has given their ratings for 149532 movies.
"""

# Number of Users
print("The ratings dataset has ", ratings["userId"].nunique(), "unique users")

# Number of movies
print('The ratings dataset has', ratings['movieId'].nunique(), 'unique movies')

# Number of ratings
print('The ratings dataset has', ratings['rating'].nunique(), 'unique ratings')

# List of unique ratings
print('The unique ratings are', sorted(ratings['rating'].unique()))

"""##### Data Visualization"""

# Merging the above two files
df = pd.merge(ratings,movies,how="left",on="movieId")
df.head()

# To see top 10  movies with highest rating
high_rated_movies = df.groupby(["title"])[["rating"]].sum().sort_values("rating",ascending=False).head(10)
high_rated_movies

plt.figure(figsize=(10,8))
sns.barplot(data=high_rated_movies,x= "rating",y = high_rated_movies.index )
plt.title("Top 10 movies with higest rating", fontsize=20)
plt.show()

#Top 10 movies with highest number of ratings
high_rating_movies = df.groupby(["title"])[["rating"]].count().sort_values("rating",ascending=False).head(10)
high_rating_movies

plt.figure(figsize=(10,8))
sns.barplot(data=high_rating_movies,x= "rating",y = high_rating_movies.index )
plt.title("Top 10 movies with highest number of ratings", fontsize=20)
plt.show()

"""From the above two charts, we can conclude that:

- `Pulp Fiction`,`Forest Gump`, `Shawshank Redemption`, `Jurassic` etc. these movies are quite popular among the users.

- `Shawshank Redemption` movie has the highest ranking and but it's position is 3rd in number of ratings chart. May be people give high ratings to this movie.

## Objective 1  (General Filtering)

In this problem we will create a system where we need to filter genres wise movies with minimum reviews threshold.

To do this first of all we have merge movies data and ratings data.
"""

#Creating a new dataframe so that our existing dataframe remain the same.
movies_new = movies.copy()
ratings_new = ratings.copy()

#merge ratings_new and movies_new datasets
df_new = pd.merge(ratings_new,movies_new,on="movieId",how="inner")

#Take a look on the data
df_new.head()

"""Let's group the movies by title, count the number of ratings."""

#Create a new dataframe by grouping the movie title to show AverageMovie rating per movie and number of reviews per each movies.
df_agg_new = df_new.groupby(["genres","title"]).agg(AverageMovieRating = ("rating","mean"),
                                      NumReviews = ("rating", "count")).reset_index()
df_agg_new.head()

#Drop the no genres listed rows
df_agg_new = df_agg_new[df_agg_new.genres !="(no genres listed)"]
df_agg_new.head()

#Lets rename the columns name
df_agg_new.rename({"genres":"Genres","title":"Movie Title",
                   "AverageMovieRating": "Average Movie Rating","NumReviews":"Num Reviews"},axis=1,inplace=True)

#Sorted dataframe by num ratings
df_agg_new = df_agg_new.sort_values(by="Num Reviews",ascending=False)

df_agg_new.head()

"""Let's ask user which genres type movies they want to watch and how many numbers of result they want to see."""

askedGenre = input("Genre (g) : ")          #loading Genres type
reviewTrashold = int(input("Minimum reviews threshold (t) :")) # check minimum number of threshold
numberRecommendatio = int(input("Num recommendations (N) :"))  #Number of result user want to see
result = df_agg_new[(df_agg_new.Genres.str.contains(askedGenre,case=False)) & (df_agg_new["Num Reviews"] >= reviewTrashold)]
print(" ")
print("Output: ")
result[["Movie Title","Average Movie Rating","Num Reviews"]].reset_index(drop=True).head(numberRecommendatio)

"""Here we have found 5 movies name which are the comedy type movie and their number of reviews is more than 100.

## Objective 2  (Content based recommender system)
Content-based filtering is one popular technique of recommendation or recommender systems. The content or attributes of the things you like are referred to as `content`.

The goal behind content-based filtering is to classify products with specific keywords, learn what the customer likes, look up those terms in the database, and then recommend similar things.

In this problem we don't need ratings dataset. We can perform by considering only movie dataset.
"""

#read the data
movies.head()

"""The content-based recommendation system works on two method.
1.   Vector Spacing Method
2.   Classification Model

In this project we will use Vecto Spacing Method.

**Vector Spacing Method**
- In this method, a user vector is created which ranks the information provided by the usersuch as `ranting`. After this, an item vector is created where movies are ranked according to their genres on it.

- With the vector, every movie name is assigned a certain value by multiplying and getting the dot product of the user and item vector, and the value is then used for recommendation.

We will aaply **TFidfVectorizer** because it is perform better in machine learning model.It is work with the purpose of reflecting how important a word is to a document (sentence) in a corpus.
"""

#Define a TF-IDF Vectorizer Object.
cv = TfidfVectorizer()

#Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = cv.fit_transform(movies["genres"])

#Output the shape of tfidf_matrix
tfidf_matrix.shape

"""Since we have used the TF-IDF vectorizer, calculating the dot product will directly give us the cosine similarity score. Therefore, we will use sklearn's linear_kernel() instead of cosine_similarities() since it is faster."""

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)

indices=pd.Series(movies.index,index=movies['title'])  #Construct a reverse map of indices and movie titles
titles=movies["title"]      #To check only movies name

# Function that takes in movie title as input and outputs most similar movies
def recommendations(title,numberOfResults):
    
    # Get the index of the movie that matches the title
    idx = indices[title] 

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx])) 

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the  similar movies
    movie_list = titles.iloc[movie_indices][:numberOfResults].values
    movie_df = pd.DataFrame(movie_list,columns=["Movie Title"])
    return movie_df

movie_title = input("Movie Title (t): ").title()           #used title to capitalize every word in movies name
numRecommendation = int(input("Num recommendations (N): "))   #number of result want to see
print("Output: ")
recommendations(movie_title,numRecommendation)

"""Now we have created a content based movie recommender system.

## Objective 3 (Collaborative Filtering)

- **Collaborative filtering** is a technique used by websites like Amazon, YouTube, and Netflix. It filters out items that a user might like on the basis of reactions of similar users.

-  There are two categories of collaborative filtering algorithms: 
1.   Memory Based approach
2.   Model Based approach.

We will use Model Based approach to build system.

**Model based approach** involves building machine learning algorithms to predict user's ratings. They involve dimensionality reduction methods that reduce high dimensional matrix containing abundant number of missing values with a much smaller matrix in lower-dimensional space.

The recommender systems will be built using `surprise` package (Matrix Factorization - based models).
"""

!pip install surprise

from surprise import Dataset, Reader
from surprise import SVD, NMF
from surprise.model_selection import cross_validate, train_test_split, GridSearchCV

# Read the rating dataset
ratings.head()

# As we are loading a custom dataset, we need to define a reader.
# We provide rating scale from 0.5 to 5 because from stastical analysis table we saw that minimum rating  is 0 and maximum is 5.
reader = Reader(rating_scale=(0.5,5.0))       
data = Dataset.load_from_df(ratings[["userId","movieId","rating"]],reader)

print('Number of ratings: %d\nNumber of books: %d\nNumber of users: %d' % (len(ratings), len(ratings['movieId'].unique()), len(ratings['userId'].unique())))

"""### SVD and NMF models comparison.

`Singular Value Decomposition (SVD)` and `Non-negative Matrix Factorization (NMF)` are matrix factorization techniques used for dimensionality reduction. Surprise package provides implementation of those algorithms.
"""

model_svd = SVD()
cv_results_svd = cross_validate(model_svd,data,cv=3)
pd.DataFrame(cv_results_svd).mean()

model_nmf = NMF()
cv_results_nmf = cross_validate(model_nmf,data,cv=3)
pd.DataFrame(cv_results_nmf).mean()

"""It's clear that for the given dataset much better results can be obtained with `SVD approach` - both in terms of accuracy and training / testing time.

### Optimisation of SVD algorithm

Grid Search Cross Validation computes accuracy metrics for an algorithm on various combinations of parameters, over a cross-validation procedure. It's useful for finding the best configuration of parameters.

It is used to find the best setting of parameters:

- n_factors - the number of factors
- n_epochs - the number of iteration of the SGD procedure
- lr_all - the learning rate for all parameters
- reg_all - the regularization term for all parameters
"""

# To find the best parameters for the model
param_grid = {"n_factors":[80,100,120],
              "n_epochs":[5,10,20],
              "lr_all":[0.002,0.005],
              "reg_all":[0.2,0.4,0.6]}

gs = GridSearchCV(SVD,param_grid,measures=["rmse","mae"],cv=3)
gs.fit(data)

print(gs.best_score['rmse'])
print(gs.best_params['rmse'])

"""### Analysis of Collaborative Filtering model results

Let's examine in detail the results obtained by the SVD model that provided the best RMSE score.
"""

trainset,testset = train_test_split(data,test_size=0.2)

model = SVD(n_factors=80,n_epochs=20,lr_all=0.005,reg_all=0.2)
model.fit(trainset)

"""### Recommending Movies
Once we have trained the model with the best hyperparameters, we can provide movie recommendations to the users. First, we have to find a list of the movies that a particular user has not seen. Afterwards, we can predict each interaction that is missing using the model. Finally, we can get top movies recommendation by ranking them.
"""

def recommendations(user_id,numberOfResults):
  # Get a list of all movie Ids from dataset
  movie_ids = ratings["movieId"].unique()

  # Get a list of all movie Ids that have been watched by user
  movie_ids_user = ratings.loc[ratings["userId"] == user_id,"movieId"]

  # Get a list off all movie IDS that that have not been watched by user
  movie_ids_to_pred = np.setdiff1d(movie_ids, movie_ids_user)

  # Get a test set of rating of 4 (only to match the surpise dataset format)
  test_set = [[user_id,movie_id,4] for movie_id in movie_ids_to_pred]

  # Predict the ratings and generate recommendations
  prediction = model.test(test_set)
  pred_ratings = np.array([pred.est for pred in prediction])

  # Rank top-n movie based n predicted ratings
  index_max = (-pred_ratings).argsort()[:numberOfResults]
  movieTitleList = []
  for i in index_max:
       movie_id = movie_ids_to_pred[i]
       movieTitleList.append(movies[movies["movieId"] == movie_id]["title"].values[0])
  movieTitleList = pd.DataFrame(movieTitleList,columns=["Movie Name"])
  return movieTitleList

user_id = int(input("UserID: "))
numberOfResults = int(input("Num Recommendations(N): "))
movielist = recommendations(user_id,numberOfResults)
print(" ")
print("Output: ")
movielist

"""Finally, we can obtain top-n item recommendations for a specific user ID."""