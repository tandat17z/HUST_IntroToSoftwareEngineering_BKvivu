import json
import chardet

path = 'func/data.json'
with open(path, 'rb') as f:
    result = chardet.detect(f.read())
with open(path, 'r', encoding=result['encoding']) as file:
    # Sử dụng hàm load() để đọc nội dung từ tệp và chuyển thành đối tượng Python
    data = json.load(file)

def getArea(city_id, district_id, ward_id):
    '''
    Trả về tên địa chỉ khi truyền vào id
    Nếu lỗi sẽ trả lại id ban đầu
    '''
    city_ = city_id
    district_ = district_id
    ward_ = ward_id
    try:
        for city in data:
            if city["Id"] == city_id:
                data_city = city
        city_ = data_city["Name"]
        for district in data_city["Districts"]:
            if district["Id"] == district_id:
                data_district = district
        district_ = data_district["Name"]
        for ward in data_district["Wards"]:
            if ward["Id"] == ward_id:
                data_ward = ward
        ward_ = data_ward["Name"]
    except:
        print("getArea bị lỗi ----")
        
    return city_, district_, ward_ 
