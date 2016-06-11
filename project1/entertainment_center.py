import media
import fresh_tomatoes

# Instantiate movies
warcraft = media.Movie("Warcraft: The Beginning","A story for wower to memorize their honorable past",
					   "http://cdn1-www.comingsoon.net/assets/uploads/gallery/warcraft-1387407720/warcraft_ver8_xlg.jpg","https://www.youtube.com/watch?v=2Rxoz13Bthc")


spirited_away = media.Movie("Spirited Away","An amazing world and a girl's story created by Ghibli",
							"http://vignette3.wikia.nocookie.net/studio-ghibli/images/4/4a/Spirited_Away_(Amerikansk_DVD).jpg/revision/latest?cb=20140116135457","https://www.youtube.com/watch?v=ByXuk9QqQkk")

castle_in_sky = media.Movie("Castle in the Sky","Technology and the love in humanity heart",
							"http://images.moviepostershop.com/laputa-castle-in-the-sky-movie-poster-1986-1020769409.jpg","https://www.youtube.com/watch?v=McM0_YHDm5A")

totoro = media.Movie("My neighbour Totoro","An excellent story about childhood",
					 "https://img.posterlounge.co.uk/images/wbig/poster-mein-nachbar-totoro-341428.jpg","https://www.youtube.com/watch?v=TuLX50_5UAI") 

whisper_of_the_heart = media.Movie("Whisper of the Heart","A story about a couple of lover in a small town",
								   "https://alualuna.files.wordpress.com/2011/12/whisper-of-the-heart-poster.jpg","https://www.youtube.com/watch?v=0pVkiod6V0U") 

memories_of_matsuko = media.Movie("Memories of Matsuko","A tragedy is always from a human's heart itself",
								  "http://iv1.lisimg.com/image/58547/421full-memories-of-matsuko-poster.jpg","https://www.youtube.com/watch?v=h5YiO1kSZdQ")

# Compile movie instances into a list
movies = [warcraft,spirited_away,castle_in_sky,totoro,whisper_of_the_heart,memories_of_matsuko]
# Dynamically generate html via external fresh_tomatoes module
fresh_tomatoes.open_movies_page(movies)