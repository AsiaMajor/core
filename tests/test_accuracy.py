import pytest
import os
from modules import analyze

def test_analyze_accuracy():
    accuracy = 0
    loop = 0
    for file in os.listdir('./tests/test_csv'):
        loop += 1
        control = analyze.Controller('./tests/test_csv/'+file).get_result()
        for item in control['top_five']:
            if str(file).split('_')[0] == item[0].split('_')[0]:
                accuracy += 1
                break
            
    assert accuracy/loop*100 > 50
