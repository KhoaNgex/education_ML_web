import matplotlib.pyplot as plt
import streamlit as st
from components.note_card import card 
    
def draw_bar_plot(df, option):    
    data = df[option].value_counts()
    feature = list(data.keys())
    values = list(data.values)
    fig2, ax2 = plt.subplots()
    ax2.barh(feature, values)
    for s in ['top', 'bottom', 'left', 'right']:
        ax2.spines[s].set_visible(False)
    ax2.xaxis.set_ticks_position('none')
    ax2.yaxis.set_ticks_position('none')
    ax2.xaxis.set_tick_params(pad = 5)
    ax2.yaxis.set_tick_params(pad = 10)
    ax2.grid(b = True, color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.2)
    ax2.invert_yaxis()
    for i in ax2.patches:
        plt.text(i.get_width()+2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
    # set bar plot title 
    bar_title = ""
    if option == "age":
        bar_title = 'Age'
    elif option == "mother_education":
        bar_title = "Mother's Education"
    elif option == "father_education":
        bar_title = "Father's Education"
    elif option == "mother_job":
        bar_title = "Mother's Job"
    elif option == "father_job":
        bar_title = "Father's Job"
    elif option == "study_time":
        bar_title = "Weekly Study Time"
    elif option == "family_quality":
        bar_title = "Quality of Family Relationships"
    elif option == "free_time":
        bar_title = "Free Time After School"
    elif option == "go_out":
        bar_title = "Going Out with Friends Frequency"
    elif option == "health":
        bar_title = "Curent Health Status"
    # display bar plot
    ax2.set_title(bar_title,
             loc ='center')
    st.pyplot(fig2)
    # display notes of categories of features (if neccessary)
    note_header = bar_title + " Note"
    note_body = ""
    if option == 'mother_education' or option == 'father_education': 
        note_body = "0 - none <br> 1 - primary education (4th grade) <br> 2 - 5th to 9th grade <br> 3 - secondary education <br> 4 - higher education"
        card(note_header, note_body)
    elif option == 'study_time': 
        note_body = "1 - less than 2 hours <br> 2 - from 2 to 5 hours <br> 3 - from 5 to 10 hours <br> 4 - greater than 10 hours"
        card(note_header, note_body)
    elif option == 'family_quality' or option == 'health':
        note_body = "1 - very bad <br> 2 - bad <br> 3 - normal <br> 4 - relatively good <br> 5 - exellent"
        card(note_header, note_body)
    elif option == 'free_time' or option == 'go_out':
        note_body = "1 - very low <br> 2 - low <br> 3 - average <br> 4 - high <br> 5 - very high"
        card(note_header, note_body)