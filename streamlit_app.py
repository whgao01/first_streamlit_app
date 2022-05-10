import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Mom\'s New Healthy Dinner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Apinach & Rocket Smoothies')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_first_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_first_fruit_list = my_first_fruit_list.set_index("Fruit")

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some Fruits:", list(my_first_fruit_list.index), ["Avocado", "Strawberries"])
fruits_to_show = my_first_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #streamlit.text(fruityvice_response.json())

    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #streamlit.text("fruityvice_normalized" + str(type(fruityvice_normalized)))
    return fruityvice_normalized



streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_datarows = get_fruit_load_list()
    df = streamlit.dataframe(my_datarows)
    #streamlit.text("my_datarows" + str(type(my_datarows)) + ",df" + str(type(df)))


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlist')")
        return "Thanks for adding " + new_fruit
    

fruit_add = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(fruit_add)
    streamlit.text(back_from_function)
    
    
    
    
    
streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("select current_user(), current_account(), current_region()")
my_cur.execute("select * from fruit_load_list")
my_datarows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
df = streamlit.dataframe(my_datarows)
#streamlit.text("my_datarows" + str(type(my_datarows)) + ",df" + str(type(df)))

fruit_add = streamlit.text_input('What fruit would you like add?', '')
my_datarows.append(fruit_add)
streamlit.write('Thanks for adding', fruit_add)
