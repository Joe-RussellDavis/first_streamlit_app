import streamlit as sl
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


sl.title('My Parents New Healthy Diner')

sl.header('Breakfast Favourites')

sl.text('🥣 Omega 3 & Blueberry Oatmeal')

sl.text(' 🥗 Kale, Spinach & Rocket Smoothie')

sl.text('🐔 Hard-Boiled Free-Range Egg')

sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#lets put a pick list here so they can pick the fruit they want to include

my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = sl.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page

sl.dataframe(fruits_to_show)

#Now for fruityvice api response

def get_fruityvice_data(this_fruit_choice):

    '''Function for communicating with fruity_vice API'''

    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # normalises the json format to stage it for a dataframe
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
     

sl.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = sl.text_input('What fruit would you like information about?')
    if not fruit_choice:
            sl.error("Please select a fruit to get information")
    else:
            sl.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
     sl.error()


#Snowflake related functions

def get_fruit_load_list():
     
    ''' Function to retrieve fruit_load_list table from snowflake'''
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Select * from fruit_load_list")
        return my_cur.fetchall()
    

#Add a button to load the fruit
sl.header('View Our Fruit List - Add Your Favourites!')
if sl.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
    sl.dataframe(get_fruit_load_list())
    my_cnx.close()
    

def insert_row_snowflake(new_fruit):
        
        ''' Function to insert row into table in snowflake'''
        with my_cnx.cursor() as my_cur:
            my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values ('{new_fruit}')")
            return "Thanks for adding " + new_fruit
        


fruit_to_add = sl.text_input('What fruit would you like to add?')

try:
    if not fruit_to_add:
        sl.error('Please select a fruit to add to the list')
    else:
        if sl.button('Add your Fruit to the list'):
            my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
            sl.text(insert_row_snowflake(fruit_to_add))
            my_cnx.close()

except URLError as e:
    sl.error()




