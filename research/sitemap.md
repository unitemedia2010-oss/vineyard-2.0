# SƠ ĐỒ CẤU TRÚC WEBSITE & URL INVENTORY (RESEARCH SITEMAP)

## 1. Tổng Quan Kiến Trúc Điều Hướng (Navigation Architecture)
Khảo sát thực tế hệ thống `https://vineyard.vn/` cho thấy website được tổ chức theo cấu trúc phân cấp hình cây (Tree Hierarchy) xoay quanh các phân loại rượu vang theo:
1. **Loại vang theo màu sắc & đặc tính**: Vang đỏ, Vang trắng, Vang hồng, Vang ngọt, Vang tăng độ, Vang cao cấp, Vang nổ (Champagne/Sparkling).
2. **Loại vang theo xuất xứ địa lý**: Vang Pháp (Bordeaux, Burgundy), Vang Ý (Puglia, Tuscany, Veneto), Vang Chile, Vang Úc, Vang Tây Ban Nha.
3. **Đồ uống khác & Phụ kiện**: Beer & RTD, Rượu mạnh (Whisky, Cognac, Brandy, Gin, Vodka), Phụ kiện rượu vang (Tủ rượu, Ly pha lê, Decanter, Đồ khui), Hộp quà tết & doanh nghiệp.
4. **Nội dung chuyên môn**: Kiến thức rượu vang, Tin tức khuyến mãi, Sự kiện hội nghị khách hàng, Thử nếm sản phẩm mới.

---

## 2. Bảng Phân Nhóm URL Thực Tế (URL Taxonomy & Inventory)

| Nhóm Trang (Page Type) | Mẫu Đường Dẫn (URL Pattern) | Mục Đích & Vai Trò | Ví Dụ Cụ Thể |
|---|---|---|---|
| **Trang Chủ** | `/` | Showcase thương hiệu, banner chính, danh mục hot | `https://vineyard.vn/` |
| **Danh Mục (Category)** | `/danh-muc/[slug]` | Hiển thị danh sách sản phẩm theo bộ lọc | `https://vineyard.vn/danh-muc/vang-do`, `https://vineyard.vn/danh-muc/vang-y` |
| **Sản Phẩm (Product)** | `/san-pham/[slug]` | Trang chi tiết chai rượu vang, thông số, giá | `https://vineyard.vn/san-pham/r9-primitivo-icono` |
| **Bài Viết / Sự Kiện** | `/post/[slug]`, `/event/[slug]` | Chia sẻ kiến thức rượu vang, tin khuyến mãi | `https://vineyard.vn/post/kham-pha`, `https://vineyard.vn/event/tat-ca-su-kien` |
| **Trang Thông Tin** | `/page/[slug]`, `/dia-chi-...` | Giới thiệu, chính sách, điều khoản, showroom | `https://vineyard.vn/dia-chi-cua-hang`, `https://vineyard.vn/page/catalogue` |

---

## 3. Cây Phân Cấp Danh Mục Chính (Category Hierarchy Tree)

```mermaid
flowchart TD
    Root[Trang Chủ VINEYARD] --> Vang[1. Rượu Vang]
    Root --> VangNo[2. Rượu Vang Nổ / Champagne]
    Root --> RuouManh[3. Rượu Mạnh & Spirits]
    Root --> PhuKien[4. Phụ Kiện Rượu Vang]
    Root --> HopQua[5. Hộp Quà & Doanh Nghiệp]
    Root --> KienThuc[6. Kiến Thức & Bài Viết]

    Vang --> VangDo[Vang Đỏ (Red Wine)]
    Vang --> VangTrang[Vang Trắng (White Wine)]
    Vang --> VangHong[Vang Hồng (Rosé)]
    Vang --> VangNgot[Vang Ngọt & Tráng Miệng]
    Vang --> VangTangDo[Vang Tăng Độ (Port Wine)]
    Vang --> VangCaoCap[Vang Cao Cấp (Icon & DOCG)]

    VangDo --> QuocGiaY[Vang Ý - Puglia, Tuscany]
    VangDo --> QuocGiaPhap[Vang Pháp - Bordeaux]
    VangDo --> QuocGiaChile[Vang Chile - Central Valley]
    VangDo --> QuocGiaUc[Vang Úc - Barossa Valley]

    PhuKien --> Ly[Ly Pha Lê Uống Rượu Vang]
    PhuKien --> Decanter[Bình Thở Decanter]
    PhuKien --> Khui[Đồ Khui Vang & Phụ Kiện]
    PhuKien --> TuRuou[Tủ Bảo Quản Rượu Vang Chuyên Dụng]
```

---

## 4. Báo Cáo Tuân Thủ Robots.txt & Tính Khả Dụng (Access Policy Audit)
- **Tệp `robots.txt`**: Khảo sát tại `https://vineyard.vn/robots.txt` trả về mã trạng thái `200 OK`.
- **Nội dung quy tắc**: Không có bất kỳ lệnh `Disallow:` nào cấm các bot tìm kiếm hoặc công cụ phân tích truy cập nội dung công khai.
- **Tốc độ truy cập**: Website hỗ trợ HTTP/1.1 trên máy chủ Apache với PHP 7.4. Thời gian phản hồi trung bình dao động từ $150\text{ms}$ đến $350\text{ms}$. Cơ chế crawler áp dụng độ trễ lịch sự $1.5\text{s}$ giữa các yêu cầu liên tiếp đảm bảo hoàn toàn không gây ảnh hưởng đến tải của máy chủ đích.
