from datetime import datetime

INITIAL_SEMESTERS = [
    ('1st', '1st'),
    ('3rd', '3rd'),
    ('4th', '4th'),
]

BOARDS = [
    ('barisal', 'Barisal'), 
    ('chittagong', 'Chittagong'), 
    ('comilla', 'Comilla'), 
    ('dhaka', 'Dhaka'), 
    ('dinajpur', 'Dinajpur'), 
    ('jessore', 'Jessore'), 
    ('mymensingh', 'Mymensingh'), 
    ('rajshahi', 'Rajshahi'), 
    ('sylhet', 'Sylhet'), 
    ('madrasah', 'Madrasah'), 
    ('tec', 'Technical'), 
    ('dibs', 'DIBS(Dhaka)')
]

SSC_YEARS = []
for y in range(2000, (datetime.now().year+1)):
    SSC_YEARS.append((y, y))

    