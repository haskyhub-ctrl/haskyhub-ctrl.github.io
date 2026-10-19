"""Bộ câu hỏi đặc thù bổ sung cho 12 loại hình cơ sở (A-L), phần 1: A, B, C, D.

Mỗi loại hình sau khi bổ sung có khoảng 15-20 câu đặc thù (gồm cả câu gốc trong
seed_data_specific.py và add_enhanced_questions.py). Câu hỏi được nạp vào CSDL đang
chạy bởi add_specific_expansion.py (idempotent, so khớp theo nội dung câu hỏi).

Nguyên tắc viết câu hỏi (làm mềm, để người dân yên tâm trả lời trung thực):
- Hỏi về tình trạng, cách bố trí, mức độ quan sát được; không hỏi "có vi phạm không".
- Không dùng các từ gợi cảm giác bị kiểm tra, xử lý: quy định, tiêu chuẩn, giấy phép,
  thẩm duyệt, nghiệm thu, kiểm định, vi phạm, trái phép, bắt buộc, cấm, tự ý...
- Các đáp án mô tả mức độ tăng dần của tình trạng, giọng trung tính, không quy lỗi.
- Không trùng với 8 nhóm câu hỏi chung (điện, nguồn lửa, thoát nạn và trang bị PCCC,
  máy móc, thiên nhiên, tự cháy, phương tiện, bổ sung).

Quy ước 4 đáp án: A = an toàn (0 điểm), B = nguy cơ thấp (1), C = nguy cơ cao (2),
D = nguy cơ rất cao (3).
"""


def q(text, a, b, c, d, ref=None, help=None):
    item = {
        "text": text,
        "options": [
            {"key": "A", "text": a, "score": 0, "risk": "safe"},
            {"key": "B", "text": b, "score": 1, "risk": "low"},
            {"key": "C", "text": c, "score": 2, "risk": "high"},
            {"key": "D", "text": d, "score": 3, "risk": "critical"},
        ],
    }
    if ref:
        item["reference"] = ref
    if help:
        item["help"] = help
    return item


EXTRA = {}

# ---------------------------------------------------------------- A: SẢN XUẤT CÔNG NGHIỆP
EXTRA["A"] = [
    q("Khu để nguyên liệu, bán thành phẩm (nhựa, vải, giấy, gỗ, bao bì) trong xưởng hiện được sắp xếp thế nào so với khu máy chạy và nơi tỏa nhiệt?",
      "Có khu để riêng, cách xa khu máy; chỉ giữ lượng vừa đủ cho ca làm việc",
      "Có khu để riêng nhưng nằm chung không gian với khu sản xuất, vẫn còn khoảng cách thoáng",
      "Nguyên liệu thường được xếp gần lối đi và gần máy do mặt bằng đang chật",
      "Mặt bằng rất hạn chế nên nguyên liệu đang để sát máy, sát tủ điện, che một phần lối đi"),
    q("Nồi hơi, bình khí nén, lò dầu tải nhiệt (nếu có) hiện được theo dõi và bảo dưỡng như thế nào?",
      "Có người phụ trách riêng, có sổ theo dõi và lịch bảo dưỡng đều đặn",
      "Có người phụ trách, bảo dưỡng theo kinh nghiệm, sổ ghi chép chưa đầy đủ",
      "Thiết bị hoạt động ổn định nhưng đã lâu chưa được kiểm tra lại toàn diện",
      "Thiết bị đã dùng nhiều năm, thỉnh thoảng có rò hơi hoặc rò dầu nhỏ, chưa có điều kiện sửa chữa"),
    q("Họng nước, bơm và hệ thống chữa cháy tự động trong xưởng (nếu có) được chạy thử và nắm cách vận hành ở mức nào?",
      "Chạy thử đều đặn, nhiều người trong xưởng biết cách vận hành",
      "Có chạy thử nhưng cách quãng, chỉ một vài người nắm cách vận hành",
      "Đã lâu chưa chạy thử, chưa rõ hệ thống còn hoạt động tốt hay không",
      "Thiết bị đang tạm ngưng hoạt động hoặc chưa ai nắm cách vận hành"),
    q("Khi mở rộng xưởng, thay đổi dây chuyền hoặc đổi công năng một khu vực, cơ sở có rà soát lại các điều kiện an toàn PCCC không?",
      "Luôn rà soát lại và trao đổi trước với cơ quan PCCC trước khi triển khai",
      "Có rà soát nội bộ nhưng chưa thường xuyên làm việc với cơ quan chức năng",
      "Việc thay đổi thường được ưu tiên tiến độ sản xuất, phần PCCC bổ sung sau",
      "Đã có một số hạng mục thay đổi, hiện chưa có điều kiện rà soát lại về PCCC"),
    q("Công nhân mới vào làm hoặc ca làm việc đêm được hướng dẫn về lối ra, vị trí bình chữa cháy và cách báo cháy như thế nào?",
      "Có buổi hướng dẫn bài bản cho công nhân mới; ca đêm luôn có người nắm quy trình báo cháy",
      "Có hướng dẫn nhưng chủ yếu truyền miệng giữa các ca",
      "Việc hướng dẫn tùy thuộc từng tổ trưởng, ca đêm ít người nắm rõ",
      "Chủ yếu dựa vào kinh nghiệm cá nhân, ca đêm thường chỉ vài người và chưa rõ ai chịu trách nhiệm báo cháy"),
]

# ---------------------------------------------------------------- B: KHO HÀNG
EXTRA["B"] = [
    q("Cơ sở nắm rõ ở mức nào về loại hàng đang lưu trong kho, kể cả hàng của khách thuê hoặc hàng gửi tạm?",
      "Có danh mục hàng cập nhật thường xuyên, trao đổi rõ với khách về hàng cần lưu ý",
      "Nắm được loại hàng chính, hàng gửi tạm ít khi ghi chép đầy đủ",
      "Phần lớn do khách tự sắp xếp, chủ kho chỉ nắm khái quát",
      "Hàng ra vào nhiều, chủ kho khó theo dõi, từng gặp hàng lạ không rõ thành phần"),
    q("Bãi hàng ngoài trời hoặc khu chứa pallet gỗ, giấy, phế liệu, hạt nhựa được bố trí thế nào so với nhà kho và công trình lân cận?",
      "Bãi riêng, đống hàng có khoảng cách và có lối cho xe đi vào",
      "Bãi riêng nhưng đống hàng khá cao, xếp gần nhau",
      "Đống hàng nằm sát tường kho hoặc hàng rào, xe lớn khó tiếp cận",
      "Mặt bằng hạn chế nên hàng đang chất cao sát công trình, xe khó vào bên trong"),
    q("Với hàng dễ nóng hoặc ẩm (than, bông, vải vụn, phân bón, giấy, bột cám), cơ sở theo dõi nhiệt độ và độ ẩm thế nào, nhất là mùa nắng nóng?",
      "Có đo nhiệt độ, độ ẩm định kỳ, kê hàng cao ráo, thông gió tốt",
      "Thỉnh thoảng kiểm tra bằng cảm nhận, chưa có ghi chép",
      "Hàng xếp thành đống lớn, ít điều kiện kiểm tra phần bên trong",
      "Từng thấy hàng bên trong nóng hoặc có mùi lạ, hiện chưa tìm được cách xử lý triệt để"),
    q("Trong kho có nguồn nước chữa cháy (bể, họng, vòi) ở vị trí gần và dùng được ngay không?",
      "Có đủ nguồn nước và bơm hoạt động tốt, nhiều người biết vị trí",
      "Có nguồn nước nhưng đặt hơi xa, ít người biết cách sử dụng",
      "Nguồn nước phải lấy từ xa hoặc áp lực yếu, chủ yếu dựa vào bình chữa cháy",
      "Hiện chưa bố trí được nguồn nước tại kho, nếu có sự cố sẽ phải chờ lực lượng chữa cháy đến"),
    q("Khi kho đóng cửa dài ngày (nghỉ lễ, cuối tuần, ca đêm), việc kiểm tra kho và liên lạc khi có sự cố được thực hiện thế nào?",
      "Có người trực hoặc kiểm tra theo giờ cố định, có số liên hệ khẩn cấp dán sẵn",
      "Có bảo vệ trực nhưng chưa có lịch kiểm tra cụ thể",
      "Kho đóng cửa dài ngày, chỉ có camera, chưa có người xử lý ngay nếu có báo động",
      "Kho thường không có người nào ở lại, chủ kho cũng khó liên lạc nhanh khi cần"),
    q("Người ra vào kho (tài xế, người bốc xếp, khách gửi hàng) được nhắc nhở thế nào về cách làm việc an toàn trong kho?",
      "Có bảng hướng dẫn tại cổng và được nhắc nhở mỗi lần vào kho",
      "Có bảng hướng dẫn nhưng ít khi nhắc trực tiếp",
      "Chủ yếu nhắc miệng, mỗi người một cách làm",
      "Người ra vào khá tự do, khó kiểm soát cách làm việc bên trong"),
]

# ---------------------------------------------------------------- C: NHÀ Ở KẾT HỢP KINH DOANH
EXTRA["C"] = [
    q("Cửa cuốn, cửa sắt mặt tiền khi mất điện hoặc khi cần ra nhanh, các thành viên trong nhà thao tác mở như thế nào?",
      "Có tay quay hoặc bình lưu điện, cửa phụ mở từ bên trong, ai trong nhà cũng biết cách",
      "Mở được bằng tay nhưng khá nặng, chủ yếu người lớn biết cách",
      "Cửa cuốn điện, mất điện là khó mở, chìa thường cất ở chỗ riêng",
      "Ban đêm cửa thường đóng kín, lối ra phụ rất hạn chế, chưa nghĩ ra phương án thay thế"),
    q("Gác lửng, gác xép, tầng áp mái trong nhà hiện được sử dụng vào việc gì?",
      "Chủ yếu để đồ nhẹ, gọn gàng, có cửa sổ hoặc lối ra thoáng",
      "Dùng chứa đồ, có người nghỉ tạm thỉnh thoảng, có cửa sổ mở được",
      "Dùng làm chỗ ngủ hoặc kho hàng, lối lên chỉ một thang nhỏ",
      "Gác kín, vừa để hàng vừa có người ngủ, không có cửa sổ hay lối ra thứ hai"),
    q("Lượng hàng, vật tư phục vụ kinh doanh được dự trữ trong nhà (hàng dễ cháy, bao bì, hóa chất, bình gas) hiện ở mức nào?",
      "Dự trữ vừa đủ bán, để khu riêng cách xa chỗ ở và bếp",
      "Dự trữ khá nhiều nhưng để khu riêng, có sắp xếp gọn",
      "Dự trữ nhiều do nhập theo đợt, một phần để gần bếp hoặc chỗ ở",
      "Mặt bằng nhỏ nên hàng dự trữ đang để khắp nhà, kể cả chỗ ngủ và gầm cầu thang"),
    q("Ban đêm, khi cả nhà nghỉ, việc kiểm tra điện, gas, tắt thiết bị kinh doanh trước khi đi ngủ được thực hiện thế nào?",
      "Có thói quen kiểm tra từng khu vực, có người phụ trách, rút điện thiết bị không cần thiết",
      "Thường kiểm tra nhưng đôi lúc quên một vài thiết bị",
      "Việc kiểm tra tùy thuộc ai là người đóng cửa tiệm lúc muộn",
      "Nhiều thiết bị chạy suốt đêm, chưa có ai chịu trách nhiệm kiểm tra"),
]

# ---------------------------------------------------------------- D: NHÀ HÀNG, KHÁCH SẠN, CHỢ, TTTM
EXTRA["D"] = [
    q("Hệ thống báo cháy tự động của cơ sở (nếu có) hiện được bảo trì và kiểm tra ở mức nào?",
      "Có đơn vị bảo trì định kỳ, chuông nghe rõ ở mọi khu vực",
      "Hoạt động bình thường nhưng đôi lúc báo lỗi chưa được xử lý ngay",
      "Một số khu vực nghe chuông không rõ hoặc có đầu báo cần thay",
      "Hệ thống đang tạm ngưng một phần hoặc chưa ai phụ trách theo dõi"),
    q("Khách lưu trú, khách đến ăn uống, mua sắm được hướng dẫn thế nào về lối thoát khi có sự cố?",
      "Phòng nào cũng có sơ đồ rõ ràng, nhân viên chủ động hướng dẫn khi khách vào",
      "Có sơ đồ ở hành lang, trong phòng chưa có",
      "Có sơ đồ nhưng đã cũ, mờ; khách chủ yếu tự tìm đường",
      "Hiện chưa có hướng dẫn rõ ràng cho khách, hành lang ban đêm khá tối"),
    q("Nhân viên (lễ tân, phục vụ, bảo vệ) nắm ở mức nào về việc báo cháy, hỗ trợ khách thoát ra và ngắt điện khi cần?",
      "Mỗi người đều được phân công và đã tập qua tình huống",
      "Đa số nắm được, nhân viên mới chưa được hướng dẫn đầy đủ",
      "Chỉ một vài người biết rõ, các ca khác còn lúng túng",
      "Ca đêm chỉ có một người trực, chưa có hướng dẫn cụ thể cho tình huống khẩn cấp"),
    q("Bình gas và đường dẫn gas phục vụ bếp nấu của cơ sở hiện được bố trí thế nào?",
      "Gas đặt ngoài khu đông người, có van ngắt nhanh, thông gió tốt",
      "Gas đặt trong khu bếp riêng, thông gió ổn, dây dẫn còn mới",
      "Bếp hơi chật, dự trữ nhiều bình trong khu chế biến, dây dẫn đã dùng lâu",
      "Bình gas đặt sát lối ra hoặc gần khu khách, khó thông gió, đôi khi có mùi gas nhẹ"),
    q("Mật độ gian hàng, quầy, bàn ghế và hàng hóa trưng bày ở chợ, trung tâm thương mại, nhà hàng hiện như thế nào?",
      "Bố trí thoáng, lối đi chính rộng, hàng không lấn ra lối đi",
      "Bố trí khá gọn, một số chỗ lối đi hơi hẹp giờ cao điểm",
      "Hàng hóa, bàn ghế thường lấn ra lối đi, xe đẩy khó qua",
      "Mật độ rất dày, lối đi quanh co hẹp, nhiều lối ra bị che bởi hàng hóa"),
    q("Rèm, thảm, trần, vách trang trí trong cơ sở (nhất là phòng khách, phòng hát, khu sự kiện) thuộc loại vật liệu nào?",
      "Vật liệu khó bắt lửa, có giấy tờ nguồn gốc rõ ràng",
      "Đa số vật liệu ổn, một vài mảng trang trí dùng vải, mút, giả da thông thường",
      "Nhiều mảng trang trí bằng mút xốp, vải sợi tổng hợp, giấy dán",
      "Nhiều khu vực trang trí dày đặc bằng vật liệu nhẹ, nằm sát đèn nóng hoặc ổ điện"),
    q("Cửa thoát và cửa phụ (cửa kho, cửa hậu, cửa ra sân thượng) ngoài giờ kinh doanh hoặc ban đêm được quản lý thế nào?",
      "Luôn mở được từ bên trong, có người kiểm tra cuối ngày",
      "Có khóa nhưng chìa treo gần cửa, nhân viên biết vị trí",
      "Chìa do một người giữ, các ca khác khó mở nhanh",
      "Vì lo an ninh nên cửa phụ thường khóa kỹ, chìa không để ở chỗ dễ lấy"),
    q("Hầm hoặc khu gửi xe của tòa nhà, trung tâm thương mại hiện được tổ chức thế nào về thông gió, khoảng cách giữa các xe và nơi xe điện sạc?",
      "Có hệ thống hút khói, lối đi rộng, khu sạc xe điện riêng và có người giám sát",
      "Có thông gió, lối đi vừa đủ, xe điện sạc ở vài vị trí cố định",
      "Xe xếp khá sát, lối đi hẹp, thông gió còn hạn chế",
      "Giờ cao điểm xe chen kín cả lối đi, khói nếu có sẽ khó thoát và dễ lan lên các tầng trên"),
]
