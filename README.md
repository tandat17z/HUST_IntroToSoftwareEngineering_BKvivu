# BKvivu - Nền tảng chia sẻ trải nghiệm và quản lý dịch vụ
- [Giới thiệu](#angel-giới-thiệu)
- [Cài đặt](#gear-cài-đặt)
- [Cách sử dụng](#anchor-cách-sử-dụng)
- [Tính năng chính](#anger-tính-năng-chính)
  
## :angel: Giới thiệu
Đây là một project mà teams phát triển đã thực hiện trong quá trình học môn `Intro to software engineering` tại `HUST`. Dự án được triển khai trên web dựa vào framework `django`. Hệ thống sẽ giúp cho người dùng dựa trên 2 vai trò chính (người chia sẻ, người quản lý). Người chia sẻ có thể tìm kiếm, mua và chia sẻ những trải nghiệm dịch vụ của mình thông qua tạo bài viết... .Còn đối với người quản lý, nền tảng sẽ cung cấp tính năng để người dùng quảng bá dịch vụ của mình cũng như kinh doanh, thống kê doanh thu....

## :gear: Cài đặt
(Đảm bảo rằng bạn đã thiết lập môi trường để chạy python và git)

### 1. Clone dự án từ GitHub:
- Tải dự án về thiết bị của bạn:
    ```bash
    git clone https://github.com/tandat17z/HUST_IntroToSoftwareEngineering_BKvivu.git
    ```
- Tới thư mục làm việc của dự án. Ví dụ:
    ```bash
    cd D:\HUST_IntroToSoftwareEngineering_BKvivu
    ```
    
### 2. Cài đặt môi trường :
- Dự án cần tới nhiều thư viện liên quan. Hãy dùng lệnh sau để thiết lập môi trường để dự án có thể hoạt động tốt nhất
    ```bash
    pip install -r requirements.txt
    ```

## :anchor: Cách sử dụng:
  - Đầu tiên, bạn cần kết nối hệ thống với cơ sở dữ liệu đã có sẵn (cập nhật cấu trúc cơ sở dữ liệu):
    ```bash
    py manage.py makemigrations homepage
    ```
    ```bash
    py manage.py makemigrations
    ```
    ```bash
    py manage.py migrate
    ```
  - Khởi chạy máy chủ (được phát triển tích hợp trong `Django`) bằng lệnh dưới đây và ấn vào địa chỉ bên dưới để truy cập web. Đến đây bạn đã có thể trải nghiệm BKvivu
    ```bash
    py manage.py runserver
    ```
## :anger: Tính năng chính: 
### HOMEPAGE:
  - Đăng kí/ Đăng nhập: (bạn cần tạo, nhập mật khẩu >= 8 kí tự)
  - Phần header
  - Hiển thị top dịch vụ theo số sao đã được vote
  - Hiển thị top bài viết có nhiều like nhất
  - Tìm kiếm sản phẩm/dịch vụ:
    - Tìm kiếm nhanh tại header: (Nhập từ khóa bạn muốn tìm kiếm và click search, sẽ được chuyển tới mục tìm kiếm)
    - Tìm kiếm:
      - Theo tag: chọn lọc (phân loại) và sau đó click vào các tag tương ứng.
      - Tìm kiếm và lọc: Nhập từ khóa (có thể thêm các thao tác chọn phân loại, chọn khu vực, thời gian) -> sau đó click search.
    - Kết quả tìm kiếm sẽ được hiển thị bên cạnh, bạn có thể đi tới xem chi tiết hoặc thêm vào giỏ hàng.
### POSTSPAGE: 
  - Bài viết:
    - Hiển thị các bài viết theo thời gian
    - Like và comment
    - Tìm kiếm bài viết
  - restaurant:
    - Hiển thị thông tin cơ bản về nơi cung cấp dịch vụ
### PROFILEPAGE:
  - Hiển thị thông tin cơ bản
  - Hiển thị sản phẩm (đối với cửa hàng)
  - Hiển thị bài viết
  - Đánh giá cửa hàng:
    - Hiển thị số sao đã đánh giá cho cửa hàng
    - Hiển thị số sao của cửa hàng
### SHOPPINGPAGE: 
  - Giỏ hàng:
    - Hiển thị sản phẩm đã thêm vào giỏ hàng theo từng cửa hàng
    - Tích chọn sản phẩm, số lượng và đặt hàng theo từng cửa hàng
  - Đơn hàng đã mua:
    - Hiển thị những đơn hàng đã mua
    - Thanh toán (nếu chưa thực hiện thanh toán)
    - Hủy đơn hàng (nếu cửa hàng chưa xác nhận)
  - Thanh toán đơn hàng:
    - Hiển thị Mã Qr thanh toán và gửi ảnh thanh toán
    - Hiển thị cửa hàng, những sản phẩm và số tiền của đơn hàng này
### SETTINGSPAGE: 
  - Chỉnh sửa thông tin
  - Tạo sản phẩm
  - Tạo bài viết
  - Hiển thị Bill
  - General (done)
  - Bill (done)
  - Product(done- có thể chỉnh lại chút ui)
  - Statistics(có thống kê về doanh số bán được theo tháng trong năm, đang làm thêm về sản phẩm)
  - Post (Chỉnh lại giao diện thêm và chỉnh bài viết cho giống giao diện khi mà bài viết được hiện thị)
### CHAT: 
  - Chỉ có người chia sẻ mới có thể nhắn với người quản lí
  - Khi người dùng nhấn vào phần chat trong cửa hàng thì nó sẽ ra phần chat của người đó và người quản lí, còn ấn vào cái chat nổi nằm phía dưới sẽ hiện ra phần chat mặc định của người chia sẻ
  - Đang phát triển thêm chat có kèm hình ảnh (continue)

## :adult: Lời cảm ơn:
    Cảm ơn bạn đã ghé thăm dự án của chúng tôi. Vì đây là dự án đầu tiên teams nghiên cứu và phát triển nên không thể tránh khỏi những vấn đề. Nếu có bất kì thắc mắc nào, đừng ngần ngại hãy liên hệ với chúng tôi, chúng tôi chắc chắn sẽ trợ giúp bạn. Thanks...
