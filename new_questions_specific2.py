# === ĐẶC THÙ A: SẢN XUẤT CÔNG NGHIỆP (KCN) - 10 câu ===
SPEC_A = {
    "name": "Đặc thù: Sản xuất công nghiệp",
    "description": "Dấu hiệu nguy cơ cháy nổ cho nhà máy, xưởng sản xuất trong KCN",
    "questions": [
        {"text": "Khu vực sơn, phun sơn có mùi dung môi nồng, hơi dung môi nhìn thấy được trong không khí không?",
         "options": [
            {"key": "A", "text": "Buồng sơn kín có quạt hút, không mùi ngoài buồng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quạt hút nhưng thoáng mùi dung môi lúc mở cửa", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sơn trong xưởng mở, hơi dung môi lan tỏa, mùi nồng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Phun sơn trong phòng kín, không thông gió, nồng độ hơi cao, có ổ cắm thường", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống hút bụi, ống dẫn bụi, silo chứa bụi có tích bụi dày hoặc đã phồng ống không?",
         "options": [
            {"key": "A", "text": "Vệ sinh định kỳ, ống sạch, silo có van xả áp", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Vệ sinh hàng tháng nhưng chưa kiểm tra nguy cơ nổ bụi", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bụi tích dày trong ống, silo chưa có van xả áp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đã phồng ống hoặc cháy nhỏ trong hệ thống hút bụi", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phoi kim loại dính dầu cắt gọt có tích đống gần máy đang chạy hoặc nguồn nhiệt không?",
         "options": [
            {"key": "A", "text": "Phoi thu gom ngay, dầu hứng khay, xử lý hàng ngày", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thu gom cuối ca, dính dầu nhưng lượng nhỏ, xa nguồn nhiệt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Phoi dính dầu tích đống nhiều ngày gần máy đang chạy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Phoi dính dầu chất đống gần khu hàn cắt, đã bốc khói", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện nhà xưởng có dấu hiệu quá tải: dây nóng, CB nhảy thường xuyên?",
         "options": [
            {"key": "A", "text": "Hệ thống đủ tải, dây không nóng, CB không nhảy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đủ tải hiện tại nhưng không còn dự phòng cho máy mới", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thêm nhiều máy mới, CB thỉnh thoảng nhảy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Dây nóng ran khi chạy, CB nhảy phải nối tắt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu nạp axit, pha hóa chất có hơi axit ăn mòn thiết bị điện xung quanh không?",
         "options": [
            {"key": "A", "text": "Không có hóa chất, hoặc có quạt hút cục bộ, thiết bị được bảo vệ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quạt hút nhưng công suất nhỏ, thoáng mùi hóa chất", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không hút hơi, axit bay hơi ăn mòn thiết bị điện gần đó", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hơi axit ăn mòn dây điện và tủ điện, đã gây chập", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thanh nhiệt trong dây chuyền đóng gói có bị kẹt vật liệu (nilon, giấy) gây cháy chảy không?",
         "options": [
            {"key": "A", "text": "Không có thanh nhiệt, hoặc có cảm biến ngắt khi kẹt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hoạt động tốt nhưng chưa có cảm biến ngắt khi kẹt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Vật liệu đôi khi kẹt vào thanh nhiệt gây chảy/cháy nhỏ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thanh nhiệt hỏng tự ngắt, quá nhiệt, đã cháy nhiều lần", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu sạc xe nâng/ắc-quy có thông gió không? Có mùi axit hoặc khí gas không?",
         "options": [
            {"key": "A", "text": "Khu sạc riêng, thông gió tốt, biển cấm lửa", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Khu sạc riêng nhưng thông gió chưa đủ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sạc ngay trong kho hàng, gần hàng dễ cháy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Sạc phòng kín, bộ sạc cũ tóe tia lửa, khí hydro tích tụ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thiết bị gia nhiệt (lò nung, sấy, nhiệt đóng gói) có dấu hiệu quá nhiệt không kiểm soát?",
         "options": [
            {"key": "A", "text": "Có tự ngắt quá nhiệt, nhiệt kế kiểm tra định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có nhiệt kế nhưng chưa hiệu chuẩn gần đây", "score": 1, "risk": "low"},
            {"key": "C", "text": "Điều chỉnh nhiệt bằng tay, không tự ngắt, công nhân canh bằng mắt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thiết bị tự chế, không kiểm soát nhiệt, đã quá nhiệt gây hỏng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Motor quạt tháp giải nhiệt, chiller có rung lắc, nóng bất thường, mùi khét không?",
         "options": [
            {"key": "A", "text": "Không có tháp/chiller, hoặc hoạt động êm, bảo trì tốt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hoạt động bình thường, chưa kiểm tra gần đây", "score": 1, "risk": "low"},
            {"key": "C", "text": "Motor nóng, rung lắc mạnh hơn trước", "score": 2, "risk": "high"},
            {"key": "D", "text": "Motor quá tải thường xuyên, tấm tản nhiệt PVC dễ cháy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Công nhân có nhận biết được dấu hiệu cảnh báo sớm (mùi khét, khói, tiếng lạ) từ quy trình mình làm không?",
         "options": [
            {"key": "A", "text": "Được đào tạo nhận biết dấu hiệu riêng cho từng vị trí", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Được đào tạo PCCC chung, chưa đi sâu dấu hiệu đặc thù", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ quản lý biết, công nhân chưa nhận ra dấu hiệu", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không ai biết dấu hiệu nguy hiểm của quy trình mình làm", "score": 3, "risk": "critical"},
        ]},
    ]
}

# === ĐẶC THÙ B: KHO HÀNG - 7 câu ===
SPEC_B = {
    "name": "Đặc thù: Kho hàng, kho vật liệu",
    "description": "Dấu hiệu nguy cơ cháy nổ cho kho hàng, kho vật liệu",
    "questions": [
        {"text": "Hàng dễ cháy (aerosol, pin lithium, dung môi) có đang để lẫn với hàng thường, không nhãn cảnh báo?",
         "options": [
            {"key": "A", "text": "Khu riêng cho hàng nguy hiểm, biển cảnh báo rõ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Để khu riêng nhưng chưa có biển cảnh báo đầy đủ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng nguy hiểm để chung hàng thường, không nhãn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Pin lithium, aerosol chất đống sát tủ điện, không bảo vệ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Lối đi chính trong kho có đang bị hàng hóa chặn, xe nâng không qua được?",
         "options": [
            {"key": "A", "text": "Lối đi thông suốt ≥2m, kiểm tra hàng ngày", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đôi khi có pallet tạm chiếm chỗ rồi dọn đi", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lối đi bị thu hẹp, xe nâng đi khó, lối thoát hẹp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Lối đi bị chặn hoàn toàn, không thể đi qua khi khẩn cấp", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho ban đêm có hệ thống báo cháy tự động hoặc camera giám sát không?",
         "options": [
            {"key": "A", "text": "Báo cháy tự động, camera nhiệt, kết nối trung tâm 24/7", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Báo cháy có nhưng không camera nhiệt, bảo vệ tuần tra", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ bảo vệ tuần tra, không hệ thống tự động", "score": 2, "risk": "high"},
            {"key": "D", "text": "Ban đêm không ai trực, không hệ thống giám sát nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Đèn chiếu sáng trong kho có loại nào tỏa nhiệt cao (sợi đốt) chạm vào hàng dễ cháy không?",
         "options": [
            {"key": "A", "text": "Đèn LED, cách hàng ≥0.5m, có chao bảo vệ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đèn LED nhưng hàng xếp cao gần sát đèn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Đèn huỳnh quang/sợi đốt, hàng dễ cháy sát đèn, ballast nóng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đèn sợi đốt chạm trực tiếp vải/giấy/nhựa, đã ố cháy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kệ hàng có bị nghiêng, cong vênh do chất quá tải hoặc xe nâng va chạm không?",
         "options": [
            {"key": "A", "text": "Kệ neo chắc, tải trọng ghi rõ, không chất vượt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kệ neo nhưng tải không ghi rõ, chất theo kinh nghiệm", "score": 1, "risk": "low"},
            {"key": "C", "text": "Kệ không neo, nghiêng do quá tải, đã bị xe nâng va cong", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kệ cong vênh vẫn dùng, đã từng đổ gây hư hại", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hàng hỏng (pin rò, aerosol méo, hóa chất đổ) có đang tích đống trong kho không?",
         "options": [
            {"key": "A", "text": "Có khu riêng, kiểm tra xử lý trong ngày", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có khu riêng nhưng xử lý hàng tuần, đôi khi tích nhiều", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng hỏng để lẫn kho chính, tích lâu ngày", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng hỏng (pin rò, hóa chất đổ) chất đống không ai quản lý", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cuối ngày, bảo vệ có kiểm tra điện từng khu vực kho trước khi khóa cửa không?",
         "options": [
            {"key": "A", "text": "Có checklist kiểm tra: điện, lối thoát, bình chữa cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đi qua kiểm tra bằng mắt, không checklist", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ tắt đèn chung và khóa cổng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không kiểm tra gì, đôi khi quên tắt điện", "score": 3, "risk": "critical"},
        ]},
    ]
}

print(f"SX công nghiệp: {len(SPEC_A['questions'])} câu")
print(f"Kho hàng: {len(SPEC_B['questions'])} câu")
