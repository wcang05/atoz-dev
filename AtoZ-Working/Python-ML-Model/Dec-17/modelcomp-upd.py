
#Importing libraries and the data set:
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
#Import models from scikit learn module:
from sklearn.linear_model import LogisticRegression

from sklearn.cross_validation import KFold   #For K-fold cross validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#load the from the file
df = pd.read_csv("D:\Machine learning Work\Data\Sample-Dataset1.csv", low_memory=False) #Reading the dataset in a dataframe using Pandas

#Quick Data Exploration


#summary of numerical fieldsprint(df.head(10))
print(df.describe())

#non-numerical values frequency check
#print(df['payment_city'].value_counts())

#Distribution analysis
df['total'].hist(bins=50)

df['analysis_category_code'].hist(bins=50)

df.boxplot(column='date_added_quarter', by = 'analysis_category_code')

df['date_added_quarter'].hist(bins=50)

#Check missing values in the dataset
df.apply(lambda x: sum(x.isnull()), axis=0)

# filling the missing values
df['analysis_category_code'].value_counts()

#df['analysis_category_code'].fillna('No',inplace=True)

my_tab = pd.crosstab(index = df["analysis_category_code"],  # Make a crosstab
                              columns="count")      # Name the count column

my_tab.plot.bar()


print (my_tab.sum(), "\n")   # Sum the counts

print (my_tab.shape, "\n")   # Check number of rows and cols

my_tab.iloc[1:7]             # Slice rows 1-6

my_tab/my_tab.sum()  # freq of the categories

#fill every column with its own most frequent value
#df = df.apply(lambda x:x.fillna(x.value_counts().index[0]))

#fill NaNs with the most frequent value from one column.
df = df.fillna(df['analysis_category_code'].value_counts().index[0])

#Coding nominal data
# Define a generic function using Pandas replace function
def coding(col, codeDict):
    colCoded = pd.Series(col, copy=True)
    for key, value in codeDict.items():
        colCoded.replace(key, value, inplace=True)
    return colCoded


#Coding analysis_category_code as I=0, S=1 etc:
print ('Before Coding:')
print (pd.value_counts(df["analysis_category_code"]))
df["analysis_category_coded"] = coding(df["analysis_category_code"], {'I':0,'S':1,'T':2,'B':3,'PA':4,'C':5,'TECH':6,'OE':7,'P':8,'R':9,'O':10 })
print ('\nAfter Coding:')
print (pd.value_counts(df["analysis_category_coded"]))


#Building a Predictive Model
#convert all our categorical variables into numeric by encoding the categories

var_mod = ['customer_id','total','order_status_id','date_added_month','date_added_year','total_qty',
           'product_quantity','product_total','analysis_category_coded','Pred_Q1','Pred_Q2','Pred_Q3','Pred_Q4']
le = LabelEncoder()
for i in var_mod:
    df[i] = le.fit_transform(df[i])
df.dtypes

outcome = ['Pred_Q1']
predictors = ['customer_id','total','order_status_id','date_added_year','analysis_category_coded','Pred_Q2','Pred_Q3','Pred_Q4']

# Perform k-fold cross-validation with 5 folds
kf = KFold(df.shape[0], n_folds=5)
error = []
for train, test in kf:
    # Filter training data
    train_predictors = (df[predictors].iloc[train, :])

    # The target we're using to train the algorithm.
    train_target = df[outcome].iloc[train]

    # Filter training data
    test_predictors = (df[predictors].iloc[test, :])

    # The target we're using to train the algorithm.
    test_target = df[outcome].iloc[test]

# Lets make model
print(test_predictors.describe())
print(test_target.describe())
print(train_predictors.describe())
print(train_target.describe())
#Logistic Regression.
model = LogisticRegression()
#fit the model i.e training
model.fit(train_predictors, train_target.values.ravel())
#predict i.e test the model
predict_probabilities = model.predict(df[predictors].iloc[test, :])
# Record error from each cross-validation run
error.append(model.score(df[predictors].iloc[test, :], df[outcome].iloc[test]))
print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(error)))

fpr, tpr, _ = roc_curve(df[outcome].iloc[test], predict_probabilities)
#roc_auc = metrics.accuracy_score(predict_probabilities, df[outcome].iloc[test])
roc_auc = auc(fpr, tpr)
print("roc_auc : %s" % "{0:.3%}".format(np.mean(roc_auc)))


#Decision Tree
model = DecisionTreeClassifier()
#fit the model i.e training
model.fit(train_predictors, train_target.values.ravel())
#predict i.e test the model
predict_probabilities = model.predict(df[predictors].iloc[test, :])
# Record error from each cross-validation run
error.append(model.score(df[predictors].iloc[test, :], df[outcome].iloc[test]))
print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(error)))

d_fpr, d_tpr, _ = roc_curve(df[outcome].iloc[test], predict_probabilities)
#d_roc_auc = metrics.accuracy_score(predict_probabilities, df[outcome].iloc[test])
d_roc_auc = auc(d_fpr, d_tpr)
print("roc_auc : %s" % "{0:.3%}".format(np.mean(d_roc_auc)))


#Random Forest
# after removing correlated variable
model = RandomForestClassifier(n_estimators=25, min_samples_split=25, max_depth=7, max_features=1)
#fit the model i.e training
model.fit(train_predictors, train_target.values.ravel())
#predict i.e test the model
predict_probabilities = model.predict(df[predictors].iloc[test, :])
# Record error from each cross-validation run
error.append(model.score(df[predictors].iloc[test, :], df[outcome].iloc[test]))
print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(error)))

r_fpr, r_tpr, _ = roc_curve(df[outcome].iloc[test], predict_probabilities)
#r_roc_auc = metrics.accuracy_score(predict_probabilities, df[outcome].iloc[test])
r_roc_auc = auc(r_fpr, r_tpr)
print("roc_auc : %s" % "{0:.3%}".format(np.mean(r_roc_auc)))

plt.figure()
plt.plot(fpr, tpr, color='darkorange',
         lw=2, label='Logistic regression (area = %0.2f)' % roc_auc)
plt.plot(r_fpr, r_tpr, color='darkgreen',
         lw=2, label='Random Forest (area = %0.2f)' % r_roc_auc)
plt.plot(d_fpr, d_tpr, color='darkblue',
         lw=2, label='Decision Tress (area = %0.2f)' % d_roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()
