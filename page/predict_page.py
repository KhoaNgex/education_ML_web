import copy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
import streamlit as st
import pickle
import os
from PIL import Image
from components.note_card import card

def load_model():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../model/saved_model.pkl')
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()


def show_predict_page():
    st.header(":male-student: :female-student: Student Performance Prediction")
    image_student = Image.open('images/student_perc.png')
    st.image(image_student)
    st.write("""### We need some information to predict the score""")
    # list of options of each feature
    school_list = (
        "GP",
        "MS"
    )
    sex_list = (
        "F",
        "M"
    )
    address_list = (
        'U',
        'R'
    )
    famsize_list = (
        'LE3',
        'GT3'
    )
    pstatus_list = (
        'T',
        'A'
    )
    parent_job_list = (
        'teacher',
        'health',
        'services',
        'at_home',
        'other'
    )
    reason_list = (
        'home',
        'reputation',
        'course',
        'other'
    )
    yes_no_list = (
        'yes',
        'no'
    )
    parent_edu_list = (
        "none",
        "primary education (4th grade)",
        "5th to 9th grade",
        "secondary education",
        "higher education"
    )
    studytime_list = (
        "less than 2 hours",
        "2 to 5 hours",
        "5 to 10 hours",
        "greater than 10 hours"
    )

    st.write(':school: Which school is that student studying in?')
    school_select = st.radio("School", school_list)

    st.write(":boy: :girl: What is student's gender?")
    sex_select = st.radio("Sex", sex_list)

    st.write(":older_man: How old is that student?")
    age_select = st.slider("Age", 15, 22, 18)

    st.write(":house_with_garden: Which area does he/she live, rural or urbar?")
    address_select = st.radio("Address", address_list)

    st.write(":family: How many people in student's family?")
    famsize_select = st.radio("Family Size", famsize_list)

    st.write(
        ":man-girl-boy: Is that student living with his/her parents or living apart?")
    pstatus_select = st.radio("Parent's Cohabitation Status", pstatus_list)

    st.write(":open_book: :girl: What is his/her mother education level?")
    medu_select_str = st.selectbox("Mother's Education", parent_edu_list)
    medu_select = parent_edu_list.index(medu_select_str)

    st.write(":open_book: :boy: What is his/her father education level?")
    fedu_select_str = st.selectbox("Father's Education", parent_edu_list)
    fedu_select = parent_edu_list.index(fedu_select_str)

    st.write(":male-office-worker: :girl: What is his/her mother occupation?")
    mjob_select = st.selectbox("Mother's Job", parent_job_list)

    st.write(":male-office-worker: :boy: What is his/her father occupation?")
    fjob_select = st.selectbox("Father's Job", parent_job_list)

    st.write(":briefcase: Why he/she chose this school?")
    reason_select = st.radio("Reason", reason_list)

    st.write(
        ":bookmark_tabs: How much time does that student spend on self-studying every week?")
    studytime_select_str = st.radio("Weekly study time", studytime_list)
    studytime_select = studytime_list.index(studytime_select_str) + 1

    st.write(":disappointed: What is the number of past class failures?")
    falure_select = st.slider("Number of past class failures", 0, 10, 1)
    if falure_select >= 3:
        falure_select = 3

    st.write(":school: Does that student obtain extra school educational support?")
    schoolsup_select = st.radio(
        "Extra school educational support", yes_no_list)

    st.write(":family: Does that student obtain family educational support?")
    famsup_select = st.radio("family educational support", yes_no_list)

    st.write(":notebook: Does that student obtain extra paid classes within the course subject (Math or Portuguese)?")
    paid_select = st.radio("Extra paid classes", yes_no_list)

    st.write(":pencil: Does that student attend extra-curricular activities?")
    act_select = st.radio("Extra-curricular activities", yes_no_list)

    st.write(":scroll: Does that student want to take higher education?")
    desire_select = st.radio("Desire for higher education", yes_no_list)

    st.write(":computer: Can that student access Internet at home?")
    internet_select = st.radio("Internet access", yes_no_list)

    st.write(":family: Student evaluates the quality of her/his family relationships (band score from 1 to 5):")
    famrel_select = st.slider("Family Relationship Score", 1, 5, 1)

    st.write(
        ":game_die: Student estimates his/her free time after school (band score from 1 to 5):")
    freetime_select = st.slider("Free time", 1, 5, 1)

    st.write(":bowling: Student estimates his/her going out frequency with friends (band score from 1 to 5):")
    goout_select = st.slider("Going out", 1, 5, 1)

    st.write(
        ":male-doctor: Student evaluates his/her current health status (band score from 1 to 5):")
    health_select = st.slider("Current health status", 1, 5, 1)

    st.write(":running: How many school absence days that student has?")
    absence_select = st.slider("Number of school absences", 0, 93, 5)

    st.write(
        ":memo: Enter the first period score (mid-semester grade) of that student:")
    g1_select = st.number_input(
        "Mid-semester Score", min_value=0, max_value=20, value=0)

    st.write(
        ":memo: Enter the second period score (assignment grade) of that student:")
    g2_select = st.number_input(
        "Assignment Score", min_value=0, max_value=20, value=0)

    st.subheader(
        ":one: Student Information you've just entered (after encoding): ")
    student_info = {
        'school': [school_select],
        'sex': [sex_select],
        'age': [age_select],
        'address': [address_select],
        'family_size': [famsize_select],
        'parents_status': [pstatus_select],
        'mother_education': [medu_select],
        'father_education': [fedu_select],
        'mother_job': [mjob_select],
        'father_job': [fjob_select],
        'reason': [reason_select],
        'study_time': [studytime_select],
        'failures': [falure_select],
        'school_support': [schoolsup_select],
        'family_support': [famsup_select],
        'paid_classes': [paid_select],
        'activities': [act_select],
        'desire_higher_edu': [desire_select],
        'internet': [internet_select],
        'family_quality': [famrel_select],
        'free_time': [freetime_select],
        'go_out': [goout_select],
        'health': [health_select],
        'absences': [absence_select],
        'period1_score': [g1_select],
        'period2_score': [g2_select]
    }

    student_info_df = pd.DataFrame(student_info)
    st.table(student_info_df)
    json_display = st.checkbox("Display JSON Format")
    if json_display:
        json_format = student_info_df.to_json(orient="index")
        st.json(json_format)

    st.subheader(":two: Student Final Score Estimator")
    st.info(":ledger: Let's see how this student performs in **final exam test**!")
    student_info_np = student_info_df.to_numpy()
    col_list = student_info_df.columns

    # dissolve label encoders
    object_attribute = ['school', 'sex', 'address', 'family_size', 'parents_status', 'mother_job', 'father_job',
                        'reason', 'school_support', 'family_support', 'paid_classes', 'activities', 'desire_higher_edu', 'internet']
    for attribute in object_attribute:
        le_name = "le_" + attribute
        globals()[le_name] = data[le_name]
    # feature encoding
    # make a deep copy
    student_info_np_encode = copy.deepcopy(student_info_np)
    for attribute in object_attribute:
        le_name = "le_" + attribute
        student_info_np_encode[:, col_list.get_loc(attribute)] = globals(
        )[le_name].transform(student_info_np_encode[:, col_list.get_loc(attribute)])

    # choose model 
    model_dict = {
        "Linear Regression": "linear_regressor",
        "LASSO Regression": "lasso_regressor",
        "Ridge Regression": "ridge_regressor",
        "Support Vector Regression": "support_vector_regressor",
        "Decision Tree Regression": "decision_tree_regressor",
        "Random Forest Regression": "random_forest_regressor"
    }
    model_select = st.radio("???? Choose the estimator. Here are some options for you:", model_dict)
    regressor_loaded = data[model_dict[model_select]]
    
    estimate_score = st.button("Estimate Final Score")
    compare_mode = st.checkbox("Compare estimated score between models")
    if estimate_score:
        score_estimated = regressor_loaded.predict(student_info_np_encode)
        if score_estimated[0] < 0:
            score_estimated[0] = 0.00
        st.subheader(f"The estimated final score is {score_estimated[0]:.2f}")

    if compare_mode:
        st.markdown("###")
        model_options = st.multiselect(
     '??? Which models you want to compare?',
     ['Linear Regression', 'LASSO Regression', 'Ridge Regression', 'Support Vector Regression', 'Decision Tree Regression', 'Random Forest Regression'],
     ['Linear Regression', 'LASSO Regression'])
        score_list = []
        if len(model_options) > 0:
            for model in model_options:
                reg = data[model_dict[model]]
                score_est = reg.predict(student_info_np_encode)
                if score_est[0] < 0:
                    score_est[0] = 0.00
                score_list.append(round(score_est[0],2))
            fig = plt.figure()
            ax = sns.barplot(model_options,score_list)
            ax.bar_label(ax.containers[0])
            ax.set_xlabel("Models")
            ax.set_ylabel("Estimated Score")
            st.pyplot(fig)

    st.subheader(":three: Student Performance Classifer")
    st.info("??????? Classify student performance based on his/her provided information. It seems to be a bit unfair but let's try!????????")
    note_header = "???? Classification Level"
    note_body = "???? POOR --- Haizz, you must learn more! <br>???? FAIR --- Well, you are fair. Let's try harder to get promoted! <br>???? GOOD --- Wow, you are god!!"
    card(note_header, note_body)
    st.markdown("###")
    # choose classifer
    classifer_dict = {
        "Decision Tree Classifer": "decision_tree_classifer",
        "Random Forest Classifer": "random_forest_classifer",
        "Support Machine Vector": "support_vector_classifer",
        "AdaBoost Classifer": "ada_boost_classifer"
    }
    classifer_select = st.radio("???? Choose the classifer. Here are some options for you:", classifer_dict)
    classifer_loaded = data[classifer_dict[classifer_select]]
    classify_score = st.button("Classify")
    if classify_score:
        perc_type = classifer_loaded.predict(student_info_np_encode)
        if perc_type == 0:
            st.warning("???? FAIR - **Well, you are fair. Let's try harder to get promoted!**")
        elif perc_type == 1:
            st.success("???? GOOD - **Wow, you are GOD!!**")
        elif perc_type == 2:
            st.error("???? POOR - **Haizz, you must learn more!**")