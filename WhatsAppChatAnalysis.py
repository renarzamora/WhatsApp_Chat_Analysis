import regex
import pandas as pd
import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import plotly.express as px
from datetime import datetime
import os

class WhatsAppChatAnalyzer():
    def __init__(self):
        self.Authors = None
        self.data = None
    
    def date_time(self, s):
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        result = regex.match(pattern,s)
        if result:
            return True
        return False
    
    def convert_date(self, date):
        # convert date dd/mm/yyyy to yyyy/mm/dd
        year = date[-4:]
        if date.find('/') == 1:
            pos = 1
            day = '0'+date[0]
        else:
            pos = 2
            day = date[0:2]
        pos2 = date.find('/', pos + 1)  
        month = date[pos+1:pos2]
        return year+'/'+month+'/'+day
    
    def find_author(self, s):
        s = s.split(':')
        if len(s) == 2:
            return True
        return False
    
    def getDatapoint(self, line):
        splitline = line.split(' - ')
        dateTime = splitline[0]
        date, time = dateTime.split(', ')
        message = ' '.join(splitline[1:])
        
        if self.find_author(message):
            splitmessage =  message.split(': ')
            author = splitmessage[0]
            message = ' '.join(splitmessage[1:])
        else:
            author = None
        return date, time, author,message
    
    def gen_dataset(self):
        data = []
        conversation = self.filepath
        
        with open(conversation, encoding='utf8') as fp:
            fp.readline()
            messageBuffer = []
            date, time, author = None, None, None
            while True:
                line = fp.readline()
                if not line:
                    break
                line = line.strip()
                if self.date_time(line):
                    if len(messageBuffer) > 0:
                        data.append([self.convert_date(date), time, author, ' '.join(messageBuffer)])
                    messageBuffer.clear()
                    date, time, author, message = self.getDatapoint(line)
                    messageBuffer.append(message)
                else:
                    messageBuffer.append(line)
        
        df = pd.DataFrame(data, columns=['Date', 'Time', 'Author', 'Message'])
        df['Date'] = pd.to_datetime(df['Date'])
        self.data = df
        print(df.tail(20))

    def split_count(self, text):
        emoji_list = []
        data = regex.findall(r'\X',text)
        for word in data:
            #if any(char in emoji.UNICODE_EMOJI[‘en’] for char in word):
            if any (char in emoji.EMOJI_DATA for char in word):

                print('word', word)
                emoji_list.append(word)
            return emoji_list
            
    def eda_process(self):
        total_messages = self.data.shape[0]
        print('Total number of messages=',total_messages)

        # Let’s have a look at the total number of media messages present in this chat
        # media_messages = self.data[self.data['Message']=='<Media omitted>'].shape[0]
        media_messages = self.data[self.data['Message']== '<Multimedia omitido>'].shape[0]
        print('Total number of media messages=',media_messages)

        # Now let’s extract the emojis present in between the chats and have a look at the emojis present in this chat
        self.data['emoji'] = self.data['Message'].apply(self.split_count)
        emojis = sum(self.data['emoji'].str.len())
        print('Total emojis in chat=',emojis)

        # Let’s extract the URLs present in this chat and have a look at the final insights
        URLPATTERN = r'(https?://\S+)'
        self.data['urlcount'] = self.data.Message.apply(lambda x: regex.findall(URLPATTERN,x)).str.len()
        links = np.sum(self.data.urlcount)

        # Let's  look at the final insights
        print('Content of the chat')
        print('Total messages', total_messages)
        print('Number of media shared',media_messages)
        print('Number of emojis shared', emojis)
        print('Number of links shared', links)

        # let’s prepare this data to get more insights to analyze all the messages sent in this chat in more detail
        #media_messages_df = self.data[self.data['Message']=='<Media omitted>']
        media_messages_df = self.data[self.data['Message']=='<Multimedia omitido>']
        messages_df = self.data.drop(media_messages_df.index)
        messages_df['Letter_count'] = messages_df['Message'].apply(lambda s : len(s))
        messages_df['Word_count'] = messages_df['Message'].apply(lambda s : len(s.split(' ')))
        messages_df['MessageCount'] = 1

        l = self.Authors
        for i in range(len(l)):
            # Filtering out messages of particular user
            req_df = messages_df[messages_df['Author'] == l[i]]
            
            # req_df will contain messages of only one particular user
            print(f'Stats of {l[i]} -')
            
            # shape will print number of rows which indirectly means the number of messages
            print('Messages sent', req_df.shape[0])
            
            # Word_Count contains of total words in one message. Sum of all words/ Total Messages will yield words per message
            words_per_message = (np.sum(req_df['Word_count'])) / req_df.shape[0]
            print('Average Words Per Messages', words_per_message)

            # media consists of media messages
            media = media_messages_df[media_messages_df['Author'] == l[i]].shape[0]
            print('Media Messages sent', media)

            #  emojis consists of total emojis
            emojis = sum(req_df['emoji'].str.len())
            print('Emojis sent', emojis)

            # links consist of total links
            links = sum(req_df['urlcount'])
            print('Links sent', links)

            # Now We'll prepare a visualization of the total emojis present in the chat and the type of emojis sent between the two people. 
            # It will help in understanding the relationship between both the people.
            total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
            total_emojis = len(total_emojis_list)

            total_emojis_list = list([a for b in messages_df.emoji for a in b])
            emoji_dict = dict(Counter(total_emojis_list))
            emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
            for i in emoji_dict:
                print(i)
            
            emoji_df = pd.DataFrame(emoji_dict, columns=['emoji','count'])
            fig = px.pie(emoji_df, values='count', names='emoji')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.show()

            # Now let’s have a look at the most used words in this WhatsApp chat by visualizing a word cloud
            text = ' '.join(review for review in messages_df.Message)
            print('There are {} words in all messages.'.format(len(text)))
            stopwords = set(STOPWORDS)

            # Generating a word cloud image
            wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)
            # Display the generated image:
            # the matplotlib way:
            plt.figure(figsize=(10,5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.show()

            # Now let’s have a look at the most used words by each person by visualizing two different word clouds.
            l = self.Authors
            for i in range(len(l)):
                dummy_df = messages_df[messages_df['Author']==l[i]]
                text = ' '.join(review for review in dummy_df.Message)
                stopwords = set(STOPWORDS)
                # Generate a word cloud image
                print('Author name', l[i])
                wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)
                # Display the generated image
                plt.figure(figsize=(10,5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.show()
                
# Usage example
if __name__ == '__main__':
    ChatAnalyzer = WhatsAppChatAnalyzer()
    filepath = os.getcwd()+'\English_Group_WhatsApp.txt'
    ChatAnalyzer.filepath = filepath 
    ChatAnalyzer.Authors = ['Renar','+52 414-7415750']
    ChatAnalyzer.gen_dataset()    
    ChatAnalyzer.eda_process()

    

