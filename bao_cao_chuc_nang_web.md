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

## 3. Đặc điểm kỹ thuật & Thẩm mỹ
*   **Giao diện:** Thiết kế hiện đại với màu xanh chủ đạo (Brand Blue), sử dụng Card Layout giúp thông tin rõ ràng.
*   **Trải nghiệm người dùng:** Tự động tải lại trang khi đổi ngôn ngữ, thông báo rõ ràng khi thao tác.
*   **Dữ liệu:** Lưu trữ nội bộ dạng CSV, dễ dàng quản lý và trích xuất.

---
*Báo cáo được khởi tạo vào ngày 01/05/2026*
