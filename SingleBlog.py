import streamlit as st
# pip install streamlit
# EDA Pkgs
import pandas as pd
import matplotlib.pyplot as plt
# pip install matplotlib
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
# pip install wordcloud

# DB
from DataBase import *

# Reading Time
def readingTime(mytext):
    total_words = len([ token for token in mytext.split(" ")])
    estimatedTime = total_words/200.0
    return estimatedTime

# Layout Templates
title_temp = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
    <h4 style="color:white;text-align:center;">{}</h4>
    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; float:left; width: 50px; height: 50px; border-radius: 50%;">
    <h6>Author:{}</h6>
    <br/>
    <br/>
    <p style="text-align:justify">{}</p>
    </div>
    """

article_temp = """
    <div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
    <h4 style="color:white;text-align:center;">{}</h4>
    <h6>Author:{}</h6>
    <h6>Post Date:{}</h6>
    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; float:left; width: 50px; height: 50px; border-radius: 50%;">
    <br/>
    <br/>
    <p style="text-align:justify">{}</p>
    </div>
    """

head_message_temp = """
    <div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
    <h4 style="color:white;text-align:center;">{}</h4>
    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; float:left; width: 50px; height: 50px; border-radius: 50%;">
    <h6>Author:{}</h6>
    <h6>Post Date:{}</h6>
    </div>
    """

full_message_temp = """
    <div style="background-color:silver;overflow-x:auto; padding:10px;border-radius:5px;margin:10px;">
    <p style="text-align:justify;color:black;padding:10px"{}</p>
    </div>
    """

def main():
    """A Simple CRUD Blog"""
    st.title("Simple Blog")
    menu = ["Home", "View Posts", "Add Post", "Search", "Manage", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        result = view_all_notes()
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_article = str(i[2])[0:30]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date),unsafe_allow_html=True)
    elif choice == "View Posts":
        st.subheader("View Articles")
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("View Posts", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.text("Reading Time:{}".format(readingTime(b_article)))
            st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)
    elif choice == "Add Posts":
        st.subheader("Add Articles")
        create_table()
        blog_author = st.text.input("Enter Author Name", max_chars=50)
        blog_title = st.text.input("Enter Post Title")
        blog_article = st.text.area("Post Article Here", height=200)
        blog_post_date = st.date.input("Date")
        if st.button("Add"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success("Post:{} saved".format(blog_title))
    elif choice == "Search":
        st.subheader("Search Articles")
        search_term = st.text_input("Enter Search Term")
        search_choice = st.radio("Field to Search By", ("title"))
        if st.button("Search"):
            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "autor":
                article_result = get_blog_by_author(search_term)
            for i in article_result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                st.text("Reading Time:{}".format(readingTime(blog_article)))
                st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
                st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)
    elif choice == "Manage Posts":
        st.subheader("Manage Articles")
        result = view_all_notes()
        clean_db = pd.DataFrame(result,columns=["Author","Title","Articles","Post Date"])
        st.dataframe(clean_db)
        unique_titles = [i[0] for i in view_all_titles()]
        delete_blog_by_title = st.sidebar.selectbox("Unique Title", unique_titles)
        if st.button("Delete"):
            delete_data(delete_blog_by_title)
            st.warning("Deleted: '{}'".format(delete_blog_by_title))
        if st.checkbox("Metrics"):
            new_df = clean_db
            new_df['Length'] = new_df['Articles'].str.len()
            st.dataframe(new_df)
            st.subheader("Author Stats")
            new_df["Author"].value_counts().plot.pie(autopct="%1.1f%%")
            st.pyplot()
        if st.checkbox("Word Cloud"):
            st.subheader("Generate Word Cloud")
            # text = new_df['Articles'].iloc[0]
            text = ','.join(new_df['Articles'])            
            wordcloud = WordCloud().generate(text)
            plt.imshow(wordcloud,interpolation='bilinear')
            plt.axis("off")
            st.pyplot()
        if st.checkbox("BarH Plot"):
            st.subheader("Lenght of Articles")
            new_df = clean_db
            new_df['Length'] = new_df['Articles'].str.len()
            bath_plot = new_df.plot.barh(x='Author', y='Length',figsize=(20,10))
            st.pyplot()

    elif choice == "About":
        st.subheader("About ToDo List App")
        st.info("Built with Streamlit")
        st.info("ademir.prado@ifpr.edu.br")
        st.text("Ademir Prado")

if __name__ == '__main__':
	main()