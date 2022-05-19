import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
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
    require_column=column_needed.copy()
    trans_edu=LabelEncoder()
    trans_edu.fit(column_needed["EdLevel"])
    column_needed["EdLevel"]=trans_edu.transform(column_needed["EdLevel"])
    trans_count=LabelEncoder()
    trans_count.fit(column_needed["Country"])
    column_needed["Country"]=trans_count.transform(column_needed["Country"])
    regressor=RandomForestRegressor(random_state=0,max_depth=8,max_features=3)
    features=column_needed.drop("Salary",axis=1)
    target=column_needed["Salary"]
    X_train,X_test,Y_train,Y_test=train_test_split(features,target,test_size=0.15,random_state=2)
    regressor.fit(X_train,Y_train)
    return require_column,trans_count,trans_edu,regressor
data,trans_count,trans_edu,regressor=load_data()

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
    