#Importing libraries and the data set:
import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.preprocessing import LabelEncoder
#Import models from scikit learn module:
from sklearn.linear_model import LogisticRegression

from sklearn.cross_validation import KFold   #For K-fold cross validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

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



# Generic function for making a classification model and accessing performance:
def classification_model(model, data, predictors, outcome):
    # Fit the model:
    model.fit(data[predictors], data[outcome])

    # Make predictions on training set:
    predictions = model.predict(data[predictors])

    # Print accuracy
    accuracy = metrics.accuracy_score(predictions, data[outcome])
    print("Accuracy : %s" % "{0:.3%}".format(accuracy))

    # Perform k-fold cross-validation with 5 folds
    kf = KFold(data.shape[0], n_folds=5)
    error = []
    for train, test in kf:
        # Filter training data
        train_predictors = (data[predictors].iloc[train, :])

        # The target we're using to train the algorithm.
        train_target = data[outcome].iloc[train]

        # Training the algorithm using the predictors and target.
        model.fit(train_predictors, train_target)

        # Record error from each cross-validation run
        error.append(model.score(data[predictors].iloc[test, :], data[outcome].iloc[test]))

    print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(error)))

    # Fit the model again so that it can be refered outside the function:
    model.fit(data[predictors], data[outcome])

# Lets make model

#Logistic Regression.
outcome_var = 'Pred_Q1'
model = LogisticRegression()
predictor_var = ['analysis_category_coded']
classification_model(model, df,predictor_var,outcome_var)

#We can try different combination of variables:
predictor_var = ['analysis_category_coded','total','date_added_month','date_added_year']
classification_model(model, df,predictor_var,outcome_var)

#Decision Tree

model = DecisionTreeClassifier()
predictor_var = ['analysis_category_coded']
classification_model(model, df,predictor_var,outcome_var)

#We can try different combination of variables:
predictor_var = ['analysis_category_coded','total','date_added_month','date_added_year']
classification_model(model, df,predictor_var,outcome_var)

#Random Forest


model = RandomForestClassifier(n_estimators=100)
predictor_var = ['analysis_category_coded']
classification_model(model, df,predictor_var,outcome_var)

#We can try different combination of variables:
predictor_var = ['customer_id','total','order_status_id','date_added_month','date_added_year','total_qty',
           'product_quantity','product_total','Pred_Q2','Pred_Q3','Pred_Q4','analysis_category_coded']
classification_model(model, df,predictor_var,outcome_var)


#Create a series with feature importances:
featimp = pd.Series(model.feature_importances_, index=predictor_var).sort_values(ascending=False)
print (featimp)

# after removing correlated variable
model = RandomForestClassifier(n_estimators=25, min_samples_split=25, max_depth=7, max_features=1)
predictor_var = ['customer_id','total','order_status_id','date_added_year','analysis_category_coded']
classification_model(model, df,predictor_var,outcome_var)




