# External packages
from tqdm import tqdm
import numpy as np
from collections import Counter
from IPython.display import HTML, display
import tabulate
import matplotlib.pyplot as plt
import pandas as pd

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from sklearn import utils
from sklearn.linear_model import LogisticRegression
from sklearn import utils
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import recall_score, precision_score
from sklearn.model_selection import KFold
from sklearn.base import BaseEstimator, TransformerMixin



#Paths
path_word_embeddings = "C:/Users/tom_v/Documents/Master/Thesis/320/combined-320.txt"

'''All the functions for the notebooks in modelling folder'''

#Creates dataframe from Sklearn results from grid search
#Source: https://www.kaggle.com/grfiv4/displaying-the-results-of-a-grid-search
def gridSearch_to_df(grid_clf):

    clf = grid_clf.best_estimator_
    clf_params = grid_clf.best_params_
    clf_score = grid_clf.best_score_
    clf_stdev = grid_clf.cv_results_['std_test_f1'][grid_clf.best_index_]
    cv_results = grid_clf.cv_results_

    print("best parameters: {}".format(clf_params))
    print("best score:      {:0.5f} (+/-{:0.5f})".format(clf_score, clf_stdev))

    scores_df = pd.DataFrame(cv_results).sort_values(by='rank_test_f1')

    return scores_df

#Plots the dataframe of grid search as created by gridSearch_to_df
#Source: https://www.kaggle.com/grfiv4/displaying-the-results-of-a-grid-search
def df_to_plot_grid(scores_df, param_name, log = False):
    
    best_row = scores_df.iloc[0, :]

    best_mean = best_row['mean_test_f1']
    best_stdev = best_row['std_test_f1']
    best_param = best_row['param_' + param_name]
    best_score = best_row['mean_test_f1']
    
    scores_df = scores_df.sort_values(by= 'param_' + param_name)


    means = scores_df['mean_test_f1']
    stds = scores_df['std_test_f1']
    params = scores_df['param_' + param_name]

    # plot
    plt.figure(figsize=(8, 8))
    plt.errorbar(params, means, yerr=stds)

    plt.axhline(y=best_mean + best_stdev, color='red')
    plt.axhline(y=best_mean - best_stdev, color='red')
    plt.plot(best_param, best_mean, 'or')
    
    #In case of logarithmic parameter scaling
    if log == True:
        plt.xscale('log')

    plt.title(param_name + " vs F1 Score\nBest F1 Score {:0.5f}".format(best_score))
    plt.xlabel(param_name)
    plt.ylabel('F1 Score')
    plt.show()
    
#Function to check whether the prediction is a TP or FN
def TPFN(prediction_all, labels_test):
    FN_ngram = []
    TP_ngram = []
    for idx, prediction in enumerate(prediction_all):
        if prediction==True  and list(labels_test)[idx] == prediction:
            TP_ngram.append(idx)
        elif prediction == False and list(labels_test)[idx] == True:
            FN_ngram.append(idx)
    return TP_ngram, FN_ngram
    



'''All the classes for the modelling notebooks'''

#All hyperparameters are set as recommended in paper and literature
vector_size_value = 300
learning_rate_value = 0.001245
epochs_value = 20
window_value = 15
dbow_words_value = 1
text_value = 'tokenized_unstemmed_unstopwords_all'
min_count_value = 5
sample_value = 1e-5
alpha_value = 0.025
negative_value = 5

#Transformer class to train the doc2vec model and transform the text
class Doc2VecTransformer(BaseEstimator):
    
    def __init__(self,text = text_value,sample = sample_value ):
        self._model = None
        self.learning_rate = learning_rate_value
        self.epochs = epochs_value
        self.vector_size = vector_size_value
        self.dbow_words = dbow_words_value
        self.pre_trained_emb =  path_word_embeddings
        self.text = text
        self.window = window_value
        self.min_count = min_count_value
        self.sample = sample
        self.negative = negative_value
        self.alpha = alpha_value
        
    def fit(self, df_x, df_y=None):
        tagged_x = [TaggedDocument(words = row, tags = [index,tag]) for index,(row, tag) in enumerate(zip(list(df_x[self.text]), list(df_x['check_relevant'])))]# adds both the index as well as the label as tags
        
        model_dbow = Doc2Vec(dm=0,dm_concat = 0, vector_size=self.vector_size, window = self.window, negative=self.negative, hs=0, min_count=self.min_count, sample = self.sample, pretrained_emb=self.pre_trained_emb, dbow_words=self.dbow_words, alpha =self.alpha)
        
        model_dbow.build_vocab([x for x in tqdm(tagged_x)])
        
        for epoch in range(self.epochs):
            model_dbow.train(utils.shuffle([x for x in tqdm(tagged_x)]), total_examples=len(tagged_x), epochs=1)
            model_dbow.alpha -= self.learning_rate
            model_dbow.min_alpha = model_dbow.alpha

        self._model = model_dbow
        return self

    def transform(self, df_x):
        return np.asmatrix(np.array([self._model.infer_vector(row[self.text])
                                     for index, row in df_x.iterrows()]))


