import webbrowser

class Movie():

	""" Summary of Movie class 

		Class contains basic movie information

        Attributes:
            title: movie title
            storyline: movie storyline
            poster_image_url: url for movie poster
            trailer_youtube_url: url for movie trailer
    """

	def __init__(self,movie_title,movie_storyline,poster_image,trailer_youtube):
		self.title = movie_title
		self.storyline = movie_storyline
		self.poster_image_url = poster_image
		self.trailer_youtube_url = trailer_youtube

	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)