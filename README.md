##Bài toán ##
Bài toán Knapsack: cho một chiếc túi có khả năng chứa khối lượng tối đa . Có vật có khối lượng lần lượt là và giá trị tương ứng là . Tìm tập con có giá trị nhất mà chiếc túi có khả năng mang được

Chọn tham số như sau : 

- Kích thước quần thể : 10

- Xác suất lai : 0.4 

- Xác suất đột biến : 0.1

Hàm thích nghi: tổng giá trị các vật được chọn trong túi. Nếu tổng các vật được chọn vượt quá khối lượng tối đa thì chọn bit 1 đầu tiên đảo thành bit 0

**Ngôn ngữ lập trình sử dụng python (2.7)**

##Thực hiện chương trình##

1.Đầu tiên thực hiện đọc file : trả về list item . Khai báo các tham số cần thiết  

2.Tạo quần thể bằng cách random NST với số lượng là pop_size . Mỗi nhiếm sắc thể là chuỗi bit 0 1 với chiều dài là số lượng item

3.Gọi hàm trả về độ thích nghi là khối lượng của NST, khởi tạo những giá trị để lưu NST cho fitness lớn nhất :

- max-fitness : fitness lớn nhất nhất

- res-weight : trọng lượng tương ứng với max-fitness 
 
- best-sol : NST có fitness lớn nhất 

4.Thực hiện vòng lặp 

- Tính fitness và weight 
 NST nào có weight > weight giới hạn thì chọn bit 1 chuyển thành bit 0 ( ở đây em chọn bít 1 đầu tiền )
 Sau đó cập nhật lại fitness và weight
- Kiểm tra xem độ thích nghi tốt nhất của NST trong quần thể 
- Sau đó tạo vòng tròn roulette bằng cách gọi hàm 
	- Random gía trị ngầu nhiên để chọn lọc NST theo vòng tron roulette Thực hiện random với số lần bằng với số NST, mỗi lần chọn ra được NST mới ta thay thế trực tiếp vào để được quần thể mới
	- Random tạo xác suất lai cho từng NST trong quần thể sau đó Ta chọn ra những ví trị NST mà p < pcross. Sau đó ta chọn bất kỳ số chắn để tạo cặp
- Thực hiện lai . Chọn ví trí bất kỳ bằng cách random idx_cr sau đó lai 
- Random tạo xác suất đột biến cho từng bit của tất cả NST trong quần thể . Nếu mà tại bit nào có xác suất < xác suất đột biến pmul thì thực hiện đảo bit

5.Sau đó cập nhật quần thể và thực hiện vòng lặp mới 