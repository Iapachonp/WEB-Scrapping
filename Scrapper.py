
#Save the microsoft form page as .htlm
#call it index1.html 

#need to be install: 
#pip install "ipython-beautifulsoup[bs4]"
#!pip install requests
#! pip install googletrans

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from googletrans import Translator



#Open HTML file
with open("index1.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp)
 
Title = soup.find("div", {"class": 'suiteheader-formtitle'}) #get title soup
Subtitle = soup.find("div", {"class": 'office-form-subtitle heading-1'})  #get sub title soup
questions = soup.find_all("div", {"class": "question-title-box"}) #get title question div soup
Answers_soup = soup.find_all("div", {"class": "office-form-question-content office-form-theme-focus-border"}) #get total div soup

#Get and translate answers & questions data and correct_value

def Answers_data_translate(trans, lang): 
    
    translator = Translator()
    Answers_Data_base= []
    Answer = {}
    for i in range(0, len(Answers_soup)):
        choices= Answers_soup[i].find_all("div", {"class": "office-form-question-choice"})
                                                
        for j in range(0, len(choices)):
            if choices[j].find("i", {"title":"Correct answer"}) != None: 
                Correct_ans = True
            else: Correct_ans= False
                
            if trans and i>2 :
                
                translation = translator.translate(choices[j].text, src='en', dest= lang) 
                Answer[translation.text] = { 'Number of question': i+1, 'Correct answer' : Correct_ans} 
                
            else:
                Answer[choices[j].text] = { 'Number of question': i+1, 'Correct answer' : Correct_ans} 
        
        Answers_Data_base.append(Answer)
        Answer = {}
        
    return(Answers_Data_base)


def Questions_data_translate(trans, lang):
    
    question_text = []
    question_number = []
    for que in questions:
        
        if trans: 
            translation = translator.translate(que.find_all("span")[1].text, src='en', dest= lang)
            question_text.append(translation.text)
        else: 
            question_text.append(que.find_all("span")[1].text)
        
        question_number.append(que.find_all("span")[0].text)
        
    return(question_text,question_number )

  # Call the functions and store de Data 
a, b = Questions_data_translate(True, 'es')
c= Answers_data_translate(True, 'es')


#Print the Assessment

for i in range(0, len(a)):
    print(b[i]+ a[i]+ str(c[i]))
