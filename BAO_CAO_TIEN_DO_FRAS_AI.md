# BÁO CÁO TIẾN ĐỘ & BÀN GIAO KỸ THUẬT HỆ THỐNG TRỢ LÝ ẢO AI PCCC (FRAS-AI)
**Địa bàn áp dụng:** Công an thành phố Bắc Ninh / Tỉnh Bắc Ninh  
**Thời điểm cập nhật:** 22/10/2026  
**Trạng thái hệ thống:** Đã tối ưu hóa hoàn chỉnh, Server đang chạy tại `http://localhost:8000`

---

## 1. TỔNG QUAN KIẾN TRÚC & NGUYÊN TẮC VẬN HÀNH

Hệ thống Trợ lý ảo AI tư vấn pháp luật và TTHC về PCCC được thiết kế theo mô hình **Hybrid 2-Tier Architecture**:

```
[ Người dùng gửi câu hỏi ]
           │
           ▼
[ BƯỚC KIỂM TRA & BẢO VỆ (Guardrails) ]
    ├─ Kiểm tra độ dài: Câu hỏi dài / tình huống (> 25 từ) ──┐ (Bỏ qua FAQ)
    └─ Kiểm tra thực thể: Tránh match chéo từ khóa          │
           │                                                │
           ▼ (Nếu câu hỏi ngắn < 25 từ)                     │
[ TIER 1: NGÂN HÀNG FAQ CHUẨN (208 FAQs) ]                 │
    ├─ Thuật toán so khớp: Jaccard (>=0.35) + Overlap       │
    ├─ Lọc thực thể loại hình (nhà nghỉ, karaoke, ANTT...)  │
    └─ Đạt chuẩn ──> Phản hồi SIÊU TỐC: 0.02s - 0.05s       │
           │ (Không khớp / Tình huống dài)                  │
           └────────────────────────────────────────────────┘
                                   │
                                   ▼
[ TIER 2: VECTOR / BM25 LOCAL RAG + LLM 9ROUTER ]
    ├─ BM25 Local RAG (utils/local_rag.py): 105 văn bản, 7.422 chunks (Tốc độ: 5ms)
    ├─ Không gọi LLM mở rộng từ khóa thừa thãi (đã bỏ _expand_queries)
    ├─ LLM: 9Router Google Pro (`ag/gemini-3.8-flash-low` / `flash`)
    ├─ Thời gian phản hồi RAG: 12s - 25s (đáp ứng tiêu chuẩn < 30s)
    └─ Cấu trúc bắt buộc 4 phần:
         [>>] Kết luận trực diện
         [## 1.] Căn cứ pháp lý và nguyên tắc chung
         [## 2.] Quy định chi tiết (bảng biểu, thông số)
         [## 3.] Trình tự và các bước thực hiện
         [## 4.] Chế tài xử lý vi phạm và Lưu ý quan trọng
```

---

## 2. KHO TRI THỨC PHÁP LÝ ĐÃ ĐƯỢC TÍCH HỢP & HIỆU LỰC 2026

1. **Khung pháp lý Trung ương năm 2026:**
   - **Nghị quyết số 66.18/2026/NQ-CP (18/5/2026):** Bãi bỏ thủ tục hành chính kiểm tra công tác nghiệm thu về PCCC tại cơ quan Công an và Xây dựng; Chủ đầu tư tự tổ chức nghiệm thu với nhà thầu và tự chịu trách nhiệm pháp lý.
   - **Nghị định số 347/2026/NĐ-CP (08/9/2026):** Sửa đổi, bổ sung Nghị định 105/2025/NĐ-CP; chính thức bãi bỏ việc cấp văn bản chấp thuận kết quả nghiệm thu PCCC; chủ cơ sở khai báo trên Hệ thống CSDL PCCC trước khi vận hành.
   - **Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15.**
   - **Nghị định số 105/2025/NĐ-CP:** Hướng dẫn chi tiết thi hành Luật 55/2024/QH15.
   - **Nghị định số 106/2025/NĐ-CP & Nghị định 69/2026/NĐ-CP:** Quy định xử phạt vi phạm hành chính trong lĩnh vực PCCC và CNCH.
   - **Quy chuẩn & Tiêu chuẩn:** QCVN 06:2022/BXD (kèm Sửa đổi 1:2023), TCVN 3890:2023, QCVN 10:2025/BCA.
   - **An ninh trật tự (ANTT):** Nghị định số 96/2016/NĐ-CP và Nghị định số 56/2023/NĐ-CP đối với các ngành nghề kinh doanh có điều kiện (lưu trú, karaoke...).

2. **Quy định đặc thù địa phương tỉnh Bắc Ninh:**
   - **Quyết định số 29/2025/QĐ-UBND (22/09/2025) của UBND tỉnh Bắc Ninh:**
     + **Khoản 2 Điều 22:** Phân cấp cho **UBND cấp xã** tổ chức kiểm tra về PCCC đối với cơ sở có cấp công trình từ **Cấp III trở xuống** thuộc Phụ lục II Nghị định 105/2025/NĐ-CP.
     + **Khoản 1 Điều 22:** Cơ quan chuyên môn cấp tỉnh (Sở Xây dựng, Sở NN&MT, Sở Công thương) kiểm tra cơ sở từ Cấp II trở lên.
     + **Điều 19:** Kiểm tra công tác nghiệm thu công trình xây dựng (công trình Cấp III vốn tư nhân không thuộc diện cơ quan xây dựng kiểm tra nghiệm thu).
   - Đã nạp toàn văn 42.323 ký tự vào kho seed RAG (`backend/kho_seed/qd29_2025_ubnd.txt`) và lập chỉ mục BM25.

---

## 3. CÁC TÌNH HUỐNG THỰC TẾ ĐÃ ĐƯỢC GIẢI QUYẾT & KIỂM THỬ THÀNH CÔNG

### Ca 1: Nhà nghỉ 5 tầng 1 tum, 300 m2 sàn, 57 phòng ngủ (bà Thủy, Quế Võ, Bắc Ninh)
* **Câu hỏi:** Cơ sở cần đáp ứng điều kiện gì về PCCC? Hồ sơ cấp Giấy chứng nhận ANTT gồm những gì? Có phải thẩm định và nghiệm thu về xây dựng không?
* **Kết quả xử lý chuẩn xác:**
  1. **Về PCCC:** Công trình lưu trú 5 tầng thuộc Phụ lục II NĐ 105/2025 $\rightarrow$ Bắt buộc phải **Thẩm duyệt thiết kế PCCC** tại cơ quan Cảnh sát PCCC; Lắp hệ thống báo cháy tự động 100% phòng ngủ, họng nước vách tường TCVN 3890:2023, 02 lối thoát nạn; Sau khi hoàn thành **tự tổ chức nghiệm thu PCCC** và **khai báo trên CSDL PCCC** (NQ 66.18/2026 & NĐ 347/2026).
  2. **Về Xây dựng:** Công trình Cấp III vốn tư nhân $\rightarrow$ **KHÔNG** thuộc diện cơ quan xây dựng thẩm định thiết kế xây dựng (Điều 82 Luật XD 2020) và **KHÔNG** thuộc diện cơ quan xây dựng kiểm tra nghiệm thu (Điều 24 NĐ 06/2021). Chủ đầu tư chỉ cần có **Giấy phép xây dựng** do UBND thị xã Quế Võ cấp và tự nghiệm thu nội bộ.
  3. **Về ANTT:** Nộp hồ sơ xin cấp Giấy chứng nhận đủ điều kiện về ANTT tại Đội Cảnh sát QLHC về TTXH Công an thị xã Quế Võ (Mẫu 01, ĐKKD, tài liệu nghiệm thu PCCC, Mẫu 02 lý lịch tư pháp, Phương án ANTT Mẫu 03).

### Ca 2: Quán Karaoke 4 tầng, diện tích 85 m2 sàn, 2 phòng hát
* **Câu hỏi:** Thuộc đối tượng quản lý của Phòng Cảnh sát PCCC&CNCH Công an tỉnh hay của UBND xã?
* **Kết luận chuẩn xác:** Thuộc thẩm quyền kiểm tra của **UBND CẤP XÃ** (do Công an xã tham mưu).
* **Căn cứ:** Nhà 4 tầng diện tích sàn 340 m2 là công trình Cấp IV (dưới Cấp III). Căn cứ khoản 2 Điều 22 Quyết định 29/2025/QĐ-UBND tỉnh Bắc Ninh, UBND tỉnh phân cấp trực tiếp cho UBND cấp xã kiểm tra PCCC cơ sở từ Cấp III trở xuống thuộc Phụ lục II NĐ 105/2025. Tuyệt đối không thuộc Phòng Cảnh sát PCCC cấp tỉnh.

### Ca 3: Tranh chấp tài sản ly hôn nhà 6 tầng, ủy quyền PCCC đến 2027
* **Câu hỏi:** Có được làm đơn xin cơ quan Công an kiểm tra và đánh giá điều kiện PCCC&CNCH cho công trình không?
* **Kết luận chuẩn xác:** **KHÔNG**.
* **Căn cứ:**
  - Pháp luật PCCC (Điều 18 NĐ 105/2025) không có thủ tục hành chính kiểm tra theo yêu cầu cá nhân.
  - Công an chỉ kiểm tra định kỳ theo kế hoạch năm hoặc kiểm tra đột xuất khi có vi phạm nghiêm trọng; không can thiệp vào tranh chấp dân sự/hôn nhân nội bộ khi giấy ủy quyền kinh doanh còn hiệu lực.
  - Hướng dẫn công dân: Thuê đơn vị tư vấn dịch vụ PCCC độc lập khảo sát đánh giá kỹ thuật; hoặc làm Đơn tố giác phản ánh vi phạm an toàn PCCC nếu bên nhận ủy quyền có hành vi vi phạm nguy hiểm.

---

## 4. CÁC TỐI ƯU HÓA KỸ THUẬT QUAN TRỌNG ĐÃ THỰC HIỆN

1. **Khắc phục lỗi nhận diện nhầm FAQ (False Positive):**
   - File sửa đổi: `backend/utils/kb_qa.py` và `backend/routers/ai_analysis.py`.
   - Ngăn chặn triệt để tình trạng câu hỏi tình huống dài bị match chéo vào FAQ ngắn 3 dòng do Overlap coefficient.
   - Thêm bộ lọc `CRITICAL_ENTITY_KEYWORDS` kiểm tra thực thể bắt buộc.

2. **Loại bỏ vòng lặp tìm kiếm Internet chậm chạp:**
   - File sửa đổi: `backend/utils/rag_search.py`.
   - Sửa biểu thức chính quy nhận diện số hiệu văn bản; các con số đời thường (số tầng, số phòng, số thửa đất 26, tờ bản đồ 20) không còn bị hiểu nhầm thành số Nghị định.

3. **Tối ưu tốc độ LLM & Tránh Timeout:**
   - Cấu hình ưu tiên `ag/gemini-3.8-flash-low` và `ag/gemini-3.8-flash`.
   - Tối ưu hóa timeout `30.0s`, chỉ thử tối đa 2 model flash nhanh nhất, không cho phép cascade vào các model `-high` gây trễ 45s.
   - RAG pipeline trả về bài viết đầy đủ 6.000 - 9.000 ký tự trong thời gian **12s - 25s**.

4. **Nâng cấp giao diện Chatbot (`frontend/js/chatbot.js`):**
   - Font chữ tối ưu `0.80rem`, khoảng cách dòng chuẩn `1.6`.
   - Tự động sinh badge số thứ tự `[1]`, `[2]`, `[3]`, `[4]` màu đỏ thương hiệu nổi bật trên nền xám xanh, tiêu đề navy đậm.
   - Bảng biểu có viền gọn gàng, tiêu đề trắng trên nền xanh công an, tự co giãn trên thiết bị di động.

5. **Bộ tự động rà soát định kỳ (Weekly FAQ Auditor):**
   - File: `backend/utils/faq_auditor.py`.
   - Tự động chạy nền mỗi 168 giờ (1 tuần) quét toàn bộ 208 câu hỏi trong ngân hàng dữ liệu để phát hiện các căn cứ văn bản bị bãi bỏ hoặc câu hỏi quá 7 ngày chưa được đối soát.

---

## 5. HƯỚNG DẪN CHO CLAUDE TIẾP TỤC TRIỂN KHAI

Nếu phiên làm việc được chuyển tiếp cho Claude, hãy tập trung vào các hạng mục sau:

1. **Kiểm tra trạng thái dịch vụ:**
   - Thư mục dự án: `D:\Antigravity\scratch\fras-ai`
   - Môi trường ảo Python: `D:\Antigravity\scratch\fras-ai\backend\venv`
   - Lệnh khởi động server:
     ```powershell
     cd D:\Antigravity\scratch\fras-ai\backend
     .\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
     ```
2. **Ngân hàng FAQ (`backend/kho_seed/faq_bank_2026.json`):**
   - Khi bổ sung câu hỏi mới, luôn tuân thủ cấu trúc 4 phần (`>>`, `## 1.`, `## 2.`, `## 3.`, `## 4.`).
   - Sau khi chỉnh sửa file JSON, chạy script `scratch/expand_faqs.py` hoặc gọi API `POST /api/ai/faq/seed-200` để đồng bộ vào bảng `kb_questions` trong SQLite `fras.db`.
3. **Quy tắc bất di bất dịch của Trợ lý ảo:**
   - Xưng là "Tôi" hoặc "Trợ lý ảo", gọi người hỏi là "bạn" (tuyệt đối không tự xưng "Chi").
   - Nghiệm thu PCCC: Nhấn mạnh đã bãi bỏ thủ tục cấp văn bản chấp thuận của Công an theo NQ 66.18/2026 và NĐ 347/2026; Chủ đầu tư tự nghiệm thu và khai báo CSDL PCCC.
   - Chứng nhận huấn luyện PCCC: Đã bãi bỏ việc cấp chứng nhận/thẻ thời hạn 5 năm; chuyển sang cơ chế huấn luyện định kỳ 5 năm/lần và bồi dưỡng hằng năm.
   - Thẩm quyền Bắc Ninh: Luôn đối chiếu Quyết định số 29/2025/QĐ-UBND (UBND cấp xã kiểm tra cơ sở cấp III trở xuống).
