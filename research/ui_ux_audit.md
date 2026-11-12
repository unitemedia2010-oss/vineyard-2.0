# ĐÁNH GIÁ TRẢI NGHIỆM NGƯỜI DÙNG TOÀN DIỆN (UI/UX AUDIT)

## 1. Phương Pháp Luận Kiểm Toán (Audit Methodology)
Kiểm toán được thực hiện dựa trên các tiêu chí:
- Khả năng định hướng (Navigation & Findability)
- Tính minh bạch của thông tin sản phẩm (Product Information Clarity)
- Tối ưu hóa chuyển đổi (Conversion Rate Optimization - CRO)
- Trải nghiệm thị giác và cảm xúc thương hiệu (Visual & Emotional Brand Experience)
- Tuân thủ quy định pháp luật về kinh doanh rượu online tại Việt Nam (Nghị định 24/2020/NĐ-CP)

---

## 2. Kết Quả Kiểm Toán Chi Tiết Từng Khu Vực

### 2.1. Thanh Điều Hướng (Header & Navigation)
- **Hiện trạng (Legacy V1)**:
  - Header chứa logo, thanh tìm kiếm đơn giản, menu cấp 1 trải dài.
  - Các icon trong menu sử dụng ảnh raster tĩnh nhỏ (`/userfiles/images/IconWeb/...`) thay vì vector SVG hiện đại, gây vỡ nét trên màn hình Retina/4K.
  - Mega-menu phân chia theo quốc gia và loại rượu có độ trễ mở (hover delay) chưa mượt.
- **Vấn đề UX**:
  - Thiếu bộ lọc nhanh trực quan (Quick Filter by Price / Country / Occasion) ngay trên header.
  - Giỏ hàng tĩnh, click mở trang giỏ hàng riêng biệt làm đứt gãy luồng duyệt sản phẩm.
- **Giải pháp V2.0**:
  - Chuyển toàn bộ icons sang SVG Crisp Vectors.
  - Xây dựng Slide-Over Mini Cart (drawer bên phải) cho phép xem giỏ hàng và số lượng mà không phải rời khỏi trang đang xem.
  - Tích hợp Command Palette (`Cmd + K` / `Ctrl + K`) để tìm kiếm nhanh theo tên rượu, giống nho hoặc hãng sản xuất.

### 2.2. Trang Danh Mục Sản Phẩm (Collection / Listing Page)
- **Hiện trạng (Legacy V1)**:
  - Hiển thị danh sách sản phẩm dạng lưới 3-4 cột với phân trang số học cổ điển (`?page=1`, `?page=2`).
  - Thiếu bộ lọc đa chiều (Faceted Filtering) theo: Mức giá, Nồng độ cồn, Giống nho, Vùng sản xuất, Niên vụ.
  - Thẻ sản phẩm chỉ có ảnh và tên, thông tin về quốc gia và nồng độ bị ẩn bên trong.
- **Giải pháp V2.0**:
  - Bổ sung thanh lọc thông minh (Faceted Filter Drawer trên Mobile & Sticky Sidebar trên Desktop).
  - Hỗ trợ xem dạng Grid (Lưới 3 cột) hoặc List (Dạng danh sách kèm Tasting Notes tóm tắt).
  - Thêm tính năng Quick View modal để xem nhanh thông số chai vang trong 1 cú click.

### 2.3. Trang Chi Tiết Sản Phẩm (Product Detail Page - PDP)
- **Hiện trạng (Legacy V1)**:
  - Rất đáng khen là website nguồn đã có khối `product-ads-content` hiển thị các icon thông số rượu rất trực quan (Quốc gia, Vùng, Giống nho, Nồng độ, Dung tích, Phân hạng, Nút chai).
  - Tuy nhiên, phần hình ảnh sản phẩm còn nhỏ, chưa có tính năng phóng to kính lúp (Deep Zoom) để người sành vang đọc kỹ chi tiết trên nhãn chai (Label Vintage, Appellation text).
  - Phần mô tả hương vị (Tasting Notes) nằm bên dưới dạng văn bản thô, chưa có biểu đồ trực quan hóa vòm miệng (Flavor Wheel / Palate Profile: Độ đậm Body, Vị chát Tannin, Độ chua Acidity, Độ ngọt Sweetness).
- **Giải pháp V2.0**:
  - Triển khai **Flavor Profile Radar / Sliders** (Body, Tannin, Acidity, Sweetness) trực quan hóa cảm giác nếm thử.
  - Ảnh chai vang tương tác 360 độ hoặc chế độ xem nhãn độ nét cực cao.
  - Khối gợi ý kết hợp món ăn (Food Pairing Carousel) với hình ảnh món ăn thịnh soạn kích thích vị giác.

### 2.4. Trải Nghiệm Thiết Bị Di Động (Mobile Ergonomics)
- **Hiện trạng (Legacy V1)**:
  - Menu hamburger còn khá sơ sài, chữ nhỏ và khoảng cách bấm (touch target) chưa đạt chuẩn tối thiểu 44x44px.
  - Nút gọi hotline hoặc tư vấn Zalo bị che khuất.
- **Giải pháp V2.0**:
  - Thiết kế thanh điều hướng cố định dưới đáy màn hình (Bottom Navigation Bar) gồm: Trang chủ, Danh mục rượu, Tìm kiếm, Giỏ hàng, Tư vấn Sommelier.
  - Sticky "Thêm vào giỏ" / "Liên hệ tư vấn" bám đáy màn hình khi cuộn qua khối sản phẩm chính.

---

## 3. Tuân Thủ Quy Định Pháp Lý & Trải Nghiệm Xác Thực Tuổi (Age Gate)
- **Hiện trạng**: Website có popup xác nhận độ tuổi 18+ ("Bạn có đủ 18 tuổi?").
- **Tối ưu V2.0**:
  - Thiết kế Age Gate mang tính nghi thức sang trọng (Elegant Vintage Vault Gate) thay vì modal thô.
  - Lưu trạng thái xác thực vào cookie/local storage có thời hạn hợp lý để không làm phiền người dùng quen thuộc.
  - Bổ sung thông điệp cảnh báo có trách nhiệm: *"Thưởng thức có trách nhiệm. Không lái xe sau khi sử dụng rượu bia. Sản phẩm không dành cho người dưới 18 tuổi và phụ nữ có thai."*
