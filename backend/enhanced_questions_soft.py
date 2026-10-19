"""Bản làm mềm cho 11 câu hỏi nâng cao (kho hàng, nhà ở kết hợp kinh doanh, nhà hàng/khách sạn, sản xuất).

Thay cho NEW_QUESTIONS_DATA cũ trong add_enhanced_questions.py. Thứ tự các câu giữ nguyên để
soften_legacy_questions.py ghép được với câu cũ trong CSDL đang chạy.
Không còn trích dẫn điều luật dưới câu hỏi; phần khuyến nghị (rec) vẫn giữ căn cứ tham khảo.
"""


def _o(key, text, score, risk, rec=None, legal=None):
    d = {"key": key, "text": text, "score": score, "risk": risk}
    if rec:
        d["rec"] = rec
    if legal:
        d["legal"] = legal
    return d


NEW_QUESTIONS_DATA = [
    # --- B: KHO HÀNG ---
    {
        "category_id": 10, "facility_type": "B",
        "question_text": "Khoảng cách từ hàng hóa trong kho tới trần, đầu phun chữa cháy tự động và đèn chiếu sáng hiện như thế nào?",
        "help_text": "Gợi ý: để khoảng trống khoảng nửa mét giúp hơi nóng thoát và chữa cháy hiệu quả hơn.",
        "reference": None,
        "options": [
            _o("A", "Hàng xếp cách đầu phun và đèn trên nửa mét, có vạch sơn giới hạn rõ ràng", 0, "safe"),
            _o("B", "Phần lớn cách trên nửa mét, đôi lúc có kiện hàng cao gần sát đèn", 1, "low"),
            _o("C", "Hàng xếp khá cao sát trần, che một phần đầu phun chữa cháy", 2, "high",
               "Hạ độ cao xếp hàng, chừa khoảng thông thoáng khoảng 0,5 m tới trần và đầu phun; kẻ vạch giới hạn khu vực xếp hàng.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
            _o("D", "Hàng dễ cháy đang chạm sát chao đèn hoặc bóng đèn tỏa nhiệt do kho đang chật", 3, "critical",
               "Nên xử lý sớm: dời hàng khỏi thiết bị chiếu sáng, thay đèn bằng loại LED có chụp bảo vệ.", "Điều 17 và 40 Nghị định 144/2021/NĐ-CP"),
        ],
    },
    {
        "category_id": 10, "facility_type": "B",
        "question_text": "Sau giờ làm việc, kho thường ngắt điện và kiểm tra các thiết bị điện như thế nào?",
        "help_text": "Gợi ý: chỉ giữ lại mạch chiếu sáng bảo vệ và camera khi kho không có người.",
        "reference": None,
        "options": [
            _o("A", "Ngắt điện phụ tải từng khu, chỉ giữ mạch chiếu sáng bảo vệ riêng", 0, "safe"),
            _o("B", "Có ngắt điện nhưng đôi khi sót quạt thông gió hoặc thiết bị phụ trợ", 1, "low"),
            _o("C", "Dùng chung một nguồn điện cho chiếu sáng và phụ tải, thường không ngắt khi đóng cửa kho", 2, "high",
               "Tách riêng mạch chiếu sáng bảo vệ và mạch phụ tải; lắp aptomat tổng ở ngoài kho để ngắt nhanh.", "QCVN 25:2025/BCT"),
            _o("D", "Có lúc sạc xe nâng hoặc dùng thiết bị điện qua đêm ngay trong kho khi không có người", 3, "critical",
               "Nên bố trí khu sạc riêng, tách khỏi kho, có thiết bị tự ngắt; tránh sạc qua đêm trong kho.", "Điều 17 Nghị định 144/2021/NĐ-CP"),
        ],
    },
    {
        "category_id": 10, "facility_type": "B",
        "question_text": "Lối đi giữa các khối hàng, kệ hàng trong kho hiện thông thoáng ở mức nào?",
        "help_text": "Gợi ý: lối đi chính rộng khoảng 1,5 m và lối giữa kệ khoảng 0,8 m giúp ra vào nhanh.",
        "reference": None,
        "options": [
            _o("A", "Lối đi chính từ 1,5 m, giữa các kệ từ 0,8 m, thông thoáng", 0, "safe"),
            _o("B", "Lối đi đủ rộng nhưng đôi khi có thùng carton, pallet rỗng để tạm", 1, "low"),
            _o("C", "Hàng lấn một phần lối đi, có chỗ dưới 0,8 m, khó tiếp cận bình chữa cháy", 2, "high",
               "Sắp xếp lại kho, giải phóng lối đi, giữ lối chính thông suốt khoảng 1,5 m.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
            _o("D", "Mặt bằng chật nên hàng che gần kín lối ra và cửa phụ của kho", 3, "critical",
               "Nên xử lý sớm: giải phóng lối ra và cửa phụ, không để hàng che các lối này.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
        ],
    },

    # --- C: NHÀ Ở KẾT HỢP KINH DOANH ---
    {
        "category_id": 11, "facility_type": "C",
        "question_text": "Khu để xe máy, xe điện ở tầng 1 (hoặc tầng bán hầm) được ngăn cách với cầu thang bộ ở mức nào?",
        "help_text": "Gợi ý: có vách và cửa ngăn giúp khói không theo cầu thang lan lên các tầng trên.",
        "reference": None,
        "options": [
            _o("A", "Có vách và cửa ngăn riêng giữa khu để xe và cầu thang bộ", 0, "safe"),
            _o("B", "Có vách và cửa ngăn nhưng cửa thường để hé hoặc chưa có tay co tự đóng", 1, "low"),
            _o("C", "Cầu thang bộ thông thẳng xuống khu để xe, chưa có cửa ngăn khói", 2, "high",
               "Làm vách ngăn và cửa ngăn khói tự đóng giữa khu để xe và cầu thang bộ.", "Nghị định 105/2025/NĐ-CP"),
            _o("D", "Khu để xe khá chật sát cửa ra vào, cầu thang thông tầng, nếu có khói sẽ khó thoát", 3, "critical",
               "Nên xử lý sớm: giảm số xe, chừa lối đi ra cửa chính, làm vách ngăn khói cho cầu thang.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
        ],
    },
    {
        "category_id": 11, "facility_type": "C",
        "question_text": "Việc sạc xe máy điện, xe đạp điện tại nhà hoặc nhà trọ hiện được bố trí thế nào?",
        "help_text": "Gợi ý: sạc ở khu riêng, có thiết bị tự ngắt và không sạc khi cả nhà đi ngủ giúp giảm nguy cơ.",
        "reference": None,
        "options": [
            _o("A", "Có khu sạc riêng, aptomat riêng, hẹn giờ tự ngắt, có người trông", 0, "safe"),
            _o("B", "Có khu sạc riêng nhưng dùng ổ cắm thông thường, chưa có tự ngắt", 1, "low"),
            _o("C", "Sạc qua đêm khá gần vật dễ cháy như rèm, mút xốp, giấy carton", 2, "high",
               "Dùng ổ cắm hẹn giờ tự ngắt, đặt xe sạc cách vật dễ cháy ít nhất 1 m.", "QCVN 25:2025/BCT"),
            _o("D", "Nhiều xe sạc chung ổ, dây nối nhiều chỗ, phích cắm từng có hiện tượng nóng", 3, "critical",
               "Nên xử lý sớm: bỏ dây nối chắp, kéo đường điện riêng có aptomat chống giật cho khu sạc.", "Điều 17 Nghị định 144/2021/NĐ-CP"),
        ],
    },
    {
        "category_id": 11, "facility_type": "C",
        "question_text": "Ngoài lối chính, nhà có lối ra thứ hai (ban công, lô gia, tầng mái) sẵn sàng sử dụng khi cần không?",
        "help_text": "Gợi ý: một ô cửa mở được trên khung bảo vệ giúp cả nhà ra ngoài nhanh khi cần.",
        "reference": None,
        "options": [
            _o("A", "Có ô cửa thoát nạn kích thước vừa người, chìa để chỗ dễ thấy hoặc có thang phụ", 0, "safe"),
            _o("B", "Có ô cửa nhưng khóa đã cũ hoặc chìa cất chỗ hơi khó tìm", 1, "low"),
            _o("C", "Ban công, lô gia đã được bảo vệ kín bằng khung sắt, chưa có ô cửa mở", 2, "high",
               "Mở thêm ô cửa thoát nạn khoảng 0,6 x 0,8 m trên khung sắt; để sẵn búa hoặc thang dây.", "Chỉ thị 01/CT-TTg"),
            _o("D", "Chưa có lối ra thứ hai, khung bảo vệ kín và khu vực ban công đang chứa nhiều đồ", 3, "critical",
               "Nên xử lý sớm: mở lối thoát trên khung sắt, dọn đồ khu vực ban công, chuẩn bị thang dây.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
        ],
    },

    # --- D: NHÀ HÀNG, KHÁCH SẠN, CHỢ, TTTM (karaoke, quán bar) ---
    {
        "category_id": 12, "facility_type": "D",
        "question_text": "Vật liệu ốp cách âm, trang trí trong phòng hát, quầy bar thuộc loại nào?",
        "help_text": "Gợi ý: vật liệu khó bắt lửa, có chứng nhận giúp lửa lan chậm và ít khói độc hơn.",
        "reference": None,
        "options": [
            _o("A", "Vật liệu không cháy hoặc khó cháy (bông khoáng, thạch cao chống cháy, tấm panel có chứng nhận)", 0, "safe"),
            _o("B", "Chủ yếu khó cháy, một số mảng trang trí bằng da, mút, gỗ công nghiệp chưa rõ nguồn gốc", 1, "low"),
            _o("C", "Một phần dùng mút xốp, xốp tổ ong để cách âm", 2, "high",
               "Thay dần lớp mút xốp bằng vật liệu cách âm khó cháy có chứng nhận.", "Thông tư 147/2020/TT-BCA"),
            _o("D", "Phần lớn vách và trần ốp mút xốp, dây điện đi sát lớp mút", 3, "critical",
               "Nên xử lý sớm: thay vật liệu mút xốp, đưa dây điện vào ống kim loại tách khỏi vật liệu dễ cháy.", "Điều 30 và 44 Nghị định 144/2021/NĐ-CP"),
        ],
    },
    {
        "category_id": 12, "facility_type": "D",
        "question_text": "Khi có báo cháy, dàn âm thanh, ánh sáng được xử lý thế nào (tự ngắt hay làm thủ công)?",
        "help_text": "Gợi ý: khi chuông báo cháy kêu, tắt nhạc và bật đèn sáng giúp mọi người nghe và nhìn rõ lối ra.",
        "reference": None,
        "options": [
            _o("A", "Có tủ liên động tự ngắt âm thanh, màn hình và bật đèn sáng khi có báo cháy", 0, "safe"),
            _o("B", "Có công tắc tắt âm thanh tập trung ở quầy lễ tân, thao tác bằng tay", 1, "low"),
            _o("C", "Chưa có ngắt âm thanh tự động, tiếng nhạc trong phòng hát có thể lấn át tiếng chuông", 2, "high",
               "Lắp rơ-le liên động giữa báo cháy tự động và nguồn điện dàn âm thanh.", "QCVN 10:2025/BCA"),
            _o("D", "Dàn âm thanh công suất lớn đấu nối chung, dây nguồn đi sát vách mút xốp, chưa luồn ống bảo vệ", 3, "critical",
               "Nên xử lý sớm: tách nguồn dàn âm thanh, lắp tủ điện bảo vệ và liên động ngắt khi có báo cháy.", "Điều 17 và 44 Nghị định 144/2021/NĐ-CP"),
        ],
    },
    {
        "category_id": 12, "facility_type": "D",
        "question_text": "Cửa ra của phòng dịch vụ và hành lang thoát ra ngoài hiện mở theo hướng nào, có biển chỉ dẫn sáng không?",
        "help_text": "Gợi ý: cửa mở ra phía lối thoát và biển EXIT luôn sáng giúp mọi người ra nhanh hơn.",
        "reference": None,
        "options": [
            _o("A", "Cửa mở theo chiều ra ngoài, biển EXIT và đèn sự cố sáng, hành lang thông thoáng", 0, "safe"),
            _o("B", "Cửa mở đúng chiều, một vài đèn EXIT hơi mờ hoặc pin dự phòng đã yếu", 1, "low"),
            _o("C", "Cửa mở vào trong, hành lang có để thùng bia, xe đẩy, đồ phục vụ", 2, "high",
               "Đổi bản lề để cửa mở ra phía lối thoát, dọn vật dụng trên hành lang.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
            _o("D", "Có cửa thường khóa chốt từ ngoài, hành lang tối, chưa có đèn sự cố", 3, "critical",
               "Nên xử lý sớm: bảo đảm cửa mở được từ bên trong, lắp đèn EXIT tự nạp điện.", "Điều 40 và 44 Nghị định 144/2021/NĐ-CP"),
        ],
    },

    # --- A: SẢN XUẤT CÔNG NGHIỆP ---
    {
        "category_id": 9, "facility_type": "A",
        "question_text": "Sau ca làm việc, việc ngắt điện các dây chuyền sản xuất và bàn giao ca được thực hiện thế nào?",
        "help_text": "Gợi ý: có bảng kiểm tra cuối ca và người phụ trách từng phân xưởng giúp không sót thiết bị.",
        "reference": None,
        "options": [
            _o("A", "Có bảng kiểm tra cuối ca, phân công người ngắt từng phân xưởng, chỉ để lại camera và đèn bảo vệ", 0, "safe"),
            _o("B", "Có người ngắt điện, chưa có sổ bàn giao, đôi khi sót quạt hoặc máy tính văn phòng", 1, "low"),
            _o("C", "Phần lớn máy biến áp, tủ phân phối và máy công cụ vẫn có điện qua đêm", 2, "high",
               "Đặt quy trình ngắt điện phụ tải sau ca; lắp aptomat phân vùng để cô lập từng khu.", "Nghị định 105/2025/NĐ-CP"),
            _o("D", "Máy hàn, máy may, lò sấy vẫn hoạt động qua đêm khi không có người trông", 3, "critical",
               "Nên xử lý sớm: không để thiết bị phát nhiệt công suất lớn chạy qua đêm không người trông.", "Điều 17 Nghị định 144/2021/NĐ-CP"),
        ],
    },
    {
        "category_id": 9, "facility_type": "A",
        "question_text": "Đường đi quanh nhà xưởng và khoảng cách giữa các xưởng liền kề hiện thuận lợi cho xe chữa cháy ở mức nào?",
        "help_text": "Gợi ý: đường rộng khoảng 3,5 m và cao thông thoáng khoảng 4,5 m giúp xe lớn tiếp cận.",
        "reference": None,
        "options": [
            _o("A", "Đường nội bộ quanh xưởng từ 3,5 m, cao thông thoáng 4,5 m, xe vào được cả 4 phía", 0, "safe"),
            _o("B", "Đường rộng đủ, đôi lúc xe tải bốc dỡ hàng đỗ tạm chắn một đoạn", 1, "low"),
            _o("C", "Khoảng giữa các xưởng có thêm mái tôn, lán tạm, kho phế liệu, xe lớn khó vào", 2, "high",
               "Dỡ phần mái tôn, lán tạm lấn khoảng lùi; dọn vật chắn đường xe chữa cháy tiếp cận.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
            _o("D", "Các xưởng xây khá sát nhau, lối tiếp cận chính hẹp hoặc bị hàng hóa chiếm", 3, "critical",
               "Nên xử lý sớm: mở khoảng hở tối thiểu 4 m giữa các khu, bố trí chỗ đỗ cho xe chữa cháy.", "Điều 40 Nghị định 144/2021/NĐ-CP"),
        ],
    },
]
