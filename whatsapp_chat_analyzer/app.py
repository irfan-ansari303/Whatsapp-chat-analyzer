import preprocessor
import streamlit as st
#word cloud is used to visualize the text data
from wordcloud import WordCloud
import helper
import matplotlib.pyplot as plt
#run the this code we use
# in terminal write streamlit run app.py
st.sidebar.title("whatsapp chat analyzer")

#this code iss used for uploading the file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #uploaded data is in the form of byte data stream to convert into string we use this function
    data = bytes_data.decode("utf-8")
    #to print the on the srceen we use this text function
    #now we call the preprocessor the chaange that data into data frame
    #df id varible
    #preproces function is present in preprocessor that convert the data into data frame
    df = preprocessor.preproces(data)

    #dataframe function is used the display the data frame in streamlit
    st.dataframe(df)
    #fetch unique user
    #tolist is used to convert the data into list
    user_list=df['user'].unique().tolist()

    #remove group notification from the unigue user
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()

    #put the message on select box
    # 0 is the posittion and overall ia thew message
    user_list.insert(0,"Overall")

    #print the unique user on the left side (sidebar) into the selectbox
    selected_user=st.sidebar.selectbox("Total indivisual user",user_list)
     #add buttton on sidebar for show analysis
    if st.sidebar.button("show Analysis"):
        #create data columns

        #The st.beta_columns() function used to create columns in Streamlit has been deprecated.
        #Instead, you should use the updated st.columns() function to create multiple columns in your Streamlit app.
        #The purpose of creating columns is to layout different Streamlit widgets or elements side by side.


        #calling the hellper function

        num_messages, words, num_media_messages = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        #add content to each columns
        #st.header() is used to display a large, bold header or title, similar to HTML's <h1> tag
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("media messages")
            st.title(num_media_messages)


    #finding the more active user for group level\
    if selected_user=="Overall":
        st.title("most busy user")
        x= helper.most_busy_users(df)
        fig , ax =plt.subplots()
        col1, col2=st.columns(2)
        with col1:
            ax.bar(x.index, x.values,color="green")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


    #word cloud
    #this function the image and we will store that image into the df_wc


    most_common_df=helper.most_common_words(selected_user,df)

    fig,ax=plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')

    st.title("most common words")

    st.pyplot(fig)


#acces the emoji function
    emoji_df=helper.emoji_helper(selected_user,df)
    #data frame is used for print in the form of data
    st.title("emoji analysis")
    col1, col2 =st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        ax.pie(emoji_df['Count'].head(),labels=emoji_df['Emoji'].head(),autopct="%0.2f")
        st.pyplot(fig)



