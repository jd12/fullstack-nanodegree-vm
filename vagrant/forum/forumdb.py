#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Database connection

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    cursor.execute("select * from posts order by time DESC")
    postsTable = cursor.fetchall()
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in postsTable]
#    posts.sort(key=lambda row: row['time'], reverse=True)
    db.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    #Grab current time
    t = time.strftime('%c', time.localtime())
    
    #Insert content and time into database 
    cursor.execute("insert into posts values (%s, %s) ", (content,t) )
    
    #Make change to database persistent 
    db.commit()
    db.close()
    #db.append((t, content))
