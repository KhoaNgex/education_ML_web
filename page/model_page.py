import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt

import streamlit as st
from PIL import Image

from components.note_card import card
from page.explore_page import load_data
from page.predict_page import load_model

data = load_model()
regressors = [
        "linear_regressor",
        "lasso_regressor",
        "ridge_regressor",
        "support_vector_regressor",
        "decision_tree_regressor",
        "random_forest_regressor"
]

classifiers = [
    "decision_tree_classifer",
    "random_forest_classifer",
    "support_vector_classifer",
    "ada_boost_classifer"
]

def calculate_metrics(y_test, y_pred, stat):
    if stat == "MSE":
        return mean_squared_error(y_test, y_pred)
    elif stat == "RMSE":
        mse = mean_squared_error(y_test, y_pred)
        return np.sqrt(mse)
    elif stat == "R2 Score":
        return r2_score(y_test, y_pred)
    else:
        return 0

def page_header():
    st.header("🤖 Compare Between Used Models")
    st.info("ℹ️ In the Prediction Page, we offer a bunch of regressors and classifers for you to choose the models you wanna use to make predictions about student performance based on your input information. ***However***, once in a while the score estimated by different models results in relatively high difference. **Why is that??**")
    st.info("🔰 Basically, every model fits well with every dataset. Besides, the properties and complexity of each model also determine the accuracy when using the model to predict data of the dataset.")
    st.success("🛣️ So, let's see which accuracy level each used model can reaches in making predictions with a random splitting way to divide our dataset into training set and test set!")
    image_model = Image.open('images/model_comp.jpg')
    st.image(image_model)

def split_dataset():
    # dissolve label encoders
    object_attribute = ['school', 'sex', 'address', 'family_size', 'parents_status', 'mother_job', 'father_job',
                        'reason', 'school_support', 'family_support', 'paid_classes', 'activities', 'desire_higher_edu', 'internet']
    col_list = df.columns

    # feature encoding
    for attribute in object_attribute:
        le_name = "le_" + attribute
        globals()[le_name] = data[le_name]
        df[attribute] = globals()[le_name].fit_transform(df[attribute])

    X = df.drop(['final_grade','final_score'],axis=1)
    y = df.final_score
    le_fg = preprocessing.LabelEncoder()
    y_c = le_fg.fit_transform(df.final_grade)
    global X_train, X_test, y_train, y_test, X_train_c,X_test_c,y_train_c,y_test_c
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25, random_state=1)
    X_train_c,X_test_c,y_train_c,y_test_c=train_test_split(X,y_c,test_size=0.25, random_state=1)

def regressor_compare():
    st.subheader(":one: Compare between Regressors used to estimate final score")
    note_title = "🪁 Here are 6 regressors"
    note_content = "Linear Regression <br> LASSO Regression <br> Ridge Regression <br> Support Vector Regression <br> Decision Tree Regression <br> Random Forest Regression"
    card(note_title, note_content)
    st.markdown("###")
    st.info("ℹ️ We will compare 6 regressors with 3 criteria. They are **MSE** *(Mean squared error)*, **RMSE** *(Root mean squared error)* and **R2 Score** *(how much our model fits this dataset)*.")
    st.success("⛳ The lower MSE or RMSE is, the better our model performs.")
    st.success("⛳ The higher R2 Score is, the better our model performs.")
    stat_select = st.selectbox("Choose the criterion:", ["RMSE", "MSE", "R2 Score"])
    stat_list = []
    for reg in regressors:
        y_pred = data[reg].predict(X_test)
        statis = calculate_metrics(y_test, y_pred, stat_select)
        stat_list.append(round(statis, 4))
    fig = plt.figure()
    ax = sns.barplot(y = regressors,x = stat_list)
    ax.bar_label(ax.containers[0])
    ax.set_ylabel("Regressors")
    ax.set_xlabel(stat_select)
    st.pyplot(fig)
    st.markdown("###")
    st.success("🗣️ Of the 6 regressors, it seems that **Random Forest Regression** can make the most accurate predictions.")

def show_confusion_heatmap():
    st.write("#### 😵‍💫 Observe the confusion matrix of each classifier on test set")
    st.info("The confusion matrix shows the ways in which your classification model is confused when it makes predictions.")
    image_conf = Image.open('images/confusion.png')
    st.image(image_conf)
    clas_select = st.selectbox("Choose a classifier:", classifiers)
    y_test_p = data[clas_select].predict(X_test_c)
    confusion_mat = confusion_matrix(y_test_c, y_test_p)
    fig = plt.figure()
    sns.heatmap(confusion_mat, linewidths=.5, cmap="Blues")
    plt.title('Confusion Heatmap', fontsize=20)
    st.pyplot(fig)

def classifier_compare():
    st.subheader(":two: Compare between Classifiers used to classify student performance")
    note_title = "🪁 Here are 4 classifiers"
    note_content = "Decision Tree Classifier <br> Random Forest Classifier <br> Support Vector Machine <br> AdaBoost Classifier"
    card(note_title, note_content)
    st.markdown("###")
    st.info("ℹ️ We will compare 4 classifers with **Accuracy Score** and will use **Confusion Matrix** to look into weak points of each classifier.")
    st.success("⛳ The higher accuracy score is, the better our model performs.")
    test_list = []
    train_list = []
    for cla in classifiers:
        y_test_pred = data[cla].predict(X_test_c)
        y_train_pred = data[cla].predict(X_train_c)
        ac_test = accuracy_score(y_test_c, y_test_pred)
        ac_train = accuracy_score(y_train_c, y_train_pred)
        test_list.append(round(ac_test, 3))
        train_list.append(round(ac_train, 3))
    stat_pf = pd.DataFrame({'Name': classifiers, 'Training Set': train_list, 'Test Set': test_list})
    st.dataframe(stat_pf)
    x = np.arange(len(classifiers))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 10))
    rects1 = ax.bar(x - width/2, train_list, width, label='Training Set')
    rects2 = ax.bar(x + width/2, test_list, width, label='Test Set')
    ax.set_ylabel('Accuracy Score')
    ax.set_title('Classifier Comparison')
    ax.set_xticks(x, classifiers)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    st.pyplot(fig)
    st.markdown("###")
    st.success("🗣️ Of the 4 classifiers, it seems that **Support Vector Machine** can make the most accurate predictions on ***Test Set*** and also the less overfitting model.")

    # display confusion heatmap
    show_confusion_heatmap()

def show_model_page():
    page_header()
    global df
    df = load_data()
    split_dataset()
    regressor_compare()
    classifier_compare()