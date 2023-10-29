import streamlit as st
import numpy as np
import pandas as pd

new_df=pd.read_csv('new_df.csv')
lawyers=pd.read_csv('lawyers_final2.csv')
st.header("Lawyer Recommendation")

from guess_indian_gender import IndianGenderPredictor
predicter = IndianGenderPredictor()
names_list = pd.read_excel("Gender_final.xlsx")
name_gender_dict = {}

special = st.multiselect("Type of Case: ",
                         ['Corporate', 'Consumer protection', 'Labor', 'Intellectual property ', 'Criminal ', 'Tax law', 'Human rights law', 'Family law', 'Civil law', 'Real estate law', 'Constitutional law', 'Media law', 'Entertainment law', 'Environmental law', 'Medical law', 'Immigration law'])
location = st.text_input("Location At:")
client_demographics = st.radio("Client Demographics", ("Small Businesses", "Individuals", "Large Corporations"))

languages = st.multiselect("Languages Spoken: ",
                         [
    'Hindi', 'Bengali', 'Telugu', 'Marathi', 'Tamil', 'Urdu', 'Gujarati',
    'Malayalam', 'Kannada', 'Odia', 'Punjabi', 'Assamese', 'Maithili',
    'Santali', 'Kashmiri', 'Nepali', 'Konkani', 'Sindhi', 'Dogri',
    'Manipuri', 'Bodo', 'Khasi', 'Mizo', 'Garo', 'Tulu', 'Konkani'
])

if st.button("Submit"):
    spec = " ".join(special)
    lan=" ".join(languages)
    details = spec + " "+spec + " "+location +" "+location +" "+location +" "+ client_demographics+" "+ lan 
    details=details.replace('law','').lower()
    # print(details)

    new_df=pd.read_csv('new_df.csv')
    
    new_df.loc[len(new_df.index)]=[len(new_df.index),'Test',details]
    new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

    # from sklearn.feature_extraction.text import CountVectorizer
    # cv=CountVectorizer(max_features=5000,stop_words='english')
    # print(new_df)
    # vectors=cv.fit_transform(new_df['tags']).toarray()
    # from sklearn.metrics.pairwise import cosine_similarity
    # similarity=cosine_similarity(vectors)
    # def recommend():
    #     def Sort_Tuple(tup):
    #     # getting length of list of tuples
    #         lst = len(tup)
    #         for i in range(0, lst):
    #             for j in range(0, lst-i-1):
    #                 if (tup[j][1] > tup[j + 1][1]):
    #                     temp = tup[j]
    #                     tup[j] = tup[j + 1]
    #                     tup[j + 1] = temp
    #         return tup
    #     index=vectors.shape[0]-1
    #     distances=similarity[index]
    #     sorted_distances=Sort_Tuple(list(enumerate(similarity[index])))[0:30]
    #     y=[]
    #     for i in sorted_distances:
    #         y.append(i[0])
    #     return y
    import difflib
    def calculate_similarity(string2):
        similarity={}
        pos=0
        for i in new_df['tags']:
            matcher = difflib.SequenceMatcher(None, i, string2)
            s=matcher.ratio()
            similarity[pos]=s
            pos+=1
        return similarity
    
    sim=calculate_similarity(details)
    def sort_dict_by_value(dict1):
        sorted_items = sorted(dict1.items(), key=lambda item: item[1], reverse=True)
        sorted_dict = {}
        for item in sorted_items:
            sorted_dict[item[0]] = item[1]

        return sorted_dict
    
    final_answer=sort_dict_by_value(sim)
    rec_lawyer_list=[]
    count=0
    for keys,values in final_answer.items():
        rec_lawyer_list.append(keys)
        count+=1
        if count ==30:
            break


    names={}
    for i in range(1,21):
        j=rec_lawyer_list[i]
        names[j]=lawyers['Lawyer Names'][j]
    # # print(names)

    males=[]
    females=[]
    mc=0
    fc=0


    for i in range(len(names_list)):
        name = names_list.iloc[i, 0]
        gender = names_list.iloc[i, 1]
        name_gender_dict[name] = gender 
    def get_gender(n):
        if n in name_gender_dict:
            if(name_gender_dict[n]=='f'):
                return True
            else:
                return False


    def guess_gender(name):
        if(predicter.predict(name)=='male'):
            return True
        else:
            return False
    for key,value in names.items():
        value=value.split()
        if(guess_gender(value[0])):
            males.append(value[0])
            mc+=1
        else:
            females.append(value[0])
            fc+=1

    for name in males:
        if get_gender(name):
            females.append(name)
            males.remove(name)

    print(females)
    print(males)

    male_l=[]
    female_l=[]

    print(names)
    for key,value in names.items():
        value=value.split()
        if value[0] in males:
            male_l.append(int(key))
        else:
            female_l.append(int(key))
    print(male_l)
    print(female_l)


    st.header("Females")
    col1, col2, col3, col4, col5  = st.columns(5)
    with col1:
       n=female_l[0]
       st.text(lawyers['Lawyer Names'][n])

    with col2:
        n=female_l[1]
        st.text(lawyers['Lawyer Names'][n])

    with col3:
        n=female_l[2]
        st.text(lawyers['Lawyer Names'][n])

    with col4:
        n=female_l[3]
        st.text(lawyers['Lawyer Names'][n])

    with col5:
        n=female_l[5]
        st.text(lawyers['Lawyer Names'][n])

    st.header("Males")

    col1, col2, col3, col4, col5  = st.columns(5)
    with col1:
       n=male_l[0]
       st.text(lawyers['Lawyer Names'][n])

    with col2:
        n=male_l[1]
        st.text(lawyers['Lawyer Names'][n])

    with col3:
        n=male_l[2]
        st.text(lawyers['Lawyer Names'][n])

    with col4:
        n=male_l[3]
        st.text(lawyers['Lawyer Names'][n])

    with col5:
        n=male_l[5]
        st.text(lawyers['Lawyer Names'][n])