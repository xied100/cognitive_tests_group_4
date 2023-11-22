from IPython.display import display, Image, clear_output, HTML
import time
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os




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
  












# ... [Your data consent and ID generation code] ...
data_consent_info = """DATA CONSENT INFORMATION:

Please read:

we wish to record your response data

to an anonymised public data repository.

Your data will be used for educational teaching purposes

practising data analysis and visualisation.

Please type yes in the box below if you consent to the upload."""

print(data_consent_info)

result = input("> ")

if result == "yes":

    print("Thanks for your participation.")
    
    print("Please contact philip.lewis@ucl.ac.uk")
    
    print("If you have any questions or concerns")
    
    print("regarding the stored results.")

else:

# end code execution by raising an exception

    raise(Exception("User did not consent to continue test."))




id_instructions = """

Enter your anonymised ID

To generate an anonymous 4-letter unique user identifier please enter:

- two letters based on the initials (first and last name) of a childhood friend

- two letters based on the initials (first and last name) of a favourite actor / actress

e.g. if your friend was called Charlie Brown and film star was Tom Cruise

then your unique identifer would be CBTC

"""

print(id_instructions)

user_id = input("> ")

print("User entered id:", user_id)





# Modified run_custom_math_ability_test function to return total_score
def run_custom_math_ability_test(questions):
    gender = input("Please enter your gender(F/M): ")
    coffee = input("Have you drunk coffee in the last 12 hours(Y/N):")
      
    print(f"Welcome to the Custom Maths Ability Test. You have 3 minutes and 30 seconds to do the test. You may need a pen and a piece of paper. No calculator is allowed.")
    time.sleep(4)
    
    total_score = 0
    total_questions = len(questions)
    total_time = 0  # To track total time taken by the user
    
    start_time = time.time()  # Record the start time
    
    for question_number, question_data in enumerate(questions, start=1):
        question_parts = question_data["question"]
        correct_answer = question_data["answer"]
        
        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        
        # Check if the time limit (210 seconds) is reached
        if elapsed_time >= 210:
            print("\nTime's up! Test will now end.")
            break
        
        # Display "Question X" for 1.5 seconds and then clear it
        question_text = f"Question {question_number}"
        display(HTML(f"<h2>{question_text}</h2>"))
        time.sleep(1.5)
        clear_output(wait=True)
        
        for part_number, part in enumerate(question_parts, start=1):
            # Display each part for 2 seconds and then clear it
            display(HTML(f"<p>{part}</p>"))
            time.sleep(2)
            clear_output(wait=True)
            
        start_time_question = time.time()
        
        user_answer = input("\nYour answer: ")
        
        end_time_question = time.time()
        question_time = end_time_question - start_time_question
        total_time += question_time  # Add the time taken for this question
        
        if user_answer.isdigit() and int(user_answer) == correct_answer:
            total_score += 5
            print(f"Correct! Score: {total_score}/{question_number * 5}")
        else:
            print(f"Wrong. The correct answer is {correct_answer}. Score: {total_score}/{question_number * 5}")
        
        display_time = 2  # Time to display "Time taken for this question" message
        print(f"Time taken for this question: {question_time:.2f} seconds")
        
        # Wait for 1 second before clearing the "Time taken for this question" message
        for _ in range(display_time, 0, -1):
            time.sleep(1)
            clear_output(wait=True)
        
        if question_number < total_questions:
            continue
        
        time.sleep(1)  # Pause before the next question
    
    average_time = total_time / total_questions  # Calculate the average time per question
    
    print("\nTest Completed!")
    print(f"Total Score: {total_score} %")
    print(f"Average time per question: {average_time:.2f} seconds")
    
    return total_score  # Return the total_score at the end of the function

# Define your custom questions here
custom_questions = [
    {"question": [ "2", "+ 5"], "answer": 7},
    {"question": [ "20", "- 13"], "answer": 7},
    {"question": ["3", "* 8"], "answer": 24},
    {"question": ["35", "/ 5"], "answer": 7},
    {"question": ["(7", "* 6)", "+4"], "answer": 46},
    {"question": ["24", "* 24"], "answer": 576},
    {"question": ["18", "* 11"], "answer": 198},
    {"question": ["3^2", "+8"], "answer": 17},
    {"question": ["sqaure root of", "289"], "answer": 17 },
    {"question": ["6!"], "answer": 720},
    {"question": ["9^2", "- (1^2)"], "answer": 80},
    {"question": ["72", "* 78"], "answer": 5616},
    {"question": ["4!", "+1"], "answer": 25},
    {"question": ["(999", "- 9)", "/ 9"], "answer": 110},
    {"question": ["35", "* 101"], "answer": 3535},
    {"question": ["(1", "* 8)", "+ 1"], "answer": 9},
    {"question": ["(12", "* 8)", "+ 2"], "answer": 98},
    {"question": ["(123", "* 8)", "+ 3"], "answer": 987},
    {"question": ["(1234", "* 8)", "+ 4"], "answer": 9876},
    {"question": ["(123456789", "* 8)", "+ 9"], "answer": 987654321}
   
    
]



# Call the function and store the returned total_score
total_score = run_custom_math_ability_test(custom_questions)

# Save data in Google form
data_dict = {'Name': user_id,
             'Score': total_score  # Now total_score is defined
            }

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd-ZyxI982GA8ARgjCEk_Vow2eVtAAUaVsTmndeXT8snVdajw/viewform?usp=sf_link"
send_to_google_form(data_dict, form_url)

# Save data in disk (using Pandas)
user_data = [data_dict]  # Initialize user_data as a list containing the current data_dict
if os.path.exists('quiz_results.csv'):
    existing_data = pd.read_csv('quiz_results.csv')
    user_data += existing_data.to_dict(orient='records')  # Append existing data to user_data
    df = pd.DataFrame(user_data)
    df.to_csv('quiz_results.csv', index=False)
else:
    df = pd.DataFrame(user_data)
    df.to_csv('quiz_results.csv', index=False)
