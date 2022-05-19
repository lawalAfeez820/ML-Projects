import streamlit as st
import pickle
import numpy as np 
from explore_page import trans_count,trans_edu,regressor

#model=pickle.load(open("model.pkl","rb"))
#trans_count=pickle.load(open("trans_count.pkl","rb"))
#trans_edu=pickle.load(open("trans_edu.pkl","rb"))
print(st.__version__)

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""## we need some information to predict salary""")

    countries=("United States",
"India",              
"United Kingdom",       
"Germany",               
"Canada",               
"Brazil",                
"France" ,                
"Spain",                  
"Australia",              
"Netherlands",            
"Poland",               
"Italy",                  
"Russian Federation",  
"Sweden")

    education=("Bachelor’s degree", "Master’s degree", "Post grad","Less than a Bachelors")

    country=st.selectbox("Country" ,countries)
    education=st.selectbox("Education Level",education)
    experience=st.slider("Year of EXperience",0,50,3)
    ok=st.button("Calculate Salary")

    if ok:
        test=np.array([[country,education,experience]])
        test[:,0]=trans_count.transform(test[:,0])
        test[:,1]=trans_edu.transform(test[:,1])
        test=test.astype(float)
        salary=regressor.predict(test)
        st.subheader(f"The estimated average salary per year is ${salary[0]:.2f}")