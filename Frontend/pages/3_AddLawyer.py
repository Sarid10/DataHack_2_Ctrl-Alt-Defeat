import streamlit as st

st.title("Add Lawyer")

experience = st.number_input("experience",)
special = st.multiselect("Specialization: ",
                         ['Dancing', 'Reading', 'Sports'])
rating = st.slider("Select the rating", 1, 5)
prize = st.number_input("price",)
avg_day_of_disposal = st.text_input("Average days for disposal")
languages = st.multiselect("Languages Spoken: ",
                         ['Dancing', 'Reading', 'Sports'])
practices = st.text_input("Practices At:")
location = st.text_input("Location At:")
isProbmo = st.radio("Is Probmo: ", ('True', 'False'))
gender = st.radio("Gender: ", ('Male', 'Female'))

st.button("Add")

