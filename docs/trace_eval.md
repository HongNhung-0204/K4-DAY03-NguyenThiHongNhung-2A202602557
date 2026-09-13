# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyen Thi Hong Nhung<br>
> **Mã Sinh Viên / Mã Học viên:** 2A202602557<br>
> **Chủ đề Lựa chọn:** Gợi ý 1.2 — Trợ lý Quản lý Thư viện & Tài liệu (tra cứu vị trí sách, tình trạng mượn/trả và gia hạn tài liệu)

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Người dùng thường hỏi theo chuỗi: nhận diện mã/tựa sách → tra vị trí kệ → kiểm tra đang sẵn sàng hay đang được mượn → nếu hết hạn/sắp đến hạn thì đề xuất gia hạn. Chatbot FAQ không đủ vì phải nối nhiều bước suy luận, không phải trả lời một phát từ kiến thức tĩnh. |
| **2. Tool Interaction** | 5 / 5 | Vị trí kệ, trạng thái mượn/trả và hạn trả là dữ liệu thời gian thực trong catalog thư viện. Agent bắt buộc gọi MCP Server (1 tool tra cứu + 1 tool hành động gia hạn). Không được bịa số kệ hay hạn trả. Chatbot cấp 2 không truy cập được CSDL nên không giải được bài toán. |
| **3. Dynamic Decision** | 5 / 5 | Bước sau phụ thuộc Observation: sách `AVAILABLE` thì trả vị trí kệ; `BORROWED` thì báo hạn trả và gợi ý đặt giữ/gia hạn; `NOT_FOUND` thì hỏi lại mã ISBN/tựa; gia hạn thất bại (quá hạn, hết lượt) thì đổi hướng xử lý. Cùng một câu hỏi có thể ra Action khác nhau tùy dữ liệu tool. |
| **4. Long Horizon Goal** | 4 / 5 | Mục tiêu xuyên suốt là giúp người dùng lấy đúng tài liệu (tìm được sách + hoàn tất mượn/gia hạn), không phải trả lời lẻ từng câu. Agent phải giữ ngữ cảnh mã sách, tình trạng hiện tại và kết quả gia hạn qua Thought → Action → Observation cho đến Final Answer. Chưa phải tác tử tự lập kế hoạch nhiều ngày nên không chấm 5. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Tổng > 12/20: bài toán phù hợp triển khai ReAct Agent + MCP. Chatbot baseline chỉ trả lời quy định thư viện chung; phần tra cứu vị trí/tình trạng và gia hạn phải đi qua Agent.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG

> ⚠️ **Trạng thái hiện tại:** Logic đã chạy đủ 5/5 test case bằng `MockOfflineProvider` để kiểm tra offline. Cần thay giá trị mẫu trong `.env` bằng API key thật và chạy lại `python src/app.py --all` trước khi nộp chính thức.

Dưới đây là đoạn trích từ file `docs/trace_waterfall.json` sau lần chạy kiểm tra offline:

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "thought": "Người dùng muốn tra cứu vị trí và tình trạng sách. Gọi library_query.",
    "query": "Kiểm tra tình trạng cuốn BK2026001 giúp tôi. Nếu sách đang được mượn và còn lượt gia hạn thì hãy gia hạn thêm 7 ngày cho độc giả RD2026001.",
    "tool_name": "library_query",
    "arguments": {
      "book_id": "BK2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "book_id": "BK2026001",
      "data": {
        "shelf_location": "Kệ A3 - Tầng 2 - Mã kệ AI-204",
        "status": "BORROWED",
        "renewals_left": 1
      }
    },
    "latency_ms": 0.0
  },
  {
    "step": 2,
    "action_type": "TOOL_EXECUTION",
    "thought": "Sách đang được mượn và còn lượt gia hạn. Gọi renew_loan.",
    "tool_name": "renew_loan",
    "arguments": {
      "book_id": "BK2026001",
      "reader_id": "RD2026001",
      "extra_days": 7
    },
    "observation": {
      "status": "SUCCESS",
      "new_due_date": "27/09/2026",
      "renewals_left": 0
    },
    "latency_ms": 0.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases (offline smoke run).
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt (TC02: 1, TC03: 1, TC04: 2, TC05: 1).
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
