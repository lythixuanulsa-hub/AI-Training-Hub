# 📝 Báo cáo Chức năng Hệ thống Quản lý Đào tạo AI 2026

## 1. Tổng quan dự án
*   **Tên hệ thống:** TPM _ AI TRAINING HUB
*   **Nền tảng:** Streamlit (Python)
*   **Mục tiêu:** Quản lý lịch trình, đăng ký và tài liệu đào tạo AI cho các bộ phận trong công ty trong năm 2026.
*   **Hỗ trợ ngôn ngữ:** Song ngữ Việt - Hàn (Tiếng Việt & 한국어).

## 2. Các phân hệ chức năng chính

| Chức năng | Nội dung chi tiết |
| :--- | :--- |
| **🏠 Trang chủ & Lịch** | - Hiển thị lịch đào tạo trực quan theo tháng (Tháng 5, 6, 7 năm 2026).<br>- Phân loại ca Sáng (🔵) và ca Chiều (🟠).<br>- Đánh dấu các buổi đã hoàn thành (✅).<br>- Xem nhanh thông tin bộ phận, team và nội dung bài học ngay trên lịch. |
| **📝 Đăng ký Đào tạo** | - Biểu mẫu đăng ký trực tuyến cho các bộ phận (Kỹ thuật, Sản xuất, QC, RD...).<br>- Chọn nội dung buổi học (Lý thuyết, Thực hành cơ bản/nâng cao, Bài tập).<br>- Đăng ký số lượng người tham gia và khung giờ cụ thể. |
| **👨‍🏫 Thông tin Giảng viên** | - Giới thiệu đội ngũ giảng viên AI (Yun kwon, Xuan, Trang, Duy...).<br>- Hiển thị chức danh, team và mô tả kinh nghiệm bằng cả hai ngôn ngữ.<br>- Có ảnh đại diện chuyên nghiệp cho từng giảng viên. |
| **📚 Kho tài liệu** | - Lưu trữ tài liệu theo danh mục: Lý thuyết, Thực hành, Bài tập bộ phận, Nhật ký đào tạo.<br>- Cho phép học viên xem mô tả và tải tài liệu về máy. |
| **🔐 Quản trị viên (Admin)** | - Bảo mật bằng mật khẩu (`admin123`).<br>- **Thống kê:** Tổng số lượt đăng ký, số bộ phận tham gia, tổng số nhân viên.<br>- **Quản lý đăng ký:** Chỉnh sửa thông tin, cập nhật trạng thái "Đã hoàn thành" hoặc xóa đăng ký.<br>- **Quản lý tài liệu:** Tải lên tài liệu mới, xóa tài liệu cũ.<br>- **Quản lý giảng viên:** Thêm/xóa giảng viên linh hoạt. |

## 3. Công nghệ và Hạ tầng (Updated)
*   **Cơ sở dữ liệu:** Google Sheets API (Dữ liệu được lưu trữ trực tuyến, an toàn, hỗ trợ nhiều người truy cập cùng lúc).
*   **Triển khai (Deployment):** Streamlit Community Cloud (Ứng dụng chạy 24/7 trên máy chủ đám mây, không phụ thuộc vào máy tính cá nhân).
*   **Bảo mật:** 
    *   Sử dụng **Google Service Account** để xác thực quyền truy cập dữ liệu.
    *   Quyền Admin được bảo vệ bằng mật khẩu và cơ chế **Session State** (Duy trì trạng thái đăng nhập trong suốt phiên làm việc).

## 4. Lợi ích của hệ thống mới
1.  **Tính sẵn sàng cao:** Người dùng có thể đăng ký mọi lúc bằng điện thoại hoặc máy tính mà không cần Admin phải bật máy chương trình.
2.  **Đồng bộ tức thì:** Dữ liệu đăng ký từ Web sẽ tự động đổ về file Google Sheet của quản lý ngay lập tức.
3.  **Khả năng mở rộng:** Dễ dàng thêm các tính năng thống kê bằng biểu đồ hoặc gửi thông báo tự động trong tương lai.
4.  **Chuyên nghiệp:** Giao diện song ngữ hiện đại, thân thiện, nâng cao hình ảnh của bộ phận TPM.

---
*Báo cáo được cập nhật ngày: 02/05/2026*
