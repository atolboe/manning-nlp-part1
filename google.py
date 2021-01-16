from nltk.corpus import movie_reviews
from google.cloud import language_v1

#returns pos or neg
def score_review(review):
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    encoding_type = language_v1.EncodingType.NONE
    
    client = language_v1.LanguageServiceClient()
    
    document = {"content": review, "type_": type_, "language": language}
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    
    if response.document_sentiment.score < 0:
        return 'neg'
    else:
        return 'pos'
        
# extract words from reviews, pair with label
reviews_pos = []
for fileid in movie_reviews.fileids('pos'):
    review = movie_reviews.raw(fileid)
    reviews_pos.append(review)

reviews_neg = []
for fileid in movie_reviews.fileids('neg'):
    review = movie_reviews.raw(fileid)
    reviews_neg.append(review)

# Create 2 smaller subsets for testing
subset_pos = reviews_pos[:10]
subset_neg = reviews_neg[:10]

results_pos = []
# When comfortable with results switch `subset_pos` to reviews_post`
for review in reviews_pos:
    result = score_review(review)
    results_pos.append(result)

results_neg = []
# When comfortable with results switch `subset_neg` to reviews_neg`
for review in reviews_neg:
    result = score_review(review)
    results_neg.append(result)
    
correct_pos = results_pos.count('pos')
accuracy_pos = float(correct_pos) / len(results_pos)
correct_neg = results_neg.count('neg')
accuracy_neg = float(correct_neg) / len(results_neg)
correct_all = correct_pos + correct_neg
accuracy_all = float(correct_all) / (len(results_pos)+len(results_neg))

print('Positive reviews: {}% correct'.format(accuracy_pos*100))
print('Negative reviews: {}% correct'.format(accuracy_neg*100))
print('Overall accuracy: {}% correct'.format(accuracy_all*100))