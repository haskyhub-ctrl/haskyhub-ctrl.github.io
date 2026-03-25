# seed_data.py — FRAS Question Bank (Updated 2026-03-22)
# Part 1: Categories + Common Questions (Groups 1-8) — 90 questions total

FACILITY_TYPES = [
    {"value": "industrial", "label": "Cơ sở sản xuất công nghiệp", "icon": "🏭", "group": "A"},
    {"value": "warehouse", "label": "Kho hàng, kho vật liệu", "icon": "🏪", "group": "B"},
    {"value": "mixed_residence", "label": "Nhà ở hỗn hợp (ở + kinh doanh)", "icon": "🏠", "group": "C"},
    {"value": "hospitality", "label": "Nhà hàng, khách sạn, chợ, TTTM", "icon": "🍽️", "group": "D"},
    {"value": "medical_education", "label": "Bệnh viện, trường học, cơ sở y tế", "icon": "🏥", "group": "E"},
    {"value": "fuel_gas", "label": "Cơ sở xăng dầu, khí gas, vật liệu nổ", "icon": "⛽", "group": "F"},
    {"value": "transport", "label": "Phương tiện giao thông", "icon": "🚌", "group": "G"},
    {"value": "residential", "label": "Khu dân cư, nhà ở, nhà trọ", "icon": "🏘️", "group": "H"},
    {"value": "construction", "label": "Công trình xây dựng đang thi công", "icon": "🏗️", "group": "I"},
    {"value": "office", "label": "Cơ quan, trụ sở hành chính, văn phòng", "icon": "🏛️", "group": "J"},
    {"value": "laboratory", "label": "Cơ sở nghiên cứu, phòng thí nghiệm", "icon": "🔬", "group": "K"},
    {"value": "agriculture", "label": "Cơ sở nông nghiệp, chế biến nông lâm sản", "icon": "🌾", "group": "L"},
]

# ======= COMMON CATEGORIES (Groups 1-8) =======
COMMON_CATEGORIES = [
    {"name": "Sự cố hệ thống, thiết bị điện", "description": "Đánh giá toàn diện hệ thống điện, thiết bị bảo vệ, vận hành và quản lý an toàn điện", "icon": "⚡", "color": "#eab308", "order_index": 1, "max_score": 60},
    {"name": "Sơ suất, bất cẩn dùng lửa/nhiệt", "description": "Đánh giá việc sử dụng lửa, nguồn nhiệt, gas và các hoạt động phát sinh tia lửa", "icon": "🔥", "color": "#ef4444", "order_index": 2, "max_score": 30},
    {"name": "Vi phạm quy định PCCC", "description": "Đánh giá tuân thủ quy định phòng cháy chữa cháy theo pháp luật", "icon": "🛡️", "color": "#f97316", "order_index": 3, "max_score": 30},
    {"name": "Sự cố kỹ thuật (thiết bị, máy móc)", "description": "Đánh giá bảo dưỡng thiết bị, máy móc công nghiệp và hệ thống kỹ thuật", "icon": "⚙️", "color": "#3b82f6", "order_index": 4, "max_score": 30},
    {"name": "Tác động thiên nhiên", "description": "Đánh giá nguy cơ từ thời tiết, môi trường tự nhiên và yếu tố bên ngoài", "icon": "🌿", "color": "#22c55e", "order_index": 5, "max_score": 30},
    {"name": "Tự cháy", "description": "Đánh giá vật liệu tự phát nhiệt, bụi nổ, hóa chất phản ứng và pin lithium", "icon": "🌡️", "color": "#a855f7", "order_index": 6, "max_score": 30},
    {"name": "Tai nạn giao thông (phương tiện cơ giới)", "description": "Đánh giá nguy cơ cháy nổ từ phương tiện, nhiên liệu và bãi đỗ xe", "icon": "🚗", "color": "#6366f1", "order_index": 7, "max_score": 30},
    {"name": "Nguyên nhân khác / Rủi ro bổ sung", "description": "Đánh giá an ninh, nhận thức PCCC, nhà thầu và kế hoạch khôi phục", "icon": "⚠️", "color": "#64748b", "order_index": 8, "max_score": 30},
]

# ======= GROUP 1: Sự cố hệ thống, thiết bị điện — 20 câu (E01–E20) =======
GROUP1_QUESTIONS = [
    # E01
    {"text": "Hệ thống điện tại cơ sở có được kiểm tra, bảo trì định kỳ bởi đơn vị có chuyên môn không?", "options": [
        {"key": "A", "text": "Có kiểm tra định kỳ hàng năm bởi đơn vị có giấy phép, có biên bản lưu hồ sơ đầy đủ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Tự kiểm tra nội bộ theo kinh nghiệm, chưa mời đơn vị chuyên nghiệp bên ngoài", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ kiểm tra khi có sự cố xảy ra hoặc khi cơ quan chức năng yêu cầu", "score": 2, "risk": "high"},
        {"key": "D", "text": "Chưa từng kiểm tra hệ thống điện kể từ khi lắp đặt ban đầu", "score": 3, "risk": "critical"},
    ]},
    # E02
    {"text": "Hệ thống dây dẫn điện tại cơ sở có dấu hiệu hư hỏng (bong tróc vỏ cách điện, rỉ sét, nối dây bằng băng keo không đúng quy cách) không?", "options": [
        {"key": "A", "text": "Dây điện còn mới, vỏ cách điện nguyên vẹn, luồn trong ống bảo vệ hoặc máng cáp đúng quy cách", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Phần lớn dây tốt, có 1-2 đoạn nhỏ vỏ hơi cũ nhưng chưa bong tróc", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhiều đoạn dây bong tróc vỏ cách điện, có mối nối bằng băng keo không đúng kỹ thuật", "score": 2, "risk": "high"},
        {"key": "D", "text": "Dây điện cũ nát, vỏ bọc nứt rạn nhiều chỗ, rỉ sét tại các mối nối, có dấu hiệu chạm chập", "score": 3, "risk": "critical"},
    ]},
    # E03
    {"text": "Các thiết bị bảo vệ điện (Cầu chì, Aptomat, CB) có dung lượng và tình trạng hoạt động như thế nào?", "options": [
        {"key": "A", "text": "Có aptomat/CB đúng dòng định mức cho từng mạch, kiểm tra hoạt động định kỳ ít nhất 1 lần/năm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có aptomat nhưng không rõ dòng định mức có phù hợp tải thực tế không, chưa từng test", "score": 1, "risk": "low"},
        {"key": "C", "text": "Dùng cầu chì dây thay aptomat, hoặc aptomat đã cũ bị kẹt chưa thay thế", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có thiết bị bảo vệ ngắt điện tự động nào, hoặc đã bị bypass (nối tắt)", "score": 3, "risk": "critical"},
    ]},
    # E04
    {"text": "Việc sử dụng ổ cắm di động (dây kéo dài) tại cơ sở được thực hiện như thế nào?", "options": [
        {"key": "A", "text": "Không sử dụng ổ cắm kéo dài, hoặc chỉ dùng loại có CB bảo vệ tích hợp, đúng công suất", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có dùng ổ cắm kéo dài nhưng kiểm soát tổng công suất thiết bị cắm vào không vượt tải", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thường xuyên dùng nhiều ổ cắm kéo dài nối chồng nhau, cắm nhiều thiết bị công suất lớn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Ổ cắm kéo dài cũ hỏng, dây bị nóng khi dùng, chân cắm lỏng lẻo, vẫn sử dụng hàng ngày", "score": 3, "risk": "critical"},
    ]},
    # E05
    {"text": "Hệ thống tiếp địa bảo vệ (nối đất) và chống sét của cơ sở được lắp đặt và kiểm tra như thế nào?", "options": [
        {"key": "A", "text": "Có hệ thống tiếp địa và chống sét đầy đủ, đo điện trở nối đất đạt ≤ 4Ω, có biên bản kiểm tra định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có hệ thống tiếp địa nhưng chưa đo điện trở nối đất gần đây, không rõ có đạt tiêu chuẩn không", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ một số thiết bị lớn có nối đất, hệ thống không đồng bộ, chưa có chống sét lan truyền", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có hệ thống nối đất bảo vệ và không có chống sét, hoặc không biết cơ sở có hay không", "score": 3, "risk": "critical"},
    ]},
    # E06
    {"text": "Cơ sở có lắp đặt thiết bị chống giật/chống rò điện (ELCB, RCD) tại các mạch điện quan trọng không?", "options": [
        {"key": "A", "text": "Có lắp ELCB/RCD 30mA cho toàn bộ các mạch điện, kiểm tra bằng nút TEST định kỳ hàng tháng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Chỉ lắp ở một số mạch quan trọng (khu vực ẩm ướt, bếp, nhà tắm)", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có lắp nhưng chưa bao giờ test, không biết còn hoạt động tốt không", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không lắp thiết bị chống rò điện nào, hoặc không biết thiết bị này là gì", "score": 3, "risk": "critical"},
    ]},
    # E07
    {"text": "Tình trạng tủ điện chính/phân phối tại cơ sở như thế nào?", "options": [
        {"key": "A", "text": "Tủ điện đặt nơi khô ráo thông thoáng, có khóa, biển cảnh báo, không có vật liệu dễ cháy trong vòng 1m", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Tủ điện đặt đúng vị trí nhưng xung quanh có để một số vật dụng, chưa có biển cảnh báo", "score": 1, "risk": "low"},
        {"key": "C", "text": "Tủ điện đặt gần vật liệu dễ cháy hoặc ở nơi ẩm ướt, cửa tủ không đóng kín", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tủ điện bị hàng hóa che khuất hoàn toàn, khó tiếp cận khi xảy ra sự cố khẩn cấp", "score": 3, "risk": "critical"},
    ]},
    # E08
    {"text": "Hệ thống chiếu sáng tại cơ sở được lắp đặt và vận hành như thế nào liên quan đến an toàn cháy nổ?", "options": [
        {"key": "A", "text": "Dùng đèn LED tiết kiệm điện, lắp đặt cách vật liệu dễ cháy ≥ 0.5m, có chao đèn bảo vệ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Phần lớn đèn LED, còn một số đèn huỳnh quang cũ nhưng hoạt động bình thường", "score": 1, "risk": "low"},
        {"key": "C", "text": "Còn dùng đèn sợi đốt/halogen tỏa nhiệt cao gần vật liệu dễ cháy như vải, giấy, gỗ", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đèn lắp áp sát trần bằng vật liệu dễ cháy, ballast đèn cũ nóng bất thường, có mùi khét", "score": 3, "risk": "critical"},
    ]},
    # E09
    {"text": "Các thiết bị điện nung nóng (bếp điện, bếp từ, lò sưởi điện, bàn ủi) được sử dụng và quản lý như thế nào tại cơ sở?", "options": [
        {"key": "A", "text": "Dùng thiết bị có CE/CR, có mạch riêng, luôn rút phích cắm khi không dùng, cách xa vật dễ cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có thiết bị nung nóng, sử dụng cẩn thận nhưng đôi khi quên rút phích cắm khi rời đi", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thiết bị nung nóng đặt gần vật dễ cháy, dùng chung ổ cắm với thiết bị khác", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thiết bị nung nóng cũ không có thermostat tự ngắt, để chạy liên tục không giám sát", "score": 3, "risk": "critical"},
    ]},
    # E10
    {"text": "Hệ thống máy điều hòa không khí (ĐHKK) tại cơ sở được bảo trì và kiểm tra an toàn như thế nào?", "options": [
        {"key": "A", "text": "Vệ sinh và kiểm tra ĐHKK định kỳ 6 tháng/lần bởi thợ chuyên nghiệp, mạch điện riêng có CB", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Vệ sinh filter tự làm 1 lần/năm, chưa kiểm tra hệ thống điện và gas lạnh", "score": 1, "risk": "low"},
        {"key": "C", "text": "ĐHKK chạy liên tục nhiều năm không bảo trì, có tiếng kêu lạ hoặc rung lắc bất thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "ĐHKK cũ bị rò gas lạnh, dây điện nóng khi chạy, có mùi khét nhưng vẫn sử dụng", "score": 3, "risk": "critical"},
    ]},
    # E11
    {"text": "Cơ sở có sử dụng máy phát điện dự phòng không? Nếu có, việc vận hành và bảo quản như thế nào?", "options": [
        {"key": "A", "text": "Không có máy phát điện; hoặc có, đặt ngoài trời/phòng riêng thông gió, bảo dưỡng định kỳ, có ATS", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có máy phát, đặt đúng nơi nhưng chưa bảo dưỡng định kỳ, chỉ chạy thử khi mất điện", "score": 1, "risk": "low"},
        {"key": "C", "text": "Máy phát đặt trong nhà kho chung, gần vật liệu dễ cháy, ống xả không dẫn ra ngoài", "score": 2, "risk": "high"},
        {"key": "D", "text": "Máy phát cũ rò rỉ nhiên liệu, đặt trong tầng hầm kín, không có hệ thống thông gió", "score": 3, "risk": "critical"},
    ]},
    # E12
    {"text": "Tải điện thực tế tại cơ sở có vượt quá công suất thiết kế ban đầu của hệ thống điện không?", "options": [
        {"key": "A", "text": "Tải thực tế nằm trong phạm vi thiết kế, có đo đạc xác nhận, dự phòng ≥ 20% công suất", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Không rõ công suất thiết kế ban đầu, nhưng chưa có dấu hiệu quá tải (dây không nóng)", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đã bổ sung nhiều thiết bị mới mà không nâng cấp hệ thống điện, aptomat thỉnh thoảng nhảy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hệ thống điện quá tải nghiêm trọng, dây nóng khi vận hành, CB nhảy thường xuyên phải nối tắt", "score": 3, "risk": "critical"},
    ]},
    # E13
    {"text": "Tại cơ sở, vật liệu dễ cháy (giấy, vải, xăng, hóa chất) có được bảo quản cách xa các thiết bị và nguồn điện không?", "options": [
        {"key": "A", "text": "Vật liệu dễ cháy bảo quản trong kho riêng, cách xa tủ điện, ổ cắm và thiết bị điện ≥ 1m", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Phần lớn cách xa, nhưng một vài vị trí vật liệu dễ cháy còn gần ổ cắm hoặc dây điện", "score": 1, "risk": "low"},
        {"key": "C", "text": "Vật liệu dễ cháy xếp gần tủ điện, ổ cắm, hoặc dưới đường đi dây điện chính", "score": 2, "risk": "high"},
        {"key": "D", "text": "Vật liệu dễ cháy chất đống sát tủ điện, che khuất thiết bị điện, dây điện đi xuyên qua", "score": 3, "risk": "critical"},
    ]},
    # E14
    {"text": "Tại cơ sở có sử dụng hệ thống UPS (lưu điện) hoặc trạm sạc pin, bình ắc-quy không? Nếu có, tình trạng như thế nào?", "options": [
        {"key": "A", "text": "Không có UPS/ắc-quy; hoặc có, đặt phòng riêng thông gió, bảo trì theo nhà sản xuất", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có UPS đặt trong phòng làm việc, hoạt động bình thường nhưng chưa kiểm tra pin gần đây", "score": 1, "risk": "low"},
        {"key": "C", "text": "UPS/ắc-quy cũ, pin phồng hoặc rò rỉ axit, đặt trong phòng kín không thông gió", "score": 2, "risk": "high"},
        {"key": "D", "text": "Nhiều bình ắc-quy cũ bảo quản cùng vật liệu dễ cháy, không có hệ thống xử lý khí hydro", "score": 3, "risk": "critical"},
    ]},
    # E15
    {"text": "Tại các khu vực có hơi khí dễ cháy nổ (kho xăng dầu, phòng sơn, kho gas), thiết bị điện được lựa chọn như thế nào?", "options": [
        {"key": "A", "text": "Không có khu vực chứa hơi khí dễ cháy; hoặc có nhưng toàn bộ thiết bị điện đạt cấp Ex phòng nổ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thiết bị điện chính đạt cấp Ex, nhưng đèn chiếu sáng và ổ cắm vẫn dùng loại thường", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có khu vực hơi khí dễ cháy nhưng dùng thiết bị điện thông thường, không phòng nổ", "score": 2, "risk": "high"},
        {"key": "D", "text": "Dùng công tắc, ổ cắm thường trong khu vực có hơi xăng dầu/gas, có nguy cơ phát tia lửa", "score": 3, "risk": "critical"},
    ]},
    # E16
    {"text": "Nhân viên tại cơ sở có được đào tạo quy trình xử lý sự cố điện (chập cháy, điện giật, mất điện đột ngột) không?", "options": [
        {"key": "A", "text": "100% nhân viên được đào tạo, biết vị trí cầu dao tổng, biết sơ cứu điện giật, có diễn tập", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Một số nhân viên phụ trách biết cách xử lý, còn lại chưa được đào tạo chính thức", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ phổ biến miệng, nhân viên không rõ vị trí cầu dao tổng và quy trình ngắt điện", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không ai được đào tạo về xử lý sự cố điện, không biết cầu dao tổng ở đâu", "score": 3, "risk": "critical"},
    ]},
    # E17
    {"text": "Tại các khu vực tập trung thiết bị điện (phòng server, tủ điện, UPS), loại bình chữa cháy nào được trang bị?", "options": [
        {"key": "A", "text": "Trang bị bình CO₂ hoặc hệ thống chữa cháy khí sạch (FM200), phù hợp cháy thiết bị điện", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bình chữa cháy bột ABC gần đó, chưa có bình CO₂ chuyên dụng cho thiết bị điện", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ có bình chữa cháy bột để ở hành lang xa, không có bình riêng tại khu vực điện", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bình chữa cháy nào gần khu vực tập trung thiết bị điện", "score": 3, "risk": "critical"},
    ]},
    # E18
    {"text": "Quy trình tắt thiết bị điện và kiểm tra an toàn trước khi rời cơ sở (cuối ngày, cuối tuần) được thực hiện như thế nào?", "options": [
        {"key": "A", "text": "Có checklist kiểm tra cuối ngày bắt buộc, người cuối cùng ký xác nhận đã ngắt thiết bị không cần thiết", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nhắc nhở tắt thiết bị nhưng không có checklist chính thức, phụ thuộc ý thức cá nhân", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không có quy trình, nhiều thiết bị để chế độ chờ hoặc chạy liên tục qua đêm và cuối tuần", "score": 2, "risk": "high"},
        {"key": "D", "text": "Toàn bộ thiết bị chạy 24/7 không ai kiểm tra, không có người trực ngoài giờ làm việc", "score": 3, "risk": "critical"},
    ]},
    # E19
    {"text": "Hồ sơ pháp lý về an toàn điện của cơ sở (thiết kế điện được thẩm duyệt, nghiệm thu điện, biên bản kiểm tra định kỳ) có đầy đủ không?", "options": [
        {"key": "A", "text": "Có đầy đủ: bản vẽ thiết kế điện, biên bản nghiệm thu, biên bản kiểm tra định kỳ còn hiệu lực", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bản vẽ thiết kế nhưng thiếu biên bản kiểm tra định kỳ gần nhất", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ có hồ sơ ban đầu, không cập nhật theo thực tế sửa chữa và mở rộng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bất kỳ hồ sơ pháp lý nào về hệ thống điện, điện lắp đặt tự phát", "score": 3, "risk": "critical"},
    ]},
    # E20
    {"text": "Cơ sở có trang bị hệ thống phát hiện và cảnh báo sớm các nguy cơ từ điện (cảm biến nhiệt, cảm biến khói, camera nhiệt hồng ngoại) không?", "options": [
        {"key": "A", "text": "Có hệ thống giám sát nhiệt tủ điện, cảm biến khói tại phòng điện, cảnh báo qua app/SMS", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có cảm biến khói chung trong tòa nhà nhưng không có giám sát nhiệt riêng cho tủ điện", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không có cảm biến tự động, chỉ dựa vào quan sát bằng mắt thường khi tuần tra", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bất kỳ hệ thống phát hiện sớm nào, cũng không có tuần tra kiểm tra", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 2: Sơ suất, bất cẩn dùng lửa/nhiệt — 10 câu (CF01–CF10) =======
GROUP2_QUESTIONS = [
    # CF01
    {"text": "Cơ sở/hộ gia đình có thực hiện đốt rác, phế thải, lá khô tại khuôn viên không? Nếu có, việc này được thực hiện như thế nào?", "options": [
        {"key": "A", "text": "Không đốt rác tại khuôn viên, thu gom và xử lý qua dịch vụ vệ sinh môi trường", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có đốt nhưng trong lò đốt chuyên dụng hoặc thùng kim loại có nắp, có người giám sát", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đốt rác lộ thiên trong sân, gần hàng rào hoặc cây cối khô, không có người trông coi liên tục", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đốt rác lộ thiên gần kho hàng, nhà xưởng hoặc khu dân cư đông đúc, khi gió lớn vẫn đốt", "score": 3, "risk": "critical"},
    ]},
    # CF02
    {"text": "Tại cơ sở hoặc hộ gia đình, việc đốt vàng mã, hóa vàng, thắp hương cúng lễ được thực hiện như thế nào?", "options": [
        {"key": "A", "text": "Không có hoạt động đốt vàng mã tại cơ sở", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Đốt trong lư/thùng kim loại trên nền bê tông, cách vật dễ cháy ≥ 3m, có người trông", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đốt vàng mã trong thùng nhưng đặt gần tường gỗ, mái tôn nhựa hoặc hàng hóa", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đốt vàng mã lộ thiên không kiểm soát, tàn bay khắp nơi, không có người trông coi", "score": 3, "risk": "critical"},
    ]},
    # CF03
    {"text": "Tại cơ sở có sử dụng nến, đèn dầu, đèn cầy không? Nếu có, cách sử dụng và bảo quản như thế nào?", "options": [
        {"key": "A", "text": "Không sử dụng nến/đèn dầu; hoặc chỉ dùng nến LED (điện tử) thay thế", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có dùng nến/đèn dầu nhưng đặt trong chụp thủy tinh, trên bề mặt không cháy, có người giám sát", "score": 1, "risk": "low"},
        {"key": "C", "text": "Dùng nến đặt gần rèm cửa, khăn trải bàn hoặc giấy tờ, đôi khi không có người trông", "score": 2, "risk": "high"},
        {"key": "D", "text": "Dùng nến/đèn dầu trong phòng ngủ hoặc kho hàng, để cháy qua đêm không ai giám sát", "score": 3, "risk": "critical"},
    ]},
    # CF04
    {"text": "Việc thắp hương (hương thẳng, hương vòng, nhang trầm) tại cơ sở/gia đình được thực hiện như thế nào?", "options": [
        {"key": "A", "text": "Không thắp hương; hoặc thắp trên bàn thờ có bát hương chắc chắn, cách trần và vật dễ cháy ≥ 0.5m", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thắp hương trên bàn thờ cố định, bát hương đầy tro nhưng vẫn ổn định, có vách sau bàn thờ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bàn thờ bằng gỗ sát trần nhà, tàn hương rơi xuống đồ thờ bằng giấy/vải", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thắp nhiều hương cùng lúc, bàn thờ đầy đồ giấy, tàn hương rơi ra sàn gỗ, không dọn", "score": 3, "risk": "critical"},
    ]},
    # CF05
    {"text": "Việc hút thuốc lá tại cơ sở/gia đình được quản lý như thế nào?", "options": [
        {"key": "A", "text": "Cấm hút thuốc hoàn toàn trong toàn bộ cơ sở, có biển cấm và chế tài xử lý vi phạm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Cho phép hút thuốc ở khu vực riêng ngoài trời, xa vật liệu dễ cháy, có gạt tàn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hút thuốc trong nhà xưởng, văn phòng, vứt tàn thuốc vào thùng rác thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hút thuốc trong kho hàng, gần khu vực chứa nhiên liệu hoặc hóa chất dễ cháy", "score": 3, "risk": "critical"},
    ]},
    # CF06
    {"text": "Việc sử dụng và bảo quản bếp gas, bình gas (LPG) tại cơ sở/gia đình được thực hiện như thế nào?", "options": [
        {"key": "A", "text": "Bếp gas đặt phòng riêng thông thoáng, dây dẫn gas mới, có van ngắt tự động và đầu dò gas", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Bếp gas đặt đúng nơi, dây dẫn chưa quá 2 năm, luôn khóa van bình sau khi nấu xong", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bình gas đặt gần nguồn nhiệt, dây dẫn cũ trên 3 năm, đôi khi quên khóa van bình", "score": 2, "risk": "high"},
        {"key": "D", "text": "Dùng bếp gas trong phòng ngủ hoặc kho hàng, dây gas nứt vá bằng băng keo, bình gas kẹt tủ kín", "score": 3, "risk": "critical"},
    ]},
    # CF07
    {"text": "Cơ sở/gia đình có tổ chức nướng than hoa ngoài trời, lửa trại hoặc các hoạt động có dùng lửa ngoài trời không?", "options": [
        {"key": "A", "text": "Không có hoạt động dùng lửa ngoài trời tại khuôn viên cơ sở", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nướng/lửa trại nhưng tại khu vực được chỉ định, nền bê tông, cách xa cây cối, có nước dập", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nướng than hoa trên ban công, sân thượng hoặc gần hàng rào, mái hiên dễ cháy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đốt lửa ngoài trời gần kho hàng, bãi xe hoặc khu vực có cỏ khô, không kiểm soát tàn lửa", "score": 3, "risk": "critical"},
    ]},
    # CF08
    {"text": "Tại cơ sở có sử dụng máy hàn hơi, máy cắt kim loại, máy khò gas hoặc đèn khò không? Quy trình an toàn khi thực hiện các công việc phát sinh tia lửa được thực hiện như thế nào?", "options": [
        {"key": "A", "text": "Không có hoạt động hàn cắt; hoặc có giấy phép hàn cắt, dọn sạch 10m, bạt chắn tia lửa, bình chữa cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có hàn cắt tại khu vực riêng, có bình chữa cháy nhưng chưa có giấy phép chính thức", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hàn cắt ngay trong khu vực sản xuất, chưa dọn vật liệu dễ cháy, không có bạt chắn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hàn cắt cạnh vật liệu dễ cháy, không bình chữa cháy, không giám sát, tia lửa bắn tự do", "score": 3, "risk": "critical"},
    ]},
    # CF09
    {"text": "Tại cơ sở/gia đình có tự bảo quản xăng dầu, cồn, dung môi dễ cháy không? Cách bảo quản như thế nào?", "options": [
        {"key": "A", "text": "Không lưu trữ xăng dầu/dung môi dễ cháy; hoặc bảo quản trong tủ chuyên dụng chống cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lưu trữ lượng nhỏ trong can kim loại có nắp kín, để nơi thông thoáng xa nguồn nhiệt", "score": 1, "risk": "low"},
        {"key": "C", "text": "Để can xăng/dung môi trong nhà kho chung, gần thiết bị điện hoặc ổ cắm", "score": 2, "risk": "high"},
        {"key": "D", "text": "Để xăng dầu trong chai nhựa hở miệng, trong phòng ngủ hoặc gần bếp nấu ăn", "score": 3, "risk": "critical"},
    ]},
    # CF10
    {"text": "Tại cơ sở/gia đình có sử dụng pháo hoa, pháo nổ, pháo sáng hoặc các vật liệu gây cháy nổ tương tự trong các dịp lễ, tết không?", "options": [
        {"key": "A", "text": "Không sử dụng pháo hoa/pháo nổ; hoặc chỉ xem pháo hoa do đơn vị có giấy phép tổ chức tại nơi công cộng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có sử dụng pháo hoa loại nhỏ cho phép, đốt ngoài trời sân rộng, xa nhà cửa và cây cối", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đốt pháo hoa gần nhà, gần mái hiên hoặc ban công, tàn pháo rơi lên mái tôn nhựa/bạt", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tự chế hoặc tích trữ pháo nổ trái phép trong nhà, bảo quản không đúng quy định", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 3: Vi phạm quy định PCCC — 10 câu (VQ01–VQ10) =======
GROUP3_QUESTIONS = [
    # VQ01
    {"text": "Cơ sở có đầy đủ hồ sơ pháp lý PCCC bắt buộc (thẩm duyệt thiết kế PCCC, nghiệm thu PCCC, giấy chứng nhận PCCC) không?", "options": [
        {"key": "A", "text": "Có đầy đủ: thẩm duyệt thiết kế, biên bản nghiệm thu, giấy chứng nhận PCCC còn hiệu lực", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có thẩm duyệt và nghiệm thu nhưng chưa cập nhật sau lần cải tạo/mở rộng gần nhất", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ có giấy phép kinh doanh, chưa hoàn thành thủ tục thẩm duyệt và nghiệm thu PCCC", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bất kỳ hồ sơ pháp lý PCCC nào, cơ sở hoạt động không phép về PCCC", "score": 3, "risk": "critical"},
    ]},
    # VQ02
    {"text": "Lối thoát hiểm và đường thoát nạn tại cơ sở có đáp ứng yêu cầu không?", "options": [
        {"key": "A", "text": "Có ≥ 2 lối thoát nạn độc lập, thông thoáng, đúng chiều rộng quy định, đèn chỉ dẫn EXIT hoạt động", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lối thoát nạn đủ nhưng một số đèn chỉ dẫn đã hỏng, chưa thay thế", "score": 1, "risk": "low"},
        {"key": "C", "text": "Lối thoát nạn bị thu hẹp do hàng hóa, đồ đạc, xe máy chiếm chỗ, vẫn đi qua được", "score": 2, "risk": "high"},
        {"key": "D", "text": "Lối thoát nạn bị chặn hoàn toàn hoặc cửa thoát nạn bị khóa cứng từ bên ngoài", "score": 3, "risk": "critical"},
    ]},
    # VQ03
    {"text": "Hệ thống báo cháy tự động tại cơ sở có được lắp đặt, duy trì và kiểm tra theo quy định không?", "options": [
        {"key": "A", "text": "Có hệ thống báo cháy tự động đầy đủ (đầu báo khói/nhiệt, trung tâm, chuông), kiểm tra định kỳ 6 tháng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có hệ thống báo cháy nhưng một số đầu báo đã lâu không kiểm tra, không rõ hoạt động", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hệ thống báo cháy đã lắp nhưng bị tắt do báo giả thường xuyên, chưa sửa chữa", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có hệ thống báo cháy tự động nào, chỉ dựa vào quan sát con người", "score": 3, "risk": "critical"},
    ]},
    # VQ04
    {"text": "Hệ thống chữa cháy tự động (Sprinkler, chữa cháy khí) tại cơ sở có hoạt động đúng không?", "options": [
        {"key": "A", "text": "Có sprinkler/chữa cháy khí đúng thiết kế, kiểm tra áp lực và thử nghiệm định kỳ, có biên bản", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có hệ thống sprinkler nhưng chưa thử nghiệm phun thực tế, chỉ kiểm tra áp lực đồng hồ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hệ thống sprinkler lắp đặt lâu, nhiều đầu phun bị che khuất bởi hàng hóa xếp cao", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có hệ thống chữa cháy tự động, hoặc hệ thống đã hỏng không sửa chữa", "score": 3, "risk": "critical"},
    ]},
    # VQ05
    {"text": "Phương tiện chữa cháy ban đầu (bình chữa cháy, hộp cứu hỏa, vòi chữa cháy vách tường) tại cơ sở có đầy đủ và sẵn sàng sử dụng không?", "options": [
        {"key": "A", "text": "Đủ số lượng theo quy định (1 bình/50m²), còn hạn, đặt đúng vị trí, dễ lấy, có bảng hướng dẫn", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bình chữa cháy nhưng số lượng chưa đủ hoặc một số bình gần hết hạn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bình chữa cháy để trong kho, bị hàng hóa che khuất, khó lấy khi cần", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bình chữa cháy hoặc toàn bộ bình đã hết hạn, hỏng van, không sử dụng được", "score": 3, "risk": "critical"},
    ]},
    # VQ06
    {"text": "Cơ sở có thành lập Đội PCCC cơ sở và xây dựng Phương án chữa cháy, thoát nạn không?", "options": [
        {"key": "A", "text": "Có đội PCCC cơ sở được huấn luyện, có phương án chữa cháy được phê duyệt, diễn tập định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có đội PCCC trên giấy tờ, có phương án nhưng chưa tổ chức diễn tập thực tế", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chưa thành lập đội PCCC, chỉ có phương án chữa cháy sơ sài để đối phó kiểm tra", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có đội PCCC, không có phương án chữa cháy, chưa từng diễn tập", "score": 3, "risk": "critical"},
    ]},
    # VQ07
    {"text": "Việc quản lý và sắp xếp hàng hóa, vật tư trong kho có tuân thủ quy định về an toàn PCCC không?", "options": [
        {"key": "A", "text": "Hàng hóa phân loại theo mức độ cháy, cách tường ≥ 0.5m, cách sprinkler ≥ 0.45m, lối đi thông thoáng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Hàng xếp gọn gàng, có lối đi nhưng chưa phân loại theo mức độ nguy hiểm cháy", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hàng hóa xếp chật, lối đi thu hẹp, hàng dễ cháy để lẫn với hàng thông thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hàng hóa chất đống tràn lan, không lối đi, che khuất tủ điện và đầu phun sprinkler", "score": 3, "risk": "critical"},
    ]},
    # VQ08
    {"text": "Các thiết bị điện, tủ điện, đầu phun sprinkler có đang bị che khuất hoặc bị hàng hóa, vật dụng chất gần ép sát không?", "options": [
        {"key": "A", "text": "Toàn bộ tủ điện, thiết bị điện và đầu phun sprinkler đều tiếp cận dễ dàng, không bị che khuất", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Phần lớn thông thoáng, nhưng 1-2 vị trí tủ điện có đồ đạc gần sát", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhiều tủ điện bị hàng hóa che trước, đầu phun sprinkler bị kệ hàng che mất", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tủ điện và đầu phun sprinkler bị chôn vùi trong hàng hóa, không thể tiếp cận được", "score": 3, "risk": "critical"},
    ]},
    # VQ09
    {"text": "Nguồn nước chữa cháy (bể nước, máy bơm, họng tiếp nước) có đủ áp lực và lưu lượng sẵn sàng không?", "options": [
        {"key": "A", "text": "Có bể nước PCCC riêng đúng dung tích, máy bơm chữa cháy hoạt động, kiểm tra áp lực định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bể nước chung (sinh hoạt + PCCC), máy bơm có nhưng chưa thử áp lực vòi gần đây", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bể nước nhỏ không đủ dung tích theo quy định, máy bơm cũ lâu không kiểm tra", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có nguồn nước chữa cháy riêng, không có máy bơm, trụ nước cứu hỏa xa cơ sở", "score": 3, "risk": "critical"},
    ]},
    # VQ10
    {"text": "Sơ đồ thoát nạn, biển chỉ dẫn PCCC và nội quy an toàn có được dán đúng vị trí và còn đọc được không?", "options": [
        {"key": "A", "text": "Sơ đồ thoát nạn dán mỗi tầng, biển PCCC đầy đủ, nội quy cập nhật, chữ rõ ràng, đúng vị trí", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có sơ đồ và biển chỉ dẫn nhưng một số đã cũ, chữ mờ, chưa cập nhật thay đổi mặt bằng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ có nội quy PCCC ở sảnh, không có sơ đồ thoát nạn tại các tầng/khu vực", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có sơ đồ, không có biển chỉ dẫn, không có nội quy PCCC niêm yết", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 4: Sự cố kỹ thuật (thiết bị, máy móc) — 10 câu (TF01–TF10) =======
GROUP4_QUESTIONS = [
    # TF01
    {"text": "Máy móc, thiết bị sản xuất tại cơ sở có được bảo trì định kỳ và kiểm tra an toàn vận hành không?", "options": [
        {"key": "A", "text": "Có lịch bảo dưỡng định kỳ theo hướng dẫn nhà sản xuất, có sổ theo dõi và biên bản", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Bảo dưỡng theo kinh nghiệm, không có lịch cố định, chỉ sửa chữa khi hỏng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thiết bị hoạt động liên tục, ít khi tắt để bảo dưỡng, có rung lắc hoặc tiếng kêu bất thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thiết bị cũ xuống cấp nghiêm trọng, chưa bảo dưỡng trong hơn 2 năm, vẫn vận hành", "score": 3, "risk": "critical"},
    ]},
    # TF02
    {"text": "Cơ sở có sử dụng nồi hơi, bình chịu áp lực, hệ thống khí nén không? Nếu có, tình trạng kiểm định và vận hành như thế nào?", "options": [
        {"key": "A", "text": "Không có thiết bị áp lực; hoặc có, đã đăng ký kiểm định đúng hạn, van an toàn hoạt động tốt", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có thiết bị áp lực, kiểm định còn hạn nhưng van an toàn lâu chưa thử nghiệm", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thiết bị áp lực đã quá hạn kiểm định nhưng vẫn đang sử dụng, chưa gia hạn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thiết bị áp lực chưa từng kiểm định, van an toàn hỏng hoặc bị nối tắt", "score": 3, "risk": "critical"},
    ]},
    # TF03
    {"text": "Hệ thống băng chuyền, dây đai truyền động và các bộ phận ma sát cao có được kiểm soát nguy cơ cháy không?", "options": [
        {"key": "A", "text": "Không có băng chuyền/truyền động; hoặc có, bôi trơn đúng lịch, kiểm tra độ căng dây đai định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có kiểm tra nhưng không thường xuyên, thỉnh thoảng dây đai bị trượt phát sinh nhiệt", "score": 1, "risk": "low"},
        {"key": "C", "text": "Dây đai cũ, hay bị kẹt gây nóng cục bộ, bụi và sợi vải tích tụ quanh bộ phận ma sát", "score": 2, "risk": "high"},
        {"key": "D", "text": "Bộ phận truyền động nóng bất thường, có mùi khét từ dây đai, bụi dễ cháy tích dày", "score": 3, "risk": "critical"},
    ]},
    # TF04
    {"text": "Cơ sở có sử dụng lò nung, lò sấy, lò nấu công nghiệp không? Hệ thống bảo vệ và kiểm soát nhiệt độ như thế nào?", "options": [
        {"key": "A", "text": "Không có lò nung/sấy; hoặc có, thermostat tự động, ngắt quá nhiệt, cách nhiệt đúng kỹ thuật", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lò nung/sấy với thermostat nhưng chưa hiệu chuẩn lại gần đây", "score": 1, "risk": "low"},
        {"key": "C", "text": "Lò nung/sấy điều chỉnh nhiệt thủ công, không có ngắt quá nhiệt tự động dự phòng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Lò nung/sấy tự chế, lớp cách nhiệt hư hỏng, vỏ ngoài nóng rát, gần vật liệu dễ cháy", "score": 3, "risk": "critical"},
    ]},
    # TF05
    {"text": "Xe nâng hàng và phương tiện vận chuyển nội bộ có gây nguy cơ cháy nổ không?", "options": [
        {"key": "A", "text": "Không có xe nâng; hoặc dùng xe nâng điện, sạc tại khu riêng thông thoáng, bảo trì đúng lịch", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Xe nâng diesel/gas bảo dưỡng định kỳ, ống xả có lưới chặn tia lửa", "score": 1, "risk": "low"},
        {"key": "C", "text": "Xe nâng cũ, ống xả không có lưới chặn, thỉnh thoảng rò rỉ dầu nhớt trên sàn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Xe nâng rò rỉ nhiên liệu, hoạt động trong khu vực có hơi khí dễ cháy hoặc bụi nổ", "score": 3, "risk": "critical"},
    ]},
    # TF06
    {"text": "Hệ thống làm lạnh công nghiệp (kho lạnh, máy lạnh công suất lớn dùng môi chất NH₃ hoặc Freon) có tiềm ẩn nguy cơ cháy nổ không?", "options": [
        {"key": "A", "text": "Không có hệ thống làm lạnh công nghiệp; hoặc có, dùng môi chất an toàn, bảo trì đúng lịch", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có hệ thống lạnh NH₃, vận hành tốt, có cảm biến rò khí và quạt thông gió dự phòng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hệ thống lạnh cũ, đường ống có dấu hiệu ăn mòn, chưa kiểm tra rò rỉ môi chất gần đây", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hệ thống lạnh NH₃ rò rỉ, không có cảm biến khí, phòng máy lạnh kín không thông gió", "score": 3, "risk": "critical"},
    ]},
    # TF07
    {"text": "Bề mặt vỏ máy, ổ bi, hộp số hoặc các bộ phận chuyển động có nóng hơn bình thường khi chạm tay vào không?", "options": [
        {"key": "A", "text": "Không có hiện tượng nóng bất thường, nhiệt độ vỏ máy trong phạm vi cho phép", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Một số vị trí ấm hơn bình thường nhưng chưa đến mức bỏng tay, đã lưu ý theo dõi", "score": 1, "risk": "low"},
        {"key": "C", "text": "Ổ bi, hộp số nóng rõ rệt khi chạm, có mùi dầu cháy nhẹ nhưng vẫn vận hành", "score": 2, "risk": "high"},
        {"key": "D", "text": "Vỏ máy nóng bỏng tay, có khói hoặc mùi khét rõ rệt từ ổ bi/hộp số, vẫn chưa dừng máy", "score": 3, "risk": "critical"},
    ]},
    # TF08
    {"text": "Máy móc có phát ra tiếng kêu lạ (rít, gõ, lục cục) hoặc rung động mạnh hơn bình thường gần đây không?", "options": [
        {"key": "A", "text": "Máy hoạt động êm ái, không có tiếng kêu lạ hay rung động bất thường", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thỉnh thoảng có tiếng kêu nhẹ khi khởi động, hết khi chạy ổn định", "score": 1, "risk": "low"},
        {"key": "C", "text": "Máy phát tiếng rít hoặc gõ liên tục khi vận hành, rung lắc mạnh hơn trước", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tiếng kêu va đập mạnh, rung động dữ dội làm lỏng bu lông, đã lâu nhưng chưa sửa chữa", "score": 3, "risk": "critical"},
    ]},
    # TF09
    {"text": "Có vết dầu mỡ nhỏ giọt xuống sàn hoặc bám trên vỏ máy, ống dẫn dầu không?", "options": [
        {"key": "A", "text": "Không có vết dầu rò rỉ, sàn nhà xưởng sạch, máy móc khô ráo", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có vết dầu nhỏ tại khớp nối nhưng đã dùng khay hứng và lau dọn thường xuyên", "score": 1, "risk": "low"},
        {"key": "C", "text": "Dầu mỡ nhỏ giọt xuống sàn tạo vũng nhỏ, chưa xử lý, sàn trơn trượt", "score": 2, "risk": "high"},
        {"key": "D", "text": "Dầu rò rỉ nhiều, bám trên vỏ máy và ống dẫn, sàn dính dầu loang rộng gần nguồn nhiệt", "score": 3, "risk": "critical"},
    ]},
    # TF10
    {"text": "Hệ thống thủy lực và khí nén có dấu hiệu rò rỉ áp lực, ống dẫn mòn hoặc khớp nối lỏng không?", "options": [
        {"key": "A", "text": "Không có hệ thống thủy lực/khí nén; hoặc có, ống dẫn tốt, khớp nối chắc, không rò rỉ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Hệ thống hoạt động ổn, có 1-2 khớp nối rỉ nhẹ đã được siết lại", "score": 1, "risk": "low"},
        {"key": "C", "text": "Ống dẫn thủy lực cũ, một số đoạn mòn mỏng, khớp nối lỏng gây rò rỉ dầu áp lực", "score": 2, "risk": "high"},
        {"key": "D", "text": "Ống thủy lực phồng rộp có nguy cơ vỡ, dầu áp lực phun ra khi vận hành, rất nguy hiểm", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 5: Tác động thiên nhiên — 10 câu (NA01–NA10) =======
GROUP5_QUESTIONS = [
    # NA01
    {"text": "Cơ sở có hệ thống chống sét trực tiếp và chống sét lan truyền (surge protection) không?", "options": [
        {"key": "A", "text": "Có chống sét trực tiếp (kim thu lôi) và chống sét lan truyền đầy đủ, kiểm tra định kỳ hàng năm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có chống sét trực tiếp nhưng chưa lắp chống sét lan truyền cho hệ thống điện/mạng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có hệ thống chống sét nhưng lâu chưa kiểm tra, điện trở tiếp địa không rõ có đạt không", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bất kỳ hệ thống chống sét nào, cơ sở ở vùng hay bị sét đánh", "score": 3, "risk": "critical"},
    ]},
    # NA02
    {"text": "Cơ sở có các yếu tố làm tăng nguy cơ cháy trong điều kiện nắng nóng, khô hanh không?", "options": [
        {"key": "A", "text": "Cơ sở xây dựng bằng vật liệu không cháy, nằm trong khu đô thị, không gần cây cối khô", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có một số vật liệu dễ cháy ngoài trời nhưng được che chắn và quản lý", "score": 1, "risk": "low"},
        {"key": "C", "text": "Mái nhà bằng lá, gỗ hoặc tôn nhựa, xung quanh có cỏ khô và cây dễ cháy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Cơ sở xây bằng vật liệu dễ cháy, nằm gần rừng/đồng cỏ khô, vùng nắng nóng kéo dài", "score": 3, "risk": "critical"},
    ]},
    # NA03
    {"text": "Cơ sở có biện pháp PCCC ứng phó với gió lớn, bão và điều kiện thời tiết cực đoan không?", "options": [
        {"key": "A", "text": "Có kế hoạch ứng phó bão, chằng chống mái, ngắt điện khi bão, cố định trang thiết bị ngoài trời", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nhắc nhở chung nhưng chưa có kế hoạch văn bản chi tiết cho từng kịch bản", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không có kế hoạch ứng phó, mái tôn lỏng lẻo, biển quảng cáo chưa chằng chống", "score": 2, "risk": "high"},
        {"key": "D", "text": "Cơ sở ở vùng bão thường xuyên, mái yếu có nguy cơ bay tốc làm đứt dây điện, chưa có biện pháp", "score": 3, "risk": "critical"},
    ]},
    # NA04
    {"text": "Cơ sở có nguy cơ bị ảnh hưởng bởi cháy rừng, cháy đồng cỏ hoặc hỏa hoạn lan từ khu vực lân cận không?", "options": [
        {"key": "A", "text": "Cơ sở nằm trong khu đô thị, không gần rừng, có tường rào ngăn cách với bên ngoài", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Gần khu vực đồi núi nhưng có đường ngăn lửa và khoảng cách an toàn với cây rừng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Gần bìa rừng hoặc đồng cỏ, không có đường ngăn lửa, mùa khô có nguy cơ cháy lan", "score": 2, "risk": "high"},
        {"key": "D", "text": "Nằm trong/giáp rừng, vùng thường xuyên cháy rừng mùa khô, không có biện pháp phòng ngừa", "score": 3, "risk": "critical"},
    ]},
    # NA05
    {"text": "Trong mùa khô hanh, cơ sở có biện pháp kiểm soát tĩnh điện tích tụ trên thiết bị và vật liệu không?", "options": [
        {"key": "A", "text": "Có biện pháp kiểm soát tĩnh điện: nối đất thiết bị, dùng sơn/tấm chống tĩnh điện, kiểm soát độ ẩm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thiết bị chính có nối đất, nhưng chưa kiểm soát tĩnh điện trên vật liệu di chuyển", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không có biện pháp chống tĩnh điện, thường xuyên bị giật tĩnh điện khi chạm thiết bị", "score": 2, "risk": "high"},
        {"key": "D", "text": "Có hơi khí/bụi dễ cháy mà không kiểm soát tĩnh điện, đã từng phát tia lửa tĩnh điện", "score": 3, "risk": "critical"},
    ]},
    # NA06
    {"text": "Cơ sở có nằm trong vùng thấp, hầm ngầm hoặc tầng 1 có nguy cơ ngập nước không? Hệ thống điện có được bảo vệ khỏi ngập nước không?", "options": [
        {"key": "A", "text": "Cơ sở ở vùng cao, không ngập; hoặc tủ điện đặt trên cao, hệ thống điện chống ngập đúng chuẩn", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Vùng thỉnh thoảng ngập nhẹ, tủ điện đặt trên cao nhưng ổ cắm tầng trệt chưa có nắp chống nước", "score": 1, "risk": "low"},
        {"key": "C", "text": "Vùng hay ngập, tủ điện đặt thấp dưới 1m, dây điện đi sát sàn có nguy cơ chập khi ngập", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tầng hầm có thiết bị điện, không có bơm thoát nước, đã từng bị ngập gây chập điện", "score": 3, "risk": "critical"},
    ]},
    # NA07
    {"text": "Trong những ngày nắng nóng cực đoan (trên 38°C), cơ sở có tăng cường biện pháp PCCC không?", "options": [
        {"key": "A", "text": "Có kế hoạch mùa nóng: tăng tần suất kiểm tra điện, hạn chế nguồn lửa, bố trí trực PCCC 24/7", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nhắc nhở chung về PCCC trong mùa nóng nhưng không có văn bản kế hoạch cụ thể", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không tăng cường biện pháp gì, mùa nóng vẫn vận hành như bình thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "Mùa nóng thiết bị chạy quá tải do ĐHKK, không tăng cường PCCC, không kiểm tra điện", "score": 3, "risk": "critical"},
    ]},
    # NA08
    {"text": "Cơ sở có dấu hiệu chuột, kiến hoặc côn trùng xâm nhập vào tủ điện, hộp nối dây không?", "options": [
        {"key": "A", "text": "Tủ điện kín, không có dấu hiệu côn trùng xâm nhập, có biện pháp chống chuột định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thỉnh thoảng thấy côn trùng nhỏ gần tủ điện nhưng chưa phát hiện xâm nhập bên trong", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đã phát hiện chuột gặm dây điện hoặc kiến lửa làm tổ trong hộp nối, chưa xử lý triệt để", "score": 2, "risk": "high"},
        {"key": "D", "text": "Chuột thường xuyên gặm nát vỏ dây điện, đã xảy ra chập do chuột, chưa khắc phục", "score": 3, "risk": "critical"},
    ]},
    # NA09
    {"text": "Các thiết bị điện ngoài trời (tủ điện ngoài trời, cáp điện, đèn chiếu sáng) có dấu hiệu gỉ sét, ăn mòn hoặc vỡ vỏ bảo vệ không?", "options": [
        {"key": "A", "text": "Thiết bị ngoài trời đạt cấp IP65, vỏ inox/composite, không gỉ sét, kiểm tra định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Một số thiết bị bắt đầu gỉ sét nhẹ bên ngoài nhưng vỏ bảo vệ còn nguyên vẹn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Vỏ tủ điện ngoài trời bị thủng, nắp hộp nối dây bị vỡ, dây cáp lộ lõi do gỉ mòn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thiết bị điện ngoài trời hư hỏng nghiêm trọng, nước mưa xâm nhập vào tủ điện gây chập", "score": 3, "risk": "critical"},
    ]},
    # NA10
    {"text": "Bụi mịn từ môi trường (bụi xi măng, bụi kim loại, bụi than) có tích tụ trên thiết bị điện và hệ thống PCCC không?", "options": [
        {"key": "A", "text": "Thiết bị điện và hệ thống PCCC được vệ sinh định kỳ, không tích tụ bụi đáng kể", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lớp bụi mỏng trên một số thiết bị nhưng vệ sinh hàng tháng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bụi tích dày trên tủ điện, ổ cắm, đầu báo khói, ảnh hưởng tản nhiệt và phát hiện cháy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Bụi dẫn điện (bụi kim loại, than) phủ dày trên thanh dẫn điện, có nguy cơ chập và nổ bụi", "score": 3, "risk": "critical"},
    ]},
]
# ======= GROUP 6: Tự cháy — 10 câu (SC01–SC10) =======
GROUP6_QUESTIONS = [
    # SC01
    {"text": "Cơ sở có bảo quản các vật liệu có khả năng tự cháy (dầu lanh, than non, vải dính dầu, phân bón có nitrat) không?", "options": [
        {"key": "A", "text": "Không có vật liệu tự cháy; hoặc bảo quản đúng cách: thông thoáng, kiểm tra nhiệt độ định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có một lượng nhỏ, bảo quản trong kho riêng thông gió nhưng chưa kiểm tra nhiệt độ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có lưu trữ vật liệu tự cháy chất đống lớn, kho thông gió kém, chưa theo dõi nhiệt", "score": 2, "risk": "high"},
        {"key": "D", "text": "Vật liệu tự cháy số lượng lớn chất đống trong kho kín, không thông gió, không giám sát", "score": 3, "risk": "critical"},
    ]},
    # SC02
    {"text": "Tại cơ sở có phát sinh bụi hữu cơ (bụi gỗ, bụi ngũ cốc, bụi đường, bụi nhôm) trong quá trình sản xuất không?", "options": [
        {"key": "A", "text": "Không phát sinh bụi hữu cơ; hoặc có hệ thống hút bụi công nghiệp, vệ sinh định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bụi nhưng vệ sinh hàng ngày, không tích tụ dày trên máy móc và sàn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bụi tích tụ dày trên máy, tường, trần, không có hệ thống hút bụi", "score": 2, "risk": "high"},
        {"key": "D", "text": "Bụi lơ lửng dày đặc tạo mây bụi khi sản xuất, có nguy cơ nổ bụi, không thông gió", "score": 3, "risk": "critical"},
    ]},
    # SC03
    {"text": "Cơ sở có bảo quản phân bón Amoni Nitrat (AN), oxy già (H₂O₂), hoặc các hóa chất tự phản ứng/tự oxy hóa không?", "options": [
        {"key": "A", "text": "Không có hóa chất tự phản ứng; hoặc bảo quản đúng SDS, kho riêng, tách biệt chất không tương thích", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lượng nhỏ, bảo quản trong tủ chuyên dụng nhưng chưa tách riêng theo tính tương thích", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hóa chất oxy hóa để chung với vật liệu dễ cháy, không có kho riêng biệt", "score": 2, "risk": "high"},
        {"key": "D", "text": "Khối lượng lớn AN hoặc chất oxy hóa mạnh bảo quản không đúng, gần nguồn nhiệt, không giám sát", "score": 3, "risk": "critical"},
    ]},
    # SC04
    {"text": "Bột màu, pigment hoặc sơn bột công nghiệp được bảo quản và xử lý như thế nào tại cơ sở?", "options": [
        {"key": "A", "text": "Không có sơn bột/pigment; hoặc bảo quản trong khu vực chuyên dụng, hút bụi tốt, thiết bị Ex", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có sơn bột, bảo quản trong thùng kín, khu vực thông gió nhưng chưa có thiết bị phòng nổ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Sơn bột rơi vãi trên sàn, tích tụ trên máy, không vệ sinh thường xuyên", "score": 2, "risk": "high"},
        {"key": "D", "text": "Bụi sơn bột phát tán dày đặc, không hút bụi, thiết bị điện thường phát tia lửa", "score": 3, "risk": "critical"},
    ]},
    # SC05
    {"text": "Cơ sở có bảo quản than củi, than đá, pellet gỗ hoặc biomass không? Đống than có được kiểm soát nhiệt độ không?", "options": [
        {"key": "A", "text": "Không có than/biomass; hoặc bảo quản đống nhỏ nơi thoáng, có đo nhiệt độ bên trong đống", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bảo quản, đống vừa phải, kho thông thoáng nhưng chưa đo nhiệt bên trong đống", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chất đống lớn trong kho kín, không kiểm tra nhiệt, chưa phát hiện nóng bất thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đống than/biomass lớn đã tự nóng, bốc khói hoặc có mùi cháy nhưng chưa xử lý", "score": 3, "risk": "critical"},
    ]},
    # SC06
    {"text": "Cơ sở có bảo quản phân hữu cơ, xác bã nông sản, hoặc chất thải hữu cơ ủ đống lớn không?", "options": [
        {"key": "A", "text": "Không có chất thải hữu cơ ủ đống; hoặc ủ đúng kỹ thuật, có đảo trộn, kiểm soát nhiệt độ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có ủ phân hữu cơ quy mô nhỏ, ngoài trời, đảo trộn không thường xuyên", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chất thải hữu cơ chất đống lớn không xử lý, trong khu vực kín, bốc mùi nóng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đống ủ lớn tự phát nhiệt, đã bốc khói hoặc âm ỉ cháy nhưng chưa dập tắt", "score": 3, "risk": "critical"},
    ]},
    # SC07
    {"text": "Cơ sở có sử dụng hoặc lưu trữ dầu thực vật, mỡ động vật, dầu cá số lượng lớn không?", "options": [
        {"key": "A", "text": "Không lưu trữ dầu mỡ số lượng lớn; hoặc bảo quản trong thùng kín, kho mát thông gió", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lưu trữ, thùng kín nơi mát nhưng giẻ lau dính dầu chưa xử lý đúng cách", "score": 1, "risk": "low"},
        {"key": "C", "text": "Giẻ lau dính dầu thực vật chất đống, thùng dầu hở nắp trong kho nóng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Giẻ lau dính dầu ăn vứt bừa bãi gần nguồn nhiệt, đã có hiện tượng nóng hoặc bốc khói", "score": 3, "risk": "critical"},
    ]},
    # SC08
    {"text": "Các thiết bị dùng pin lithium (laptop, điện thoại, xe điện, máy bay không người lái) được sạc và bảo quản như thế nào?", "options": [
        {"key": "A", "text": "Sạc tại nơi thông thoáng, dùng sạc chính hãng, không sạc qua đêm không giám sát, pin không phồng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Sạc trong nhà, dùng sạc chính hãng, thỉnh thoảng sạc qua đêm nhưng nơi thoáng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Sạc nhiều thiết bị cùng lúc trong phòng kín, dùng sạc không chính hãng, pin một số cái phồng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Pin lithium phồng vẫn sử dụng, sạc qua đêm trong phòng ngủ kín, dùng sạc kém chất lượng", "score": 3, "risk": "critical"},
    ]},
    # SC09
    {"text": "Cơ sở có bảo quản hóa chất phản ứng mạnh với nước (natri kim loại, canxi cacbua, thuốc tím) không?", "options": [
        {"key": "A", "text": "Không có hóa chất phản ứng với nước; hoặc bảo quản trong tủ chống ẩm, cách xa nguồn nước", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lượng nhỏ, bảo quản trong tủ kín nhưng chưa có biện pháp chống ẩm chuyên dụng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hóa chất phản ứng với nước để gần khu vực ẩm ướt, gần ống nước hoặc bồn rửa", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hóa chất phản ứng mạnh với nước bảo quản trong kho bị dột, gần họng nước chữa cháy", "score": 3, "risk": "critical"},
    ]},
    # SC10
    {"text": "Rơm rạ, trấu, vỏ cà phê hoặc bã mía tại cơ sở được bảo quản và xử lý như thế nào sau mùa thu hoạch?", "options": [
        {"key": "A", "text": "Không có rơm rạ/trấu; hoặc bảo quản khô, đống nhỏ, nơi thoáng, có kiểm tra nhiệt định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Bảo quản trong kho thoáng, đống vừa phải nhưng chưa kiểm tra nhiệt bên trong", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chất đống lớn ngoài trời không che chắn, ẩm ướt sau mưa, không kiểm soát", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đống rơm/trấu lớn đã ẩm mục tự phát nhiệt, bốc hơi nóng, gần nhà dân hoặc kho hàng", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 7: Tai nạn giao thông (phương tiện cơ giới) — 10 câu (TA01–TA10) =======
GROUP7_QUESTIONS = [
    # TA01
    {"text": "Khu vực đỗ xe (ô tô, xe máy) trong cơ sở có tiềm ẩn nguy cơ cháy nổ không?", "options": [
        {"key": "A", "text": "Bãi đỗ xe riêng biệt, có hệ thống báo cháy, sprinkler (nếu trong nhà), cách xa khu sản xuất/kho", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Đỗ xe trong sân chung nhưng xa kho hàng, có bình chữa cháy gần bãi xe", "score": 1, "risk": "low"},
        {"key": "C", "text": "Xe đỗ trong tầng 1 nhà ở, gần cầu thang, gần hàng hóa dễ cháy, không có PCCC", "score": 2, "risk": "high"},
        {"key": "D", "text": "Nhiều xe máy/ô tô đỗ trong nhà kho, tầng hầm chật, chắn lối thoát nạn, không có PCCC", "score": 3, "risk": "critical"},
    ]},
    # TA02
    {"text": "Cơ sở có nằm gần đường vận chuyển hàng hóa nguy hiểm (xe bồn xăng dầu, xe chở gas, xe hóa chất) không? Có biện pháp phòng ngừa gì?", "options": [
        {"key": "A", "text": "Không gần đường vận chuyển hàng nguy hiểm; hoặc có tường rào, dải cách ly an toàn", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Gần đường có xe bồn đi qua nhưng có hàng rào và khoảng cách ≥ 10m", "score": 1, "risk": "low"},
        {"key": "C", "text": "Sát đường xe bồn xăng dầu thường đi, không có rào chắn hay dải cách ly", "score": 2, "risk": "high"},
        {"key": "D", "text": "Cơ sở nằm sát ngã tư/cua gấp trên đường xe bồn, đã có tai nạn xe bồn gần đó", "score": 3, "risk": "critical"},
    ]},
    # TA03
    {"text": "Xe cứu hỏa có thể tiếp cận nhanh và thuận tiện vào cơ sở khi xảy ra sự cố không?", "options": [
        {"key": "A", "text": "Đường vào rộng ≥ 3,5m, xe cứu hỏa vào tận nơi, có bãi quay xe, họng tiếp nước sẵn", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Đường vào đủ rộng cho xe cứu hỏa nhưng đôi khi bị xe đậu hai bên thu hẹp", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đường vào hẹp (< 3,5m), xe cứu hỏa phải đỗ ngoài đường chính, kéo vòi vào xa", "score": 2, "risk": "high"},
        {"key": "D", "text": "Cơ sở trong ngõ hẻm sâu, xe cứu hỏa không thể tiếp cận, không có nguồn nước gần", "score": 3, "risk": "critical"},
    ]},
    # TA04
    {"text": "Xe cơ giới (ô tô, xe tải, xe nâng) đậu trong nhà xưởng hoặc kho có dấu hiệu rò rỉ nhiên liệu không?", "options": [
        {"key": "A", "text": "Xe không đậu trong kho/xưởng; hoặc kiểm tra rò rỉ trước khi vào, sàn sạch không vết dầu", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Xe đậu trong nhà xưởng, kiểm tra định kỳ, chưa phát hiện rò rỉ nhiên liệu", "score": 1, "risk": "low"},
        {"key": "C", "text": "Phát hiện vết dầu loang dưới xe trong kho nhưng chưa xác định nguồn rò rỉ", "score": 2, "risk": "high"},
        {"key": "D", "text": "Xe rò rỉ nhiên liệu rõ ràng, vẫn đậu trong kho hàng dễ cháy, mùi xăng trong nhà kho", "score": 3, "risk": "critical"},
    ]},
    # TA05
    {"text": "Xe nâng, xe đẩy hoặc phương tiện nội bộ có thường xuyên va chạm vào kệ hàng, tường, hoặc thiết bị không?", "options": [
        {"key": "A", "text": "Có lối đi riêng cho xe nâng, bollard bảo vệ kệ hàng và thiết bị, tài xế có chứng chỉ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Lối đi đủ rộng, thỉnh thoảng va quẹt nhẹ kệ hàng nhưng không gây hư hại", "score": 1, "risk": "low"},
        {"key": "C", "text": "Xe nâng hay va chạm kệ hàng làm nghiêng, đã từng đổ hàng hóa lên thiết bị điện", "score": 2, "risk": "high"},
        {"key": "D", "text": "Xe nâng va chạm mạnh vào ống gas, đường ống dẫn hoặc tủ điện, gây hư hại nghiêm trọng", "score": 3, "risk": "critical"},
    ]},
    # TA06
    {"text": "Nhiên liệu và dầu nhớt dự trữ cho đội xe của cơ sở được bảo quản như thế nào?", "options": [
        {"key": "A", "text": "Kho nhiên liệu riêng biệt, tường chống cháy, biển cấm lửa, hệ thống chống tràn, bình chữa cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Để trong khu vực riêng ngoài trời, thùng có nắp kín, xa nguồn nhiệt", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thùng dầu nhớt để trong nhà xưởng chung, gần thiết bị điện và máy móc", "score": 2, "risk": "high"},
        {"key": "D", "text": "Xăng dầu để trong can nhựa hở, trong garage chung với nhiều xe, gần ổ cắm điện", "score": 3, "risk": "critical"},
    ]},
    # TA07
    {"text": "Hệ thống điện và cầu chì của phương tiện cơ giới trong đội xe có được kiểm tra bảo dưỡng định kỳ không?", "options": [
        {"key": "A", "text": "Kiểm tra hệ thống điện xe theo lịch bảo dưỡng, cầu chì đúng ampe, dây điện không hở", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Bảo dưỡng định kỳ theo km nhưng chưa kiểm tra chuyên sâu hệ thống điện", "score": 1, "risk": "low"},
        {"key": "C", "text": "Xe cũ, hệ thống điện chưa kiểm tra lâu, cầu chì thay bằng dây đồng nghiệp dư", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hệ thống điện xe hỏng nặng, dây điện chạm chập, đã có hiện tượng khói/tia lửa từ khoang điện", "score": 3, "risk": "critical"},
    ]},
    # TA08
    {"text": "Khu vực rửa xe và bảo dưỡng xe có tuân thủ quy định phòng cháy không?", "options": [
        {"key": "A", "text": "Không có khu rửa xe/bảo dưỡng; hoặc có, sàn chống trơn, thoát nước tốt, bình chữa cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có khu bảo dưỡng riêng, có bình chữa cháy nhưng sàn đôi khi dính dầu nhớt", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bảo dưỡng xe ngay trong kho/xưởng, sàn dính dầu, giẻ lau dầu vứt bừa bãi", "score": 2, "risk": "high"},
        {"key": "D", "text": "Rửa xe bằng xăng/dung môi trong nhà kín, không thông gió, không bình chữa cháy", "score": 3, "risk": "critical"},
    ]},
    # TA09
    {"text": "Xe bồn chở xăng dầu hoặc xe chở khí gas của cơ sở có được kiểm tra bình áp lực và van an toàn định kỳ không?", "options": [
        {"key": "A", "text": "Không có xe bồn/xe gas; hoặc có, kiểm định đúng hạn, van an toàn hoạt động, dây tiếp địa đủ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Xe kiểm định còn hạn nhưng dây tiếp địa chống tĩnh điện chưa kiểm tra gần đây", "score": 1, "risk": "low"},
        {"key": "C", "text": "Xe bồn quá hạn kiểm định nhưng vẫn hoạt động, van an toàn lâu chưa thử", "score": 2, "risk": "high"},
        {"key": "D", "text": "Xe bồn cũ nát, rò rỉ xăng dầu, van an toàn hỏng, không kiểm định, vẫn vận hành", "score": 3, "risk": "critical"},
    ]},
    # TA10
    {"text": "Khu vực đỗ xe ban đêm có được kiểm tra trước khi nhân viên rời cơ sở không?", "options": [
        {"key": "A", "text": "Có kiểm tra bãi xe cuối ngày: rò rỉ nhiên liệu, ngắt điện sạc, khóa cổng, camera giám sát", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Bảo vệ tuần tra bãi xe nhưng không có checklist kiểm tra cụ thể về PCCC", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không kiểm tra bãi xe ban đêm, xe đỗ qua đêm không ai giám sát", "score": 2, "risk": "high"},
        {"key": "D", "text": "Bãi xe trong tầng hầm/kho, không camera, không tuần tra, không PCCC, khóa cửa kín", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 8: Nguyên nhân khác / Rủi ro bổ sung — 10 câu (OR01–OR10) =======
GROUP8_QUESTIONS = [
    # OR01
    {"text": "Cơ sở có các biện pháp bảo mật vật lý để ngăn ngừa hành vi phóng hỏa cố ý không?", "options": [
        {"key": "A", "text": "Có camera giám sát 24/7, bảo vệ trực, hàng rào/cổng kín, chiếu sáng an ninh ngoài trời", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có camera và khóa cổng nhưng không có bảo vệ trực ngoài giờ làm việc", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không có camera, cổng lỏng lẻo, người lạ có thể xâm nhập khuôn viên dễ dàng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Khuôn viên mở, không bảo mật, đã có dấu hiệu bị đe dọa hoặc phá hoại", "score": 3, "risk": "critical"},
    ]},
    # OR02
    {"text": "Cơ sở lân cận (hàng xóm, cơ sở cùng khu công nghiệp) có mang lại rủi ro cháy lan sang cơ sở của bạn không?", "options": [
        {"key": "A", "text": "Có tường ngăn cháy với cơ sở bên cạnh, khoảng cách an toàn đủ theo quy định", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Liền kề nhưng cơ sở bên cạnh có hoạt động ít nguy cơ cháy (văn phòng, trường học)", "score": 1, "risk": "low"},
        {"key": "C", "text": "Liền kề cơ sở có nguy cơ cháy cao (kho hàng, xưởng gỗ) mà không có tường ngăn cháy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Sát nhà hàng xóm kinh doanh xăng dầu, gas hoặc hóa chất, mái nhà thông nhau", "score": 3, "risk": "critical"},
    ]},
    # OR03
    {"text": "Mức độ nhận thức và ý thức về an toàn PCCC của toàn thể nhân viên tại cơ sở như thế nào?", "options": [
        {"key": "A", "text": "100% nhân viên được đào tạo PCCC, biết dùng bình chữa cháy, biết lối thoát, số 114", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Phần lớn nhân viên biết cơ bản, một số nhân viên mới chưa được đào tạo", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhân viên ít quan tâm PCCC, không biết vị trí bình chữa cháy và lối thoát nạn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Nhân viên hoàn toàn không có kiến thức PCCC, chưa từng được phổ biến hay đào tạo", "score": 3, "risk": "critical"},
    ]},
    # OR04
    {"text": "Cơ sở có đang hoặc vừa trải qua quá trình xây dựng, sửa chữa, cải tạo không? Công tác PCCC trong thời gian thi công được quản lý như thế nào?", "options": [
        {"key": "A", "text": "Không có thi công; hoặc có, đã thông báo Cảnh sát PCCC, có phương án PCCC tạm thời", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Đang sửa chữa nhỏ, có bình chữa cháy tại khu vực thi công nhưng chưa thông báo PCCC", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đang cải tạo lớn, hệ thống PCCC bị ngắt tạm thời, chưa có biện pháp bù đắp", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thi công trong khi vẫn hoạt động, PCCC bị vô hiệu hóa, hàn cắt không kiểm soát", "score": 3, "risk": "critical"},
    ]},
    # OR05
    {"text": "Rác thải, vật liệu phế phẩm và phế liệu có tích tụ tại cơ sở mà không được thu gom kịp thời không?", "options": [
        {"key": "A", "text": "Thu gom rác hàng ngày, phế liệu xử lý kịp thời, khu vực rác sạch sẽ, thùng có nắp", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thu gom 2-3 ngày/lần, có thùng chứa nhưng đôi khi đầy tràn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Rác phế liệu tích tụ thành đống trong góc xưởng, chưa xử lý nhiều ngày", "score": 2, "risk": "high"},
        {"key": "D", "text": "Phế liệu dễ cháy chất đống lớn, gần nguồn nhiệt/điện, lâu ngày không thu gom", "score": 3, "risk": "critical"},
    ]},
    # OR06
    {"text": "Nhà thầu phụ, kỹ thuật viên bên ngoài hoặc nhân viên giao hàng vào cơ sở có được phổ biến quy tắc PCCC không?", "options": [
        {"key": "A", "text": "Có quy trình phổ biến PCCC bắt buộc cho người ngoài, đăng ký ra vào, có nhân viên đi kèm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nhắc nhở cơ bản nhưng không có quy trình chính thức, không đăng ký", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhà thầu ra vào tự do, không phổ biến PCCC, tự ý hàn cắt khi cần", "score": 2, "risk": "high"},
        {"key": "D", "text": "Nhà thầu mang thiết bị phát lửa vào khu vực nguy hiểm, không ai kiểm soát", "score": 3, "risk": "critical"},
    ]},
    # OR07
    {"text": "Trong các dịp lễ hội, sự kiện hoặc mùa tăng ca cao điểm, cơ sở có điều chỉnh biện pháp PCCC không?", "options": [
        {"key": "A", "text": "Tăng cường trực PCCC, kiểm tra điện trước sự kiện, bổ sung bình chữa cháy, giới hạn người", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nhắc nhở chung nhưng không tăng cường trực hay kiểm tra thêm", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không điều chỉnh, thêm đèn trang trí gây quá tải điện, lối thoát bị thu hẹp do đông người", "score": 2, "risk": "high"},
        {"key": "D", "text": "Sự kiện đông nghịt vượt sức chứa, đèn trang trí bịt kín lối thoát, không ai phụ trách PCCC", "score": 3, "risk": "critical"},
    ]},
    # OR08
    {"text": "Nhân viên có sử dụng điện thoại hoặc sạc pin cá nhân trong khu vực nguy hiểm hoặc kho hàng không?", "options": [
        {"key": "A", "text": "Cấm sử dụng và sạc thiết bị cá nhân trong khu nguy hiểm/kho, có biển cấm, có chế tài", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Cho phép sử dụng điện thoại nhưng cấm sạc pin trong kho hàng và khu nguy hiểm", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhân viên tự ý sạc pin trong kho hàng, cắm vào ổ cắm không được phép", "score": 2, "risk": "high"},
        {"key": "D", "text": "Sạc nhiều điện thoại cùng lúc bằng ổ cắm tạm trong kho hàng dễ cháy, sạc qua đêm", "score": 3, "risk": "critical"},
    ]},
    # OR09
    {"text": "Phòng máy chủ (server room) hoặc phòng điều khiển của cơ sở có được bảo vệ PCCC chuyên dụng không?", "options": [
        {"key": "A", "text": "Có hệ thống chữa cháy khí sạch, báo cháy sớm, kiểm soát ra vào, ĐHKK dự phòng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có báo cháy và bình CO₂ riêng, ĐHKK hoạt động nhưng chưa có chữa cháy tự động", "score": 1, "risk": "low"},
        {"key": "C", "text": "Phòng server không có PCCC riêng, chung hệ thống với tòa nhà, nhiều giấy tờ trong phòng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Phòng server không có PCCC, ĐHKK hỏng, nhiệt độ cao, máy chạy quá tải liên tục", "score": 3, "risk": "critical"},
    ]},
    # OR10
    {"text": "Cơ sở có bảo hiểm cháy nổ hợp lệ và kế hoạch khôi phục hoạt động sau sự cố cháy (Business Continuity Plan) không?", "options": [
        {"key": "A", "text": "Có bảo hiểm cháy nổ bắt buộc còn hiệu lực và BCP được lập, cập nhật hàng năm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bảo hiểm cháy nổ nhưng chưa có kế hoạch khôi phục hoạt động sau cháy", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bảo hiểm cháy nổ đã hết hạn hoặc mức bảo hiểm quá thấp so với giá trị tài sản", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bảo hiểm cháy nổ, không có BCP, chưa từng nghĩ đến kịch bản sau cháy", "score": 3, "risk": "critical"},
    ]},
]

ALL_COMMON_QUESTIONS = [
    (0, GROUP1_QUESTIONS),
    (1, GROUP2_QUESTIONS),
    (2, GROUP3_QUESTIONS),
    (3, GROUP4_QUESTIONS),
    (4, GROUP5_QUESTIONS),
    (5, GROUP6_QUESTIONS),
    (6, GROUP7_QUESTIONS),
    (7, GROUP8_QUESTIONS),
]
