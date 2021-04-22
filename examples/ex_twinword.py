from core.english_modules import Twinword
from tools.json_utils import read_json

info_dic = read_json('./data/private_information.json')
model = Twinword(**info_dic['twinword'])

results = model.get('decide')
print(results)