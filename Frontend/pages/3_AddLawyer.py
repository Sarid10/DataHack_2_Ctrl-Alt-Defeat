import streamlit as st
from operations.db_operations import insert, get
from operations.vectors import getVector

st.title("Add Lawyer")

name = st.text_input("Name",)
experience = st.text_input("Experience",)
special = st.multiselect("Specialization: ",
                         ['Corporate law', 'Consumer protection law', 'Labor law', 'Intellectual property law', 'Criminal law', 'Tax law', 'Human rights law', 'Family law', 'Civil law', 'Real estate law', 'Constitutional law', 'Media law', 'Entertainment law', 'Environmental law', 'Medical law', 'Immigration law'])
rating = st.slider("Select the rating", 1, 5)
price = st.text_input("price",)
avg_day_of_disposal = st.text_input("Average days for disposal")
languages = st.multiselect("Languages Spoken: ",
                         [
    'Hindi', 'Bengali', 'Telugu', 'Marathi', 'Tamil', 'Urdu', 'Gujarati',
    'Malayalam', 'Kannada', 'Odia', 'Punjabi', 'Assamese', 'Maithili',
    'Santali', 'Kashmiri', 'Nepali', 'Konkani', 'Sindhi', 'Dogri',
    'Manipuri', 'Bodo', 'Khasi', 'Mizo', 'Garo', 'Tulu', 'Konkani'
])
practices = st.text_input("Practices At:")
location = st.text_input("Location At:")
client_demographics = st.radio("Client Demographics", ("Small Businesses", "Individuals", "Large Corporations"))
isProbo = st.radio("Is Probo: ", ('True', 'False'))
gender = st.radio("Gender: ", ('Male', 'Female'))


if st.button("Add"):
    details = []
    s = ' '.join([i for i in special])
    l = ' '.join([i for i in languages])
    details.append(experience)
    details.append(s)
    details.append(str(rating))
    details.append(gender[0].lower())
    details.append(price)
    details.append(avg_day_of_disposal)
    details.append(l)
    details.append(practices)
    details.append(location)
    details.append(isProbo)

    details = " ".join(details)

    vector = getVector(details)

    try:
        insert(name, [vector])
        st.success("Lawyer Inserted Successfully")
    except Exception as e:
        st.error("Error while Inserting")
        print(e)
    

