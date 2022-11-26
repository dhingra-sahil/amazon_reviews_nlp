# __author:Owner
# date:6/16/2022
import streamlit as st
import pandas as pd
from PIL import Image
#import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

#db_conn = mysql.connector.connect(**st.secrets["mysql"])
#cur = db_conn.cursor()

df_reviews = pd.read_csv('/Users/sahildhingra/Downloads/MSDS/SEM_4/NLP/NLP_FinalProject-main/Phase 3/code/df_reviews.csv')

df_clean_reviews = pd.read_csv('/Users/sahildhingra/Downloads/MSDS/SEM_4/NLP/NLP_FinalProject-main/Phase 3/code/clean_reviews.csv')

df_topic_review_ui = pd.read_csv('/Users/sahildhingra/Downloads/MSDS/SEM_4/NLP/NLP_FinalProject-main/Phase 3/code/df_topic_review_ui.csv')

df_topics_ui = pd.read_csv('/Users/sahildhingra/Downloads/MSDS/SEM_4/NLP/NLP_FinalProject-main/Phase 3/code/df_topics_ui.csv')

auto_word_list =['tire','air','im','sure','pressure','make','didnt','know','read','got','battery','light','lights','power','bright','unit','charge','plug','trailer','towel','wax','water','paint','stuff','wash','products','shine','clean','black','spray','install','fit','fits','nice','wheel','jeep','looks','look','cover','item','oil','filter','price','tool','wiper','fit','change','engine','quality','windshield']

clean_category = list(df_reviews.Category.unique())


sw_word_list = ["Microsoft", "Apple"]

#def run_query(query):
#    cur.execute(query)
#    return cur.fetchall()

#import hashlib
#def make_hashes(password):
#    return hashlib.sha256(str.encode(password)).hexdigest()

#def check_hashes(password,hashed_text):
#    if make_hashes(password) == hashed_text:
#        return hashed_text
#    return hashed_text



def home_page_module():
    st.title("NLP - Amazon review Analysis")
    image = Image.open( 'nlp_homepage.jpeg' )
    st.image( image , caption='** Amazon reviews analysis ** ' )
    st.subheader("About Application:")
    st.write("The objective of our project is to analyze amazon reviews for certain categories like auto, magazine, gift cards and do the following:")
    st.write("1. Show Clean data for all categories to the user.")
    st.write("2. Topic modeling: Extract topics and see reviews pertaining to those. ")
    st.write("3. Sentiment Analysis: Perform sentiment analysis on reviews and predict the review sentiment.")
    st.write("4. Research relevant statistics about the reviews.")

def sentiment_analysis():
    pass
    

def plot_avg_by_state():
    viz_query_str = """ select avg(price) as average_price, state
                          from listing l
                          join city c on l.city_id = c.id
                         group by state
                         order by avg(price) desc;"""
    
    resultset = run_query(viz_query_str)
    resultdf = pd.DataFrame(resultset, columns=('Average Price','State'))
    
    fig, ax = plt.subplots()
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.barh(resultdf['State'], resultdf['Average Price'], align='center')
    ax.set_ylabel('States')
    ax.set_xlabel('Average Housing Price')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title('Average Housing Price by States')
    
    st.pyplot(fig)    


def plot_avg_by_cities(inState):
    viz_query_str = """ select avg(price) as average_price, city
                          from listing l
                          join city c on l.city_id = c.id
                        where state = '""" + inState
    viz_query_str += """' group by city
                         order by avg(price) desc
                         limit 25;"""
    
    resultset = run_query(viz_query_str)
    resultdf = pd.DataFrame(resultset, columns=('Average Price','City'))
    
    fig, ax = plt.subplots()
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.barh(resultdf['City'], resultdf['Average Price'], align='center')
    ax.set_ylabel('Cities')
    ax.set_xlabel('Average Housing Price')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title('Average Housing Price by Cities')
    
    st.pyplot(fig) 


def plot_avg_by_zip(inState):
    viz_query_str = """ select avg(price) as average_price, CONVERT(zip_code,char) as zip
                          from listing l
                          join city c on l.city_id = c.id
                        where state = '""" + inState
    viz_query_str += """' group by zip_code
                         order by avg(price) desc
                         limit 25;"""
    
    resultset = run_query(viz_query_str)
    resultdf = pd.DataFrame(resultset, columns=('Average Price','Zip'))
    
    fig, ax = plt.subplots()
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.barh(resultdf['Zip'], resultdf['Average Price'], align='center')
    ax.set_ylabel('Zip Code')
    ax.set_xlabel('Average Housing Price')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title('Average Housing Price by Zip Codes')
    
    st.pyplot(fig) 
    


def main():
    if 'loggedIn' not in st.session_state:
        st.session_state.loggedIn = False
    
    menu = ["Home","Search Reviews" , "Topic Modeling","Sentiment analysis", "Statistical Plots", "Login", "SignUp" ]
    #menu = ["Home" ,"Topic Modeling","Sentiment analysis","Statistical Plots", "Login", "SignUp" ]
    choice = st.sidebar.selectbox("Menu",menu )
    
    ## HOME PAGE
    if choice == "Home":
        home_page_module()
        

        
    ## LOGIN PAGE AND SUBSEQUENT FUNCTIONS
    elif choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox( "Login" ) :
            #hashed_pswd = make_hashes( password )
            result =True #run_query('SELECT * FROM userstable WHERE username ="{}" and password="{}"'. format(username,check_hashes( password , hashed_pswd )))
            
            if result:
                st.session_state.loggedIn = True
                st.success( "successfully logged in as "+  username)
            else :
                st.warning( "incorrect usernmae/password" )


    
        

    elif choice == "Sentiment analysis":
        
        with st.expander('Sentiment analysis'):
			#df_emotions = pd.DataFrame(view_all_prediction_details(),columns=['Rawtext','Prediction','Probability','Time_of_Visit'])
			#st.dataframe(df_emotions)
            st.dataframe(df_reviews.head())
        with st.expander('Count plot'):
            image = Image.open( 'nlp_homepage.jpeg' )
            st.image( image , caption='** Buy a Listing** ' )
			#prediction_count = df_reviews['Overall'].value_counts().rename_axis('Overall').reset_index(name='Counts')
			#pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction',y='Counts',color='Prediction')
			#st.altair_chart(pc,use_container_width=True)
        #st.dataframe(df_reviews.head())
       
    
    elif choice == "Topic Modeling":
        option = st.selectbox( "Please Select Category" , ('-- Choose One -','Automotive','Software') )
        
        with st.expander('Topics'):
            if option == 'Automotive':
                
                st.dataframe(df_topics_ui.iloc[:, 1:].head())
            elif option =='Software':
                st.dataframe(df_topic_review_ui.head(10))
            elif option =='3':
                st.dataframe(df_topic_review_ui.head(10))
            elif option =='4':
                st.dataframe(df_topic_review_ui.head(10))
            elif option =='5':
                st.dataframe(df_topic_review_ui.head(10))
            else:
                st.info("Please select an appropiate Category")
        
        with st.expander('Topic Modeling'):
            word_select= ""
            if option == 'Automotive':
                
                word_select= st.selectbox( "Please Select Word" , (auto_word_list) )
            elif option =='Software':
                word_select= st.selectbox( "Please Select Word" , (sw_word_list) ) 
            
            
            
            if len(word_select)>1:
                derive_topic = df_topics_ui.apply(lambda row: row[row == word_select], axis=1)
                
                derive_topic.columns[0]
                query = np.where((df_topic_review_ui['Category']==option) & (df_topic_review_ui['predicted']==derive_topic.columns[0]))
                
            #clean_db = pd.DataFrame( resultset ,columns=["Listing_ID" , "Listing_Status" , "Listing_Price" , "Listing_city","Listing_state","Listing_zipcode","Listing_type","listing_bed","listing_bath","Listing_Acrelot" ,"Listing_house_size" , "Listing_full_address" , "Listing_street"] )
                #st.dataframe(df_topic_review_ui.loc[query].head(10) )
                #st.dataframe(df_topic_review_ui.loc[query].head(10) )
                data = df_topic_review_ui.loc[query].head(10)
                gb = GridOptionsBuilder.from_dataframe(data)
                gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
                gb.configure_side_bar() #Add a sidebar
                gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
                gridOptions = gb.build()
                
                grid_response = AgGrid(
                    data,
                    gridOptions=gridOptions,
                    data_return_mode='AS_INPUT', 
                    update_mode='MODEL_CHANGED', 
                    fit_columns_on_grid_load=False,
                    theme="streamlit",
                    #theme='ALPINE', #streamlit, balham,material
                    enable_enterprise_modules=True,
                    height=350, 
                    width='100%',
                    reload_data=True
                )
                data = grid_response['data']
                selected = grid_response['selected_rows'] 
                df = pd.DataFrame(selected)
            else:
                st.info("Please select an appropiate word from Topic list")
                

            #st.dataframe(df_topic_review_ui.head())
          
        
        with st.expander('Topics Word Cloud'):    
            
            image = Image.open( 'Figure 2022-11-13 172808.png' )
            st.image( image , caption='** Auto Topics ** ' )
			#prediction_count = df_reviews['Overall'].value_counts().rename_axis('Overall').reset_index(name='Counts')
			#pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction',y='Counts',color='Prediction')
			#st.altair_chart(pc,use_container_width=True)
        #st.dataframe(df_reviews.head())
    ## STATISTICAL VISUALIZATIONS
    elif choice == "Statistical Plots":
        if st.session_state.loggedIn:
            plotChoice = st.sidebar.selectbox("Select the plot you want to see",["-- Choose One --","Auto", "Magazine"])
            topsent = st.sidebar.selectbox("Select Topic or Sentiments",["-- Choose One --","Topic", "Sentiment"])
            image = Image.open( 'stats2.png' )
            st.image( image , caption='** Sentiment Score ** ' )
            if plotChoice == "Average Housing Price by Region":
                regionChoice = st.sidebar.selectbox("Select the Region for visualization",["States","Cities","Zip"])
                
                if regionChoice == "States":
                    plot_avg_by_state()
                else:
                    inState = st.sidebar.selectbox("Choose a State",states)
                    if regionChoice == "Cities":
                        plot_avg_by_cities(inState)
                    elif regionChoice == "Zip":
                        plot_avg_by_zip(inState)
        else:
            st.error("You need to login to be able to view statistics")
                
    ## SIGNUP PAGE
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            #sql="INSERT INTO userstable(username,password) VALUES (%s,%s)"
            #val= (new_user , make_hashes(new_password))
            #cur.execute(sql,val)
            #cur.execute('commit')
            # add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
            
    ## SEARCH PAGE
    elif choice == "Search Reviews":
        data = df_clean_reviews.head(200)
        #(AgGrid(data))
        
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        gridOptions = gb.build()
        
        grid_response = AgGrid(
            data,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=False,
            theme="streamlit",
            #theme='ALPINE', #streamlit, balham,material
            enable_enterprise_modules=True,
            height=350, 
            width='100%',
            reload_data=True
        )
        data = grid_response['data']
        selected = grid_response['selected_rows'] 
        df = pd.DataFrame(selected) 


if __name__ == '__main__':
    main()
