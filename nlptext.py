# Load the required packages
import numpy as np
import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics, svm
from sklearn.model_selection import (
    train_test_split, learning_curve, StratifiedShuffleSplit, GridSearchCV,
    cross_val_score)

# sns.set_context('notebook', font_scale=1.4)
# %config InlineBackend.figure_format = 'retina'
# %matplotlib inline

def preprocess_text(messy_string):
	stop_words = nltk.corpus.stopwords.words('english')
	porter = nltk.PorterStemmer()
	assert(type(messy_string) == str)
	cleaned = re.sub(r'([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', 'emailaddr', messy_string)
	cleaned = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', 'httpaddr',
                     cleaned)
	cleaned = re.sub(r'£|\$', 'moneysymb', cleaned)
	cleaned = re.sub(
        r'\b(\+\d{1,2}\s)?\d?[\-(.]?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
        'phonenumbr', cleaned)
	cleaned = re.sub(r'\d+(\.\d+)?', 'numbr', cleaned)
	cleaned = re.sub(r'[^\w\d\s]', ' ', cleaned)
	cleaned = re.sub(r'\s+', ' ', cleaned)
	cleaned = re.sub(r'^\s+|\s+?$', '', cleaned.lower())
	return ' '.join(
		porter.stem(term) 
		for term in cleaned.split()
		if term not in set(stop_words)
    )

def make_tidy(sample_space, train_scores, valid_scores):
    # Join train_scores and valid_scores, and label with sample_space
    messy_format = pd.DataFrame(
        np.stack((sample_space, train_scores.mean(axis=1),
                  valid_scores.mean(axis=1)), axis=1),
        columns=['# of training examples', 'Training set', 'Validation set']
    )
    
    # Re-structure into into tidy format
    return pd.melt(
        messy_format,
        id_vars='# of training examples',
        value_vars=['Training set', 'Validation set'],
        var_name='Scores',
        value_name='F1 score'
    )

def spam_filter(message, final_clf, vectorizer):
    if final_clf.predict(vectorizer.transform([preprocess_text(message)])):
        return 'RESULT: spam'
    else:
        return 'RESULT: not spam'

def main():
	example = """  ***** CONGRATlations **** You won 2 tIckETs to Hamilton in 
	NYC http://www.hamiltonbroadway.com/J?NaIOl/event   wORtH over $500.00...CALL 
	555-477-8914 or send message to: hamilton@freetix.com to get ticket !! !  """
	
	df = pd.read_table('SMSSpamCollection.txt', header=None)
	df.head()
	y = df[0]
	le = LabelEncoder()
	y_enc = le.fit_transform(y)

	raw_text = df[1]
	
	processed = raw_text.apply(preprocess_text)

	vectorizer = TfidfVectorizer(ngram_range=(1, 2))
	X_ngrams = vectorizer.fit_transform(processed)

	X_train, X_test, y_train, y_test = train_test_split(
	    X_ngrams,
	    y_enc,
	    test_size=0.2,
	    random_state=42,
	    stratify=y_enc
	)

	# Train SVM with a linear kernel on the training set
	clf = svm.LinearSVC(loss='hinge')
	clf.fit(X_train, y_train)

	# Evaluate the classifier on the test set
	y_pred = clf.predict(X_test)

	# Compute the F1 score
	metrics.f1_score(y_test, y_pred)

	# Display a confusion matrix
	resultmat = pd.DataFrame(
	    metrics.confusion_matrix(y_test, y_pred),
	    index=[['actual', 'actual'], ['spam', 'ham']],
	    columns=[['predicted', 'predicted'], ['spam', 'ham']]
	)

	print(resultmat)

	# Select 10 different sizes of the entire dataset
	sample_space = np.linspace(500, len(raw_text) * 0.8, 10, dtype='int')

	# Compute learning curves without regularization for the SVM model
	train_sizes, train_scores, valid_scores = learning_curve(
	    estimator=svm.LinearSVC(loss='hinge', C=1e10),
	    X=X_ngrams,
	    y=y_enc,
	    train_sizes=sample_space,
	    cv=StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=40),
	    scoring='f1',
	    n_jobs=-1
	)

	# Initialize a FacetGrid object using the table of scores and facet on
	# the type of score
	g = sns.FacetGrid(
	    make_tidy(sample_space, train_scores, valid_scores), hue='Scores', size=5
	)

	# Plot the learning curves and add a legend
	g.map(plt.scatter, '# of training examples', 'F1 score')
	g.map(plt.plot, '# of training examples', 'F1 score').add_legend()

	# Select a range of values to test the regularization hyperparameter
	param_grid = [{'C': np.logspace(-4, 4, 20)}]

	# Inner cross-validation loop to tune the hyperparameter
	grid_search = GridSearchCV(
	    estimator=svm.LinearSVC(loss='hinge'),
	    param_grid=param_grid,
	    cv=StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=42),
	    scoring='f1',
	    n_jobs=-1
	)

	# print(grid_search)

	# Outer cross-validation loop to assess the model's performance
	scores = cross_val_score(
	    estimator=grid_search,
	    X=X_ngrams,
	    y=y_enc,
	    cv=StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=0),
	    scoring='f1',
	    n_jobs=-1
	)

	# print("X_test" + X_test)
	# print("y_test" + y_test)

	print("scores svm", scores)
	print("scores.mean()", scores.mean())

	# Identify the optimal regularization hyperparameter
	grid_search.fit(X_ngrams, y_enc)

	# # Train the classifier on the entire dataset using the optimal hyperparameter
	final_clf = svm.LinearSVC(loss='hinge', C=grid_search.best_params_['C'])
	final_clf.fit(X_ngrams, y_enc);

	# # Display the features with the highest weights in the SVM model
	result = pd.Series(
	    final_clf.coef_.T.ravel(),
	    index=vectorizer.get_feature_names()
	).sort_values(ascending=False)[:20]

	print(result)

	cat = spam_filter('Ohhh, but those are the best kind of foods', final_clf, vectorizer)
	print(cat)
	

if __name__ == '__main__':
  main()
