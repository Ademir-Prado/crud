# # DB
# pip install pysqlite3 
import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

# Functions

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Blog_Table (author TEXT, title TEXT, article TEXT, postdate DATE)')

def add_data(author, title, article, postdate):
    c.execute('INSERT INTO Blog_Table (author, title, article, postdate) VALUES (?,?,?,?)', (author, title, article, postdate))
    conn.commit()

def view_all_notes():
    c.execute('SELECT * FROM Blog_Table')
    data = c.fetchall()
    return data

def view_all_titles():
    c.execute('SELECT DISTINCT title FROM Blog_Table')
    data = c.fetchall()
    return data

def get_blog_by_title(title):
    c.execute('SELECT * title FROM Blog_Table where title="{}"'.format(title))
    data = c.fetchall()
    return data

def get_blog_by_author(author):
    c.execute('SELECT * title FROM Blog_Table where author="{}"'.format(author))
    data = c.fetchall()
    return data

def delete_data(title):
    c.execute('DELETE FROM Blog_Table WHERE title="{}"'.format(title))
    conn.commit()