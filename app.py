# Data Viz Pkgs
import pandas as pd

from collections import Counter
import altair as alt 
from PIL import Image
import os
from pathlib import Path
import seaborn as sns 



import streamlit as st 
import streamlit.components.v1 as stc
# Text Cleaning Pkgs
import neattext as nt
import neattext.functions as nfx


import spacy_streamlit
# Text Viz Pkgs
from wordcloud import WordCloud 
from textblob import TextBlob
from gensim.summarization.textcleaner import clean_text_by_sentences 
import gensim 
from gensim.summarization import summarize 
# Emoji
import emoji
from spacy import displacy
import nltk
#nltk.download('punkt') 
#from gensim.summarization import summarize # textrank algorithm
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use('Agg')
import en_core_web_sm
nlp = en_core_web_sm.load()


# evaluate summary 
from rouge import Rouge
def evaluate_summary (summary,reference):
	F=Rouge()#f = fscore, p is precision,r is recall
	eval_score=F.get_scores(summary,reference)
	eval_score_df=pd.DataFrame(eval_score[0])
	return eval_score_df
	

HTML_BANNER = """
	<div style="background-color:#3872fb;padding:10px;border-radius:10px;border-style:ridge;">
	<h1 style="color:white;text-align:center;"> NLP APP BOX </h1>
	</div>
	"""

# def get_most_common_tokens(docx,num=10):
# 	word_freq = Counter(docx.split())
# 	most_common_tokens = word_freq.most_common(num)
# 	return dict(most_common_tokens)


def plot_most_common_tokens(docx,num=7):
	word_freq = Counter(docx.split())
	most_common_tokens = word_freq.most_common(num)
	x,y = zip(*most_common_tokens)
	fig = plt.figure(figsize=(20,10))
	plt.bar(x,y)
	plt.title("Most Common Tokens")
	plt.xticks(color='black', rotation=45, fontweight='bold', fontsize='44')
	plt.yticks( fontweight='bold', fontsize='24')
 
	plt.show()
	st.pyplot(fig)


def plot_wordcloud(docx):
	mywordcloud = WordCloud().generate(docx)
	fig = plt.figure(figsize=(20,10))
	plt.imshow(mywordcloud,interpolation='bilinear')
	plt.axis('off')
	st.pyplot(fig)


def plot_mendelhall_curve(docx):
	word_length = [ len(token) for token in docx.split()]
	word_length_count = Counter(word_length)
	sorted_word_length_count = sorted(dict(word_length_count).items())
	x,y = zip(*sorted_word_length_count)
	fig = plt.figure(figsize=(20,10))
	plt.plot(x,y)
	plt.title("Plot of Word Length Distribution")
	plt.show()
	st.pyplot(fig)



def plot_mendelhall_curve_2(docx):
	word_length = [ len(token) for token in docx.split()]
	word_length_count = Counter(word_length)
	sorted_word_length_count = sorted(dict(word_length_count).items())
	x,y = zip(*sorted_word_length_count)
	mendelhall_df = pd.DataFrame({'tokens':x,'counts':y})
	st.line_chart(mendelhall_df['counts'])



# Functions
def generate_tags_with_spacy(docx):
	docx_with_spacy = nlp(docx)
	tagged_docx = [[[(token.text,token.pos_) for token in sent] for sent in docx_with_spacy.sents]]
	return tagged_docx

def generate_tags(docx):
	tagged_tokens = TextBlob(docx).tags
	return tagged_tokens

def generate_tags_with_textblob(docx):
	tagged_tokens = TextBlob(docx).tags
	tagged_df = pd.DataFrame(tagged_tokens,columns=['token','tags'])
	return tagged_df 

def plot_pos_tags(tagged_docx):
	# Create Visualizaer, Fit ,Score ,Show
	pos_visualizer = PosTagVisualizer()
	pos_visualizer.fit(tagged_docx)
	pos_visualizer.show()
	st.pyplot()



TAGS = { 'NN'   : 'green', 'NNS'  : 'green', 'NNP'  : 'green', 'NNPS' : 'green', 'VB'   : 'blue', 'VBD'  : 'blue', 'VBG'  : 'blue', 'VBN'  : 'blue', 
'VBP'  : 'blue', 'VBZ'  : 'blue', 'JJ'   : 'red', 'JJR'  : 'red', 'JJS'  : 'red', 'RB'   : 'cyan', 'RBR'  : 'cyan', 'RBS'  : 'cyan', 'IN'   : 'darkwhite', 
 'POS'  : 'darkyellow', 'PRP$' : 'magenta', 'PRP$' : 'magenta', 'DET'   : 'black', 'CC'   : 'black', 'CD'   : 'black', 'WDT'  : 'black', 'WP'   : 'black', 
 'WP$'  : 'black', 'WRB'  : 'black', 'EX'   : 'yellow', 'FW'   : 'yellow', 'LS'   : 'yellow', 'MD'   : 'yellow', 'PDT'  : 'yellow', 'RP'   : 'yellow', 
 'SYM'  : 'yellow', 'TO'   : 'yellow', 'None' : 'off'
		}



def mytag_visualizer(tagged_docx):
	colored_text = []
	for i in tagged_docx:
		if i[1] in TAGS.keys():
		   token = i[0]
		   print(token)
		   color_for_tag = TAGS.get(i[1])
		   result = '<span style="color:{}">{}</span>'.format(color_for_tag,token)
		   colored_text.append(result)
	result = ' '.join(colored_text)
	print(result)
	return result

def sentiment(raw_text):
	blob = TextBlob(raw_text)
	polarity = blob.sentiment.polarity
	subjectivity = blob.sentiment.subjectivity
	if polarity > 0.1:
		custom_emoji = ':smile:'
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
		st.write("Text is Positve")
	elif polarity < -0.1:
		custom_emoji = ':disappointed:'
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
		st.write("Text is Negative")
	else:
		st.write(emoji.emojize(':expressionless:',use_aliases=True))
		st.write("Text is Neutral")

	st.info("Polarity Score is:: {} Subjectivity Score is {}".format(polarity,subjectivity))	

def summarizer(raw_text):

   #|(len(_clean_text_by_sentences(raw_text))<2
   sent=len(clean_text_by_sentences(raw_text))
   if((len(raw_text)<3) & sent <2 ):
   	return st.write(raw_text)
   sentences = _clean_text_by_sentences(raw_text)

   my_summary =gensim.summarization.summarize(raw_text)
   st.write(my_summary)
   document_len= {"original": len (raw_text),"summary":len (my_summary)}
   st.write(document_len)
   st.info("Rouge Score")
   score=evaluate_summary(my_summary,raw_text)
   #st.write(score)
   st.dataframe(score)

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
			


def main():
	"""Author Attribution and Verifying App"""
	stc.html(HTML_BANNER)
	#menu = ["Home","About"]
	st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {1500}px;
        padding-top: {1}rem;
        padding-right: {1}rem;
        padding-left: {1}rem;
        padding-bottom: {1}rem;
    }}
 
</style>
""",
        unsafe_allow_html=True,
    )
	


	choice = "Home"#st.sidebar.selectbox("Menu",menu)

	if choice == 'Home':
		st.subheader("Text Analysis")
		raw_text = st.text_area('Enter Text Here')
		

		if ( len(raw_text) > 2 & st.button("Analyze")):
			col1,col2,col3 = st.beta_columns(3)
			process_text = nfx.remove_stopwords(raw_text)
			with col1:


				with st.beta_expander("Preview Tagged Text"):
					tagged_docx = generate_tags(raw_text)
					processed_tag_docx = mytag_visualizer(tagged_docx)
					stc.html(processed_tag_docx,scrolling=True)

				with st.beta_expander("Plot Mendelhall Curve"):
					plot_mendelhall_curve_2(raw_text)


				with st.beta_expander("NER"):
					
					# st.write(most_common_tokens)
					docx = nlp(raw_text)
					html = displacy.render(docx,style="ent")
					html = html.replace("\n\n","\n")
					st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
					#spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe("ner").labels)

			with col2:
				with st.beta_expander('Process Text'):
					st.write(process_text)

				with st.beta_expander("Most Common Words"):
					#st.write(raw_text)
					plot_most_common_tokens(process_text)

				with st.beta_expander("Plot Wordcloud"):
					st.info("word Cloud")
					plot_wordcloud(process_text)

				
			
			with col3:
				with st.beta_expander("Tokenizer"):
					docx = nlp(raw_text)
					spacy_streamlit.visualize_tokens(docx, attrs=["text", "pos_", "dep_", "ent_type_"])

				with st.beta_expander("Sentiment Analysis"):
					sentiment(raw_text)

				with st.beta_expander("Summarizer"):
					summarizer(raw_text)



		elif (len(raw_text) == 1 ):
			st.warning("Insufficient Text, Minimum must be more than 1") 
			


			


		

	elif choice == "About":
		st.subheader("Text Analysis NLP App")
		
	

					

if __name__ == '__main__':
	main()
