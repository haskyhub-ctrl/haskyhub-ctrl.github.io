# seed_data.py — FRAS Question Bank
# Part 1: Categories + Common Questions (Groups 1-8)

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
    {"name": "Sự cố hệ thống, thiết bị điện", "description": "Đánh giá hệ thống dây dẫn, cầu dao, thiết bị điện", "icon": "⚡", "color": "#eab308", "order_index": 1, "max_score": 55},
    {"name": "Sơ suất, bất cẩn dùng lửa/nhiệt", "description": "Đánh giá việc sử dụng bếp gas, hàn cắt, hút thuốc", "icon": "🔥", "color": "#ef4444", "order_index": 2, "max_score": 15},
    {"name": "Vi phạm quy định PCCC", "description": "Đánh giá tuân thủ quy định phòng cháy chữa cháy", "icon": "🛡️", "color": "#f97316", "order_index": 3, "max_score": 10},
    {"name": "Sự cố kỹ thuật (thiết bị, máy móc)", "description": "Đánh giá bảo dưỡng thiết bị, chống sét, thiết bị áp lực", "icon": "⚙️", "color": "#3b82f6", "order_index": 4, "max_score": 7},
    {"name": "Tác động thiên nhiên", "description": "Đánh giá nguy cơ từ vị trí địa lý và thời tiết", "icon": "🌿", "color": "#22c55e", "order_index": 5, "max_score": 4},
    {"name": "Tự cháy", "description": "Đánh giá vật liệu tự phát nhiệt và rác thải hữu cơ", "icon": "🌡️", "color": "#a855f7", "order_index": 6, "max_score": 4},
    {"name": "Tai nạn giao thông (phương tiện cơ giới)", "description": "Đánh giá phương tiện và nhiên liệu dự phòng", "icon": "🚗", "color": "#6366f1", "order_index": 7, "max_score": 3},
    {"name": "Nguyên nhân khác / Rủi ro bổ sung", "description": "Lịch sử sự cố và nguy cơ an ninh", "icon": "⚠️", "color": "#64748b", "order_index": 8, "max_score": 2},
]

# ======= GROUP 1: Hệ thống, thiết bị điện — 14 câu, 55 điểm =======
GROUP1_QUESTIONS = [
    {"text": "Hệ thống dây dẫn điện (dây điện chính, dây nhánh) trong cơ sở của bạn được lắp đặt như thế nào?", "max": 4, "options": [
        {"key": "A", "text": "Dây điện có tiết diện phù hợp tải, luồn trong ống bảo vệ hoặc máng cáp, có nhãn ghi thông số rõ ràng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Dây điện đúng tiết diện nhưng chưa luồn ống bảo vệ ở một số đoạn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Dây điện được nối thêm nhiều lần, dùng băng keo quấn tạm, không rõ tiết diện", "score": 3, "risk": "high"},
        {"key": "D", "text": "Dây điện cũ, vỏ bọc nứt/bong tróc, hoặc không biết tình trạng dây điện", "score": 4, "risk": "critical"},
    ]},
    {"text": "Cầu dao tự động (aptomat/CB) tại cơ sở bạn có được lắp đặt và bảo dưỡng không?", "max": 4, "options": [
        {"key": "A", "text": "Có aptomat đúng dòng định mức cho từng mạch, kiểm tra hoạt động ít nhất 1 lần/năm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có aptomat nhưng không rõ dòng định mức có phù hợp không, chưa từng kiểm tra", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Dùng cầu chì thay aptomat, hoặc aptomat bị hỏng chưa thay", "score": 3, "risk": "high"},
        {"key": "D", "text": "Không có thiết bị bảo vệ ngắt điện tự động nào", "score": 4, "risk": "critical"},
    ]},
    {"text": "Thiết bị chống rò điện (RCCB/ELCB) có được lắp tại cơ sở không?", "max": 4, "options": [
        {"key": "A", "text": "Có lắp RCCB/ELCB cho toàn bộ các mạch điện, kiểm tra định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Chỉ lắp ở một số mạch quan trọng (phòng ẩm ướt, bếp điện)", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Không lắp nhưng biết và có kế hoạch lắp trong thời gian tới", "score": 3, "risk": "high"},
        {"key": "D", "text": "Không lắp và không biết thiết bị này là gì", "score": 4, "risk": "critical"},
    ]},
    {"text": "Hệ thống nối đất bảo vệ (tiếp địa) tại cơ sở bạn:", "max": 4, "options": [
        {"key": "A", "text": "Đã lắp hệ thống tiếp địa đúng tiêu chuẩn, điện trở nối đất đo ≤ 4Ω, có biên bản kiểm tra", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có dây nối đất nhưng chưa đo điện trở, không rõ đạt tiêu chuẩn không", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Chỉ một số thiết bị có nối đất, không đồng bộ", "score": 3, "risk": "high"},
        {"key": "D", "text": "Không có hệ thống nối đất, hoặc không biết cơ sở có nối đất không", "score": 4, "risk": "critical"},
    ]},
    {"text": "Việc sử dụng ổ cắm điện và phích cắm tại cơ sở bạn như thế nào?", "max": 4, "options": [
        {"key": "A", "text": "Dùng đúng loại ổ cắm theo công suất thiết bị, không cắm chung nhiều thiết bị công suất lớn vào 1 ổ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thỉnh thoảng dùng ổ cắm nối dài cắm nhiều thiết bị, nhưng tổng công suất không vượt quá mức", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Thường xuyên dùng nhiều ổ cắm nối dài chồng chéo nhau, cắm cùng lúc nhiều thiết bị", "score": 3, "risk": "high"},
        {"key": "D", "text": "Ổ cắm bị hở, chân cắm bị méo, hoặc không có nắp bảo vệ ở nơi ẩm ướt", "score": 4, "risk": "critical"},
    ]},
    {"text": "Các thiết bị điện có công suất lớn (điều hòa, máy bơm, lò điện, máy hàn…) được quản lý như thế nào?", "max": 4, "options": [
        {"key": "A", "text": "Mỗi thiết bị công suất lớn có mạch điện riêng, aptomat riêng, đúng tiết diện dây", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Một số thiết bị dùng chung mạch điện nhưng không dùng đồng thời", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Nhiều thiết bị công suất lớn dùng chung một mạch điện", "score": 3, "risk": "high"},
        {"key": "D", "text": "Không kiểm soát, thiết bị nào cũng cắm vào ổ điện sẵn có", "score": 4, "risk": "critical"},
    ]},
    {"text": "Thói quen tắt điện và ngắt thiết bị điện khi không sử dụng hoặc khi rời khỏi cơ sở:", "max": 4, "options": [
        {"key": "A", "text": "Luôn tắt điện tất cả thiết bị, rút phích cắm các thiết bị không cần hoạt động liên tục", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Tắt điện những thiết bị chính, một số thiết bị phụ vẫn để chạy", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thường để nhiều thiết bị ở chế độ chờ qua đêm hoặc cuối tuần", "score": 3, "risk": "high"},
        {"key": "D", "text": "Không có quy định về tắt điện, thiết bị chạy liên tục kể cả khi không có người", "score": 4, "risk": "critical"},
    ]},
    {"text": "Kiểm tra, bảo dưỡng định kỳ hệ thống điện tại cơ sở:", "max": 4, "options": [
        {"key": "A", "text": "Có kiểm tra hệ thống điện định kỳ hàng năm bởi đơn vị có chức năng, có biên bản", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Tự kiểm tra nội bộ hàng năm, chưa mời đơn vị chuyên nghiệp", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ kiểm tra khi có sự cố hoặc khi cơ quan chức năng yêu cầu", "score": 3, "risk": "high"},
        {"key": "D", "text": "Chưa từng kiểm tra hệ thống điện kể từ khi lắp đặt", "score": 4, "risk": "critical"},
    ]},
    {"text": "Hệ thống điện tại cơ sở đã sử dụng được bao lâu kể từ lần lắp đặt/cải tạo gần nhất?", "max": 4, "options": [
        {"key": "A", "text": "Dưới 5 năm, lắp đặt mới hoặc cải tạo toàn bộ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Từ 5–10 năm, có cải tạo một phần", "score": 1, "risk": "low"},
        {"key": "C", "text": "Từ 10–20 năm, chưa cải tạo đáng kể", "score": 3, "risk": "high"},
        {"key": "D", "text": "Trên 20 năm hoặc không biết hệ thống điện được lắp đặt từ khi nào", "score": 4, "risk": "critical"},
    ]},
    {"text": "Khu vực lắp đặt tủ điện chính (tủ phân phối điện) tại cơ sở:", "max": 4, "options": [
        {"key": "A", "text": "Tủ điện đặt nơi thông thoáng, khô ráo, không có vật liệu dễ cháy trong vòng 1m, có khóa và biển cảnh báo", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Tủ điện đặt đúng vị trí nhưng xung quanh có để một số vật dụng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Tủ điện đặt gần vật liệu dễ cháy hoặc ở nơi ẩm ướt", "score": 3, "risk": "high"},
        {"key": "D", "text": "Tủ điện đặt trong kho hàng hoặc bị che khuất, khó tiếp cận khi sự cố", "score": 4, "risk": "critical"},
    ]},
    {"text": "Hệ thống dây điện đi qua vách ngăn, tường, sàn nhà được bảo vệ như thế nào?", "max": 4, "options": [
        {"key": "A", "text": "Dây điện qua tường, sàn đều có ống bảo vệ, bịt kín lỗ xuyên tường bằng vật liệu chống cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có ống bảo vệ nhưng một số lỗ xuyên tường chưa được bịt kín", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Dây điện qua tường trực tiếp, không có ống bảo vệ", "score": 3, "risk": "high"},
        {"key": "D", "text": "Dây điện chạy nổi bên ngoài tường, qua khe hở không được bảo vệ", "score": 4, "risk": "critical"},
    ]},
    {"text": "Thiết bị điện trong cơ sở có nguồn gốc xuất xứ và chứng nhận an toàn như thế nào?", "max": 4, "options": [
        {"key": "A", "text": "Thiết bị có nhãn hiệu rõ ràng, chứng nhận hợp quy (CR), mua từ đại lý chính hãng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Phần lớn thiết bị có nhãn hiệu, nhưng một số mua tại chợ điện lẻ", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Nhiều thiết bị không rõ xuất xứ, không có nhãn mác", "score": 3, "risk": "high"},
        {"key": "D", "text": "Chủ yếu dùng thiết bị điện cũ, đã qua sử dụng, không rõ xuất xứ", "score": 4, "risk": "critical"},
    ]},
    {"text": "Tình trạng nhiệt độ của dây điện và thiết bị điện khi đang hoạt động:", "max": 4, "options": [
        {"key": "A", "text": "Không có hiện tượng nóng bất thường, không có mùi khét từ ổ cắm hay thiết bị", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thỉnh thoảng ổ cắm hơi ấm nóng nhưng không thường xuyên", "score": 1, "risk": "low"},
        {"key": "C", "text": "Một số ổ cắm hoặc dây điện thường xuyên nóng ấm khi sử dụng", "score": 3, "risk": "high"},
        {"key": "D", "text": "Đã từng có hiện tượng ổ cắm cháy đen, tóe lửa, hoặc mùi khét", "score": 4, "risk": "critical"},
    ]},
    {"text": "Tại cơ sở có lắp đặt và sử dụng hệ thống điện mặt trời không?", "max": 3, "options": [
        {"key": "A", "text": "Không có hệ thống điện mặt trời", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có hệ thống điện mặt trời, lắp đặt bởi đơn vị có chứng chỉ, có thiết bị chống sét và aptomat riêng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có hệ thống điện mặt trời nhưng không rõ đơn vị lắp đặt có đủ năng lực không", "score": 3, "risk": "high"},
        {"key": "D", "text": "Có hệ thống điện mặt trời lắp đặt không đúng kỹ thuật, không có aptomat riêng", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 2: Sơ suất, bất cẩn dùng lửa/nhiệt — 5 câu, 15 điểm =======
GROUP2_QUESTIONS = [
    {"text": "Việc sử dụng bếp gas, bếp dầu hoặc thiết bị đun nấu dùng nhiên liệu tại cơ sở:", "max": 3, "options": [
        {"key": "A", "text": "Không sử dụng bếp gas/dầu; hoặc có nhưng đặt trong phòng riêng thông thoáng, bình gas để nơi thoáng mát", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có sử dụng bếp gas, bình gas đặt đúng nơi quy định, nhưng chưa lắp van ngắt tự động", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bình gas đặt gần nguồn nhiệt hoặc gần vật liệu dễ cháy, không có quạt hút mùi", "score": 2, "risk": "high"},
        {"key": "D", "text": "Dùng bếp gas ngay trong kho hàng, phòng ngủ, hoặc dùng bếp tự chế", "score": 3, "risk": "critical"},
    ]},
    {"text": "Hành vi đốt hương, đốt vàng mã, thắp nến (nếu có thực hành tín ngưỡng tại cơ sở):", "max": 3, "options": [
        {"key": "A", "text": "Không có thực hành đốt hương/vàng mã tại cơ sở", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có đốt hương/nến nhưng tại nơi cố định, có lư/bát hương chắc chắn, có người giám sát", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đốt vàng mã trong thùng kim loại nhưng đặt gần tường gỗ hoặc vật liệu dễ cháy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đốt vàng mã lộ thiên trong sân kho hàng, hoặc không có người trông coi", "score": 3, "risk": "critical"},
    ]},
    {"text": "Hoạt động hàn cắt kim loại, dùng súng khò lửa tại cơ sở:", "max": 3, "options": [
        {"key": "A", "text": "Không có hoạt động hàn cắt, khò lửa tại cơ sở", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nhưng thực hiện ở khu vực riêng biệt, đã dọn sạch vật liệu dễ cháy, có bình chữa cháy", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có hàn cắt nhưng chưa xin phép, chưa dọn dẹp vật liệu dễ cháy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thường xuyên hàn cắt ngay trong kho hàng, xưởng sản xuất có vật liệu dễ cháy", "score": 3, "risk": "critical"},
    ]},
    {"text": "Hành vi hút thuốc lá trong khuôn viên cơ sở:", "max": 3, "options": [
        {"key": "A", "text": "Cấm hút thuốc hoàn toàn trong toàn bộ cơ sở, có biển cấm, có chế tài xử lý", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Cho phép hút thuốc ở khu vực riêng ngoài trời, xa vật liệu dễ cháy", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hút thuốc trong phòng làm việc, nhà xưởng nhưng không có vật liệu dễ cháy gần đó", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hút thuốc trong kho hàng, xưởng sản xuất hoặc gần khu vực chứa nhiên liệu", "score": 3, "risk": "critical"},
    ]},
    {"text": "Việc xử lý tàn thuốc, tàn than, tro bếp sau khi sử dụng:", "max": 3, "options": [
        {"key": "A", "text": "Tàn thuốc/tàn than luôn được dập tắt hoàn toàn trước khi vứt vào thùng kim loại có nắp", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Vứt tàn thuốc vào thùng rác thông thường nhưng đảm bảo đã tắt hẳn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đôi khi vứt tàn thuốc ra ngoài nền đất nhưng chưa đảm bảo tắt hoàn toàn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thường vứt tàn thuốc còn cháy hoặc tàn than còn âm ỉ gần khu vực có rác", "score": 3, "risk": "critical"},
    ]},
]

# ======= GROUP 3: Vi phạm quy định PCCC — 4 câu, 10 điểm =======
GROUP3_QUESTIONS = [
    {"text": "Cơ sở có đủ trang thiết bị chữa cháy ban đầu theo quy định không?", "max": 3, "options": [
        {"key": "A", "text": "Có đủ số lượng bình chữa cháy theo quy định, còn hạn sử dụng, đặt đúng vị trí", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bình chữa cháy nhưng số lượng chưa đủ hoặc một số bình đã hết hạn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ có 1 bình chữa cháy cho toàn bộ cơ sở có diện tích lớn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có bình chữa cháy nào, hoặc bình đã hết hạn từ lâu", "score": 3, "risk": "critical"},
    ]},
    {"text": "Cơ sở có tổ chức huấn luyện nghiệp vụ PCCC và thoát nạn cho toàn bộ người làm việc không?", "max": 3, "options": [
        {"key": "A", "text": "Tổ chức huấn luyện PCCC định kỳ hàng năm, có biên bản, thực tập phương án chữa cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có tổ chức huấn luyện nhưng không thường xuyên (2–3 năm một lần)", "score": 1, "risk": "low"},
        {"key": "C", "text": "Chỉ phổ biến miệng cho nhân viên mới, chưa tổ chức huấn luyện chính thức", "score": 2, "risk": "high"},
        {"key": "D", "text": "Chưa từng tổ chức bất kỳ hình thức huấn luyện PCCC nào", "score": 3, "risk": "critical"},
    ]},
    {"text": "Cơ sở có Nội quy PCCC được ban hành và niêm yết công khai không?", "max": 2, "options": [
        {"key": "A", "text": "Có nội quy PCCC ban hành văn bản, niêm yết tại cửa ra vào, nơi làm việc, khu vực nguy hiểm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nội quy nhưng chỉ niêm yết ở một vài vị trí", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có nội quy nhưng đã cũ, chưa cập nhật, niêm yết chỗ khó thấy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có nội quy PCCC hoặc chưa từng ban hành", "score": 2, "risk": "critical"},
    ]},
    {"text": "Lối thoát nạn (hành lang, cầu thang thoát hiểm, cửa thoát nạn) có đảm bảo không bị cản trở?", "max": 2, "options": [
        {"key": "A", "text": "Lối thoát nạn luôn thông thoáng, có chiều rộng đúng quy định, có đèn chỉ dẫn hoạt động tốt", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Lối thoát nạn thông thoáng nhưng đèn chỉ dẫn một số đã hỏng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Lối thoát nạn bị thu hẹp do để hàng hóa, vẫn đi được nhưng khó khăn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Lối thoát nạn bị bịt kín, chứa hàng hóa chắn ngang, hoặc cửa thoát nạn bị khóa", "score": 2, "risk": "critical"},
    ]},
]

# ======= GROUP 4: Sự cố kỹ thuật — 3 câu, 7 điểm =======
GROUP4_QUESTIONS = [
    {"text": "Các thiết bị máy móc, động cơ điện, máy nén khí, máy phát điện có được bảo dưỡng định kỳ?", "max": 3, "options": [
        {"key": "A", "text": "Có lịch bảo dưỡng định kỳ theo hướng dẫn nhà sản xuất, có biên bản lưu hồ sơ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Bảo dưỡng theo kinh nghiệm, không có lịch định kỳ, chỉ sửa khi hỏng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thiết bị hoạt động liên tục, ít khi tắt để bảo dưỡng, có rung lắc bất thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thiết bị cũ, xuống cấp nghiêm trọng, chưa bảo dưỡng trong hơn 2 năm", "score": 3, "risk": "critical"},
    ]},
    {"text": "Hệ thống chống sét (thu lôi) của cơ sở có được lắp đặt và kiểm tra không?", "max": 2, "options": [
        {"key": "A", "text": "Có hệ thống chống sét đúng tiêu chuẩn TCVN, kiểm tra điện trở tiếp địa định kỳ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có hệ thống chống sét nhưng chưa kiểm tra điện trở tiếp địa", "score": 2, "risk": "medium"},
        {"key": "C", "text": "Không có hệ thống chống sét, cơ sở là nhà thấp tầng trong khu vực có nhiều công trình cao hơn", "score": 1, "risk": "low"},
        {"key": "D", "text": "Không có hệ thống chống sét, cơ sở là công trình cao nhất hoặc vùng hay bị sét", "score": 2, "risk": "high"},
    ]},
    {"text": "Thiết bị áp lực (bình chứa khí nén, bình gas công nghiệp, nồi hơi…) nếu có:", "max": 2, "options": [
        {"key": "A", "text": "Không có thiết bị áp lực tại cơ sở", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có thiết bị áp lực, đã đăng ký và kiểm định đúng hạn, van an toàn hoạt động tốt", "score": 0, "risk": "safe"},
        {"key": "C", "text": "Có thiết bị áp lực, đã quá hạn kiểm định nhưng vẫn đang sử dụng", "score": 1, "risk": "high"},
        {"key": "D", "text": "Có thiết bị áp lực chưa từng được kiểm định, không rõ nguồn gốc", "score": 2, "risk": "critical"},
    ]},
]

# ======= GROUP 5: Tác động thiên nhiên — 2 câu, 4 điểm =======
GROUP5_QUESTIONS = [
    {"text": "Vị trí địa lý và đặc điểm môi trường xung quanh cơ sở có tiềm ẩn nguy cơ từ thiên nhiên?", "max": 3, "options": [
        {"key": "A", "text": "Cơ sở nằm trong khu đô thị, không gần rừng, không có lịch sử bị sét đánh", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Cơ sở gần khu vực đồi núi hoặc có cây cao, địa hình trống trải dễ bị sét", "score": 1, "risk": "low"},
        {"key": "C", "text": "Cơ sở nằm gần rừng, bãi cỏ khô hoặc trong khu vực từng có cháy do nắng hạn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Cơ sở nằm trong/liền kề khu rừng hoặc vùng thường xuyên có cháy rừng mùa khô", "score": 3, "risk": "critical"},
    ]},
    {"text": "Vào mùa khô hanh (tháng 11 – tháng 4), cơ sở có biện pháp phòng ngừa tăng cường?", "max": 1, "options": [
        {"key": "A", "text": "Có kế hoạch mùa khô cụ thể: tăng cường kiểm tra điện, hạn chế nguồn lửa, trực PCCC", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có nhắc nhở chung về PCCC trong mùa khô nhưng không có kế hoạch văn bản", "score": 0, "risk": "safe"},
        {"key": "C", "text": "Không có biện pháp tăng cường đặc biệt cho mùa khô", "score": 1, "risk": "medium"},
    ]},
]

# ======= GROUP 6: Tự cháy — 2 câu, 4 điểm =======
GROUP6_QUESTIONS = [
    {"text": "Cơ sở có lưu trữ các vật liệu có khả năng tự phát nhiệt hoặc tự bốc cháy không?", "max": 3, "options": [
        {"key": "A", "text": "Không có vật liệu nào có khả năng tự cháy tại cơ sở", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có một số vật liệu nhưng lưu trữ đúng cách: thông thoáng, kiểm tra định kỳ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có lưu trữ vật liệu dễ tự cháy nhưng chất đống lớn, kho không thông thoáng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Có lưu trữ khối lượng lớn vật liệu tự cháy trong kho kín, không thông gió", "score": 3, "risk": "critical"},
    ]},
    {"text": "Rác thải, vật liệu phế phẩm hữu cơ tại cơ sở được xử lý như thế nào?", "max": 1, "options": [
        {"key": "A", "text": "Thu gom và xử lý ngay trong ngày, không để tích tụ qua đêm", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thu gom định kỳ 2–3 ngày/lần, bảo quản trong thùng có nắp ở nơi thông thoáng", "score": 0, "risk": "safe"},
        {"key": "C", "text": "Để tích đống trong góc xưởng, xử lý khi đầy, không có thùng chứa chuyên dụng", "score": 1, "risk": "medium"},
    ]},
]

# ======= GROUP 7: Tai nạn giao thông — 2 câu, 3 điểm =======
GROUP7_QUESTIONS = [
    {"text": "Phương tiện cơ giới có được để trong nhà, kho, xưởng hoặc gần vật liệu dễ cháy?", "max": 2, "options": [
        {"key": "A", "text": "Không có phương tiện cơ giới, hoặc xe được đỗ ngoài trời/bãi riêng xa khu sản xuất", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có phương tiện, đỗ trong nhà xưởng nhưng khu vực đỗ xe có tường ngăn cháy", "score": 1, "risk": "low"},
        {"key": "C", "text": "Phương tiện đỗ trong nhà xưởng chung với khu sản xuất, có xăng dầu gần xe", "score": 2, "risk": "high"},
        {"key": "D", "text": "Phương tiện đỗ trong kho hàng hoặc khu vực có nhiều vật liệu dễ cháy", "score": 2, "risk": "critical"},
    ]},
    {"text": "Bình xăng, can xăng, dầu diesel dự phòng có được bảo quản đúng quy định?", "max": 1, "options": [
        {"key": "A", "text": "Không lưu trữ xăng dầu dự phòng; hoặc có nhưng bảo quản trong kho chuyên dụng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lưu trữ xăng dầu trong can có nắp kín, để ngoài trời hoặc phòng riêng", "score": 0, "risk": "safe"},
        {"key": "C", "text": "Để can xăng trong nhà kho chung hoặc gần thiết bị điện", "score": 1, "risk": "high"},
        {"key": "D", "text": "Để can xăng hở miệng, để ngay trong phòng làm việc hoặc gần nguồn nhiệt", "score": 1, "risk": "critical"},
    ]},
]

# ======= GROUP 8: Nguyên nhân khác — 2 câu, 2 điểm =======
GROUP8_QUESTIONS = [
    {"text": "Cơ sở có lịch sử xảy ra sự cố cháy, nổ, hoặc suýt cháy trong 3 năm gần đây?", "max": 1, "options": [
        {"key": "A", "text": "Chưa từng xảy ra bất kỳ sự cố cháy hoặc suýt cháy nào trong 3 năm qua", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có xảy ra 1 sự cố nhỏ đã được xử lý và khắc phục nguyên nhân", "score": 0, "risk": "safe"},
        {"key": "C", "text": "Có xảy ra 1–2 sự cố, đã xử lý nhưng chưa khắc phục triệt để nguyên nhân", "score": 1, "risk": "high"},
        {"key": "D", "text": "Đã xảy ra nhiều sự cố hoặc 1 vụ cháy gây thiệt hại, chưa phòng ngừa mới", "score": 1, "risk": "critical"},
    ]},
    {"text": "Cơ sở có nằm trong khu vực có nguy cơ an ninh cao hoặc có tranh chấp?", "max": 1, "options": [
        {"key": "A", "text": "Không có nguy cơ an ninh đặc biệt, khu vực trật tự, an ninh tốt", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Khu vực có một số vụ trộm cắp nhưng chưa có vụ phá hoại liên quan cháy nổ", "score": 0, "risk": "safe"},
        {"key": "C", "text": "Đã từng bị đe dọa hoặc có tranh chấp nghiêm trọng, lo ngại phá hoại", "score": 1, "risk": "high"},
        {"key": "D", "text": "Khu vực có tiền lệ cháy do phá hoại cố ý hoặc tranh chấp gay gắt", "score": 1, "risk": "critical"},
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
