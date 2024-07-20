![alt text](whatsapp_image.jpg)

**WhatsApp Chat Analysis**
================

**we analyze an English Learning WhatsApp**
-------------------------------------------

We can find a lot of information from our own or Bussiness WhatsApp messages, which can also help us to solve business problems
or find new business oportunities. WhatsApp data could be used for many data science tasks like sentiment analysis, 
keyword extraction, named entity recognition and so on.

### ETL Process
In this process we took an exported file from WhatsApp chat, then it converted in a Pandas datafram, with four columns, Date, Time, Author and Message.
![alt text](English_Group_WhatsApp_txt.png)


### EDA Process
Here We got significant insights like total messages, total media messages, total shared links and then we got data from chat's users'
We used Pieplot and Worlmaps.

![alt text](Eda_Graphic1.png)

![alt text](Eda_Graphic1.png)

![alt text](Eda_Graphic2.png)

# Total emojis present in the chat and the type of emojis sent between two peoples.
![alt text](whatsapp_plot.png)

# Let’s have a look at the most used words in this WhatsApp chat by visualizing a word cloud
![alt text](word_map1.png)

# Let’s have a look at the most used words by each person by visualizing two different word clouds
# First user
![alt text](word_map2.png)

# Second user
![alt text](word_map3.png)


### Usage

# Generate one instance of WhatsAppChatAnalyzer, then We choosen two users within a Dictionary, run gen_dataset to get 
# a Panda dataframe from a txt file WhatsApp chat and last run eda_process to obtain signicant insights.


**Authors**
------------

* Renar Zamora - renarzamora@gmail.com

**Tools**
----------------

* Python 3.11, Visual Studio Code, Matplotlib, Plotly, WordCloud, Emoji, Collections, Pandas and Numpy