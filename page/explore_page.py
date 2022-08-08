from sklearn.base import BaseEstimator, TransformerMixin
from typing import Tuple
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
from PIL import Image
from components.bar_plot import draw_bar_plot
from components.note_card import card

#-----------------GLOBAL VARIABLES-----------------#
df = pd.DataFrame()
#--------------------------------------------------#

#-----------------SUPPORT CLASSES/FUNCTIONS-----------------#
# classes and functions for removing outliers
# use Quantile based flooring and capping method to remove outliers of 'absence' attribute


def find_boxplot_boundaries(
    col: pd.Series, whisker_coeff: float = 1.5
) -> Tuple[float, float]:
    """Find minimum and maximum in boxplot.
    Args:
        col: a pandas serires of input.
        whisker_coeff: whisker coefficient in box plot
    """
    Q1 = col.quantile(0.25)
    Q3 = col.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - whisker_coeff * IQR
    upper = Q3 + whisker_coeff * IQR
    return lower, upper


class BoxplotOutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, whisker_coeff: float = 1.5):
        self.whisker = whisker_coeff
        self.lower = None
        self.upper = None

    def fit(self, X: pd.Series):
        self.lower, self.upper = find_boxplot_boundaries(X, self.whisker)
        return self

    def transform(self, X):
        return X.clip(self.lower, self.upper)


def score_outliers_remove(column_name):
    global df
    categories = df[column_name].value_counts().to_frame()
    categories = categories.reset_index()
    categories.columns = ['unique_values', 'counts']
    drop_value = list(categories[categories["counts"] < 5].unique_values)
    for i in range(len(drop_value)):
        df = df[df[column_name] != drop_value[i]]

#-----------------------------------------------------#

#--------------------MAIN FUNCTION--------------------#


def load_data():
    global df
    # read dataset.csv
    dir_name = os.path.dirname(__file__)
    full_path = os.path.join(dir_name, '../data/dataset.csv')
    if os.path.exists(full_path):
        df = pd.read_csv(full_path)
        if df.empty:
            st.warning("Your dataset is empty!!!")
        else:
            # data cleaning
            # drop columns with NaN
            df = df.dropna(axis=1)
            # remove outliers
            # "absences" -> using Quantile based flooring and capping method
            clipped_absences = BoxplotOutlierClipper(
            ).fit_transform(df["absences"])
            df['absences'] = clipped_absences.astype(int)
            # "period1_score" and "period2_score" -> remove rows of outliers
            score_outliers_remove('period1_score')
            score_outliers_remove('period2_score')
            # display dataset
            st.subheader("Dataset after Cleaning")
            st.write("Number of Features: ", df.shape[1])
            st.write("Number of Students: ", df.shape[0])
            st.dataframe(df)
            return df
    else:
        st.warning("Please Upload Dataset!")
    return None


def display_filter():
    st.subheader("Choose feature and key word to filter")
    feature = ['none']
    feature.extend(df.columns)
    option = st.selectbox(
     'Please choose a feature to filter',
     tuple(feature))
    
    if option == 'none':
        st.warning('Please select a feature!')
    else:
        message = "You selected: " + option
        st.success(message)
        # Pre-Processing
        sub_df = df.copy()
        # Input
        input = st.text_input('Key Word','')
        st.subheader("Dataset after Filtering")
        # Filter
        if input!='':
            sub = sub_df[option]
            if sub.dtypes == 'int64':
                try:
                    input = int(input)
                except:
                    st.warning("Invalid Value!")
                sub = (sub == input)
            elif sub.dtypes == 'float64':
                try:
                    input = float(input)
                except:
                    st.warning("Invalid Value!")
                sub = (sub == input)
            else:    
                for i in range(0,len(sub)):
                    sub.iloc[i,]=sub.iloc[i,].upper()
                input = input.upper()
                sub_list = []
                for i in range(0,len(sub)):
                    if sub.iloc[i,].find(input)==-1:
                        sub.iloc[i,] = False
                    else:
                        sub_list.append(sub.iloc[i,])
                        sub.iloc[i,] = True
            data_filter = df[sub]
            data_filter.index = np.arange(1,len(data_filter)+1)
            # Show dataframe
            st.write("Number of Students: ", data_filter.shape[0])
            st.dataframe(data_filter)


def display_typical_metrics():
    st.subheader("Typical Metrics")
    # calculate percentage of students who have good grade
    good_grade_freq = df.loc[df.final_grade == 'good', 'final_grade'].count()
    good_grade_freq_str = str(good_grade_freq)
    good_grade_perc = int(good_grade_freq/df.shape[0]*100)
    good_grade_perc_str = str(good_grade_perc) + "%"
    # calculate average score
    aver_score = round(df.final_score.mean())
    aver_score_str = str(aver_score) + "/20"
    # display metrics
    met_col1, met_col2, met_col3 = st.columns(3)
    met_col1.metric(
        "Total", value=df.shape[0], delta=df.shape[0], delta_color="off")
    met_col2.metric("Good Grade", good_grade_freq_str, good_grade_perc_str)
    met_col3.metric("Average Grade", value=aver_score_str, delta="Fair")


def display_perc_dist():
    st.subheader("Pie Chart - Percentage distribution of Students")
    st.info("A ***pie charts*** can be used to show percentages of a whole, and represents percentages at a set point in time. Unlike bar graphs and line graphs, pie charts **do not show changes over time**.")
    image_pie = Image.open('images/pie_chart.jpg')
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.write("")
    with col2:
        st.image(image_pie)
    with col3:
        st.write("")
    option = st.selectbox(
        'Please choose a categorial feature',
        ('none', 'school', 'sex', 'address', 'family_size', 'parents_status', 'mother_job', 'father_job', 'reason', 'final_grade'))

    if option == 'none':
        st.warning('Please select a feature...')
    else:
        message = "You selected: " + option
        st.success(message)
        # calculate frequency
        data = df[option].value_counts()
        # Make figure and axes
        colors = sns.color_palette("pastel")
        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels=data.index, autopct='%.0f%%',
                textprops={'size': 'smaller'}, colors=colors)
        ax1.axis("equal")
        st.pyplot(fig1)


def display_bar_chart():
    # info
    st.subheader("Bar Chart")
    st.info("A ***bar chart*** is used to show a distribution of data points or perform a comparison of metric values across different subgroups of your data. From a bar chart, we can see **which groups are highest or most common, and how other groups compare against the others.**")
    image_bar = Image.open('images/bar_chart.png')
    st.image(image_bar)
    # feature selection
    option = st.selectbox(
        'Please choose a feature',
        ('none', 'age', 'mother_education', 'father_education', 'study_time', 'family_quality', 'free_time', 'go_out', 'health', 'mother_job', 'father_job'))
    message = "You selected: " + option
    if option == 'none':
        st.warning('Please select a feature...')
    else:
        st.success(message)
        # multiple bar plot
        mul_bar_plot = st.checkbox('Multiple Bar Plot')
        if mul_bar_plot:
            st.info('See **multiple bar plot** with comparisons between subgroups.')
            cate_feature = st.radio(
                "Choose a categorical feature to divide dataset into subgroups:",
                ('final_grade', 'school', 'sex', 'address', 'parents_status', 'school_support', 'family_support', 'paid_classes', 'activities', 'desire_higher_edu', 'internet'))
            cate_message = "You selected: " + cate_feature
            st.success(cate_message)
            st.markdown("###")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                # horizontal customise
                hori_cus = st.checkbox('Horizontal')
            with col2:
                # inverted customise
                invert_cus = st.checkbox('Inverted')
            with col3:
                # stacked bar chart
                stacked_cus = st.checkbox('Stacked Bar Chart')
            with col4:
                st.write("")

            st.info("A ***stacked bar chart*** is used to *compare total values across several categories* and, at the same time, to *identify which series is to “blame” for making one total bigger or perhaps smaller than another*")
            st.markdown("###")
            # draw plot
            if invert_cus:
                temp = option
                option = cate_feature
                cate_feature = temp
            if stacked_cus:
                stacked_bar = alt.Chart(df).mark_bar(cornerRadiusTopLeft=3,
                                                     cornerRadiusTopRight=3).encode(
                    x=option+":O",
                    y='count():Q',
                    color=cate_feature+":N"
                ).properties(
                    width=200,
                    height=500
                )
                st.altair_chart(stacked_bar, use_container_width=True)
            else:
                fig = plt.figure(figsize=(10, 8))
                if hori_cus:
                    sns.countplot(y=option, hue=cate_feature, data=df)
                else:
                    sns.countplot(x=option, hue=cate_feature, data=df)
                st.pyplot(fig)
        else:
            st.markdown('###')
            # draw horizontal bar chart
            draw_bar_plot(df, option)


def display_corr_heatmap():
    st.subheader("Correlation Heatmap")
    st.info(" A ***correlation heatmap*** can be used to find **potential relationships** between variables and to understand **the strength of these relationships**. In addition, correlation plots can be used to identify outliers and to **detect linear and nonlinear relationships**.")
    # create a dataframe containing correlation coefficients between couples of variable
    st.markdown('###')
    corr = df.corr()
    fig = plt.figure()
    sns.heatmap(corr, linewidths=.5, cmap="vlag")
    plt.title('Correlation Heatmap', fontsize=20)
    st.pyplot(fig)


def display_score_hist(option):
    hori_hist_cus = st.checkbox("Horizontal Histogram")
    discrete_cus = st.checkbox("Discrete Mode")
    kde_cus = st.checkbox("Add kernel density estimate")
    subgroup_cus = st.checkbox("Divide into subgroup")
    bin_num = st.slider('Adjusting the number of bins',
                        1, 30, 12, disabled=discrete_cus)
    # draw histogram
    fig = plt.figure()
    if discrete_cus:
        bin_num = 'auto'
    dis_mode = 'layer'
    cate_feature = None
    if subgroup_cus:
        cate_feature = st.radio(
            "Choose a categorical feature to divide dataset into subgroups:",
            ('school', 'sex', 'address', 'parents_status', 'school_support', 'family_support', 'paid_classes', 'activities', 'desire_higher_edu', 'internet'))
        cate_message = "You selected: " + cate_feature
        st.success(cate_message)
        stacked = st.checkbox("Stacked Histogram")
        if stacked:
            dis_mode = 'stack'
    if hori_hist_cus:
        sns.histplot(data=df, y=option, kde=kde_cus, hue=cate_feature,
                     discrete=discrete_cus, bins=bin_num, multiple=dis_mode)
    else:
        sns.histplot(data=df, x=option, kde=kde_cus, hue=cate_feature,
                     discrete=discrete_cus, bins=bin_num, multiple=dis_mode)
    st.pyplot(fig)


def display_mean_comparison(option):
    mean_option = st.selectbox(
        'Please pick up a feature for comparison',
        ('none', 'school', 'sex', 'age', 'address', 'reason', 'study_time', 'failures', 'family_quality', 'free_time', 'go_out', 'health', 'absences'))
    if mean_option == "none":
        st.warning('Please select a feature for comparison...')
    else:
        mean_message = "You selected: " + mean_option
        st.success(mean_message)
        line_chart = False
        if mean_option == "age" or mean_option == "absences":
            line_chart = st.checkbox("Line Chart Mode")
        st.markdown("###")
        # draw comparison chart
        mean_data = df.groupby([mean_option])[
            option].mean().sort_values(ascending=True)
        st.table(mean_data)
        if line_chart:
            st.line_chart(mean_data)
        else:
            st.bar_chart(mean_data)


def display_score_explore():
    st.subheader("Score Exploring")
    image_score = Image.open('images/edu_score.png')
    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        st.write("")
    with col2:
        st.image(image_score)
    with col3:
        st.write("")
    option = st.selectbox(
        'Please choose score type for exploration',
        ('none', 'period1_score', 'period2_score', 'final_score'))
    # Types of Score
    note_header = "Score Meaning"
    note_body = "Range: from 0 to 20 <br> period1_grade: mid-semester grade <br> period2_grade: assignment grade <br> final_grade: final exam grade"
    card(note_header, note_body)
    st.markdown('###')
    message = "You selected: " + option
    if option == 'none':
        st.warning('Please select a score type...')
    else:
        st.success(message)
        # display histogram
        st.write(':sunglasses: **Histogram**')
        st.info("A ***histogram*** represents the **distribution of one or more variables** by counting the number of observations that fall within disrete bins.")
        display_score_hist(option)
        # display mean comparison chart
        st.write(':sunglasses: **Mean Score based on Feature**')
        display_mean_comparison(option)
#--------------------------------------------------------------#

#------------------------CORE FUNCTION--------------------------#


def show_explore_page():
    st.header("See Uploaded Dataset")
    load_data()
    st.markdown('#')
    # display EDA
    if df.empty == False:
        st.header("Filter")
        display_filter()
        st.markdown('#')
        st.header("Explore Statistics")
        display_typical_metrics()
        st.markdown('##')
        display_perc_dist()
        st.markdown('##')
        display_bar_chart()
        st.markdown('##')
        display_corr_heatmap()
        st.markdown('##')
        display_score_explore()
