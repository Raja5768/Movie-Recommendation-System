# Importing necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Data loading
file_path = r"C:\Users\bajju\Desktop\Recommandation\dataset_used\dataset.csv"  # Updated file path with raw string
try:
    movies = pd.read_csv(file_path)
    print("File loaded successfully.")
except FileNotFoundError:
    print(f"File not found at {file_path}. Please check the path and try again.")
    exit()

# Data exploration
print(movies.describe())
print("Missing values per column:\n", movies.isnull().sum())

# Feature selection
if {'id', 'title', 'overview', 'genre'}.issubset(movies.columns):
    movies = movies[['id', 'title', 'overview', 'genre']]
    movies['tags'] = movies['overview'].fillna('') + ' ' + movies['genre'].fillna('')
    newdata = movies[['id', 'title', 'tags']]
else:
    print("Required columns are missing in the dataset.")
    exit()

# Text vectorization
cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(newdata['tags'].values.astype('U')).toarray()
similarity = cosine_similarity(vector)

# Recommendation function
def recommend(movie_title):
    movie_title = movie_title.strip().lower()
    index = newdata[newdata['title'].str.lower() == movie_title].index
    if not index.empty:
        index = index[0]
        distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
        recommended_movies = [newdata.iloc[i[0]].title for i in distances[1:6]]  # Top 5 recommendations
        return recommended_movies
    else:
        return None

# Testing
print("\n-------------------------------MOVIE RECOMMENDATION SYSTEM-------------------------------\n")
print("Here are 20 sample movie titles for testing:")
print("\n".join(newdata['title'].head(20)))

user_input = input("\nWhich movie would you like to watch? ")

recommended_movies = recommend(user_input)

if recommended_movies:
    print("\nYou might also like these movies:")
    for movie in recommended_movies:
        print(f"- {movie}")
else:
    print("\nSorry, no recommendations found.")

print("\n------------------------------------------------------------------------------------")
