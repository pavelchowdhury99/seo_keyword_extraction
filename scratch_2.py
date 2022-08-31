import pandas as pd
import spacy
import re
import pytextrank

# Reading the scraped data
df = pd.read_pickle('data.pkl')

# Step 3. Cleaning the text content from pages

def text_cleaning(text):
    try:
        # removing more than one newline or spaces
        text = re.sub(r'[\n\r]+', '\n', text)
    except:
        print(f"Failed to clean")
    return text

# Testing step 3
df['text'] = df['text'].apply(text_cleaning)
print('Done Cleaning text')

# Step 4. Extracting Keyphrases from content
def get_top_n_keyphrases(text,top_n=25):

    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    if top_n>len(doc._.phrases):
        top_n=len(doc._.phrases)

    rank_dict = {phrase.text:phrase.rank for phrase in doc._.phrases[:top_n]}
    return pd.DataFrame.from_dict(rank_dict,orient='index')

# Testing step 4
text = ''.join(df['text'].to_list())
topics_rank = get_top_n_keyphrases(text=text,top_n=29)
print('a')