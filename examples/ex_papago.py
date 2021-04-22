
from core.english_modules import Papago
from tools.json_utils import read_json

info_dic = read_json('./data/private_information.json')
model = Papago(**info_dic['papago'])

print(model.get('I am going to analyze the database.'))
print(model.get('오늘 영어 숙제를 해야 합니다.'))
print(model.get('determinate'))