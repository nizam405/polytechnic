import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import re
from datetime import datetime
from django.core.exceptions import EmptyResultSet

class EduInfo:
    def __init__(self, year, board, roll, reg, exam='ssc'):
        self.exam = exam
        self.year = year
        self.board = board
        self.roll = roll
        self.reg = reg
        # Make a get request to home page
        self.r_home = requests.get('http://www.educationboardresults.gov.bd/')
        home_html = self.r_home.text
        # Extract data from response
        home_soup = BeautifulSoup(home_html, 'html.parser')
        self.form = home_soup.form

    def calculate(self):
        # bypass calculation challange
        form = self.form
        # print(form.text)
        exp = re.search(r'[^\w][\+\-\*\/]{1}', form.text).group()
        exp = form.text[form.text.index(exp)-2:form.text.index(exp)+5]
        a, b = re.findall(r'[\d]+',exp)
        a, b = int(a), int(b)
        operator = re.findall(r'[^\d\s]+',exp)[0]
        result = None
        if operator == '+':
            result = a + b
        elif operator == '-':
            result = a - b
        elif operator == '*':
            result = a * b
        elif operator == '/':
            result = a / b
        # print(a,operator,b)
        # print(result)
        return result

    def get_data(self):
        form = self.form
        data = {}
        sr = form.find(id='sr')
        data['sr'] = sr.attrs['value']
        et = form.find(id='et')
        data['et'] = et.attrs['value']
        data['exam'] = self.exam
        data['year'] = self.year
        data['board'] = self.board
        data['roll'] = self.roll
        data['reg'] = self.reg
        data['value_s'] = self.calculate()
        btn_submit = form.find(id='button2')
        data['button2'] = btn_submit.attrs['value']
        print(data)
        return data

    def getInfo(self):
        data = self.get_data()
        cookie = self.r_home.headers['Set-Cookie']
        PHPSESSID = cookie[cookie.index('=')+1:cookie.index(';')]
        url = 'http://www.educationboardresults.gov.bd/result.php'
        header = {'Cookie': f'PHPSESSID={PHPSESSID}'}
        try:
            req = requests.post(url, data=data, headers=header)          
            result_html = req.text
            # Extract data from response
            result_soup = BeautifulSoup(result_html, 'html.parser')
            script = result_soup.script
            err_text = ""
            if script is not None:
                err_text = script.string
            if 'index.php?err=' in err_text: 
                raise EmptyResultSet()
            else: 
                sample_tag = result_soup.find('td', text='Roll No')
                parent1_tag = sample_tag.find_parent('tr')
                result_tag = parent1_tag.find_parent('table')
                info = {}
                rows = result_tag.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    col_num = int(len(cols)/2)
                    count = 0
                    for i in range(col_num):
                        if cols[count].text == 'Date of Birth':
                            date = datetime.strptime(cols[count+1].text, "%d-%m-%Y")
                            date = date.strftime("%Y-%m-%d")
                            # print(date)
                            info[cols[count].text] = date
                        else:
                            info[cols[count].text] = cols[count+1].text
                        count += 2
                return info
        except ConnectionError as e:
            print(e)
            exit()
    
    def getSSCInfo(self):
        info = self.getInfo()
        data = {
                # Input ssc info
                'ssc_year'      : self.year,
                'ssc_board'     : self.board,
                'ssc_roll'      : self.roll,
                'ssc_reg'       : self.reg,
                # result of ssc info
                'ssc_gpa'       : info['GPA'],
                'ssc_group'     : info['Group'],
                'name'          : info['Name'],
                'father_name'   : info["Father's Name"],
                'mother_name'   : info["Mother's Name"],
                'date_of_birth' : info['Date of Birth'],
                'verified'      : True,
                }
        return data
            
# nizam = EduInfo('2013','dhaka','440077','1010877712',exam='ssc')
# print(nizam.getInfo())



# def getBoardInfo():
#     # Make a get request to home page
#     r = requests.get('http://www.educationboardresults.gov.bd/')
#     home_html = r.text
#     # Extract data from response
#     home_soup = BeautifulSoup(home_html, 'html.parser')
#     form = home_soup.form
#     board = form.find(id='board')
#     board_options = board.find_all('option')
#     # return board_options
#     boards = []
#     for board in board_options:
#         if board.attrs['value'] != '':
#             boards.append((board.attrs['value'], board.string))
#     return boards
# print(getBoardInfo())
