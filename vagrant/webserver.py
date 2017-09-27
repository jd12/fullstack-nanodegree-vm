from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Create session and connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		if self.path.endswith("/hello"):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			message = ""
			message += "<html><body>"
			message += "<h1>Hello</h1>"
			message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>''' 
			message += "</body></html>"
			self.wfile.write(message)
			print message
			return
		if self.path.endswith("/restaurants/new"):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			message = ""
			message += "<html><body>"
                        message += "<h1>Make a New Restaurant</h1>"
			message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                        message += "<input name='newRestaurantName' type='text' placeholder= 'New Restaurarant Name' >"
                        message += "<input type='submit' value='Create'> </form>"
			message += "</body></html>"
			self.wfile.write(message)
			return
		if self.path.endswith("/edit"):
                        restaurantIDPath = self.path.split("/")[2]
                        restaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                        if restaurant:
                            self.send_response(200)
                            self.send_header('Content-type','text/html')
                            self.end_headers()
                            message = ""
                            message += "<html><body>"
                            message += "<h1>%s</h1>" % restaurant.name
                            message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant.id
                            message += "<input name='newRestaurantName' type='text' placeholder= '%s' >" % restaurant.name
                            message += "<input type='submit' value='Update'> </form>"
                            message += "</body></html>"
                            self.wfile.write(message)
                            return
                if self.path.endswith("/restaurants") or self.path.endswith("/restaurants/"):
                        restaurants = session.query(Restaurant).all()
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			message = ""
			message += "<html><body>"
                        message += "<a href='/restaurants/new'> Make a New Restaurant</a>" 
			message += "<h1>Restaurants in Database</h1>"
                        for restaurant in restaurants:
                            message += restaurant.name
                            message += "<br>"
                            message += "<a href='/restaurants/%s/edit'>Edit</a><br>" % restaurant.id
                            message += "<a href='#'>Delete</a><br>"
                            message += "<br><br><br>"
			message += "</body></html>"
			self.wfile.write(message)
			return
		else:
			self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
                        if self.path.endswith("/edit"):
                            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                            if ctype == 'multipart/form-data':
                                    fields = cgi.parse_multipart(self.rfile,pdict)
                                    messagecontent = fields.get('newRestaurantName')
                                    restaurantIDPath = self.path.split("/")[2]
                                    restaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                                    if restaurant:

                                        #Create new Restaurant object
                                        restaurant.name = messagecontent[0]
                                        session.add(restaurant)
                                        session.commit()

                                        #Finish up webpage
                                        self.send_response(301)
                                        self.send_header('Content-type', 'text/html')
                                        self.send_header('Location', '/restaurants')
                                        self.end_headers()
                        if self.path.endswith("/restaurants/new"):
                            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                            if ctype == 'multipart/form-data':
                                    fields = cgi.parse_multipart(self.rfile,pdict)
                                    messagecontent = fields.get('newRestaurantName')

                                    #Create new Restaurant object
                                    newRestaurant = Restaurant(name=messagecontent[0])
                                    session.add(newRestaurant)
                                    session.commit()

                                    #Finish up webpage
                                    self.send_response(301)
                                    self.send_header('Content-type', 'text/html')
                                    self.send_header('Location', '/restaurants')
                                    self.end_headers()
                                
		except:
			pass
def main():
	try:
		port = 8080
		server = HTTPServer(('', port), WebServerHandler)
		print "Web Server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()


if __name__ == '__main__':
	main()

