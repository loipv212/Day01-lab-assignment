# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Cả bốn câu trả lời đều xoay quanh cùng một sự thật (Hang Sơn Đoòng) nhưng độ ngẫu nhiên trong cách diễn đạt tăng dần theo temperature: ở 0.0 và 0.5 câu chữ gần như giống hệt nhau và tập trung vào ngày phát hiện, ở 1.0 mô hình bắt đầu thêm chi tiết mới (chứa được tòa nhà 40 tầng, hệ sinh thái riêng), còn ở 1.5 cách dùng từ phá cách hơn ("hùng vĩ", đặt tên hang trong dấu ngoặc kép). Quy luật là: temperature càng cao → output càng đa dạng từ ngữ và có nguy cơ "bịa" thêm chi tiết, temperature càng thấp → output càng ổn định và dễ lặp lại.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ đặt temperature ở khoảng **0.2 – 0.3**. Chatbot hỗ trợ khách hàng cần câu trả lời nhất quán, đúng quy trình, hạn chế tối đa việc "sáng tạo" sai thông tin sản phẩm hoặc chính sách. Mức 0.2–0.3 đủ thấp để giữ output ổn định nhưng vẫn linh hoạt hơn 0.0 (tránh nghe quá máy móc khi gặp các câu hỏi tương tự nhau).

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tổng output: 10.000 × 3 × 350 = **10.500.000 token / ngày = 10.500 K token**.
> - GPT-4o: 10.500 × $0.010 = **$105,00 / ngày** (~$3.150 / tháng)
> - GPT-4o-mini: 10.500 × $0.0006 = **$6,30 / ngày** (~$189 / tháng)
>
> **GPT-4o đắt hơn GPT-4o-mini khoảng 16,7 lần** (tỉ lệ giá output 0.010 / 0.0006).

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> - **GPT-4o xứng đáng:** trợ lý phân tích hợp đồng pháp lý hoặc báo cáo tài chính cho doanh nghiệp — sai một dòng có thể gây thiệt hại hàng nghìn USD, nên trả thêm ~17 lần phí token để có chất lượng suy luận và độ chính xác cao là hoàn toàn hợp lý, đặc biệt khi volume thấp.
> - **GPT-4o-mini tốt hơn:** chatbot phân loại email / gắn nhãn intent / tóm tắt ngắn các bài viết — tác vụ đơn giản, lặp lại với volume rất lớn (hàng triệu request/ngày). Mini đủ chính xác trong khi tiết kiệm 94% chi phí và độ trễ thấp hơn.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các giao diện hội thoại trực tiếp với người dùng — chatbot, copilot lập trình, công cụ viết — nơi câu trả lời có thể dài vài trăm token và độ trễ cảm nhận quyết định trải nghiệm: thấy chữ chạy ra ngay sau ~300ms khiến người dùng cảm thấy hệ thống "đang nghĩ" thay vì treo, đồng thời họ có thể đọc/dừng sớm nếu thấy câu trả lời đi sai hướng. Ngược lại, non-streaming phù hợp hơn cho các pipeline tự động không có người ngồi chờ: gọi LLM trong job batch, trích xuất JSON có schema cố định, function calling, hoặc các API nội bộ mà service phía sau cần response hoàn chỉnh để parse — ở đó streaming chỉ làm code phức tạp thêm mà không mang lại lợi ích UX nào.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định
