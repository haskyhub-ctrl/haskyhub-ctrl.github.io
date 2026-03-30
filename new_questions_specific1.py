# === ĐẶC THÙ C: NHÀ Ở HỖN HỢP (ở + kinh doanh) - 10 câu ===
SPEC_C = {
    "name": "Đặc thù: Nhà ở kết hợp kinh doanh",
    "description": "Dấu hiệu nguy cơ cháy nổ cho nhà ở kết hợp kinh doanh, sản xuất",
    "questions": [
        {"text": "Khu bán hàng/sản xuất tầng dưới có ngăn cách với khu ngủ tầng trên bằng tường và cửa chắn không?",
         "options": [
            {"key": "A", "text": "Tường chịu lửa, cửa chắn tự đóng, lối đi riêng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có tường gạch, cửa thường, nhưng lối đi chung qua khu kinh doanh", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ phân biệt bằng nội thất, hàng hóa tràn vào khu ở", "score": 2, "risk": "high"},
            {"key": "D", "text": "Toàn bộ nhà kể cả phòng ngủ, cầu thang đều chứa hàng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Từ phòng ngủ tầng trên có lối thoát nào KHÔNG đi qua khu hàng hóa tầng dưới không?",
         "options": [
            {"key": "A", "text": "Có cầu thang thoát riêng hoặc ban công nối nhà bên", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cầu thang bê tông qua tầng kinh doanh, có cửa ngăn mỗi tầng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cầu thang duy nhất qua khu hàng hóa đầy ắp, không cửa ngăn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Tầng trên bị giam kín (chuồng cọp), chỉ 1 lối qua tầng dưới", "score": 3, "risk": "critical"},
        ]},
        {"text": "Điện kinh doanh và điện sinh hoạt có riêng mạch, riêng aptomat (CB) không?",
         "options": [
            {"key": "A", "text": "Tách riêng hoàn toàn, CB riêng, ngắt độc lập được", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có CB riêng cho kinh doanh nhưng chung dây tổng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dùng chung mạch, thiết bị kinh doanh và gia đình cắm cùng ổ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chung mạch, thường quá tải, CB nhảy liên tục", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hàng hóa kinh doanh có đang xếp sát ổ cắm, tủ điện hoặc tràn vào khu ngủ không?",
         "options": [
            {"key": "A", "text": "Hàng gọn tầng dưới, cách xa ổ cắm/tủ điện >1m", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hàng gọn nhưng gần ổ cắm, không tràn lên tầng ngủ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng dễ cháy sát tủ điện, tràn vào khu sinh hoạt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng chất khắp nhà kể cả cầu thang, phòng ngủ, sát thiết bị điện", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng ngủ có cảm biến khói không?",
         "options": [
            {"key": "A", "text": "Có cảm biến khói trong mỗi phòng ngủ, hoạt động tốt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có ở hành lang tầng ngủ nhưng chưa lắp trong phòng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có ở tầng kinh doanh, tầng ngủ không có", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có cảm biến khói nào trong nhà", "score": 3, "risk": "critical"},
        ]},
        {"text": "Tủ đông, tủ mát, biển hiệu LED chạy 24/7 có tiếng kêu lạ, motor nóng, mùi khét không?",
         "options": [
            {"key": "A", "text": "Hoạt động bình thường, bảo dưỡng định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hoạt động bình thường nhưng chỉ sửa khi hỏng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chạy nhiều năm không bảo dưỡng, motor kêu, dây nóng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Motor cháy khét vẫn chạy, biển hiệu chập chờn, chưa sửa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bếp kinh doanh và bếp gia đình có cùng phòng nhỏ, nhiều bình gas, ít thông gió không?",
         "options": [
            {"key": "A", "text": "Bếp riêng biệt, quạt hút riêng, thoáng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cùng phòng bếp nhưng thoáng, bình gas đặt nơi thông gió", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chung bếp quá tải, nhiều bình gas phòng nhỏ, thông gió kém", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bếp kinh doanh ngay khu bán hàng hoặc gần kho dễ cháy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Trẻ em trong nhà có biết đường thoát khi cháy và biết làm gì khi nghe chuông báo cháy không?",
         "options": [
            {"key": "A", "text": "Trẻ đã được dạy, biết đường thoát, đã diễn tập", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đã nói cho trẻ biết lối thoát nhưng chưa diễn tập", "score": 1, "risk": "low"},
            {"key": "C", "text": "Trẻ chưa được hướng dẫn về thoát nạn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Trẻ nhỏ ngủ phòng kín tầng cao, không lối thoát thứ hai", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cầu thang có bị xe máy, hàng hóa chiếm chỗ không? Có cửa ngăn khói mỗi tầng không?",
         "options": [
            {"key": "A", "text": "Cầu thang thông thoáng, có cửa ngăn khói tự đóng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Không cửa ngăn khói nhưng thông thoáng, không để đồ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Xe máy, đồ đạc chiếm chỗ, phải len qua", "score": 2, "risk": "high"},
            {"key": "D", "text": "Cầu thang gỗ duy nhất, chất đầy đồ, khi cháy tầng 1 kẹt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Gia đình đã từng diễn tập thoát nạn ban đêm chưa? Nhà có thang dây hoặc lối phụ không?",
         "options": [
            {"key": "A", "text": "Đã diễn tập, có thang dây hoặc lối thoát phụ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đã bàn kế hoạch nhưng chưa thực hành, có đèn pin", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chưa nghĩ đến, không có kế hoạch", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nhà nhiều tầng, khóa kín ban đêm, không ai biết phải làm gì", "score": 3, "risk": "critical"},
        ]},
    ]
}

# === ĐẶC THÙ H: KHU DÂN CƯ, NHÀ TRỌ, NHÀ Ở - 10 câu ===
SPEC_H = {
    "name": "Đặc thù: Khu dân cư, nhà trọ, nhà ở",
    "description": "Dấu hiệu nguy cơ cháy nổ cho nhà trọ, chung cư mini, khu dân cư",
    "questions": [
        {"text": "Nhà trọ/chung cư mini có bao nhiêu lối thoát nạn? Các lối thoát có thông thoáng 24/7 không?",
         "options": [
            {"key": "A", "text": "≥2 lối thoát độc lập, luôn thông, có thang thoát phụ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "2 lối nhưng 1 lối phụ (ban công, cửa sổ), lối chính thông", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ 1 cầu thang duy nhất, cửa phụ bị khóa hoặc chặn đồ", "score": 2, "risk": "high"},
            {"key": "D", "text": "1 lối duy nhất, khóa cổng sắt ban đêm, không ai có chìa dự phòng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Chuồng cọp, lưới chống trộm có lối mở khẩn cấp không? Mọi người có biết cách mở không?",
         "options": [
            {"key": "A", "text": "Không có chuồng cọp, hoặc có lối mở, chìa để cạnh, mọi người biết", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cửa mở nhưng chìa cất trong phòng, phải tìm", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chuồng cọp hàn kín, chỉ 1 cửa ra vào chính", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàn kín toàn bộ cửa sổ và ban công, không lối mở nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Mỗi phòng trọ có aptomat (CB) riêng không? Hay nhiều phòng dùng chung?",
         "options": [
            {"key": "A", "text": "Mỗi phòng CB riêng, có CB chống rò tổng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "CB riêng mỗi phòng nhưng chưa có CB chống rò tổng", "score": 1, "risk": "low"},
            {"key": "C", "text": "2-3 phòng chung CB, quá tải thì mất điện cả mấy phòng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Toàn nhà chung 1 CB, dây nối tạm, CB nhảy thì nối tắt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bình nước nóng trong phòng tắm có bị rỉ sét, dây điện hở trong môi trường ẩm ướt không?",
         "options": [
            {"key": "A", "text": "Bình tốt, có thiết bị chống giật riêng, nối đất đúng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có thiết bị chống giật nhưng lắp đã lâu, chưa kiểm tra", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bình cũ không có thiết bị chống giật, chung CB với ổ cắm phòng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bình rỉ sét, dây hở trong phòng tắm ẩm, rất nguy hiểm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Người thuê có nấu gas trong phòng trọ kín không? Bình gas để ở đâu?",
         "options": [
            {"key": "A", "text": "Cấm gas trong phòng, có bếp chung hoặc bếp điện từ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Dùng bếp gas mini nhỏ, phòng thông thoáng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bếp gas trong phòng nhỏ kín, bình gas 12kg, ít thông gió", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bếp gas phòng kín, dây nứt, bình gas dưới gầm giường", "score": 3, "risk": "critical"},
        ]},
        {"text": "Có ai giữ chìa khóa tổng (master key) và chìa cổng khẩn cấp 24/7 không?",
         "options": [
            {"key": "A", "text": "Chủ nhà giữ master key 24/7, chìa cổng trong hộp kính phá vỡ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Chủ nhà giữ nhưng không ở tại chỗ 24/7, phải gọi điện", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ chủ nhà có chìa, chủ ở xa, ban đêm không liên lạc được", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không master key, mỗi phòng khóa riêng, cổng khóa xích", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe cứu hỏa có vào được hẻm/ngõ nơi nhà trọ tọa lạc không?",
         "options": [
            {"key": "A", "text": "Đường rộng ≥3.5m, xe cứu hỏa vào tận nơi", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hẻm hơi hẹp, xe cứu hỏa phải đỗ ngoài kéo vòi", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không biết, hẻm nhỏ xe cứu hỏa không vào được", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hẻm cụt, xe cứu hỏa không thể tiếp cận", "score": 3, "risk": "critical"},
        ]},
        {"text": "Chủ nhà trọ có dán sơ đồ thoát nạn mỗi tầng và phổ biến cho người thuê không?",
         "options": [
            {"key": "A", "text": "Sơ đồ dán mỗi tầng, phổ biến cho người thuê mới", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Phổ biến miệng nhưng chưa dán sơ đồ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chưa phổ biến, nội quy cũ mờ chữ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không nội quy, sơ đồ, người thuê không biết lối thoát", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhà trọ có cảm biến khói ở hành lang và phòng trọ không?",
         "options": [
            {"key": "A", "text": "Cảm biến khói trong mỗi phòng và hành lang, có chuông", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Ở hành lang mỗi tầng nhưng chưa lắp trong phòng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ ở tầng 1, các tầng trên không có", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có cảm biến hay chuông báo cháy nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe máy, xe đạp điện có sạc trong phòng trọ/phòng ngủ kín qua đêm không?",
         "options": [
            {"key": "A", "text": "Khu sạc riêng tầng trệt thông thoáng, có bình chữa cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Sạc tầng trệt khu chung, chưa có bình chữa cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sạc trong phòng trọ gần đồ dùng cá nhân", "score": 2, "risk": "high"},
            {"key": "D", "text": "Sạc qua đêm phòng kín, pin cũ phồng, sạc kém chất lượng", "score": 3, "risk": "critical"},
        ]},
    ]
}

print(f"Nhà ở HH: {len(SPEC_C['questions'])} câu")
print(f"Nhà trọ: {len(SPEC_H['questions'])} câu")
