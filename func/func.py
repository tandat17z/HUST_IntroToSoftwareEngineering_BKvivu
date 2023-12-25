import json
import chardet

path = 'func/data.json'
with open(path, 'rb') as f:
    result = chardet.detect(f.read())
with open(path, 'r', encoding=result['encoding']) as file:
    # Sử dụng hàm load() để đọc nội dung từ tệp và chuyển thành đối tượng Python
    data = json.load(file)

def getArea(city_id, district_id, ward_id):
    for city in data:
        if city["Id"] == city_id:
            data_city = city
    
    for district in data_city["Districts"]:
        if district["Id"] == district_id:
            data_district = district

    for ward in data_district["Wards"]:
        if ward["Id"] == ward_id:
            data_ward = ward
    return data_city["Name"], data_district["Name"], data_ward["Name"]
