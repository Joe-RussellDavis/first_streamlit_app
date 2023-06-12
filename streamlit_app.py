import streamlit as sl
import pandas as pd

sl.title('My Parents New Healthy Diner')

sl.header('Breakfast Favourites')

sl.text('🥣 Omega 3 & Blueberry Oatmeal')

sl.text(' 🥗 Kale, Spnach & Rocket Smoothie')

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

