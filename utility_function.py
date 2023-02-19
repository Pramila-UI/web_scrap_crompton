import pandas as pd
import requests
from bs4 import BeautifulSoup


def merging_datadrame(df_list):
    try:
        final_df = pd.concat(df_list)
        context = {
            "Status" :"Success" ,
            "Result" : final_df
        }
        return context

    except Exception as e:
        context = {
            "Status" :"Failure" ,
            "Message" : f"Exception while merging the dataframes :- {e}",
        }
        return context


def writing_df_into_csv_file(df):
    try:
        res = df.to_csv('DealerData_Info.csv' , index=False)
        context = {
            "Status" :"Success" ,
            "Message" : "Successfully Created the csv file" ,
            "Result" : res
        }
        return context

    except Exception as e:
        context = {
            "Status" :"Failure" ,
            "Message" : f"Exception while writing the dataframe into csv file :- {e}",
            "Result" : None
        }
        return context
  


def drop_duplicates(df):
    if df.duplicated().sum() > 0:
        df.drop_duplicates(inplace=True , keep='first')
        return df
    return df



def get_web_details_using_requests(url):
    web_site_url = requests.get(url)
    website_soup = BeautifulSoup(web_site_url.text , 'html.parser')
    return website_soup


def get_data_from_website(website_soup):
    ### To get the total of the total count 
    total_count = website_soup.find('input' , {'id':'totalCount'}).get_attribute_list('value')[0]
    total_count = int(total_count)

    ### selecting the all the states from the dropdowm
    states_name =  website_soup.select('#service_center_state_dealer > option:nth-child(n)')
    all_states = [state.text for state in states_name[1:]]

    context = {
        "totalCount" : total_count ,
        "all_states" : all_states
    }
    return context


def get_dealer_details_list(soup):
    ### using the class name for the p tag extract the data.
    shop_names = []
    for i in soup.find_all('p' ,{"class": "shop-name"}):
        shop_names.append(i.text)

    ### using the css selector scrap the data if then not provided the id and the  class name 
    address = []
    for i in soup.select('li:nth-child(n) > p:nth-child(2)'):
        address.append(i.text)
    
    emails = []
    for i in soup.find_all('a' ,{'class':'sidea emicon inline'}):
        emails.append(i.text)
    
    mobile_num_result= soup.select('li:nth-child(n) > ul.add-contact.contactnumber > li > a')
    mobile_num = []
    for i in mobile_num_result:
        mobile_num.append(i.text)

    context = {
        "address" : address ,
        "emails" :emails ,
        "mobile_num" :mobile_num ,
        "shop_names" : shop_names

    }

    return context

def get_dealer_info_using_selenium(browser):

    #### Extract the data required 
    shop_names =  browser.find_elements(by='xpath',value="//*[@id='address-slider-dealer']/ul/li/p[1]")
    shopnames = [shop.text  if shop.text != '' else '-' for shop in shop_names]


    address_list =  browser.find_elements(by='xpath',value="//*[@id='address-slider-dealer']/ul/li/p[2]")
    address = [addr.text  if addr.text != '' else '-' for addr in address_list]

    email_list =  browser.find_elements(by='xpath',value="//*[@id='address-slider-dealer']/ul/li/span/a")
    emails = [email.text  if email.text != '' else '-' for email in email_list]


    mobileno_list =  browser.find_elements(by='xpath',value="//*[@id='address-slider-dealer']/ul/li/ul[1]/li[1]/a")
    mobile_nums = [num.text  if num.text != '' else '-' for num in mobileno_list]

    context = {
        "address" : address ,
        "emails" :emails ,
        "mobile_num" :mobile_nums ,
        "shop_names" : shopnames

    }

    return context
