#!/usr/bin/env python
# coding: utf-8

# In[258]:


import pandas as pd
import plotly.express as px
pd.options.plotting.backend = "plotly"
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

# In[259]:

main_path = ""
starbucks_1 = pd.read_csv(main_path+"Starbucks_satisfactory_survey.csv")
starbucks_2 = pd.read_csv(main_path+"Starbucks_encode.csv")

#change name in starbuck_1
starbucks_1.columns = ['date', 'gender_1', 'age_range', 'occupation', 'annual_income', 'visit_frequency', 'consume_method', 'time_spent', 
              'nearest_outlet', 'member_card', 'item_purchase', 'avg_amt_spent', 'product_quality_rate', 'price_range_rate', 
              'promotions_importance_rate', 'ambiance_rate', 'wifi_quality_rate','service_rate', 'meeting_hangout_place_rate', 
              'received_promotions_method', 'continue_buying']

#change the names to a prettier one, create a new dict
starbucks_1_pretty = [col.replace('_', ' ').title() for col in starbucks_1.columns]


#merge starbucks_1 and starbucks_2
starbucks_merged = pd.merge(left=starbucks_1, right=starbucks_2,left_index=True, right_index=True, how = "left")


#change date to datetime
starbucks_merged["date"] = pd.date_range(start='2019-10-01', freq='D', periods=122)

#.replace
starbucks_merged['consume_method'] = starbucks_merged['consume_method'].replace(['Never','never','never buy',
                                                                                 'Never buy', 'Never ',
                                                                                 'I dont like coffee'],'Never')
starbucks_merged['item_purchase'] = starbucks_merged['item_purchase'].replace(['Never buy any', 'Never', 'never','Nothing '],'Never buy')   .replace(['cake '],'Cake')   .replace(['Cold drinks;Never'],'Cold drinks')   .replace(['Cold drinks;Pastries','Coffee;Sandwiches','Coffee;Cold drinks','Coffee;Pastries'],'More than 1 item')   .replace(['Coffee;Cold drinks;Juices;Pastries;Sandwiches','Coffee;Juices;Pastries;Sandwiches','Coffee;Cold drinks;Pastries;Sandwiches','Coffee;Pastries;Sandwiches','Cold drinks;Pastries;Sandwiches','Cold drinks;Juices;Pastries'],'More than 2 items')




starbucks_merged[['itemPurchaseCoffee', 'itempurchaseCold', 'itemPurchasePastries', 'itemPurchaseJuices', 'itemPurchaseSandwiches', 'itemPurchaseOthers']] = starbucks_merged[['itemPurchaseCoffee', 'itempurchaseCold', 'itemPurchasePastries', 'itemPurchaseJuices', 'itemPurchaseSandwiches', 'itemPurchaseOthers']] .replace({0.0: 1, 1.0: 0})



# In[260]:


#convert 'yes' and 'no' to True and False
yes_no = {"Yes": True, "No": False}

for col in [
    "member_card",
    "continue_buying"
    ]:
    starbucks_merged[col] = starbucks_merged[col].map(yes_no)
    
def map_to_no_yes(value):
    if value == 1.0:
        return "no"
    elif value == 0.0:
        return "yes"
    else:
        return "missing"

columns_to_map = ['itemPurchaseCoffee', 'itempurchaseCold', 'itemPurchasePastries','itemPurchaseJuices',
                  'itemPurchaseSandwiches', 'itemPurchaseOthers','promoMethodApp','promoMethodSoc',
                  'promoMethodEmail','promoMethodDeal','promoMethodFriend', 'promoMethodDisplay',
                  'promoMethodBillboard', 'promoMethodOthers','loyal']
for column in columns_to_map:
    starbucks_merged[column] = starbucks_merged[column].apply(map_to_no_yes)
    
    
#name: column name:pretty names
prettyname_dict = {'date':'Date',
                   'gender_1':'Gender',
                   'age_range':'Age',
                   'occupation':'Occupation', 
                   'annual_income':'Annual Income',
                   'visit_frequency':'Visit Frequency',
                   'consume_method':'Consume Method',
                   'time_spent':'Time Spent',
                   'nearest_outlet':'Nearest Outlet',
                   'member_card':'Member Card', 
                   'item_purchase':'Item Purchase',
                   'avg_amt_spent':'Avg Amount Spent',
                   'product_quality_rate':'Product Quality Rate',
                   'price_range_rate':'Price Range Rate',
                   'promotions_importance_rate':'Promotion Importance Rate',
                   'ambiance_rate':'Ambiance Rate',
                   'wifi_quality_rate':'Wifi Quality Rate',
                   'service_rate':'Service Rate',
                   'meeting_hangout_place_rate':'Meeting & Hangout Place Rate', 
                   'received_promotions_method':'Promotion Method Received', 
                   'continue_buying':'Continue Buying',
                   'itemPurchaseCoffee':'Item Purchase Coffee', 
                   'itempurchaseCold': 'Item Purchase Cold',
                   'itemPurchasePastries':'Item Purchase Pastries', 
                   'itemPurchaseJuices':'Item Purchase Juices',
                   'itemPurchaseSandwiches':'Item Purchase Sandwiches',
                   'itemPurchaseOthers':'Item Purchase Others',
                   'spendPurchase':'Spend on Purchase',
                   'productRate':'Rate of Product', 
                   'priceRate':'Rate of Price', 
                   'promoRate': 'Rate of Promotion', 
                   'ambianceRate': 'Rate of Ambiance',
                   'wifiRate':'Rate of Wifi',
                   'serviceRate':'Rate of Service',
                   'chooseRate':'Rate of Choose'}

#[prettyname_dict [col] for ...]
#for pd.melt


main_cols = ['date', 'gender_1','age_range', 'occupation']

factors = ['product_quality_rate', 'price_range_rate', 'promotions_importance_rate', 'ambiance_rate',
           'wifi_quality_rate','service_rate', 'meeting_hangout_place_rate'] 

loyal_category = ['age_range', 'occupation','annual_income']

cat_col = ['gender_1', 'age_range', 'occupation','visit_frequency', 'annual_income', 'consume_method','nearest_outlet', 'member_card', 'item_purchase', 'avg_amt_spent','received_promotions_method', 'continue_buying']

cat_col_2 = ['visit_frequency', 'annual_income', 'consume_method', 'member_card', 'item_purchase', 'avg_amt_spent','received_promotions_method', 'continue_buying']

demographics = ['gender_1', 'age_range', 'occupation','annual_income','member_card']

demographics_simple = ['gender_1', 'age_range', 'occupation']

key_insights = ['visit_frequency', 'time_spent','consume_method','nearest_outlet','item_purchase','avg_amt_spent']

consume_cols = ['age_range', 'occupation','visit_frequency', 'annual_income','nearest_outlet']

itempurchase=['itemPurchaseCoffee','itempurchaseCold','itemPurchasePastries','itemPurchaseJuices','itemPurchaseSandwiches','itemPurchaseOthers']

#pretty name dictionary
main_cols_dic =  {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in main_cols}

factors_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in factors}

loyal_category_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in loyal_category}

cat_col_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in cat_col}

cat_col2_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in cat_col_2}

demographics_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in demographics}

demographics_simple_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in demographics_simple}

key_insights_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in key_insights}

consume_cols_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in consume_cols}

itempurchase_dic = {p_col:u_col for u_col, p_col in prettyname_dict.items() if u_col in itempurchase}




# In[292]:


#for histogram category orders
category_orders_dict = {'age_range': ['Below 20', 'From 20 to 29', 'From 30 to 39', '40 and above'],
                        'visit_frequency': ['Never', 'Rarely', 'Monthly', 'Weekly', 'Daily'],
                        'time_spent':['Below 30 minutes', 'Between 30 minutes to 1 hour', 
                                      'Between 1 hour to 2 hours', 'Between 1 hour to 2 hours','More than 3 hours'],
                       'nearest_outlet':['within 1km', '1km - 3km', 'more than 3km'],
                       'annual_income': ['Less than RM25,000', 'RM25,000 - RM50,000', 'RM50,000 - RM100,000',
                                        'RM100,000 - RM150,000','More than RM150,000' ],
                       'avg_amt_spent': ['Zero', 'Less than RM20', 'Around RM20 - RM40',
                                        'More than RM40'],
                       'consume_method':['Dine in', 'Take away','Drive-thru','Never'],
                       'item_purchase':['Coffee','Cold drinks','Cake','Pastries','Jaws chip ','More than 1 item',
                                        'More than 2 items','Never buy']}

age_range_orders = {'age_range': category_orders_dict['age_range']}
visit_frequency_orders = {'visit_frequency': category_orders_dict['visit_frequency']}
time_spent_order = {'time_spent': category_orders_dict['time_spent']}





# In[262]:


null_counts = starbucks_merged.isnull().sum()


# # Annual Income

# ### Annual income vs. Levels of choose starbucks
# ### Student are the groups of customers have higher rate for choosing starbucks as a hangout place 

# In[263]:


with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning','Exploratory Analysis','Analysis of Demographic', 'Analaysis of Consume Habit', 'Conclusion', 'Bibliography'],
		menu_icon = 'arrow-down-right-circle-fill',
		icons = ['bookmark-check', 'book', 'box', 'map', 'boxes', 'bar-chart', 
		'check2-circle'],
		default_index = 0,
		)

if selected=='Abstract':
    st.title("Starbucks Malaysia User Profile")
    st.markdown("This dataset provides valuable insights into the customer retention strategies employed by Starbucks in Malaysia. It contains survey data collected from customers who have visited Starbucks outlets in various locations across the country. The survey covers several aspects of the Starbucks customer experience, such as the quality of the coffee, the atmosphere of the outlet, the friendliness of the staff, and the overall satisfaction of the customers. The data is aimed at helping Starbucks improve its customer retention rates by identifying areas that require improvement and areas that are performing well.")
    st.markdown("This dataset provides an excellent opportunity to analyze the factors that contribute to customer loyalty in the highly competitive coffee industry in Malaysia. Where by exploring the demographic information about customers, purchase habits, and facilities and features that contribute to customer behavior, I can gain a deeper understanding of the customer profile and tailor your business strategies accordingly.")
    
    
    st.dataframe(starbucks_merged)


if selected=="Background Information":
    st.title("Background Information")
    st.markdown("Starbucks, a leading coffee chain, has become a popular destination for coffee lovers in Malaysia. Starbucks entered the Malaysian market in 1998 through a licensing agreement with Berjaya Corporation Berhad, a Malaysian conglomerate. The company's entry into the Malaysian market was part of its broader strategy to expand globally and establish itself as a premium coffee brand.")

    st.markdown("To cater to the Malaysian market, Starbucks has adopted a variety of strategies, such as offering local food options, providing comfortable and trendy store designs, and partnering with local businesses. For instance, the company has introduced local flavors such as kaya (coconut jam) and nasi lemak (a Malaysian dish made with coconut rice) to its menu, which has helped it appeal to local tastes.")

    st.markdown("Malaysia is a unique market that has its own cultural and economic characteristics. The country's diverse population and unique demographics, such as a sizable Muslim population, influence the types of food and beverages that Starbucks offers in the country. This makes Starbucks in Malaysia different from other countries and highlights the importance of understanding the country's unique market dynamics to tailor the company's marketing strategies and product offerings.")
    
    st.markdown("As Malaysia is a growing market with a strong middle class that is increasingly interested in premium products and experiences. To understand the factors contributing to Starbucks' success and diverse strategies in Malaysia, we can analyze the Starbucks Customer Retention Malaysia Survey dataset. The dataset, which is available on Kaggle, contains data on customers' satisfaction levels and preferences regarding various aspects of the Starbucks experience, such as product quality, service quality, and store atmosphere. Analyzing this dataset can provide insights into the factors that contribute to Starbucks' popularity among Malaysians and establish it as a symbol of a premium lifestyle in the country.")
    
if selected=="Data Cleaning":
    st.title('Data Cleaning')
    st.markdown("During the data cleaning process, I merged two datasets that contained both string variables and encoded numbers into one dataframe. I also took care of missing values and repetitive values to ensure that the final dataset is clean and accurate.")
    code_insert='''starbucks_merged = pd.merge(left=starbucks_1, right=starbucks_2,left_index=True, right_index=True, hows="left")'''
    
    st.code(code_insert,language='python')
    st.markdown("The second raw data frame has been encoded with 0.0 representing true and 1.0 representing false, but for ease of use in later operations, these values have been replaced with 0 and 1. ")
    st.code('''starbucks_merged[['itemPurchaseCoffee','itempurchaseCold','itemPurchasePastries','itemPurchaseJuices','itemPurchaseSandwiches','itemPurchaseOthers']] = starbucks_merged[['itemPurchaseCoffee','itempurchaseCold','itemPurchasePastries','itemPurchaseJuices', 'itemPurchaseSandwiches','itemPurchaseOthers']].replace({0.0: 1, 1.0: 0}),language='python''')
    st.markdown("After merge the two dataset and replacement of variables, the data show in the date column contain useless information of time, in forms of hour, which is an uncessary data for the analysis. Therefore, these values have been removed and change the date variable in forms that representing year-month-date.")
    code3='''starbucks_merged["date"] = pd.date_range(start = '2019-10-01',freq = 'D',periods = 122)'''
    st.code(code3,language='python')
    st.dataframe(starbucks_merged.head(5))
    
    st.markdown("Lastly, there were cells in columns that contain mutiple forms of 'never', which are the variables that need to be cleaned up into a uniform 'Never' to efficiently run the functions for later analysis.  ")
    st.code('''starbucks_merged['item_purchase'] = starbucks_merged['item_purchase'].replace(['Never buy any', 'Never', 'never','Nothing '],'Never buy')   .replace(['cake '],'Cake')   .replace(['Cold drinks;Never'],'Cold drinks')   .replace(['Cold drinks;Pastries','Coffee;Sandwiches','Coffee;Cold drinks','Coffee;Pastries'],'More than 1 item')   .replace(['Coffee;Cold drinks;Juices;Pastries;Sandwiches','Coffee;Juices;Pastries;Sandwiches','Coffee;Cold drinks;Pastries;Sandwiches','Coffee;Pastries;Sandwiches','Cold drinks;Pastries;Sandwiches','Cold drinks;Juices;Pastries'],'More than 2 items'),language='python''')
    

    








if selected=="Exploratory Analysis":

    st.title('Exploratory Analysis')
    st.markdown("Exploratory data analysis of this dataset can provide valuable insights into the behavior and preferences of Starbucks customers in Malaysia, which can help professionals to understand its customer base and improve its products and services. By examining patterns in the data and identifying correlations between variables, it is possible to gain a better understanding of customer behavior and loyalty, and to identify areas for improvement in terms of product quality, pricing, promotions, ambiance, wifi quality, and customer service that are specifically focused in Malaysia.")


  
#graph 1    check box for percentage 
    st.subheader('Exploring Customer Demographics')
    col1, col2 = st.columns([4, 5])
    category_col1 = col1.selectbox("Select One Category For Exploring Customer Demographics", np.setdiff1d(list(demographics_dic.keys()), ['Date']),key=1)
    fig1 = px.histogram(starbucks_merged, x=demographics_dic[category_col1], category_orders=category_orders_dict, barmode="group",
                 title=f"{category_col1} For Demographic Exploration", labels = prettyname_dict,
                 color_discrete_sequence=['#036635'], height=550, width = 550)
    fig1.update_traces(texttemplate='%{y:1f}')
    col2.plotly_chart(fig1)
    col1.markdown("By analyzing these customer demographic columns, we can better understand the target audience and preferences of Starbucks customers in Malaysia.")
    col1.markdown("While the demographic analysis may suggest that Starbucks in Malaysia is focusing on 20-29 years old females who are currently employed with less than RM25000 annual income, it is not necessarily true that the company is exclusively targeting this specific group.")
    col1.markdown("Therefore, it is essential to conduct more in-depth analysis and gather additional data to confirm any assumptions or conclusions made from the demographic analysis.")


 
 #graph 2  reorder the category order
    st.subheader('Exploring Data By Gender')
    
    col3,col4=st.columns([4,5])
    with st.form("Select One Category For Exploration By Gender"):      
        category_col2 = col3.selectbox("Select a Column", np.setdiff1d(list(cat_col2_dic.keys()), ['Gender']), key=2)
        col3_checkbox= col3.checkbox("Check For a Normalized Bar Chart")
        submitted=st.form_submit_button("Submit to produce bar chart")
        if submitted:
            Percent = None
            if col3_checkbox:
                Percent = "percent"
            fig2 = px.histogram(starbucks_merged, x=cat_col2_dic[category_col2], color = "gender_1", category_orders = category_orders_dict, barmode="group",title = f"{category_col2} Compare to Gender",histnorm=Percent,labels={"gender": "Gender (0=Female, 1=Male)"}, color_discrete_sequence=['#036635','#82b74b', '#c1946a'],height=500, width = 550)	
            fig2.update_traces(texttemplate='%{y:.1f}')
            col4.plotly_chart(fig2)
    ### never set column into a list!!!!
 

#graph 3: selectbox with catgory columns and colorcolum 
    st.subheader('Key Customer Insights for Starbucks in Malaysia')
    col_submit,col_submit_chart=st.columns([4,5])
    with st.form("Select One Category Column and One Group in Color"):
        category_col = col_submit.selectbox("Select a Column",demographics_dic.keys(), key =3)
        color_col = col_submit.selectbox("Select a Column for Color", key_insights_dic.keys(),key=4)
        submitted=st.form_submit_button("Submit to produce bar chart")
        if submitted:
            fig3 = px.histogram(starbucks_merged, x=demographics_dic[category_col], color= key_insights_dic[color_col], barmode='group',category_orders=category_orders_dict,title=f'{category_col} vs. {color_col}',labels = prettyname_dict,
                                color_discrete_sequence=['#036635','#82b74b', '#c1946a', '#3e4444'],height=550, width = 550)
            fig3.update_traces(texttemplate='%{y:.1f}')
            col_submit_chart.plotly_chart(fig3)
            

# graph 4  
    st.subheader('Exploring Customer Loyalty')
    col5,col6=st.columns([4,5])  
    selection_option = col5.selectbox("Select One Category For Measure of Loyalty", loyal_category_dic.keys(), key=5)
    col5.markdown("The histogram plots the selected loyalty category against the frequency of customers in each loyalty group. The colors of the bars represent the loyalty groups, and the legend shows the corresponding labels.")
    col5.markdown("Based on the plot, we can see that customers aged 20-29, who are employed with an annual income less than RM25000, are the most loyal customer group to Starbucks in Malaysia.")
    fig4 = px.histogram(starbucks_merged, x= loyal_category_dic[selection_option], color='loyal', barmode='group',labels=prettyname_dict, color_discrete_sequence=['#036635','#82b74b', '#c1946a', '#3e4444'],height=550, width = 550)
    fig4.update_traces(texttemplate='%{y:.1f}')
    col6.plotly_chart(fig4)      

# graph 5
    st.subheader('Ratings Affect Customer Experience and Loyalty at Starbucks in Malaysia')
    col7,col8=st.columns([4,5])
    with st.form("Select Two Categories of Ratings"):
        rating_option2 = col7.multiselect("Select Two Categories of Ratings",factors_dic.keys(), max_selections= 3)
        selected_cols = [factors_dic[col] for col in rating_option2]
        fig5 = px.histogram(starbucks_merged, x="visit_frequency", y=selected_cols, color="occupation", histfunc="avg", nbins=20, text_auto=True, barmode="group", category_orders=category_orders_dict, labels=prettyname_dict, color_discrete_sequence=['#036635','#82b74b', '#c1946a', '#3e4444'],height=550, width = 550)
        fig5.update_traces(texttemplate='%{y:.1f}')
        submitted2 =st.form_submit_button("Submit to produce bar chart")
        if submitted2:
            col8.plotly_chart(fig5)
   
    
        
#graph 6 
    st.subheader('Exploring Customer Ratings With Income')
    col9,col10 = st.columns([4,5])
    rating_option= col9.selectbox("Select rating",factors_dic.keys(),key =6)
    fig6 = px.histogram(starbucks_merged, x="annual_income", y=factors_dic[rating_option], color = "occupation",category_orders = category_orders_dict, histfunc="avg", nbins=20, text_auto=True, barmode="group",title = f"{rating_option} vs. Annual Income",labels=prettyname_dict, color_discrete_sequence=['#036635','#82b74b', '#c1946a', '#3e4444'],height=550, width = 550)
    fig6.update_traces(texttemplate='%{y:.1f}')
    col10.plotly_chart(fig6)
    col9.markdown("This graph can help us to visualize the relationship between the selected rating and the annual income of customers at Starbucks in Malaysia. It visualizes how customers with different occupations and annual incomes rate their experience at Starbucks. By selecting a specific rating value, the histogram shows the average rating for each income range, color-coded by occupation.")

    
#graph 7 consume methods
    st.subheader('Exploring Patterns in Consume Method')
    col11,col12=st.columns([4,5])
    with st.form("Select One y Gender"):
        consume_option= col11.selectbox("Select Categories",consume_cols_dic.keys(),key =7)
        col11_checkbox= col11.checkbox("Check Percentages")
        if consume_option:
            Percent = None
            if col11_checkbox:
                Percent = "percent"
    fig7 = px.histogram(starbucks_merged, x="consume_method", color = consume_cols_dic[consume_option],category_orders = category_orders_dict, histfunc="avg", nbins=20, text_auto=True, barmode="group",title = f"{consume_option} vs. Consume Method",histnorm=Percent,labels=prettyname_dict,  color_discrete_sequence=['#82b74b', '#036635','#c1946a', '#3e4444'],height=550, width = 550)
    fig7.update_traces(texttemplate='%{y:.1f}')
    col12.plotly_chart(fig7)
    col11.markdown("Based on the bar chart comparing customer demographics and consumption methods, it appears that customers across all demographic categories prefer to choose Takeaway as their primary consumption method. In terms of occupation, employees tend to choose Takeaway more often than other groups, and students tend to choose Dine in. Additionally, customers who live in distance of 1km-3km to the store tend to prefer Takeaway more than those who live farther away. Overall, the results suggest that Takeaway is the preferred consumption method among Starbucks customers in Malaysia, regardless of their demographic characteristics.")

                    
#graph 8 items purchase
    st.subheader('Exploring Items Purchase ')
    col13,col14 = st.columns([4,5])
    demo_option= col13.selectbox("Select items",demographics_dic.keys(),key =8)
    fig8 = px.histogram(starbucks_merged, x='item_purchase', color = demographics_dic[demo_option],category_orders =category_orders_dict, histfunc="avg", nbins=20, text_auto=True, barmode="group",title = f"{demo_option} vs. Items Purchase",labels=prettyname_dict,  color_discrete_sequence=['#82b74b', '#036635','#c1946a', '#3e4444'],height=550, width = 550)
    fig8.update_traces(texttemplate='%{y:.1f}')
    col14.plotly_chart(fig8)
    col13.markdown("The given code creates a histogram to explore the relationship between different demographics and items purchased at Starbucks. The x-axis represents the number of items purchased, and the y-axis represents the average count for each demographic group. The bars are grouped by the different types of items that were purchased, with different colors indicating different demographic groups. Based on the plot, it appears that people mostly order 'coffee' and 'cold drinks' at Starbucks, regardless of demographic group. Among all the demographics, these two items have the highest average count. However, there are some variations across demographics. For instance, younger people (18-24) tend to purchase more 'food' items than older age groups.")
      
    
#graph 9 sunburst # change the names try
    st.subheader('Exploring Visit Frequncy')
    col15,col16 = st.columns([4,5])
    
    with st.form("Select Two Categories For the Inner Rings"):
        rating_option3 = col15.multiselect("Select Inner Most Category First",demographics_dic.keys(), max_selections= 2)
        selected_cols2 = [demographics_dic[col] for col in rating_option3] +["visit_frequency"]        
    
        submitted2 =st.form_submit_button("Submit to produce sunburst")
        if submitted2:
            fig9 = px.sunburst(starbucks_merged,path=selected_cols2,values = "visitNo",color = "visit_frequency",
title = f"{rating_option3} vs. Visit Frequency",labels = prettyname_dict, height= 600, width = 600, color_discrete_sequence=[ '#82b74b', '#036635', '#3e4444'])
            col16.plotly_chart(fig9)
   
    

#graph 10 box plot #add the order
    st.subheader('Exploring Average Amount Spent')
    col_submit,col_submit_chart = st.columns([4,5])
    with st.form("Select One Demographics and One Rating"):
        boxdemo_col = col_submit.selectbox("Select a Demographic",demographics_simple_dic.keys(),key =10)
        colorrating_col = col_submit.selectbox("Select a Rating", factors_dic.keys(),key=11 )
        submitted=st.form_submit_button("Submit to produce box plot")
        if submitted:
            fig10 =  px.box(starbucks_merged,x="avg_amt_spent", y =factors_dic[colorrating_col],
                            color=demographics_simple_dic[boxdemo_col],
                            title = f"{boxdemo_col} with {colorrating_col} vs. Average Amount Spent", labels = prettyname_dict,
                            category_orders = category_orders_dict,  color_discrete_sequence=['#82b74b', '#036635','#c1946a', '#3e4444'],height=550, width = 550)
            fig10.update_traces(quartilemethod="exclusive")
            col_submit_chart.plotly_chart(fig10)
            
            
    #box_option = col17.selectbox("Select a Demographic",demographics_dic.keys(),key =10)
    #fig10 = px.box(starbucks_merged,x="avg_amt_spent", y = 'Id', color=demographics_dic[box_option],
                  # title = f"{demo_option} vs. Items Purchase",labels = prettyname_dict)
   # fig10.update_traces(quartilemethod="exclusive")
   # col18.plotly_chart(fig10)
   # col17.markdown("markdown")


    
    
    
if selected=="Analysis of Demographic":
    st.title("Analysis of Demographic")
    
    st.header("Analysis Demographics of Malaysia Starbucks ")
    st.markdown("By analyzing the dataset, we can gain insights into the customer profile of Starbucks in Malaysia. We will explore the demographic variables such as age, gender, occupation, and income, and their relationship with various factors such as product quality ratings, visit frequency, and items purchased.")
    st.markdown("The major findings of this analysis will help us understand the trends of Starbucks customer profiles in Malaysia. We will be able to identify the most popular items purchased by different demographic groups, how often they visit Starbucks, and the factors that drive customer satisfaction.")
    
#1
    st.subheader("Major Demographics")
    col5,col6 = st.columns([1,1])
    col7,col8 = st.columns([1,1])
    col5.markdown("")
    col5.markdown("The histogram graph provides valuable insights into the demographic characteristics of loyal customers to Starbucks in Malaysia. From the graph, it can be observed that customers who are between 20-29 years old and employed exhibit the highest loyalty to the coffee chain. This can be attributed to their disposable income and perception of Starbucks as a trendy and desirable place to frequent. Similarly, students and employed individuals within this age range and with an annual income of less than RM25000 are also more likely to be loyal customers due to the affordability of Starbucks and the company's loyalty program.")
    col5.markdown("Conversely, customers who are 40 years or older and housewives have the least loyalty to Starbucks, possibly due to established routines or limited financial means. The histogram also suggests that customers within the age range of 30-39 years old with an annual income of more than RM75000 are more likely to be loyal customers due to their financial stability and convenience of Starbucks as a social and business meeting place.")

    
    fig_ana_1 = px.histogram(starbucks_merged, x='occupation', color='loyal', barmode='group',
                  title = 'Occupation vs. Loyalty',labels=prettyname_dict,  color_discrete_sequence=['#036635', '#82b74b','#c1946a' ])
    fig_ana_1.update_traces(texttemplate='%{y:1f}')
    fig_ana_2 = px.histogram(starbucks_merged, x='age_range', color='loyal', barmode='group',
                  title = 'Age Range vs. Loyalty',labels=prettyname_dict, color_discrete_sequence=['#036635', '#82b74b','#c1946a'])
    fig_ana_2.update_traces(texttemplate='%{y:1f}')
    fig_add_2 = px.histogram(starbucks_merged, x='annual_income', color='loyal', barmode='group',
                  title = 'Annual Income vs. Loyalty',labels=prettyname_dict,  color_discrete_sequence=['#036635', '#82b74b','#c1946a'])
    fig_add_2.update_traces(texttemplate='%{y:1f}')
    
    col6.plotly_chart(fig_ana_1)
    col7.plotly_chart(fig_ana_2)
    col8.plotly_chart(fig_add_2)
    
#2
    st.subheader("Visit Frequency Patterns of Demographics") 

    st.markdown("The sunburst chart represents hierarchical data with inner rings representing higher-level categories and outer rings representing lower-level categories. The color of each segment represents different demographic groups. The chart is organized based on three levels of data: gender, the selected demographic category, and visit frequency. The size of each segment represents the average rating for the product quality rate.") 
    st.markdown("Based on the chart, people who are female, in the age group of 20-29, and students & employees are more likely to visit Starbucks in their everyday lives. In general, the chart provides an effective visualization for exploring the relationship between different demographics and their visit frequency to Starbucks, and how it can vary across different groups.")
    col9,col10=st.columns([5,5])
    #col9_5,col10_5 = st.columns([5,5])
    col10.markdown("")
    col10.markdown("")
    col10.markdown("")
#change the title to markdown
    fig_ana_3 = px.sunburst(starbucks_merged,path=["gender_1", "age_range", "visit_frequency"],
                       values = "visitNo",color = "age_range",
                       labels = prettyname_dict, height = 600, width = 600, color_discrete_sequence=['#82b74b', '#036635', '#3e4444'])
    
    fig_ana_4 = px.sunburst(starbucks_merged,path=["gender_1", "occupation", "visit_frequency"],
                       values = "visitNo",color = "occupation",
                       labels = prettyname_dict, height = 600, width = 600, color_discrete_sequence=[ '#82b74b', '#036635', '#3e4444'])
    fig_ana_3.update_layout(margin=dict(l=20, b=45))
    fig_ana_4.update_layout(margin=dict(t=25))
    
    col9.plotly_chart(fig_ana_3, use_container_width=True)
    col10.plotly_chart(fig_ana_4, use_container_width=True)
    
    #title = "Age vs. Visit Frequncy",
    
if selected=="Analaysis of Consume Habit":
    st.title("Analaysis of Consume Habit")
    
    st.subheader("Customer's Consume Habits Relative With Visit Frequency")
    col11,col12 =st.columns([6,5])
    
    col11.markdown("After analyzing the visit frequency of Starbucks customers in Malaysia through the provided graphs, we can conclude that females who are students or employees in the age range of 20-29 years old are the most frequent customers of Starbucks. To gain a better understanding of the specific customer profile, it is important to explore the preferred consume methods of Starbucks customers.")
    col11.markdown("The provided code generates a histogram graph that compares the consume methods of Starbucks customers with their visit frequency. The graph suggests that customers who rarely visit Starbucks tend to choose either dine-in or take away options. However, customers who visit Starbucks daily prefer to use take away and drive-through options.")
    
    fig_ana_5 = px.histogram(starbucks_merged, x="consume_method", color = "visit_frequency",category_orders = category_orders_dict, histfunc="avg", nbins=20, text_auto=True, barmode="group",title ="Consume Method vs. Visit Frequency",labels=prettyname_dict, color_discrete_sequence=['#82b74b', '#036635','#c1946a', '#3e4444'])
    fig_ana_5.update_traces(texttemplate='%{y:.1f}')
    col12.plotly_chart(fig_ana_5)
    
    st.subheader("Customer's Average Spending With Price Rates")
    col13,col14=st.columns([6,5])
    col13.markdown("This box plot graph shows the relationship between the gender, price range ratings, and average amount spent at Starbucks. The x-axis represents the average amount spent in RM (Malaysian currency ), while the y-axis represents the price range ratings. The color of the boxes indicates the gender, with green representing female, dark green representing male, and brown representing unknown.")
    col13.markdown("Indicating that most people spend less than RM 20 and give a price rating of 3. However, there are some outliers, especially among males, who spend an average of RM 40 and give the highest rating of 5 for the price range.")
    fig_ana_6 = px.box(starbucks_merged,x="avg_amt_spent", y ="price_range_rate",
                       color="gender_1",title = "Gender With Price Ratings vs. Average Amount Spent", labels = prettyname_dict,
                       category_orders = category_orders_dict, color_discrete_sequence=['#82b74b', '#036635','#c1946a', '#3e4444'])
    fig_ana_6.update_traces(quartilemethod="exclusive")
    col14.plotly_chart(fig_ana_6)
    
#4
    st.subheader("Compare Each Rating Values Based on Gender")
    st.markdown("The facet histograms provide a clear visual representation of the variables of ratings from both male and female customers. It is evident that both male and female customers have lower ratings on price. However, there is a slightly higher proportion of female customers who rate the WiFi as 3, suggesting that female customers are more likely to connect to the store WiFi.")
    
    st.markdown("Furthermore, female customers give higher ratings for ambiance and service at rate 4, indicating that they are more satisfied with the overall experience at the store. Additionally, both male and female customers give a full rating on the importance of promotions. It is worth noting that male customers have lower ratings than female customers across all rating variables, and this may be due to the fact that there were more female customers surveyed. Overall, the facet histograms provide valuable insights into the ratings and preferences of both male and female customers, highlighting the areas where the store can improve to better serve its customers.")
   
    starbucks_merged_melt = pd.melt(starbucks_merged, id_vars = main_cols, value_vars = factors, value_name = 'Rating')
    starbucks_merged_melt = starbucks_merged_melt.sort_values(by='Rating')
    fig = px.histogram(starbucks_merged_melt, nbins=50, x='gender_1', color='variable',facet_col='Rating',facet_col_wrap=2, barmode='group',height = 800, width = 1050,labels = prettyname_dict, color_discrete_sequence=['#82b74b', '#036635','#0088cc', '#66b3ff','#c1946a','#90653c', '#3e4444'])
    fig.update_xaxes(showticklabels=True)
#fig.update_yaxes(title_text='Count of people') # limit the y-axis title
    fig.update_layout(yaxis=dict(title_text='Count of people'), yaxis3=dict(title_text='Count of people'),
                      yaxis5=dict(title_text='Count of people'))
    fig.update_traces(texttemplate='%{y:1f}')
    st.plotly_chart(fig)
    
    
  
    
    







#1    
    #fig = px.pie(starbucks_merged, values='visitNo', names='occupation',hover_data=['time_spent'],
#title='Occupation vs. Visit Number', labels={'visitNo':'Visit Number'})
    #fig.update_traces(textposition='inside', textinfo='percent+label')
    #st.plotly_chart(fig)
    

    
    
    
if selected=="Conclusion":
    st.title("Conclusion")
    st. markdown("Based on the analysis of the Starbucks Customer Retention Malaysia Survey dataset, it can be concluded that Starbucks in Malaysia primarily attracts customers between the ages of 20-29, who are either students or employees and have an annual income less than RM25000. These customers perceive Starbucks as a trendy and desirable place to frequent, and the company's loyalty program and affordability of products further increase their loyalty towards the coffee chain. Conversely, customers who are 40 years or older and housewives have the least loyalty to Starbucks.")
    
    st.markdown("The analysis also provides insights into the visit frequency patterns of different demographics. Female customers in the age group of 20-29 and are students or employees are the most frequent customers of Starbucks in Malaysia. Conversely, customers who are 40 years or older and housewives have the least loyalty to Starbucks, possibly due to established routines or limited financial means.")
                
    st.markdown("Additionally, customers who visit Starbucks daily prefer take away and drive-through options, while those who visit less often prefer dine-in or take away. ")
    
    st.markdown("From the analysis, it shows that most customers spend less than RM 20 would give a price rating of 3, but there are some male customers who spend an average of RM 40 give the highest price rating of 5. But in general, both male and female customers have lower ratings on price, indicating that Starbucks could consider offering more affordable products to improve customer satisfaction in this area.")
    
    st.markdown("The analysis indicates that female customers in Malaysia are more satisfied with the ambiance and service at Starbucks compared to male customers, which suggests that Starbucks could focus on improving these areas to attract and retain more female customers. Hence, to attract more female customers, Starbucks in Malaysia could focus on providing a comfortable and safe environment, as well as enhancing the quality of its customer service. Starbucks could also consider introducing more products and promotions that appeal to female customers' tastes and preferences. Additionally, Starbucks can continue to leverage its partnership with local businesses to offer unique products and experiences that cater to the local market.")
    
    
if selected=="Bibliography":
    st.title("Bibliography")
    
    st.markdown("Archie. “Company Analysis of Starbucks Coffee Malaysia.” StudyBay, September 18, 2019. https://studybayhelp.co.uk/blog/company-analysis-of-starbucks-coffee-malaysia/?ref=1d10f08780852c55.")
    st.markdown("HAMZAH, MAHIRA . “Starbucks Customer Survey.” www.kaggle.com, 2020. https://www.kaggle.com/datasets/mahirahmzh/starbucks-customer-retention-malaysia-survey.")
    st.markdown("Shrestha, Sulabh. “Dissection of Starbucks Corporation on Malaysia.” Medium, March 24, 2022. https://sulabh4.medium.com/dissection-of-starbucks-corporation-on-malaysia-374c3aa564e5.")


    
    









# ### Average amount of money most people would spend in starbucks
# ### Equivalent students and employed would spent less than RM20, but more employed would spend around 20-40.

# In[279]:


fig = px.histogram(starbucks_merged, x="avg_amt_spent", color = "occupation",barmode="group",
                   title = "Average Amount Money Spent vs. Numbers of people")
fig.update_layout(bargap=0.2)


# # Ratings

# ### Comparing count of male and female for each rating values
# ### Rating =1: Male & Female - Price range rate(most count)
# ### Rating =2: Male & Female - Price range rate  
# ### Rating =3: Male - Service rate, Female - Wifi quality rate 
# ### Rating =4: Male - Product quality rate, Female - Service rate
# ### Rating =5: Male & Female - Promotions importance rate

# In[265]:


starbucks_merged_melt = pd.melt(starbucks_merged, id_vars = main_cols, value_vars = factors, value_name = 'Rating')

starbucks_merged_melt = starbucks_merged_melt.sort_values(by='Rating')

fig = px.histogram(starbucks_merged_melt, nbins=50, x='gender_1', color='variable',
                   facet_col='Rating',facet_col_wrap=2, barmode='group',height = 800, width = 1050)
fig.update_xaxes(showticklabels=True)
#fig.update_yaxes(title_text='Count of people') # limit the y-axis title

fig.update_layout(title='Compare Each Rating Values Based on Gender',
                 yaxis=dict(title_text='Count of people'), yaxis3=dict(title_text='Count of people'),
                 yaxis5=dict(title_text='Count of people'))



# ### Price rate (in average) vs. Annual income
# ### Student with 50000-100000 annual income have avg price rate of 4
# ### employed with >150000 annual income have avg price rate of 4
# ### housewife with 50000-100000 annual income and students with <150000 have the lowest price rate

# In[294]:


fig = px.histogram(starbucks_merged, x="annual_income", y="priceRate", color = "occupation",
                   histfunc="avg", nbins=20, text_auto=True, barmode="group",category_orders = category_orders_dict,
                  title = "Price Rate (in average) vs. Annual Income")


# ### Product Rate (in average) vs. Annual income
# ### Self-employed overall have the highest average product rate 
# ### Students with 50000-100000 annual income have lower product rate compare to price
# ### Employed with  50000-100000 annual income have higher product rate comapare to price rate 

# In[295]:


fig = px.histogram(starbucks_merged, x="annual_income", y="productRate", color = "occupation",category_orders = category_orders_dict,
                   histfunc="avg", nbins=20, text_auto=True, barmode="group",
                  title = "Product Rate (in average) vs. Annual Income")


# From the graoh above, it is showing that: groups of customers have higher annual income are tends to have a lower ratings toward starbuck's products quality. BUT people in the first three ranges of annual income are tend to rate the product quality higher, especially people with 50,000 - 100000 RM annual income.
# 
# pypothesis 1: starbucks are targeting 50000 - 100000 annual income customers, majorlly lower to middle class.
# 
# based on research: https://www.dosm.gov.my/v1/index.php?r=column/pdfPrev&id=SzNvU0ZhaGpCMUROVlpCdTU1WWJSdz09
# 
# people from ages 15-24 years old and 25-35 years old people with semi-skilled and skilled jobs are more likely to be the target customer for malaysia starbucks
# 
# hence: comparing the age, occupation, income, and visit_frequency

# # Visit Frequency

# ### Price Rate (in average) vs. Vist Frenquency

# In[296]:


fig = px.histogram(starbucks_merged, x="visit_frequency", y="priceRate", color = "occupation",
                   histfunc="avg", nbins=20, text_auto=True, barmode = "group",
                  title = "Price Rate (in average) vs. Vist Frequency", category_orders=category_orders_dict)


# ### Age Rate vs. Visit Frenquency

# In[269]:





# ### Occupation vs. Visit Number

# In[270]:






# # Loyal

# ### Comparing loyalties with occupation
# ### Employed and students are the most loyalty group of customers

# In[271]:


fig = px.histogram(starbucks_merged, x='occupation', color='loyal', barmode='group',
                  title = 'Occupation vs. Loyalty')




# In[272]:


fig = px.histogram(starbucks_merged, x='age_range', color='loyal', barmode='group',
                  title = 'Occupation vs. Loyalty')




# # Comsume Method

# ### Compare consume_method with count of gender

# In[273]:


fig = px.histogram(starbucks_merged, x="consume_method", color = "gender_1", barmode="group",
                  title = "Consume Method vs. Numbers of Female and Male")
fig.update_layout(bargap=0.2)



# In[274]:


fig = px.histogram(starbucks_merged, x="consume_method", color = "occupation", barmode="group",
                  title = "Consume Method vs. Occupation")
fig.update_layout(bargap=0.2)
 


# In[275]:


fig = px.histogram(starbucks_merged,x="nearest_outlet", color="consume_method", barmode = "group",
                   category_orders = category_orders_dict,
                  title = "Distance to Nearest Store vs. Consume Method")




# In[304]:


merge_pie = pd.merge(starbucks_merged['item_purchase'].str.split(';').explode(),starbucks_merged['time_spent'],
        left_index=True, right_index=True).reset_index(drop=True)


# In[308]:


fig = px.pie(merge_pie , names='item_purchase',
             title='Item Purchase in Percentage')
fig.update_traces(textposition='inside', textinfo='percent+label')


# In[ ]:




