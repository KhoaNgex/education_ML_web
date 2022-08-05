# Core Pkgs
from pydoc import html
import streamlit as st
from PIL import Image
# Utils Pkgs
import codecs

# Components Pkgs
import streamlit.components.v1 as stc

from components.note_card import card

# Custom Components Fxn

# Use html if you want :>


def st_render(render_html, width=700, height=500):
    calc_file = codecs.open(render_html, 'r')
    page = calc_file.read()
    stc.html(page, width=width, height=height, scrolling=False)


def home_intro():
    st.write('  The academic performance of student is usually stored in various formats like files, documents, records etc. The available data would be analyzed to extract useful information. It becomes difficult to analyze student data by applying statistical techniques or other traditional database management tools. Hence there is a need to develop an automated tool for student performance analysis that would analyze student performance and will guide them by displaying the areas where they need improvement, in order to contribute to a student\'s overall growth by generating a score card for the same. ')
    st.write('The proposed system will display results of student performance on a single click action by the user, thus inducing automation and reducing efforts of staff in analyzing student performance manually. The proposed system finds out student trends on the basis of outcomes of students academic performance, strengths, weakness, hobbies and extra - curricular activities. Academic data includes unit test, students theory, practicals and term work marks. This data gathered will be processed by classification algorithm of data mining. A result from classification algorithm will be recognizing as Trend. This trend will help us to track where the students excel and where not and what are their abilities which can be enhanced. The analysis will summarize the outcome and will classify students based on the results.')


def home_result():
    st.info(
        "Dataset: [http://archive.ics.uci.edu/ml/datasets/Student+Performance#](http://archive.ics.uci.edu/ml/datasets/Student+Performance#y)")
    st.warning(
        'Google Colab: [Assignment3_Group1.ipynb](https://drive.google.com/file/d/1oVoCSEIr0IWa3FSdN6mM_LvmH2UAiV65/view?usp=sharing)')
    st.error(
        'Landing Page: [Assignment1_Group1](http://anduckhmt146.me/BDC_Assignment1/)')


def home_data():
    st.info(
        'This data approach student achievement in secondary education of two Portuguese schools. The data attributes include student grades, demographic, social and school related features and it was collected by using school reports and questionnaires. Two datasets are provided regarding the performance in two distinct subjects: Mathematics (mat) and Portuguese language (por).')
    data_preview = Image.open('images/dataset.png')
    st.image(data_preview)


def home_aim():
    aim_header = "Our Process"
    aim_body = "🔎 Collecting data from Moodle <br> 🚀 Conduct steps in data pre-processing, data exploring (EDA), data visualization and data miming to analyze dataset <br> 👨‍💻 Build model to predict final results of student achievement in secondary education from sample dataset <br> 🌐 Build a website to allow user to interact with analysis system"
    card(aim_header, aim_body)


def home_team():
    st_render('index.html')


def home_reference():
    st.info('Paper:[Applying Data Mining in Moodle, 12/06/2018, Cristóbal Romero Morales](https://drive.google.com/file/d/11MuWcfKdhXFOBEA_x7vewxYcmQhtouy-/view)')
    st.info('Paper: [Real-Time Analysis of Students Activities on an E-Learning Platform based on Apache Spark, Vol.8, No.7, 2017, Abdelmajid Chaffai, Larbi Hassouni, Houda Anoun](https://drive.google.com/file/d/1j27Bs6Cw26ZVeBfVBrwMfiF4i5iUzGg-/view)')
    st.info('Paper: [Development of Machine Learning Models using Study Behavior Predictors of Students Academic Performance Through Moodle, Volume-8, Issue-6S3, April 2019,Edmund D. Evangelista](https://drive.google.com/file/d/12E2XcER52hApPStQelgJC4ZKMO8yw068/view)')
    st.warning(
        'Course: [Analytics Vidhya](https://courses.analyticsvidhya.com/)')
    st.warning('Course: [Kaggle](https://www.kaggle.com)')


def home_contact():
    st.write(
        'If you have any questions, please do not hesitate to contact us [here](mailto:khoa.nguyenakaivn@hcmut.edu.vn)')


def show_home_page():
    """A Calculator App with Streamlit Components"""
    # You can use html here, but I'm lazy :> So I use markdown instead
    # st_render('page/home_page/home.html')
    st.header(':house: Welcome to our project')
    home_intro()
    st.subheader('⛳ Result')
    home_result()
    st.subheader('🔢 About Dataset')
    home_data()
    st.subheader('🎯 Aim')
    home_aim()
    st.subheader('💑 Our Team')
    home_team()
    st.subheader('📚 References')
    home_reference()
    st.subheader('📫 Contact')
    home_contact()
