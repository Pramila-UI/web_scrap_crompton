import pandas as pd
import time
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from utility_function import  ( get_dealer_info_using_selenium , merging_datadrame  , writing_df_into_csv_file  , drop_duplicates)
from send_email import send_mail


if __name__ == "__main__":
    start_time = time.time()

    ### open the browser 
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.maximize_window() 

    ##open the website using the  browser
    browser.get('https://www.crompton.co.in/dealer-locator/')

    time.sleep(5) ## waiting for the page to load

    states_name = browser.find_elements(by='xpath' , value="//*[@id='service_center_state_dealer']/option") 
    all_states = [state.text for state in states_name[2:]] ## fetch the all the states 

    data_frame_list = []
    for state in all_states:
        ### adding the option value to the dropdowm and clicking that 
        browser.find_element(by='xpath', value=f"//select[@name='service_center_state_dealer']/option[text()='{state}']").click()
        time.sleep(4)  ### waiting  to load the page 

        totalCount = browser.find_element(by='xpath',value="//input[@id='totalCount']").get_attribute('value')

        ### Click the View Button :- totalcount should be greater than 21
        if int(totalCount) > 21:
            while True:
                ### load the view more page (clicking the button multiple times )
                element = browser.find_element(by = 'xpath', value="//a[@class='brandbtn']")
                browser.execute_script("arguments[0].click();", element)

                time.sleep(5)

                ## checking the button is visible or not . if its value is '' break the loop
                btn_text = browser.find_element(by='xpath' , value="//*[@id='address-slider-dealer']/div")
                if btn_text.text == '':
                    break

        ## call the function to Extract the  required data
        dealer_data = get_dealer_info_using_selenium(browser)
        state_name = state

        ## store the data into dataframe
        if len(dealer_data['shop_names']) == len(dealer_data['address']) == len(dealer_data['emails']) == len(dealer_data['mobile_num']) :
            df = pd.DataFrame(zip(dealer_data['shop_names'] , dealer_data['address'] , dealer_data['mobile_num'] , dealer_data['emails']) , columns=['Shop Name' ,'Address' ,'Mobile Number' ,'Email'])
            df['State'] = state_name

            ## calling drop_duplicate function to drop th duplicate rows 
            drop_duplicate_res = drop_duplicates(df)
            data_frame_list.append(drop_duplicate_res) ## append the df to the list

        else:
            pass

    if len(data_frame_list) > 0:
        #### merge the dataframes 
        merge_res = merging_datadrame(data_frame_list)

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

            else:
                print(res_csv['Message'])
        else:
            print(merge_res['Message'])

    else:
        print("There is no dataframe to create the csv file")

    end_time = time.time()
    print("Total time taken:" , end_time-start_time)

    ### After Completing the task closing the btowser
    browser.quit()
