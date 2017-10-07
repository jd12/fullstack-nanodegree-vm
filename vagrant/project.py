from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    return "page to create a new menu item, Task 1 Complete"

@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/edit')
def editMenuItem(restaurant_id, item_id):
    return "page to edit a menu item, Task 2 Complete"

@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/delete')
def deleteMenuItem(restaurant_id, item_id):
    return "page to delete a menu item, Task 3 complete"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
