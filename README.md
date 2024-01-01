<<<<<<< HEAD
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
    - Khi chưa đăng nhập: chỉ hiện slide show + footer không cho sử dụng tính năng nào nữa **ok**
    - Đăng kí/Đăng nhập: **(ok đã check)**
        - Đăng nhập thành công: **ok** (đã check đăng nhập sai psw, đăng nhập với tk chưa có)
        - Đăng nhập thất bại: (alert) **ok**
        - Đăng kí: **ok**
          - Các trường hợp đã check: đăng nhập với tk đã tạo; psw khác repsw;
        - Hiệu ứng: Nhập psw >= 8 mới bấm đc (login + register)
    - Hiển thị top cửa hàng theo sao: **ok**
    - Hiển thị product mới theo thời gian: `sắp oke`
    - Tìm kiếm sản phẩm/dịch vụ: **ok**
        - Hiển thị mặc định: -> `Sản phẩm` sắp xếp theo like
        - Tìm kiếm nhanh ở header -> trả ra `sản phẩm` theo từ khóa tìm kiếm (sắp xếp theo thời gian)
        - Tìm kiếm chuẩn: (phân loại, từ khóa, khu vực, thời gian)
            - Theo tag: Tìm kiếm `sản phẩm` theo tag đã gán (hoặc chứa từ khóa của tag)
            - Theo đầy đủ: Tìm kiếm `cửa hàng` (sắp xếp theo vote), tìm kiếm `sản phẩm` (sắp xếp theo mới nhất)
            - Tìm kiếm theo từng loại khu vực: city, district, ward
- posts: Có 2 trang: posts (Hiển thị các bài viết), restaurant(Đề xuất các cửa hàng)
    - posts:
      - Hiển thị các bài viết theo thời gian
      - like + comment **ok**
      - Show các comment, xóa comment (của mình) **ok**
      - Link trực tiếp tới trang cá nhân **ok**
      - Tìm kiềm bài viết (đang làm)
    - restaurant:
      - Hiện giao diện **ok**
      - (Đang làm)
- Profile:
    - Hiển thị bài viết/ sản phẩm
    - Vote
- settings:
     - Chỉnh sửa thông tin
     - Tạo sản phẩm
     - Tạo bài viết
     - Hiển thị Bill
=======
Setting :

    -General (done)
    -Bill (done)
    -Product(done- có thể chỉnh lại chút ui)
    -Statistics(có thống kê về doanh số bán được theo tháng trong năm, đang làm thêm về sản phẩm)
    -Post (Chỉnh lại giao diện thêm và chỉnh bài viết cho giống giao diện khi mà bài viết được hiện thị)
Chat : 

    -UI : done
    -chức năng : done
    -chưa tích hợp vào shop
    
>>>>>>> ntThanh
