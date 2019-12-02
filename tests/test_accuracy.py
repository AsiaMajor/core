import pytest
import os
from modules import preprocess, analyze


def test_analyze_prediction_accuracy():
    accuracy = 0
    loop = 0
    for file in os.listdir('./tests/test_csv'):
        loop += 1
        control_analyze = analyze.Controller('./tests/test_csv/'+file).get_result()

        # #CHECK TOP PREDICTED SHEET
        if str(file).split('_')[0] == str(control_analyze['predicted']).split('_')[0]:
            accuracy += 1

    print("\nTop predicted sheet accuracy: ", accuracy/loop*100, '%')
    assert accuracy/loop*100 > 50

def test_analyze_bucket_accuracy():
    accuracy = 0
    loop = 0
    for file in os.listdir('./tests/test_csv'):
        loop += 1
        control_analyze = analyze.Controller('./tests/test_csv/'+file).get_result()
        
        # CHECK TOP FIVE SHEETS
        for item in control_analyze['sheets_in_bucket']:
            if str(file).split('_')[0] == item['name'].split('_')[0]:
                accuracy += 1
                break

    print("\nTop 3 sheets accuracy: ", accuracy/loop*100, '%')
    assert accuracy/loop*100 > 50


def test_analyze_top3_accuracy():
    accuracy = 0
    loop = 0
    for file in os.listdir('./tests/test_csv'):
        loop += 1
        control_analyze = analyze.Controller('./tests/test_csv/'+file).get_result()
        
        # CHECK TOP FIVE SHEETS
        for item in control_analyze['top_three']:
            if str(file).split('_')[0] == item['name'].split('_')[0]:
                accuracy += 1
                break

    print("\nTop 3 sheets accuracy: ", accuracy/loop*100, '%')
    assert accuracy/loop*100 > 50

def test_analyze_top5_accuracy():
    accuracy = 0
    loop = 0
    for file in os.listdir('./tests/test_csv'):
        loop += 1
        control_analyze = analyze.Controller('./tests/test_csv/'+file).get_result()
        
        # CHECK TOP FIVE SHEETS
        for item in control_analyze['top_five']:
            if str(file).split('_')[0] == item['name'].split('_')[0]:
                accuracy += 1
                break

    print("\nTop 5 sheets accuracy: ", accuracy/loop*100, '%')
    assert accuracy/loop*100 > 50
