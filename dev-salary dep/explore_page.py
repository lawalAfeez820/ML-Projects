import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 

def join_country(cat,cutoff):
    cat_join={}
    for i in cat.index:
        if cat[i]>=cutoff:
            cat_join[i]=i

        else:
            cat_join[i]="others"
    return cat_join

def clean_experience(x):
    if x=="More than 50 years":
        return 50
    if x=="Less than 1 year":
        return 0.5
    return float(x)    

def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree" 
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
            return "Post grad"
    return "Less than a Bachelors"
@st.cache
def load_data():
    df=pd.read_csv("survey.csv")
    column_needed=df.loc[:,["Country","EdLevel","YearsCodePro","Employment","ConvertedComp"]]
    column_needed=column_needed.rename({"ConvertedComp":"Salary"},axis=1)
    column_needed=column_needed[~column_needed["Salary"].isnull()]
    column_needed=column_needed.dropna()
    column_needed= column_needed[column_needed["Employment"]=="Employed full-time"]

    column_needed=column_needed.drop("Employment",axis=1)
    country_map=join_country(column_needed["Country"].value_counts(),400)
    column_needed["Country"]=column_needed["Country"].map(country_map)
    column_needed=column_needed[column_needed["Salary"]<=250000]
    column_needed=column_needed[column_needed["Salary"]>10000]
    column_needed=column_needed[column_needed["Country"]!="others"]  
    column_needed["YearsCodePro"]=column_needed["YearsCodePro"].apply(clean_experience)
    column_needed["EdLevel"]=column_needed["EdLevel"].apply(clean_education)
    return column_needed
data=load_data()
def show_explore_page():
    st.title("Explore Software Engineer Average Salary")
    st.write("""### Stack Overflow Developer Salary""")
    dataneeded=data["Country"].value_counts()
    fig,ax=plt.subplots()
    ax.pie(dataneeded,labels=dataneeded.index,shadow=True,startangle=90)
    ax.axis("equal")
    st.write("""#### Number Of Data From Each Country""")
    st.pyplot(fig)

    st.write("""#### Mean Salary Base On The Country""")
    mean=data.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(mean)

    st.write("""#### Mean Salary Base On The Experience""")
    mean=data.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(mean)
    