# seed_data_specific.py — Facility-Specific Questions (Groups A-L)

# ======= GROUP A: Cơ sở sản xuất công nghiệp =======
SPECIFIC_CATEGORY_A = {
    "name": "Đặc thù: Sản xuất công nghiệp",
    "description": "Câu hỏi đặc thù cho xưởng may, chế biến gỗ, nhựa, hóa chất, cơ khí",
    "icon": "🏭", "color": "#dc2626", "facility_type": "industrial",
    "questions": [
        {"text": "Vật liệu sản xuất chính tại cơ sở có đặc tính dễ cháy không?", "max": 3, "options": [
            {"key": "A", "text": "Vật liệu chủ yếu là kim loại, đá, gốm sứ — nguy cơ cháy thấp", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Vật liệu là nhựa, cao su, vải, giấy — cháy được nhưng không bùng phát nhanh", "score": 1, "risk": "low"},
            {"key": "C", "text": "Vật liệu là gỗ, sơn, dung môi hữu cơ — dễ cháy, lan nhanh", "score": 2, "risk": "high"},
            {"key": "D", "text": "Vật liệu là hóa chất dễ bắt lửa, bột kim loại, dung môi bay hơi", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bụi công nghiệp (bụi gỗ, bụi bông, bụi kim loại…) có được kiểm soát?", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống hút bụi công nghiệp, vệ sinh máy móc định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có vệ sinh nhưng bụi vẫn tích tụ ở một số góc khuất, máng đèn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có hệ thống hút bụi, bụi lắng đọng dày trên máy móc", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bụi tích tụ dày, có bụi lơ lửng tạo thành mây bụi dễ nổ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho chứa thành phẩm và nguyên liệu có tách biệt với khu vực sản xuất?", "max": 3, "options": [
            {"key": "A", "text": "Kho chứa tách biệt hoàn toàn bằng tường ngăn cháy, có cửa ngăn cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kho chứa liền kề xưởng, có vách ngăn thông thường", "score": 1, "risk": "low"},
            {"key": "C", "text": "Kho và xưởng trong cùng một không gian mở, không ngăn cách", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nguyên liệu để ngổn ngang trong xưởng, không có khu vực kho riêng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống thông gió, hút khí độc/dễ cháy trong xưởng:", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống thông gió cưỡng bức, không tích tụ hơi dung môi", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thông gió tự nhiên qua cửa sổ, đủ thoáng nhưng không có hệ thống hút", "score": 1, "risk": "low"},
            {"key": "C", "text": "Xưởng kín, ít cửa sổ, thông gió kém, có dùng hóa chất bay hơi", "score": 2, "risk": "high"},
            {"key": "D", "text": "Xưởng kín hoàn toàn, có hơi dung môi/khí dễ cháy tích tụ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cơ sở có lắp đặt hệ thống báo cháy và/hoặc chữa cháy tự động?", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống báo cháy tự động và sprinkler, kiểm tra định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Chỉ có hệ thống báo cháy tự động (chuông, còi), không có sprinkler", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có detector khói nhưng không có chuông báo động toàn cơ sở", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có hệ thống báo cháy hoặc chữa cháy tự động nào", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP B: Kho hàng, kho vật liệu =======
SPECIFIC_CATEGORY_B = {
    "name": "Đặc thù: Kho hàng, kho vật liệu",
    "description": "Câu hỏi cho kho chứa hàng hóa, vật liệu xây dựng, nông sản, kho lạnh",
    "icon": "🏪", "color": "#f59e0b", "facility_type": "warehouse",
    "questions": [
        {"text": "Hàng hóa trong kho được xếp đặt như thế nào so với hệ thống điện?", "max": 3, "options": [
            {"key": "A", "text": "Hàng hóa cách đèn, ổ cắm, dây điện ít nhất 0,5m, có lối đi thông thoáng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hàng hóa xếp gần đèn (dưới 0,5m) nhưng là hàng không dễ cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng hóa dễ cháy xếp ngay dưới bóng đèn sợi đốt hoặc halogen tỏa nhiệt cao", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng hóa che kín tủ điện, che bảng phân phối điện", "score": 3, "risk": "critical"},
        ]},
        {"text": "Chiều cao xếp hàng và khoảng cách đến mái/đèn:", "max": 3, "options": [
            {"key": "A", "text": "Hàng xếp thấp hơn đỉnh kho ít nhất 0,5m, cách đèn ít nhất 0,5m", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hàng xếp cao gần sát mái nhưng là hàng ít dễ cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng dễ cháy xếp gần sát mái, không có khoảng cách đến đèn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng xếp sát mái, chạm kết cấu mái, đèn nằm trong đống hàng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho có hệ thống phát hiện cháy sớm không?", "max": 3, "options": [
            {"key": "A", "text": "Có detector khói/nhiệt tự động kết nối chuông báo động, kiểm tra định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có detector khói nhưng không kiểm tra định kỳ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có hệ thống tự động, chỉ phát hiện bằng quan sát nhân viên", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kho không có người trực, không có hệ thống phát hiện cháy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe nâng hàng, xe điện dùng trong kho có được sạc pin đúng quy định?", "max": 3, "options": [
            {"key": "A", "text": "Không có xe nâng điện trong kho", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có xe nâng điện, sạc pin tại khu vực riêng biệt, thông thoáng", "score": 0, "risk": "safe"},
            {"key": "C", "text": "Sạc pin ngay trong kho nhưng xung quanh không có hàng dễ cháy", "score": 1, "risk": "medium"},
            {"key": "D", "text": "Sạc pin qua đêm không giám sát, dây sạc cũ", "score": 2, "risk": "high"},
            {"key": "E", "text": "Sạc pin giữa kho hàng dễ cháy, bộ sạc cũ hỏng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho có cửa thoát nạn và lối tiếp cận cho xe chữa cháy?", "max": 3, "options": [
            {"key": "A", "text": "Có ít nhất 2 cửa thoát nạn, đường tiếp cận rộng ≥ 3,5m cho xe chữa cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có 2 cửa nhưng một cửa thường xuyên bị khóa hoặc chắn bởi hàng hóa", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có 1 cửa ra vào duy nhất, đường vào kho hẹp (dưới 3,5m)", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kho nằm sâu trong ngõ hẹp, xe chữa cháy không thể tiếp cận", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP C: Nhà ở hỗn hợp =======
SPECIFIC_CATEGORY_C = {
    "name": "Đặc thù: Nhà ở hỗn hợp (ở + kinh doanh)",
    "description": "Nhà phố vừa ở vừa kinh doanh, cửa hàng tạp hóa kết hợp nhà ở",
    "icon": "🏠", "color": "#22c55e", "facility_type": "mixed_residence",
    "questions": [
        {"text": "Khu vực kinh doanh và khu vực sinh hoạt gia đình có được ngăn cách không?", "max": 3, "options": [
            {"key": "A", "text": "Ngăn cách bằng tường/cửa riêng, có lối thoát nạn độc lập", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thông nhau, nhưng hàng hóa không phải loại dễ cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thông nhau, hàng hóa dễ cháy bày tràn vào khu sinh hoạt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Toàn bộ nhà (kể cả phòng ngủ) đều chứa hàng hóa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Lối thoát nạn cho người ở tầng trên khi cháy xảy ra ở tầng dưới:", "max": 3, "options": [
            {"key": "A", "text": "Có cầu thang thoát hiểm riêng hoặc ban công có thể thoát qua nhà bên cạnh", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Chỉ có một cầu thang đi qua khu kinh doanh, bằng vật liệu không cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cầu thang duy nhất đi qua khu kinh doanh, làm bằng gỗ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Tầng trên hoàn toàn không có lối thoát thứ hai, bịt kín tứ phía", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hàng hóa kinh doanh tại tầng trệt có phải loại nguy hiểm cháy nổ?", "max": 3, "options": [
            {"key": "A", "text": "Thực phẩm, đồ dùng kim loại, sứ — nguy cơ cháy thấp", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Quần áo, văn phòng phẩm, đồ nhựa — cháy được nhưng không bùng nhanh", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sơn, keo, hóa chất tẩy rửa, gas mini, bật lửa — dễ cháy, có khả năng nổ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kinh doanh xăng dầu, gas, hóa chất công nghiệp — nguy hiểm cao", "score": 3, "risk": "critical"},
        ]},
        {"text": "Ban đêm cửa hàng tầng dưới có người trực hoặc hệ thống phát hiện cháy sớm?", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống báo cháy tự động kết nối chuông báo thức phòng ngủ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có khóa cửa chắc chắn, cửa bằng vật liệu chống cháy, không có báo cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có báo cháy, tầng dưới nhiều hàng dễ cháy, chỉ phát hiện khi cháy lớn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có báo cháy, tầng trên hoàn toàn bị cô lập khi cháy tầng dưới", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP D: Nhà hàng, khách sạn, chợ, TTTM =======
SPECIFIC_CATEGORY_D = {
    "name": "Đặc thù: Nhà hàng, khách sạn, chợ, TTTM",
    "description": "Câu hỏi cho nhà hàng, khách sạn, chợ, trung tâm thương mại",
    "icon": "🍽️", "color": "#f97316", "facility_type": "hospitality",
    "questions": [
        {"text": "Hệ thống bếp có trang bị hệ thống hút mùi và chống cháy bếp?", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống hút mùi công nghiệp, màng lọc dầu mỡ vệ sinh định kỳ, có dập cháy bếp tự động", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có hút mùi nhưng màng lọc dầu mỡ không được vệ sinh thường xuyên", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có quạt thông gió thông thường, dầu mỡ tích đọng trên đường ống", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có hệ thống hút mùi, bếp trong không gian kín, dầu mỡ bám đầy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khách sạn/nhà nghỉ nhiều tầng — hệ thống PCCC tầng cao:", "max": 3, "options": [
            {"key": "A", "text": "Có báo cháy tự động từng phòng, sprinkler, đèn chỉ dẫn, thang thoát hiểm riêng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có báo cháy tự động và đèn chỉ dẫn nhưng chưa có sprinkler", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có bình chữa cháy hành lang, không có báo cháy tự động", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có thiết bị PCCC đặc thù nào cho tầng cao", "score": 3, "risk": "critical"},
        ]},
        {"text": "Chợ/TTTM — hàng hóa có tuân thủ khoảng cách an toàn cháy nổ?", "max": 3, "options": [
            {"key": "A", "text": "Hàng xếp gọn trong gian hàng, không lấn chiếm lối đi, lối thoát thông thoáng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hàng tràn ra lối đi một phần nhưng vẫn đủ rộng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng chắn gần hết lối đi, lối thoát nạn thu hẹp đáng kể", "score": 2, "risk": "high"},
            {"key": "D", "text": "Lối đi và lối thoát nạn bị chắn hoàn toàn bởi hàng hóa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Có kế hoạch thoát nạn cho khách hàng/người mua?", "max": 3, "options": [
            {"key": "A", "text": "Có sơ đồ thoát nạn rõ ràng, nhân viên được huấn luyện hướng dẫn khách, thực tập định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có sơ đồ thoát nạn nhưng nhân viên chưa được huấn luyện cụ thể", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có sơ đồ thoát nạn, nhân viên không biết quy trình", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có kế hoạch thoát nạn, cơ sở đông người, nhiều khu vực khó thoát", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP E: Bệnh viện, trường học =======
SPECIFIC_CATEGORY_E = {
    "name": "Đặc thù: Bệnh viện, trường học, cơ sở y tế",
    "description": "Câu hỏi cho bệnh viện, trường học, cơ sở giáo dục, cơ sở y tế",
    "icon": "🏥", "color": "#ec4899", "facility_type": "medical_education",
    "questions": [
        {"text": "Kế hoạch sơ tán người không tự di chuyển được khi cháy:", "max": 3, "options": [
            {"key": "A", "text": "Có phương án sơ tán cụ thể cho từng đối tượng đặc biệt, đã thực tập", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có phương án chung nhưng chưa phân công cụ thể", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có phương án cho người tự di chuyển, chưa có cho người phụ thuộc", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bất kỳ phương án thoát nạn nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho hóa chất, dược phẩm, chất khử trùng có bảo quản đúng quy định?", "max": 3, "options": [
            {"key": "A", "text": "Kho riêng biệt, có thông gió, phân loại hóa chất tương thích, biển cảnh báo, bình CO₂", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hóa chất để trong tủ khóa riêng nhưng chưa phân loại đầy đủ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hóa chất để lẫn lộn, không thông gió, chưa phân loại", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hóa chất dễ cháy (cồn, oxy) để chung với vật liệu dễ cháy, gần nguồn nhiệt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện y tế có nguồn điện dự phòng và bảo vệ chống cháy?", "max": 3, "options": [
            {"key": "A", "text": "Có UPS và máy phát điện dự phòng, hệ thống điện y tế có aptomat riêng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Chỉ có UPS cho thiết bị quan trọng, không có máy phát dự phòng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có nguồn điện dự phòng, thiết bị dùng chung hệ thống điện", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thiết bị y tế dùng điện không ổn định, thường xuyên mất điện đột ngột", "score": 3, "risk": "critical"},
        ]},
        {"text": "Trường học — học sinh có được học và thực hành kỹ năng thoát nạn?", "max": 3, "options": [
            {"key": "A", "text": "Có giảng dạy và thực tập thoát nạn định kỳ ít nhất 1 lần/năm", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có phổ biến lý thuyết nhưng chưa thực tập thực tế", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chưa từng tổ chức hoạt động giáo dục thoát nạn cho học sinh", "score": 2, "risk": "high"},
            {"key": "D", "text": "Học sinh không biết vị trí lối thoát nạn và cách xử lý khi cháy", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP F: Xăng dầu, khí gas =======
SPECIFIC_CATEGORY_F = {
    "name": "Đặc thù: Xăng dầu, khí gas, vật liệu nổ",
    "description": "Câu hỏi cho cơ sở xăng dầu, khí gas, vật liệu nổ",
    "icon": "⛽", "color": "#b91c1c", "facility_type": "fuel_gas",
    "questions": [
        {"text": "Hệ thống tiếp địa chống tĩnh điện cho bồn chứa, xe bồn và thiết bị bơm:", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống tiếp địa chống tĩnh điện đầy đủ, đo kiểm định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có tiếp địa cho bồn chứa, chưa có dây tiếp địa di động cho xe bồn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hệ thống tiếp địa đã lắp nhưng chưa kiểm tra từ lâu", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có hệ thống tiếp địa chống tĩnh điện", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thiết bị phát hiện khí gas rò rỉ và hệ thống ngắt khẩn cấp:", "max": 3, "options": [
            {"key": "A", "text": "Có cảm biến phát hiện gas rò rỉ tự động, kết nối van ngắt khẩn cấp và chuông", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cảm biến gas nhưng chỉ có chuông, không có van ngắt tự động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có cảm biến tự động, chỉ phát hiện bằng mũi và kiểm tra thủ công", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bất kỳ thiết bị phát hiện gas rò rỉ nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khoảng cách an toàn từ bồn chứa xăng dầu/gas đến công trình lân cận:", "max": 3, "options": [
            {"key": "A", "text": "Đúng theo quy định, có biên bản nghiệm thu", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Gần đúng quy định nhưng chưa có biên bản chính thức", "score": 1, "risk": "low"},
            {"key": "C", "text": "Nhỏ hơn quy định, đã được nhắc nhở nhưng chưa khắc phục", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bồn chứa nằm sát công trình khác hoặc trong tầng hầm không đúng quy định", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên vận hành có được đào tạo chuyên sâu về PCCC?", "max": 3, "options": [
            {"key": "A", "text": "Tất cả có chứng chỉ đào tạo PCCC chuyên ngành, đào tạo lại định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Một số có chứng chỉ, một số chưa được đào tạo chính thức", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ được phổ biến miệng khi mới vào làm, không có chứng chỉ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không được đào tạo bất kỳ kiến thức PCCC chuyên ngành nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Biển cấm lửa, cấm hút thuốc và quy định an toàn có được thực thi?", "max": 3, "options": [
            {"key": "A", "text": "Có biển cấm đầy đủ, nhân viên thực thi nghiêm, kiểm soát khách tắt máy xe", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có biển cấm nhưng thực thi chưa nghiêm, đôi khi khách không tắt máy xe", "score": 1, "risk": "low"},
            {"key": "C", "text": "Có biển cấm nhưng không ai kiểm soát, khách tự do hút thuốc", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có biển cấm hoặc biển đã mờ, không có quy định kiểm soát nguồn lửa", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP G: Phương tiện giao thông =======
SPECIFIC_CATEGORY_G = {
    "name": "Đặc thù: Phương tiện giao thông",
    "description": "Xe khách, xe tải, tàu thuyền, máy bay dân dụng",
    "icon": "🚌", "color": "#0891b2", "facility_type": "transport",
    "questions": [
        {"text": "Phương tiện có trang bị bình chữa cháy đúng quy định và còn hạn?", "max": 3, "options": [
            {"key": "A", "text": "Có đủ bình đúng chủng loại, còn hạn, kiểm tra trước mỗi chuyến", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có bình chữa cháy nhưng chưa kiểm tra hạn gần đây", "score": 1, "risk": "low"},
            {"key": "C", "text": "Có bình đã hết hạn hoặc không đúng chủng loại", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bình chữa cháy hoặc bình đã bị tháo ra", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống nhiên liệu có được kiểm tra định kỳ?", "max": 3, "options": [
            {"key": "A", "text": "Kiểm tra theo lịch bảo dưỡng định kỳ, không rò rỉ, có giấy tờ kiểm định", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra theo cảm tính, chưa phát hiện rò rỉ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Phương tiện cũ, hệ thống nhiên liệu chưa kiểm tra từ lâu, đôi khi ngửi thấy mùi xăng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đã từng có rò rỉ nhiên liệu, chưa sửa triệt để", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe khách/xe buýt — lối thoát khẩn cấp và búa phá kính:", "max": 3, "options": [
            {"key": "A", "text": "Có đầy đủ cửa thoát hiểm, búa phá kính, lái xe được đào tạo", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cửa thoát hiểm và búa nhưng lái xe chưa được đào tạo chính thức", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cửa thoát hiểm bị hỏng khóa hoặc búa phá kính bị mất", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có hoặc không biết phương tiện có thiết bị thoát nạn hay không", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP H: Khu dân cư, nhà ở, nhà trọ =======
SPECIFIC_CATEGORY_H = {
    "name": "Đặc thù: Khu dân cư, nhà ở, nhà trọ",
    "description": "Câu hỏi cho nhà ở đơn lẻ, nhà trọ, chung cư mini",
    "icon": "🏘️", "color": "#059669", "facility_type": "residential",
    "questions": [
        {"text": "Nhà có từ 2 tầng trở lên — lối thoát nạn thứ hai từ tầng cao:", "max": 3, "options": [
            {"key": "A", "text": "Có ban công/lô gia kết nối nhà hàng xóm hoặc thang thoát nạn", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cửa sổ lớn tầng trên có thể trèo ra, chiều cao dưới 4m", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có một cầu thang duy nhất, bê tông, không có lối thoát thứ hai", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chỉ có cầu thang gỗ duy nhất đi qua khu vực hay để hàng hóa/xe máy tầng trệt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe máy, xe đạp điện có được sạc pin đúng cách?", "max": 3, "options": [
            {"key": "A", "text": "Sạc ngoài ban công, ngoài trời, không sạc qua đêm không giám sát", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Sạc trong nhà tầng trệt, gần cửa ra vào, không gần đồ dễ cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sạc trong phòng ngủ hoặc trên tầng cao qua đêm, không giám sát", "score": 2, "risk": "high"},
            {"key": "D", "text": "Sạc trong nhà trọ chật hẹp, nhiều xe cùng lúc, dây sạc cũ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhà trọ nhiều phòng — chủ nhà trọ có thực hiện trách nhiệm PCCC?", "max": 3, "options": [
            {"key": "A", "text": "Có đăng ký, nội quy PCCC niêm yết, bình chữa cháy đủ, phổ biến cho người thuê", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có bình chữa cháy nhưng chưa phổ biến quy định cho người thuê", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có bình chữa cháy, không có nội quy, chưa đăng ký quản lý", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chủ nhà không biết mình có trách nhiệm PCCC đối với người thuê", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống bếp gas trong nhà ở/nhà trọ có an toàn?", "max": 3, "options": [
            {"key": "A", "text": "Dây dẫn gas còn tốt (chưa đến hạn 2 năm), van khóa sau nấu, bình gas nơi thoáng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Dây dẫn gas trên 2 năm chưa thay, van khóa sau nấu xong", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dây dẫn gas cũ, có vết nứt, đôi khi quên khóa van", "score": 2, "risk": "high"},
            {"key": "D", "text": "Dây gas đã hỏng vá bằng băng keo, bình gas đặt trong tủ kín", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP I: Công trình xây dựng =======
SPECIFIC_CATEGORY_I = {
    "name": "Đặc thù: Công trình xây dựng đang thi công",
    "description": "Công trình đang xây dựng, cải tạo, sửa chữa lớn",
    "icon": "🏗️", "color": "#78716c", "facility_type": "construction",
    "questions": [
        {"text": "Vật liệu xây dựng dễ cháy (ván ép, xốp, bạt, gỗ cốt pha) được bảo quản?", "max": 3, "options": [
            {"key": "A", "text": "Lưu trữ khu vực riêng, cách xa nguồn lửa, hàn cắt; có che chắn", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Tập kết trên công trường nhưng có người bảo vệ trực 24/7", "score": 1, "risk": "low"},
            {"key": "C", "text": "Để lẫn lộn gần khu vực hàn cắt, không có biện pháp ngăn cách", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chất đống lớn, không có người trực, gần nguồn điện và hàn cắt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hoạt động hàn cắt trên công trường có được kiểm soát?", "max": 3, "options": [
            {"key": "A", "text": "Có giấy phép hàn cắt từng ca, người giám sát an toàn, bạt chắn tia lửa, bình chữa cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có bình chữa cháy nhưng không có giấy phép và người giám sát chuyên trách", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàn cắt tự do, không có bạt chắn, tia lửa bắn sang vật liệu gần đó", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàn cắt cạnh vật liệu dễ cháy, không bình chữa cháy, không giám sát", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện tạm phục vụ thi công có an toàn?", "max": 3, "options": [
            {"key": "A", "text": "Có aptomat riêng, dây đúng tiết diện, không kéo lòng thòng qua vũng nước", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có aptomat nhưng dây kéo tạm bợ, một số đoạn lộ lõi", "score": 2, "risk": "high"},
            {"key": "C", "text": "Không có aptomat, dây điện kéo tự do trên mặt sàn, qua vũng nước", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP J: Văn phòng, trụ sở hành chính =======
SPECIFIC_CATEGORY_J = {
    "name": "Đặc thù: Cơ quan, văn phòng, trụ sở",
    "description": "Câu hỏi cho cơ quan hành chính, văn phòng làm việc",
    "icon": "🏛️", "color": "#4f46e5", "facility_type": "office",
    "questions": [
        {"text": "Phòng lưu trữ hồ sơ, tài liệu giấy có biện pháp PCCC?", "max": 3, "options": [
            {"key": "A", "text": "Có tường/cửa ngăn cháy, báo cháy riêng, không có thiết bị điện không cần thiết", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có bình CO₂ riêng nhưng chưa có tường ngăn cháy và báo cháy tự động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hồ sơ trong phòng làm việc thông thường, chung với máy tính", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hồ sơ giấy chất đống trong phòng kho không có biện pháp PCCC", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thiết bị văn phòng có được tắt nguồn hoàn toàn ngoài giờ?", "max": 3, "options": [
            {"key": "A", "text": "Có quy định bắt buộc tắt nguồn cuối ngày, có người kiểm tra", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Phần lớn tắt, một số máy tính chạy qua đêm do công việc", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thiết bị thường xuyên để standby qua đêm và cuối tuần", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có quy định, toàn bộ thiết bị hoạt động liên tục", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng máy chủ (server room), phòng UPS có PCCC đặc thù?", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống chữa cháy khí sạch (FM200), báo cháy sớm, kiểm soát nhiệt độ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có báo cháy tự động và bình CO₂ riêng, chưa có chữa cháy tự động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có bình chữa cháy thông thường, không có báo cháy riêng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có biện pháp PCCC đặc thù nào cho phòng máy chủ", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP K: Phòng thí nghiệm =======
SPECIFIC_CATEGORY_K = {
    "name": "Đặc thù: Nghiên cứu, phòng thí nghiệm",
    "description": "Câu hỏi cho cơ sở nghiên cứu khoa học, phòng thí nghiệm",
    "icon": "🔬", "color": "#7c3aed", "facility_type": "laboratory",
    "questions": [
        {"text": "Hóa chất trong phòng thí nghiệm có phân loại theo nguyên tắc tương thích?", "max": 3, "options": [
            {"key": "A", "text": "Phân loại đầy đủ theo bảng tương thích, lưu trữ tủ riêng từng nhóm", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có nhãn và phân loại nhưng chưa tách biệt hoàn toàn nhóm không tương thích", "score": 1, "risk": "low"},
            {"key": "C", "text": "Để lẫn lộn trong tủ chung, chưa phân loại theo nhóm", "score": 2, "risk": "high"},
            {"key": "D", "text": "Để tràn lan trên bàn thí nghiệm, không có tủ bảo quản", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thiết bị đun nóng trong phòng thí nghiệm có được giám sát?", "max": 3, "options": [
            {"key": "A", "text": "Luôn có người giám sát khi hoạt động, có cài đặt nhiệt độ giới hạn tự động", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cài đặt tự ngắt nhưng đôi khi để chạy không giám sát", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thường để chạy qua đêm không có người trực", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thường xuyên chạy qua đêm, không có ngắt tự động, không giám sát", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP L: Nông nghiệp, chế biến nông lâm sản =======
SPECIFIC_CATEGORY_L = {
    "name": "Đặc thù: Nông nghiệp, chế biến nông lâm sản",
    "description": "Xưởng xay xát, kho thóc, xưởng chế biến gỗ, trại chăn nuôi",
    "icon": "🌾", "color": "#65a30d", "facility_type": "agriculture",
    "questions": [
        {"text": "Bụi nông sản (bụi thóc, bụi cám, mùn cưa) có được kiểm soát?", "max": 3, "options": [
            {"key": "A", "text": "Có hệ thống hút bụi, vệ sinh máy móc sau mỗi ca sản xuất", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Vệ sinh hàng tuần nhưng vẫn còn bụi ở góc khuất", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có hệ thống hút bụi, bụi tích tụ dày trên máy móc", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bụi nông sản lơ lửng dày đặc khi sản xuất, không thông gió, có nguy cơ nổ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hầm biogas (nếu có) có van an toàn và kiểm tra rò rỉ?", "max": 3, "options": [
            {"key": "A", "text": "Không có hầm biogas tại cơ sở", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có hầm biogas, có van an toàn, kiểm tra rò rỉ định kỳ", "score": 0, "risk": "safe"},
            {"key": "C", "text": "Có hầm biogas nhưng van an toàn chưa kiểm tra, đường ống cũ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Có hầm biogas tự xây không theo thiết kế chuẩn, không có van an toàn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho thóc, nông sản khô có bảo quản đúng độ ẩm tránh tự cháy?", "max": 3, "options": [
            {"key": "A", "text": "Phơi/sấy đạt độ ẩm chuẩn, kho thông gió tốt, kiểm tra nhiệt độ đống hàng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra độ ẩm trước nhập kho nhưng không theo dõi nhiệt độ đống hàng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Nhập kho theo kinh nghiệm, không đo độ ẩm, kho ít thông gió", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nhập kho nông sản còn ẩm, chất đống lớn trong kho kín, không theo dõi", "score": 3, "risk": "critical"},
        ]},
    ]
}

# All specific categories in order
ALL_SPECIFIC_CATEGORIES = [
    SPECIFIC_CATEGORY_A, SPECIFIC_CATEGORY_B, SPECIFIC_CATEGORY_C,
    SPECIFIC_CATEGORY_D, SPECIFIC_CATEGORY_E, SPECIFIC_CATEGORY_F,
    SPECIFIC_CATEGORY_G, SPECIFIC_CATEGORY_H, SPECIFIC_CATEGORY_I,
    SPECIFIC_CATEGORY_J, SPECIFIC_CATEGORY_K, SPECIFIC_CATEGORY_L,
]
