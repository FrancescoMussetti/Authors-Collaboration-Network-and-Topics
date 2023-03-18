import string
import nltk
import re
def tokenizer(text):
        stopwords = nltk.corpus.stopwords.words('english')
        wnl = nltk.WordNetLemmatizer()
        text_without_punctuation = re.sub("\W", " ", text)
        text_clean = re.sub("\d", " ", text_without_punctuation)
        tokens = [t for t in nltk.word_tokenize(text_clean.lower())
                    if t not in string.punctuation
                    and t not in stopwords
                    and len(t) > 2
                  ]
        return [wnl.lemmatize(t) for t in tokens]
