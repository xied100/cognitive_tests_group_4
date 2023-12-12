# added by PWL to force images to be downloaded before test starts
import glob
from IPython.display import HTML
png_list = glob.glob("./pics/*.png")
image_list = ""
for png in png_list:
    image_list+=f"<image src='{png}' width='1px' >"
display(HTML('<p>'+image_list+'</p>'))

from IPython.display import display, Image, clear_output, HTML
import time
import pandas as pd
import json

#import for google form
import requests
from bs4 import BeautifulSoup
import json
import time

# import for buttons
import ipywidgets as widgets
from jupyter_ui_poll import ui_events
from IPython.display import display, Image, clear_output, HTML
import time

#Apply send to google form
def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form 
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

#Apply using button:
event_info = {
    'type': '',
    'description': '',
    'time': -1}

def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):    
    start_wait = time.time()

    # set event info to be empty
    # as this is dict we can change entries
    # directly without using
    # the global keyword
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            # add pause before looping
            # to check events again
            time.sleep(interval)
    
    # return event description after wait ends
    # will be set to empty string '' if no event occured
    return event_info

def register_btn_event(btn):
    event_info['type'] = "button click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

def register_text_input_event(text_input):
    event_info['type'] = "text_entry"
    event_info['description'] = text_input.value
    event_info['time'] = time.time()
    return

def text_input(prompt=None):
    text_input = widgets.Text(description=prompt, style= {'description_width': 'initial'})
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text_input.on_submit(register_text_input_event)
    display(text_input)
    event = wait_for_event(timeout=10)
    text_input.disabled = True
    return event['description']

def consent_collection():
    """
    Participant can only start if they agreed with the consent.
    """
    #consent
    data_consent_info = """DATA CONSENT INFORMATION:
Please read:
we wish to record your response data
to an anonymised public data repository. 
Your data will be used for educational teaching purposes
practising data analysis and visualisation.
Please type   yes   in the box below if you consent to the upload."""

    print(data_consent_info)
    btn1 = widgets.Button(description= "yes")
    btn2 = widgets.Button(description= "no")
    btn1.on_click(register_btn_event)
    btn2.on_click(register_btn_event)
    panel = widgets.HBox([btn1, btn2])
    display(panel)
    result = wait_for_event()
    clear_output(wait=False)

    if result['description'] == "yes": 
        print("Thanks for your participation.")
        print("Please contact philip.lewis@ucl.ac.uk")
        print("If you have any questions or concerns")
        print("regarding the stored results.")
        time.sleep(1.5)
        clear_output(wait=False)
    else: 
        raise Exception("User did not consent to continue test.")

def get_user_info():
    """
    Some basic information need to be collected for further analysis

    Returns: 
    username, username_age, username_sex, username_drink
    """
    # the start of the test
    print("Welcome to the Approximation Number Sense(ANS) test!")
    time.sleep(1.5)
    print("In this test, image with blue and yellow dots will be presented.")
    time.sleep(1.5)
    print("You will be asked to identidy which sides has MORE dots.")
    time.sleep(1.5)
    
    btn3 = widgets.Button(description="Click me to continue")
    btn3.on_click(register_btn_event)
    display(btn3)
    wait_for_event()
    clear_output(wait=False)
    
    # produce anonymised ID
    while True:
        id_instructions = """
        Enter your anonymized ID
        To generate an anonymous 4-letter unique user identifier, please enter:
        - two letters based on the initials (first and last name) of a childhood friend
        - two letters based on the initials (first and last name) of a favorite actor / actress
        e.g. if your friend was called Charlie Brown and film star was Tom Cruise
        then your unique identifier would be CBTC
        """
        print(id_instructions)
        username = text_input('Enter your name:')
        print("User Entered", username)
        clear_output(wait=False)
        if len(username) == 4 and username.isalpha():  
            break
        else:
            print("Please enter a 4-letter ID containing only letters. Try again.")

    display(btn3)
    wait_for_event()
    clear_output(wait=False)
    print("Please enter your age; \nthis will only be used for educational purpose.")
    username_age = text_input("Enter age:")
    clear_output(wait=False)
    
    print("Please select your sex; \nthis will only be used for educational purpose.")
    btn4 = widgets.Button(description="male")
    btn5 = widgets.Button(description="female")
    btn4.on_click(register_btn_event)
    btn5.on_click(register_btn_event)
    panel2 = widgets.HBox([btn4, btn5])
    display(panel2)
    result = wait_for_event()
    username_sex = result['description']
    clear_output(wait=False)
    
    print("Before taking the test, if you have any of the following please enter：\n a for coffee or tea or any energy drink; \n b for alcohol or any psychiatric drugs; \n c for none of them.")
    btn6 = widgets.Button(description="a")
    btn7 = widgets.Button(description="b")
    btn8 = widgets.Button(description="c")
    btn6.on_click(register_btn_event)
    btn7.on_click(register_btn_event)
    btn8.on_click(register_btn_event)
    panel3 = widgets.HBox([btn6, btn7,btn8])
    display(panel3)
    result = wait_for_event()
    username_drink = result['description']
    clear_output(wait=False)

    return username, username_age, username_sex, username_drink

def try_out_test():
    #try out before taking the test
    print('Here is a test for you to try out before taking the test')
    print('the other questions in the test will have the same format.')
    print('The result of try_out will not be included in the main test.')
    time.sleep(3)
    clear_output(wait=False)
    
    display(image31)
    time.sleep(1.5)
    clear_output(wait=False)
    
    btn9 = widgets.Button(description="left")
    btn10 = widgets.Button(description="right")
    btn9.on_click(register_btn_event) 
    btn10.on_click(register_btn_event) 
    myhtml1 = HTML("<h1>Which side has more dots?</h1>")
    display(myhtml1)
    myhtml2 = HTML("<h2>You have 3 seconds to answer</h2>")
    display(myhtml2)
    panel = widgets.HBox([btn9, btn10])
    display(panel)
    result = wait_for_event(timeout=3)
    clear_output()
    
    if result['description'] == "left":
        print("Correct!")
    elif result['description'] == "right":
        print("Sorry, this is not the correct answer.")   
    else:
        print("Sorry you do not click on time.")

#store images
image1 = Image("Slide1.PNG", width = 600)
image2 = Image("Slide2.PNG", width = 600)
image3 = Image("Slide3.PNG", width = 600)
image4 = Image("Slide4.PNG", width = 600)
image5 = Image("Slide5.PNG", width = 600)
image6 = Image("Slide6.PNG", width = 600)
image7 = Image("Slide7.PNG", width = 600)
image8 = Image("Slide8.PNG", width = 600)
image9 = Image("Slide9.PNG", width = 600)
image10 = Image("Slide10.PNG", width = 600)
image11 = Image("Slide11.PNG", width = 600)
image12 = Image("Slide12.PNG", width = 600)
image13 = Image("Slide13.PNG", width = 600)
image14 = Image("Slide14.PNG", width = 600)
image15 = Image("Slide15.PNG", width = 600)
image16 = Image("Slide16.PNG", width = 600)
image17 = Image("Slide17.PNG", width = 600)
image18 = Image("Slide18.PNG", width = 600)
image19 = Image("Slide19.PNG", width = 600)
image20 = Image("Slide20.PNG", width = 600)
image21 = Image("Slide21.PNG", width = 600)
image22 = Image("Slide22.PNG", width = 600)
image23 = Image("Slide23.PNG", width = 600)
image24 = Image("Slide24.PNG", width = 600)
image25 = Image("Slide25.PNG", width = 600)
image26 = Image("Slide26.PNG", width = 600)
image27 = Image("Slide27.PNG", width = 600)
image28 = Image("Slide28.PNG", width = 600)
image29 = Image("Slide29.PNG", width = 600)
image30 = Image("Slide30.PNG", width = 600)
image31 = Image("try_out.PNG", width = 600)
#store images in list
image_list = [image1, image2, image3, image4, image5, image6, image7,image8, image9,image10,image11,image12,image13,image14,image15,image16,image17, image18, image19, image20, image21, image22, image23,image24, image25,image26,image27,image28,image29,image30]
#store answer in list
ans_list = ['left','right','left','right','right','left','right','left','right','left','right','right','left','right','right','left','right','left','right','left','left','right','left','left','left','left','left','left','right','left']

#info_list
#result of each question is recorded:
time_taken_list = []
score_each_list = []
user_ans = []

def collect_each_result():
    """
    Runs a set of ANS tests for a given set of images.
 
    Args:time_taken_list(str)
         score_each_list(str)
         user_ans(str): user's answers
         
    Returns:
        dict: the results of the ANS test (answer, score_each, time_taken)
    """
    results_each = {
        'user_ans': [],
        'score_each_list': [],
        'time_taken_list': [],}
    
    # store results
    results_each['user_ans'].append(user_ans)
    results_each['score_each_list'].append(score_each_list)
    results_each['time_taken_list'].append(time_taken_list)
    return results_each

def run_full_test():
    """
    Runs full stroop test
  
    Returns:
        tuple: (total_score, average_time_taken, results_json)
    """
    print("The test is about to start, are you ready for that!")
    ready = text_input("enter ready to start!")

    #set initial values of score and the start time
    score = 0
    time_allstart = time.time()
    for i in range(30):
    #showing the image
        display(image_list[i])
        time.sleep(1.5)
        start_time = time.time()
        clear_output(wait=False)
    #showing the button
        btn9 = widgets.Button(description="left")
        btn10 = widgets.Button(description="right")
        btn9.on_click(register_btn_event) 
        btn10.on_click(register_btn_event) 
        myhtml1 = HTML("<h1>Which side has more dots?</h1>")
        display(myhtml1)
        myhtml2 = HTML("<h2>You have 3 seconds to answer</h2>")
        display(myhtml2)
        panel = widgets.HBox([btn9, btn10])
        display(panel)
        result = wait_for_event(timeout=3)
        user_ans.append(result['description'])
        clear_output()
        
    #setting up ans to collect data
        if result['description'] == ans_list[i]:
            score = score + 1
            score_each_list.append(1)
        else:
           score_each_list.append(0)
            
        end_time = time.time()
        time_taken = end_time - start_time
        time_taken_list.append(time_taken)

        time.sleep(1.5)
        clear_output(wait=False)
        
    print('Thank you for taking the test \nHere is your result')
    total_score = score /30 * 100
    print(f"total score = {total_score}")

    average_time_taken = sum(time_taken_list)/30
    print(f"average time taken: {average_time_taken}")
    time.sleep(5)
    clear_output(wait=False)

    #collect results from test
    result_analysis = collect_each_result()
    df_results = pd.DataFrame(result_analysis) 
    results_json = df_results.to_json()

    return total_score, average_time_taken, results_json

#Run the test
#Start the test
def do_the_test():
    collection_1 = consent_collection()
    collection_2 = get_user_info()
    try_out = try_out_test()
        
    #run function with data:
    result_tuple = run_full_test()
    total_score, average_time_taken, results_json = result_tuple
 
    #send to google form:
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdW9qzCp2vqy8FgM1SWKeUu0AUdvih-0NhXS28ZGc-nO-TioA/viewform?usp=sf_link"
    data_dict = {
        # from get_user_info(), collection_2
        'user_id': collection_2[0], 
        'age': collection_2[1],
        'sex': collection_2[2],
        'drink': collection_2[3],
        #from run_full_test()
        'score': total_score,
        'average_time_taken': average_time_taken,
        'results': results_json}
    send_to_google_form(data_dict, form_url)
    return

do_the_test()