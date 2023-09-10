# Netflix Clone using ReactJS and Django

This project is a Netflix Clone that allows users to browse hundreds of different movies and TV Shows from over 20 genres such as action, horror and science fiction.

The Functionalities of this website include:

1. Displaying real time movie data (eg images, short video trailers, movie titles, movie ratings, release date, movie summary and genres for each movie)
2. Like movies and add movies to watchlist
3. Search for movies based on their title, genres or overview


These are the Tech Stack/Frameworks used for the project:

1. FRONTEND - ReactJS, Tailwind CSS, Bootstrap, Font Awesome CSS
2. BACKEND - Django
3. API - The Movie DataBase (TMDB) API
4. Languages used: Python, Javascript, JSX

FRONTEND UI Technologies:
1. Scrolling Movie Cards - React
2. Navigation Bar - HTML and Tailwind CSS
3. Welcome Page Animations - React and CSS
4. Welcome Page, Homepage, Moviespage, TVShows Page, Watchlist Page, Liked Movies Page - HTML, React, Tailwind CSS

BACKEND Technology:
DJANGO

Integration of client and server side development:

As I wanted to display real time movie data for movies that are currently popular on Netflix, I used the Movie DataBase (TMDB) API. My React movie cards component made a fetch request to a Django URL endpoint I constructed, and I wrote a backend Django function related to this Django url. This django "retrieve" function then made various API calls to the TMDB API, to retrieve various information. It retrieved various genres and their ids using the TMDB API, before saving the information in a GenresMovies Django Model I created. The function also retrieved movie data for a specific genre, saving relevant information such as the title, rating, overview, imageurl, and a video url(containing link to short youtube trailer for that movie). These information were then saved in a Movies Django model I created. The django function then filtered through Movies Model for movies with a certain genre, creating a list of dictionaries, where each dictionary contained detailed information for a single movie for a specific genre. It finally returned a JSONresponse of this list of dictionaries to the React movie cards component. I created a "moviedata" state for the react movie cards component, the "moviedata" state was set to the list of dictionaries JSONresponse. The map function was then used to create a div/moviecard for every movie in the "moviedata" state, displaying relevant information for each movie.

As I wanted to display TV shows as well, I reused my React movie cards component and edited it accordingly in order to display TV shows apart from movies. I repeated the process in the previous paragraph, creating additional django Models, Functions and URLs/Endpoints linked to the React TV Show Cards Component, and making separate TMDB API calls to retrieve data for TV shows as well. The TV Shows data was then displayed in the React TV Shows movie cards. I also added functionality such as enabling users to like movies/TV Shows and add them to watchlist, as well as search for Movies/TV shows. These were done by writing React Client side functions and Django server side functions, to update Django databases as well as dynamically display information in React components.




   
