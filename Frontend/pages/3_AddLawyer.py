import streamlit as st, pandas as pd, time
from operations.db_operations import insert, get
from operations.vectors import getVector

st.title("Add Lawyer")

choice = st.radio("Choose", ("Single Entry", "Upload File"))

if choice != "Single Entry":

    uploaded_file = st.file_uploader("Upload a CSV file")
    if uploaded_file:
        with open(f"uploaded_file.csv", "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Insert"):
            if uploaded_file:
                st.success("File Uploaded Successfully...Please wait while we insert all the records")  

            lawyers=pd.read_csv('uploaded_file.csv')
            names = lawyers["Lawyer Names"]
            # converting information into data
            lawyers['Information']=lawyers['Information'].apply(lambda x : x.split('. '))
            info_lawyers=pd.DataFrame(lawyers['Information'].apply(pd.Series))
            lawyers=lawyers.drop('Information',axis=1)
            import re
            def ey(text):
                pattern = r'(\d+) years?'
                years_matches = re.findall(pattern, text)
                years = [int(match) for match in years_matches]
                return years[0]
            lawyers['experience']=info_lawyers[0].apply(ey)
            def fi(str1):
                pattern = r'in (.*)'
                match = re.search(pattern, str1)
                if match:
                    return match.group(1)
                else:
                    return None
            info_lawyers[0]=info_lawyers[0].apply(fi)
            def remove_and(str1):
                str1_without_and = str1.replace("and", "")
                return str1_without_and
            info_lawyers[0]=info_lawyers[0].apply(remove_and)

            def add_comma(str1):
                if str1[-1] != ",":
                    str1 += ","
                    return str1
            info_lawyers[0]=info_lawyers[0].apply(add_comma)
            lawyers['field']=info_lawyers[0].apply(lambda x:list(set(x.split('Law,'))))
            def extract_feedback(str1):
                pattern = r'Client Feedback of (\d+\.\d+)'
                match = re.search(pattern, str1)
                if match:
                    return match.group(1)
                else:
                    return None
            lawyers['feedback']=info_lawyers[1].apply(extract_feedback)
            names_list = pd.read_excel("Gender_final.xlsx")
            name_gender_dict = {}

            for i in range(len(names_list)):
                name = names_list.iloc[i, 0]
                gender = names_list.iloc[i, 1]
                name_gender_dict[name] = gender
            
            def get_gender(name):
                if name in name_gender_dict:
                    return name_gender_dict[name]
                else:
                    return 'm'
                
            gender_list = [get_gender(name.split()[0]) for name in lawyers["Lawyer Names"]]
            lawyers["gender"] = gender_list
            def extract_charge(str1):
                pattern = r'charges (\d+\.\d+) USD per hour'
                match = re.search(pattern, str1)
                if match:
                    return float(match.group(1))
                else:
                    return None
            lawyers['charge']=info_lawyers[3].apply(extract_charge)
            def extract_avgdays(str1):
                pattern = r'takes (\d+\.\d+) Avg Days for Disposal'
                match = re.search(pattern, str1)
                if match:
                    return float(match.group(1))
                else:
                    return None
            lawyers['avg_days_for_disposal']=info_lawyers[4].apply(extract_avgdays)
            lang_list=[]
            def get_languages(text):
                colon_index = text.find(':')
                if colon_index != -1:
                    languages = re.findall(r'\b[A-Za-z]+\b', text[colon_index + 1:])
                else:
                    languages = []
                languages.remove('and')
                lang_list.append(list(set(languages)))
                return list(set(languages))
            lawyers['lang']=info_lawyers[5].apply(get_languages)
            def get_practices_at(text):
                at_index = text.find('at')
                if at_index != -1:
                    comma_index = text.find(',', at_index)
                    if comma_index != -1:
                        return text[at_index + 3:comma_index]
                return None
            lawyers['practices_at']=info_lawyers[6].apply(get_practices_at)
            def get_location(text):
                if not text:
                    return None

                words = text.split()
                return words[-1]
            lawyers['location']=info_lawyers[6].apply(get_location)
            def get_cd(text):
                is_index = text.find(' is ')
                if is_index != -1:
                    return text[is_index + 3:].replace(".","")
                return None
            lawyers['cd']=info_lawyers[8].apply(get_cd)
            def isProbo(text):
                return 'not' in text
            lawyers['isprobo']=info_lawyers[7].apply(isProbo)
            def remove_null_values(list):
                list = [item for item in list if item != '']
                return list
            lawyers['field']=lawyers['field'].apply(remove_null_values)
            def remove_extra_whitespaces(string):
                regex = r'\s\s+'
                result = re.sub(regex, ' ', string)
                return result
            # getting fields finally
            lawyers['experience']=lawyers['experience'].apply(lambda x:str(x))
            lawyers['feedback']=lawyers['feedback'].apply(lambda x:str(x))
            lawyers['field']=lawyers['field'].apply(lambda x:' '.join(x))
            lawyers['lang']=lawyers['lang'].apply(lambda x:' '.join(x))
            lawyers['charge']=lawyers['charge'].apply(lambda x:str(x))
            lawyers['avg_days_for_disposal']=lawyers['avg_days_for_disposal'].apply(lambda x:str(x))
            lawyers['isprobo']=lawyers['isprobo'].apply(lambda x:str(x))
            lawyers['field']=lawyers['field'].apply(remove_extra_whitespaces)
            
            def remove_non_ascii(text):
                regex = r'[^\x00-\x7F]'
                result = re.sub(regex, '', text)
                return result

            lawyers['Lawyer Names'] = lawyers['Lawyer Names'].apply(remove_non_ascii)

            # for i in lawyers['gender']:
            #     if i == 'm':
            #         a = getVector('Male')
            #     else:
            #         a = getVector('Female')

            count = 0
            for i in range(len(lawyers)):
                if count > 50:
                    break
                vec=[]
                vec.append(getVector(lawyers['experience'][i]))
                vec.append(getVector(lawyers['field'][i]))
                vec.append(getVector(lawyers['feedback'][i]))
                vec.append(1 if lawyers['gender'][i] == 'm' else 0)
                vec.append(getVector(lawyers['charge'][i]))
                a = lawyers['avg_days_for_disposal'][i].split('.')[0]
                vec.append(getVector(a))
                vec.append(getVector(lawyers['lang'][i]))
                vec.append(getVector(lawyers['practices_at'][i]))
                vec.append(getVector(lawyers['location'][i]))
                b = 0
                if lawyers['cd'][i].lower() == 'Large Corporations':
                    b = 1
                elif lawyers['cd'][i].lower() == 'Small Businesses':
                    b = 0
                else:
                    b = 0.5
                vec.append(b)
                vec.append(0 if lawyers['isprobo'][0].lower() == 't' else 1)
                insert(lawyers['Lawyer Names'][i], vec)
                count += 1

            # print(new['Lawyer Names'][28])

            count = 0
            # try:
            #     for name, tag in zip(new["Lawyer Names"], new["tags"]):
            #         if count > 50:
            #             break
            #         vec = getVector(tag)
            #         insert(name, [vec])
            #     st.success("All the values inserted successfully")
            # except Exception as e:
            #     st.error("Error Occurred while inserting")
            #     print(e)
    
else:
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
    

