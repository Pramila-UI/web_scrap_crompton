import requests
from bs4 import BeautifulSoup
import pandas as pd
from utility_function import  ( merging_datadrame  , writing_df_into_csv_file , drop_duplicates ,
        get_web_details_using_requests , get_data_from_website , get_dealer_details_list) 
import time
from send_email import send_mail

if __name__ == "__main__":
    start_time = time.time()
    
    website_soup =  get_web_details_using_requests('https://www.crompton.co.in/dealer-locator/')

    """ call this function and get from the website  """
    website_details = get_data_from_website(website_soup)
    totalCount = website_details['totalCount']

    data_frame_list = []
    for state in website_details['all_states']:

        base_url = f"https://www.crompton.co.in/wp-admin/admin-ajax.php?action=getDealerCenters&service_center_state={state}&startLimit=0&endLimit={totalCount}"
        res = requests.get(base_url).json()
        # print(f"For the State : {state} , Dealer count is : {res['res_count']}")
        
        soup = BeautifulSoup(res['liresult'] , 'html.parser')

        """ Calling the function to extact the result from the soute"""
        dealer_data =get_dealer_details_list(soup)
        state_name = state

        if len(dealer_data['shop_names']) == len(dealer_data['address']) == len(dealer_data['emails']) == len(dealer_data['mobile_num']) :
            df = pd.DataFrame(zip(dealer_data['shop_names'] , dealer_data['address'] , dealer_data['mobile_num'] , dealer_data['emails']) , columns=['Shop Name' ,'Address' ,'Mobile Number' ,'Email'])
            df['State'] = state_name

            drop_duplicate_res = drop_duplicates(df) ## drop th duplicate 
            data_frame_list.append(drop_duplicate_res)  ## append the df into the data_frame_list
        
        else:
            pass

    if len(data_frame_list) > 0:
        merge_res = merging_datadrame(data_frame_list)  ## merging the dataframe
        if merge_res['Status'] == "Success":

            res_csv =  writing_df_into_csv_file(merge_res['Result'])

            if res_csv['Status'] == "Success":
                print(res_csv['Message'])

                #### Call the function to send the mail (Chnage the to and from email id)
                MESSAGE_BODY = "Hi , Please find the attached file for the crompton dealer information"
                EMAIL_SUBJECT = "Sending crompton dealer information"
                EMAIL_FROM = "testingpurpose217@gmail.com"
                EMAIL_TO = "pramilaproms012@gmail.com"
                FILE_NAME = "crompton_dealer_information.csv"
                PATH_TO_CSV_FILE = "DealerData_Info.csv"

                mail_res =  send_mail( EMAIL_TO , EMAIL_FROM , EMAIL_SUBJECT ,MESSAGE_BODY , FILE_NAME , PATH_TO_CSV_FILE )
                print(mail_res['Message'])


                end_time = time.time()
                print("Total time taken:" , end_time-start_time)

            else:
                print(res_csv['Message'])
        else:
            print(merge_res['Message'])

    else:
        print("There is no dataframe to create the csv file")