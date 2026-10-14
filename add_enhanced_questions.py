import os
import sys

# Ensure backend imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from database import SessionLocal
from models import Question, QuestionOption, QuestionCategory, Recommendation

NEW_QUESTIONS_DATA = [
    # --- NHÓM B: KHO HÀNG (category_id = 10, facility_type = 'B') ---
    {
        "category_id": 10,
        "facility_type": "B",
        "question_text": "Khoảng cách xếp đặt hàng hóa trong kho tới trần nhà, đầu phun chữa cháy tự động (sprinkler) và đèn chiếu sáng có đảm bảo tối thiểu 0,5 mét không?",
        "help_text": "Theo QCVN 06:2022/BXD và TCVN 7336:2021, hàng hóa phải cách trần và đầu phun tối thiểu 0,5m để đảm bảo hiệu quả chữa cháy.",
        "reference": "TCVN 7336:2021 & QCVN 06:2022/BXD",
        "options": [
            {"key": "A", "text": "Hàng hóa xếp cách đầu phun sprinkler và đèn chiếu sáng trên 0,5m; có vạch sơn phân lô giới hạn rõ ràng.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hàng hóa xếp cách 0,5m nhưng thỉnh thoảng có vài kiện hàng cao gần sát đèn chiếu sáng.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng hóa chất cao sát trần hoặc che khuất tầm phun của đầu sprinkler, cản trở chữa cháy tự động.", "score": 2, "risk": "high", "rec": "Hạ độ cao xếp dỡ hàng hóa, đảm bảo khoảng cách thông thủy tối thiểu 0,5m tới trần và đầu phun sprinkler; kẻ vạch giới hạn lưu kho.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP"},
            {"key": "D", "text": "Hàng hóa dễ cháy chất chạm trực tiếp vào chao đèn chiếu sáng hoặc bóng đèn sợi đốt/cao áp phát nhiệt.", "score": 3, "risk": "critical", "rec": "Xử lý khẩn cấp trong 24h: Di dời ngay hàng hóa đang tiếp xúc với thiết bị chiếu sáng; thay thế toàn bộ đèn chiếu sáng kho bằng đèn LED chống nổ có chụp bảo vệ.", "legal": "Điều 17 & 40 Nghị định 144/2021/NĐ-CP"}
        ]
    },
    {
        "category_id": 10,
        "facility_type": "B",
        "question_text": "Quy trình kiểm tra và ngắt nguồn điện phụ tải của kho hàng sau giờ làm việc hàng ngày được thực hiện như thế nào?",
        "help_text": "Nghị định 105/2025/NĐ-CP quy định kho hàng sau giờ làm việc phải ngắt toàn bộ điện phụ tải, chỉ duy trì chiếu sáng bảo vệ.",
        "reference": "Nghị định 105/2025/NĐ-CP & QCVN 25:2025/BCT",
        "options": [
            {"key": "A", "text": "Ngắt toàn bộ cầu dao/aptomat phụ tải kho hàng; chỉ duy trì đường điện chiếu sáng bảo vệ riêng biệt.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quy định ngắt điện nhưng nhân viên đôi khi quên tắt quạt thông gió hoặc thiết bị phụ trợ.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dùng chung một nguồn điện duy nhất cho cả thắp sáng và phụ tải; không ngắt điện phụ tải khi đóng cửa kho.", "score": 2, "risk": "high", "rec": "Tách riêng mạch điện chiếu sáng bảo vệ và mạch động lực sản xuất; lắp đặt aptomat đóng ngắt tổng đặt ngoài kho.", "legal": "QCVN 25:2025/BCT"},
            {"key": "D", "text": "Cắm sạc ắc quy xe nâng điện, thiết bị sấy hoặc thiết bị điện tự chế qua đêm trong kho không người trực.", "score": 3, "risk": "critical", "rec": "Nghiêm cấm sạc ắc quy xe nâng trong kho hàng qua đêm; bố trí trạm sạc riêng biệt cách ly ngoài kho có hệ thống ngắt tự động.", "legal": "Điều 17 Nghị định 144/2021/NĐ-CP"}
        ]
    },
    {
        "category_id": 10,
        "facility_type": "B",
        "question_text": "Lối đi thông gió, thoát nạn và khoảng cách giữa các khối pallet/kệ hàng trong kho có đảm bảo thông thoáng theo quy chuẩn không?",
        "help_text": "Lối đi chính tối thiểu 1.5m, lối đi giữa các giá kệ tối thiểu 0.8m theo quy định an toàn kho bãi.",
        "reference": "QCVN 06:2022/BXD & Luật PCCC số 55/2024/QH15",
        "options": [
            {"key": "A", "text": "Lối đi chính rộng tối thiểu 1,5m; lối đi giữa các giá kệ rộng tối thiểu 0,8m; thông thoáng hoàn toàn.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Lối đi đủ kích thước nhưng đôi khi có vỏ thùng carton, pallet rỗng để tạm trên lối đi.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng hóa chất lấn chiếm lối đi, bề rộng lối thoát nạn bị thu hẹp dưới 0,8m; khó tiếp cận bình chữa cháy.", "score": 2, "risk": "high", "rec": "Sắp xếp lại kho, giải tỏa toàn bộ pallet lấn chiếm lối đi; duy trì lối đi chính rộng tối thiểu 1,5m thông suốt.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP"},
            {"key": "D", "text": "Hàng hóa chất bịt kín hoàn toàn lối thoát nạn hoặc cửa kho phụ; không có đường thoát khi xảy ra cháy.", "score": 3, "risk": "critical", "rec": "Giải tỏa khẩn cấp trong 24h: Khơi thông ngay lối thoát nạn và cửa thoát hiểm; cấm tuyệt đối việc chất hàng cản trở cửa ra vào.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP"}
        ]
    },

    # --- NHÓM C: NHÀ Ở HỖN HỢP / CHUNG CƯ MINI / NHÀ TRỌ (category_id = 11, facility_type = 'C') ---
    {
        "category_id": 11,
        "facility_type": "C",
        "question_text": "Khu vực để xe máy, xe điện tại tầng 1 (hoặc tầng bán hầm) có được ngăn cách chống cháy, chống khói lan lên cầu thang bộ thoát nạn không?",
        "help_text": "Chỉ thị 01/CT-TTg và quy chuẩn phòng chống khói yêu cầu ngăn cách triệt để khu vực để xe với thang bộ bằng tường, vách chống cháy và cửa tự đóng.",
        "reference": "Chỉ thị 01/CT-TTg & Luật PCCC số 55/2024/QH15",
        "options": [
            {"key": "A", "text": "Có vách ngăn chống cháy và cửa chống cháy ngăn riêng biệt khu để xe với lồng cầu thang bộ thoát nạn.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có vách ngăn và cửa ngăn nhưng cửa thường xuyên mở hé hoặc không có tay co tự đóng.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cầu thang bộ thông thẳng trực tiếp xuống khu vực để xe tầng 1, không có vách hoặc cửa ngăn khói.", "score": 2, "risk": "high", "rec": "Xây dựng vách ngăn chống cháy hoặc vách thạch cao chống cháy và lắp cửa ngăn khói tự đóng giữa khu để xe và cầu thang bộ.", "legal": "Nghị định 105/2025/NĐ-CP"},
            {"key": "D", "text": "Khu để xe quá tải chật kín sát cửa ra vào; cầu thang hở thông tầng; khi cháy khói sẽ phong tỏa toàn bộ lối thoát nạn.", "score": 3, "risk": "critical", "rec": "Khắc phục khẩn cấp trong 24h-48h: Giảm mật độ xe, tạo lối đi thông thoáng ra cửa chính; làm vách ngăn khói cách ly cầu thang bộ lên các tầng trên.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP & Luật PCCC 55/2024"}
        ]
    },
    {
        "category_id": 11,
        "facility_type": "C",
        "question_text": "Quy định và hạ tầng sạc xe máy điện, xe đạp điện tại cơ sở/nhà trọ được bố trí như thế nào?",
        "help_text": "Khuyến cáo an toàn PCCC về sạc pin xe điện: sạc tại khu vực riêng, dây dẫn đúng tiết diện, có aptomat tự ngắt và cấm sạc qua đêm không người trông coi.",
        "reference": "Khuyến cáo Cục Cảnh sát PCCC & CNCH",
        "options": [
            {"key": "A", "text": "Bố trí khu sạc xe điện riêng biệt, có aptomat chống quá tải riêng, có người giám sát hoặc hẹn giờ tự ngắt.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có khu vực sạc riêng nhưng dây cắm sạc dòng tải cao dùng ổ cắm thông thường, chưa có thiết bị tự ngắt.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Người thuê/chủ nhà tự cắm sạc xe điện qua đêm sát các vật liệu dễ cháy (mút xốp, rèm cửa, giấy carton).", "score": 2, "risk": "high", "rec": "Lắp đặt ổ cắm sạc chuyên dụng có cầu dao chống quá tải, trang bị ổ cắm hẹn giờ tự ngắt điện sau 6 tiếng; cách xa vật liệu cháy tối thiểu 1m.", "legal": "QCVN 25:2025/BCT"},
            {"key": "D", "text": "Dây sạc chắp vá, câu móc chằng chịt, sạc đồng thời nhiều xe chung ổ cắm có hiện tượng nóng chảy phích cắm.", "score": 3, "risk": "critical", "rec": "Xử lý ngay lập tức: Cắt bỏ các đường dây câu móc chắp vá; lắp đường dây dẫn chịu tải riêng cho khu sạc xe điện có aptomat chống giật RCBO.", "legal": "Điều 17 Nghị định 144/2021/NĐ-CP"}
        ]
    },
    {
        "category_id": 11,
        "facility_type": "C",
        "question_text": "Lối thoát nạn khẩn cấp thứ hai (qua ban công, lô gia, tầng mái hoặc chuồng cọp) có đảm bảo sẵn sàng mở ra khi có sự cố không?",
        "help_text": "Chỉ thị 01/CT-TTg yêu cầu 100% hộ gia đình, nhà ở nhiều tầng mở lối thoát nạn khẩn cấp thứ hai qua ban công, chuồng cọp.",
        "reference": "Chỉ thị 01/CT-TTg & Luật PCCC số 55/2024/QH15",
        "options": [
            {"key": "A", "text": "Chuồng cọp có cửa thoát nạn kích thước tối thiểu 0,6x0,8m, chìa khóa để vị trí dễ thấy hoặc có thang sắt ngoài nhà.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cửa thoát nạn ở ban công/chuồng cọp nhưng khóa bị rỉ sét hoặc chìa khóa cất chỗ kín khó tìm khi khẩn cấp.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Ban công/lô gia bị rào kín bằng lồng sắt (chuồng cọp) kiên cố hoàn toàn không có cửa mở thoát hiểm.", "score": 2, "risk": "high", "rec": "Mở ngay cửa thoát nạn trên lồng sắt/chuồng cọp với kích thước tối thiểu 0,6m x 0,8m; bố trí búa phá dỡ hoặc thang dây thoát nạn.", "legal": "Chỉ thị 01/CT-TTg của Thủ tướng Chính phủ"},
            {"key": "D", "text": "Không có lối thoát thứ hai; chuồng cọp hàn kín mít và chất đầy đồ đạc phế liệu bịt kín lối ra.", "score": 3, "risk": "critical", "rec": "Khắc phục khẩn cấp trong 48h: Cắt mở lối thoát hiểm trên chuồng cọp, dọn sạch đồ phế liệu ban công; trang bị thang dây hoặc ống tụt cứu người.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP"}
        ]
    },

    # --- NHÓM D: KARAOKE, QUÁN BAR, VŨ TRƯỜNG, NHÀ HÀNG (category_id = 12, facility_type = 'D') ---
    {
        "category_id": 12,
        "facility_type": "D",
        "question_text": "Vật liệu ốp cách âm, trang trí nội thất trong phòng hát, quầy bar có sử dụng vật liệu chống cháy lan (thử nghiệm theo QCVN 06:2022/BXD) không?",
        "help_text": "Thông tư 147/2020/TT-BCA và Thông tư 02/2021/TT-BXD nghiêm cấm sử dụng mút xốp, vật liệu dễ cháy làm cách âm quán karaoke.",
        "reference": "Thông tư 147/2020/TT-BCA & QCVN 06:2022/BXD",
        "options": [
            {"key": "A", "text": "Sử dụng vật liệu không cháy hoặc khó cháy (bông khoáng, thạch cao chống cháy, tấm panel chống cháy có chứng chỉ kiểm định).", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Vật liệu khó cháy nhưng một số mảng trang trí bề mặt dùng da mút, gỗ công nghiệp chưa kiểm định cháy lan.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sử dụng mút xốp cao su, xốp mút tổ ong dễ bắt cháy và khi cháy tỏa ra khí độc cực mạnh (Cyanide, CO).", "score": 2, "risk": "high", "rec": "Tháo dỡ ngay lớp mút xốp bắt cháy, thay thế bằng vật liệu cách âm chống cháy đạt tiêu chuẩn theo QCVN 06:2022/BXD.", "legal": "Thông tư 147/2020/TT-BCA"},
            {"key": "D", "text": "Toàn bộ vách và trần ốp mút xốp xốp trứng, nilon dễ cháy; đường dây điện đi ngầm sát ngay lớp mút xốp.", "score": 3, "risk": "critical", "rec": "Đình chỉ sử dụng phòng hát ngay lập tức: Tháo dỡ hoàn toàn vật liệu mút xốp nguy hiểm; đi lại hệ thống điện trong ống kim loại cách ly.", "legal": "Điều 30 & 44 Nghị định 144/2021/NĐ-CP"}
        ]
    },
    {
        "category_id": 12,
        "facility_type": "D",
        "question_text": "Hệ thống điện và dàn âm thanh, ánh sáng có được liên động tự động ngắt khi hệ thống báo cháy kích hoạt không?",
        "help_text": "TCVN 3890 / QCVN 10:2025/BCA quy định cơ sở dịch vụ karaoke, vũ trường phải có hệ thống liên động ngắt âm thanh và bật sáng khi có cháy.",
        "reference": "QCVN 10:2025/BCA & TCVN 3890",
        "options": [
            {"key": "A", "text": "Có tủ điều khiển liên động tự động ngắt điện âm thanh, màn hình và bật sáng đèn chiếu sáng sự cố khi có báo cháy.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có công tắc ngắt âm thanh tập trung tại quầy lễ tân nhưng phải thao tác thủ công bằng tay.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có hệ thống ngắt âm thanh tự động; âm thanh lớn trong phòng hát lấn át hoàn toàn tiếng chuông báo động cháy.", "score": 2, "risk": "high", "rec": "Lắp đặt rơ-le liên động giữa hệ thống báo cháy tự động và nguồn cấp điện dàn âm thanh theo quy chuẩn QCVN 10:2025/BCA.", "legal": "QCVN 10:2025/BCA"},
            {"key": "D", "text": "Dàn âm thanh công suất lớn đấu nối quá tải; dây nguồn đi trực tiếp sau vách mút xốp không luồn ống chống cháy.", "score": 3, "risk": "critical", "rec": "Khắc phục khẩn cấp trong 24h: Tách nguồn âm thanh công suất lớn, lắp tủ điện bảo vệ và hệ thống ngắt tự động khi có chuông báo cháy.", "legal": "Điều 17 & 44 Nghị định 144/2021/NĐ-CP"}
        ]
    },
    {
        "category_id": 12,
        "facility_type": "D",
        "question_text": "Cửa thoát nạn của phòng dịch vụ và hành lang thoát hiểm mở ra theo chiều nào và có biển chỉ dẫn EXIT phát sáng liên tục không?",
        "help_text": "Cửa phòng karaoke, quán bar phải mở ra theo chiều thoát nạn, không được lắp gương gây nhầm lẫn đường thoát.",
        "reference": "QCVN 06:2022/BXD & QCVN 10:2025/BCA",
        "options": [
            {"key": "A", "text": "Cửa mở theo chiều thoát nạn; biển EXIT và đèn sự cố chiếu sáng độc lập tối thiểu 2 giờ; thông thoáng 100%.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cửa mở đúng chiều nhưng một vài đèn EXIT bị mờ hoặc ắc quy tích điện dự phòng đã yếu.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cửa mở vào trong (ngược chiều thoát); hành lang bị thu hẹp do để thùng bia, xe đẩy hoặc đồ đạc phục vụ.", "score": 2, "risk": "high", "rec": "Hoán đổi bản lề để cửa mở ra theo chiều thoát nạn; giải phóng toàn bộ vật cản trên hành lang chung.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP"},
            {"key": "D", "text": "Cửa thoát nạn bị khóa chốt từ bên ngoài; hành lang tối, không có đèn sự cố, lắp gương gây ảo giác mất phương hướng.", "score": 3, "risk": "critical", "rec": "Xử lý khẩn cấp trong 24h: Mở toàn bộ khóa chốt cửa thoát hiểm; tháo dỡ gương đánh lừa thị giác; lắp đặt đèn EXIT tự nạp điện.", "legal": "Điều 40 & 44 Nghị định 144/2021/NĐ-CP"}
        ]
    },

    # --- NHÓM A: SẢN XUẤT CÔNG NGHIỆP (category_id = 9, facility_type = 'A') ---
    {
        "category_id": 9,
        "facility_type": "A",
        "question_text": "Quy trình cách ly và ngắt aptomat tổng các dây chuyền sản xuất cơ khí, may mặc, chế biến gỗ sau ca làm việc được thực hiện ra sao?",
        "help_text": "Nghị định 105/2025/NĐ-CP quy định nhà xưởng sau ca làm việc phải ngắt điện thiết bị sản xuất để triệt tiêu nguy cơ chập cháy do quá tải hoặc quá nhiệt.",
        "reference": "Nghị định 105/2025/NĐ-CP & QCVN 25:2025/BCT",
        "options": [
            {"key": "A", "text": "Có bảng kiểm tra cuối ca, phân công rõ người ngắt aptomat từng phân xưởng; chỉ để lại lộ điện camera và chiếu sáng bảo vệ.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có người ngắt điện nhưng không có sổ theo dõi bàn giao; thỉnh thoảng vẫn để sót quạt thông gió hoặc máy tính văn phòng xưởng.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không ngắt điện phụ tải xưởng; máy biến áp, tủ điện phân phối và các máy công cụ vẫn ngâm điện qua đêm.", "score": 2, "risk": "high", "rec": "Ban hành quy chế bắt buộc ngắt điện phụ tải sau ca; lắp đặt aptomat phân vùng để dễ dàng cô lập nguồn điện khi hết giờ làm việc.", "legal": "Nghị định 105/2025/NĐ-CP & QCVN 25:2025/BCT"},
            {"key": "D", "text": "Để máy hàn, máy may, lò sấy cắm điện hoạt động tự động qua đêm mà không có người trực giám sát.", "score": 3, "risk": "critical", "rec": "Xử lý khẩn cấp trong 24h: Cấm tuyệt đối vận hành thiết bị phát nhiệt sinh công suất lớn qua đêm không người trực; kiểm điểm cá nhân vi phạm.", "legal": "Điều 17 Nghị định 144/2021/NĐ-CP"}
        ]
    },
    {
        "category_id": 9,
        "facility_type": "A",
        "question_text": "Khoảng cách chống cháy lan và đường giao thông cho xe chữa cháy tiếp cận giữa các nhà xưởng liền kề có đảm bảo thông thoáng không?",
        "help_text": "QCVN 06:2022/BXD quy định đường cho xe chữa cháy phải rộng tối thiểu 3.5m, chiều cao thông thủy tối thiểu 4.5m.",
        "reference": "QCVN 06:2022/BXD & Luật PCCC số 55/2024/QH15",
        "options": [
            {"key": "A", "text": "Đường nội bộ xung quanh xưởng rộng tối thiểu 3,5m, chiều cao thông thủy 4,5m; xe chữa cháy tiếp cận thông suốt 4 phía.", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đường cho xe chữa cháy rộng 3,5m nhưng thỉnh thoảng có xe tải bốc dỡ hàng đỗ tạm gây cản trở cục bộ.", "score": 1, "risk": "low"},
            {"key": "C", "text": "Khoảng cách giữa các xưởng bị cơi nới mái tôn, làm lán tạm chứa hàng hóa phế liệu, xe chữa cháy không vào được.", "score": 2, "risk": "high", "rec": "Tháo dỡ ngay phần mái tôn cơi nới lấn chiếm khoảng lùi; giải tỏa vật liệu chắn đường xe chữa cháy tiếp cận.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP"},
            {"key": "D", "text": "Xưởng xây san sát không có khoảng cách an toàn; lối tiếp cận duy nhất bị rào chắn kiên cố hoặc chất đầy hàng hóa.", "score": 3, "risk": "critical", "rec": "Khắc phục khẩn cấp trong 48h: Tháo bỏ rào chắn, tạo khoảng hở tối thiểu 4m giữa các khu vực nguy hiểm cháy nổ; bố trí bãi đỗ xe chữa cháy theo QCVN 06.", "legal": "Điều 40 Nghị định 144/2021/NĐ-CP"}
        ]
    }
]

def add_enhanced_questions():
    db = SessionLocal()
    added_questions = 0
    added_options = 0
    added_recs = 0

    try:
        for q_data in NEW_QUESTIONS_DATA:
            # Check if question already exists to prevent duplication
            existing_q = db.query(Question).filter(
                Question.question_text == q_data["question_text"]
            ).first()

            if existing_q:
                print(f"Skipping existing: {q_data['question_text'][:50]}...")
                continue

            # Determine order_index in category
            max_order = db.query(Question).filter(
                Question.category_id == q_data["category_id"]
            ).count()

            new_q = Question(
                category_id=q_data["category_id"],
                question_text=q_data["question_text"],
                question_type="single",
                facility_type=q_data["facility_type"],
                help_text=q_data.get("help_text"),
                reference=q_data.get("reference"),
                order_index=max_order + 1,
                is_active=True
            )
            db.add(new_q)
            db.flush()
            added_questions += 1

            for idx, opt_data in enumerate(q_data["options"]):
                new_opt = QuestionOption(
                    question_id=new_q.id,
                    option_key=opt_data["key"],
                    option_text=opt_data["text"],
                    score=opt_data["score"],
                    risk_level=opt_data["risk"],
                    order_index=idx + 1
                )
                db.add(new_opt)
                db.flush()
                added_options += 1

                # If recommendation exists for risky option
                if "rec" in opt_data:
                    priority = "urgent" if opt_data["score"] == 3 else "high"
                    deadline_days = 2 if opt_data["score"] == 3 else 30
                    new_rec = Recommendation(
                        question_option_id=new_opt.id,
                        recommendation_text=opt_data["rec"],
                        priority=priority,
                        deadline_days=deadline_days,
                        legal_reference=opt_data.get("legal"),
                        is_active=True
                    )
                    db.add(new_rec)
                    added_recs += 1

        db.commit()
        print(f"SUCCESS: Added {added_questions} questions, {added_options} options, {added_recs} recommendations!")

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_enhanced_questions()
