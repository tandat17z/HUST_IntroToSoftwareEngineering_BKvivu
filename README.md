# BKvivu
# Hust_AIproject_PathfindingProblem
- [Giới thiệu](#angel-giới-thiệu)
- [Cài đặt](#gear-cài-đặt)
- [Quy trình](#airplane-quy-trình)
- [Cách sử dụng](#anchor-cách-sử-dụng)
- [Tính năng](#anger-tính-năng)
## :angel: Giới thiệu
Đây là một project ...
## :gear: Cài đặt
(Đảm bảo rằng bạn đã thiết lập môi trường để chạy python và git)

**1. Clone dự án từ GitHub:**
  ```bash
  git clone https://github.com/tandat17z/Hust_AIproject_PathfindingProblem.git
  ```
Tới thư mục làm việc của dự án. Ví dụ:
  ```bash
  cd D:\Hust_AIproject_PathfindingProblem
  ```
**2. Cài đặt môi trường :**

Dự án cần sử dụng đến nhiều thư viện như:  `folium`, `shapely`, `geopandas`, `django`, .... cụ thể trong file **requirements.txt**<br>
**HOÀN THÀNH CÀI ĐẶT MÔI TRƯỜNG CHO DỰ ÁN** sau khi thực hiện xong câu lệnh sau.
  ```bash
  pip install -r requirements.txt
  ```

## :airplane: Quy trình

## :anchor: Cách sử dụng:
  - Tới thư mục làm việc **website**
  ```bash
  cd ../website
  ```
  - Khởi chạy máy chủ (được phát triển tích hợp trong `Django`) bằng lệnh dưới đây và ấn vào địa chỉ bên dưới để truy cập web. Giao diện web hiển thị bản đồ khu vực để chúng ta thực hiện các thao tác tiếp theo.
  ```bash
  py manage.py runserver
  ```
## :anger: Tính năng: 
_Đang phát triển_
### Đã hoàn thành
- HOMEPAGE:
    - Đăng kí/Đăng nhập:
        - Đăng nhập thành công: ok
        - Đăng nhập thất bại: (alert) ok
        - Đăng kí: (Đăng kí với mật khẩu ngắn ok - thêm ràng buộc psw)
    - Hiển thị top của hàng theo sao
    - Hiển thị product mới theo thời gian
    - Tìm kiếm sản phẩm/dịch vụ:
        - Hiển thị mặc định: -> `Sản phẩm` sắp xếp theo like
        - Tìm kiếm nhanh ở header -> trả ra `sản phẩm` theo từ khóa tìm kiếm (sắp xếp theo thời gian)
        - Tìm kiếm chuẩn: (phân loại, từ khóa, khu vực, thời gian)
            - Theo tag: Tìm kiếm `sản phẩm` theo tag đã gán (hoặc chứa từ khóa của tag)
            - Theo đầy đủ: Tìm kiếm `cửa hàng` (sắp xếp theo vote), tìm kiếm `sản phẩm` (sắp xếp theo mới nhất)
- posts
- Profile:
    - Hiển thị bài viết/ sản phẩm
    - Vote
- settings:
     - Chỉnh sửa thông tin
     - Tạo sản phẩm
     - Tạo bài viết
     - Hiển thị Bill
