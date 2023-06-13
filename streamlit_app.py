import streamlit as sl
import pandas as pd
import requests
import snowflake.connector


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



sl.header("Fruityvice Fruit Advice!")

fruit_choice = sl.text_input('What fruit would you like information about?', 'all')
sl.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)



# normalises the json format to stage it for a dataframe
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# dataframe
sl.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
sl.header("the fruit load list contains:")
sl.dataframe(my_data_row)

fruit_choice = sl.text_input('What fruit would you like to add?')
my_cur.execute(f'INSERT INTO FRUIT_LOAD_LIST VALUES {fruit_choice}')

