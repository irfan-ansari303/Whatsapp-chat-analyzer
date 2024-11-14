import pandas as pd
from collections import Counter
import emoji


#this function tell the selected user
def fetch_stats(selected_user,df):
    #this is used to check the data is gruop level or not
    if selected_user=="Overall":
        #if data is group level then return data frame
        #this return the overall msg send in the group
        num_messages = df.shape[0]

        # fetch the no.of word
        words=[]
        for message in df['message']:
            words.extend(message.split())

        #fetch number of media messages
        num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

        return num_messages,len(words),num_media_messages
    else:
         #this return a total message do by a particular user
         new_df=df[df['user']==selected_user]
         num_messages=new_df.shape[0]

        #fetch the media
         num_media_messages = df[(df['user'] == selected_user) & (df['message']=='<Media omitted>\n')].shape[0]
         words = []
         for message in new_df['message']:
             words.extend(message.split())
         return num_messages,len(words),num_media_messages

def most_busy_users(df):
    #fetch the top 5 user wo active more or send a largest message
    x=df['user'].value_counts().head()
    return x


#creatting wordclod
# def create_wordcloud(selected_user,df):
#     #this is used to select a particular user or select overall
#     if selected_user != "Overall":
#         df=df[df['user']==selected_user]
#
#         #configure the word clod
#         wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
#         #it create a word cloud as an image
#         #word cloud is genrated by the the message columns
#
#         df_wc = wc.generate(df['message'].str.cat(sep=" "))
#         return df_wc


#most common word
def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']


    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    # Check for emoji version compatibility
    emoji_dict = emoji.EMOJI_DATA if hasattr(emoji, 'EMOJI_DATA') else emoji.UNICODE_EMOJI

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji_dict])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emoji', 'Count'])
    return emoji_df
