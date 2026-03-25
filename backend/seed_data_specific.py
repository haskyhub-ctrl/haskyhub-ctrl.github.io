# seed_data_specific.py — Facility-Specific Questions (Groups 1-12) — 120 questions total

# ======= GROUP 1: Sản xuất công nghiệp (IN01–IN10) =======
SPECIFIC_CATEGORY_A = {
    "name": "Đặc thù: Sản xuất công nghiệp",
    "description": "Câu hỏi đặc thù cho xưởng sản xuất, chế biến, cơ khí, hóa chất",
    "icon": "🏭", "color": "#dc2626", "facility_type": "industrial",
    "questions": [
        {"text": "Quy trình sản xuất có sử dụng nhiệt độ cao (lò nung, lò sấy, nhiệt đóng gói) có được kiểm soát tự động không?", "options": [
            {"key": "A", "text": "Có thermostat tự động, ngắt quá nhiệt dự phòng độc lập, kiểm tra hiệu chuẩn định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có thermostat nhưng chưa hiệu chuẩn lại gần đây, không có ngắt quá nhiệt dự phòng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Điều chỉnh nhiệt thủ công, không có ngắt tự động, công nhân tự theo dõi bằng mắt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thiết bị gia nhiệt tự chế, không kiểm soát nhiệt, đã xảy ra quá nhiệt gây hỏng sản phẩm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực sơn, phun sơn hoặc sử dụng dung môi hữu cơ có được thông gió và kiểm soát nồng độ hơi không?", "options": [
            {"key": "A", "text": "Có buồng sơn kín với quạt hút, bộ lọc, cảm biến VOC, thiết bị điện đạt cấp Ex phòng nổ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quạt hút nhưng không có cảm biến VOC, thiết bị điện chưa đạt cấp Ex", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sơn phun trong xưởng mở, chỉ dùng quạt thông gió thường, hơi dung môi lan tỏa", "score": 2, "risk": "high"},
            {"key": "D", "text": "Phun sơn/dung môi trong phòng kín, không thông gió, nồng độ hơi cao, có ổ cắm thường", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống truyền tải bụi (ống hút bụi, silo, cyclone) có được vệ sinh và kiểm tra nguy cơ nổ bụi định kỳ không?", "options": [
            {"key": "A", "text": "Có lịch vệ sinh định kỳ, kiểm tra nguy cơ nổ bụi, van xả áp trên silo/cyclone", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Vệ sinh hàng tháng nhưng chưa đánh giá nguy cơ nổ bụi chuyên sâu", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lâu chưa vệ sinh, bụi tích tụ dày trong ống dẫn, silo chưa có van xả áp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bụi tích cực dày trong toàn hệ thống, đã xảy ra phồng ống hoặc cháy nhỏ trong hệ thống hút", "score": 3, "risk": "critical"},
        ]},
        {"text": "Chất làm mát (coolant), dầu cắt gọt kim loại có tích tụ trên phoi kim loại và mùn cưa không?", "options": [
            {"key": "A", "text": "Phoi kim loại thu gom ngay, dầu coolant hứng trong khay, xử lý hàng ngày", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thu gom cuối ca, phoi có dính dầu nhưng lượng nhỏ, cách xa nguồn nhiệt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Phoi kim loại dính dầu tích đống nhiều ngày gần máy tiện, máy phay đang chạy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Phoi dính dầu chất đống lớn gần nguồn nhiệt/hàn cắt, đã có hiện tượng bốc khói", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện trong nhà xưởng có được thiết kế và bảo trì phù hợp với tải sản xuất thực tế hiện tại không?", "options": [
            {"key": "A", "text": "Hệ thống điện thiết kế theo tải sản xuất, có dự phòng 20%, kiểm tra định kỳ bởi kỹ sư điện", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hệ thống đáp ứng tải hiện tại nhưng không còn dư phòng cho thiết bị mới", "score": 1, "risk": "low"},
            {"key": "C", "text": "Đã bổ sung nhiều máy mới mà không nâng cấp hệ thống điện, CB thỉnh thoảng nhảy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hệ thống điện quá tải nghiêm trọng, dây nóng khi chạy, đã phải nối tắt CB vì nhảy liên tục", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực nạp axit, pha hóa chất hoặc xử lý bề mặt kim loại có hệ thống thông gió và kiểm soát hơi axit không?", "options": [
            {"key": "A", "text": "Không có khu vực hóa chất; hoặc có quạt hút cục bộ, trung hòa axit, PPE đầy đủ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quạt hút nhưng công suất nhỏ, nhân viên có PPE nhưng không đầy đủ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có hệ thống hút hơi, axit bay hơi tự do, ăn mòn thiết bị điện xung quanh", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hơi axit mạnh ăn mòn dây điện và tủ điện gần đó, đã gây chập cháy thiết bị", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống làm mát tháp nước hoặc chiller công nghiệp có được kiểm tra nguy cơ cháy nổ từ hóa chất xử lý nước không?", "options": [
            {"key": "A", "text": "Không có tháp giải nhiệt; hoặc có, dùng hóa chất xử lý nước an toàn, bảo trì đúng lịch", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có hệ thống chiller, bảo trì định kỳ nhưng chưa đánh giá nguy cơ cháy từ hóa chất", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hệ thống cũ, motor quạt tháp giải nhiệt nóng bất thường, rung lắc mạnh", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hệ thống cũ nát, dùng tấm tản nhiệt bằng nhựa PVC dễ cháy, motor quá tải thường xuyên", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện trở và cuộn sấy trong dây chuyền đóng gói có được kiểm tra ngăn vật liệu đóng gói tiếp xúc trực tiếp không?", "options": [
            {"key": "A", "text": "Không có máy sấy/hàn nhiệt đóng gói; hoặc có, thanh nhiệt có bảo vệ, cảm biến ngắt kẹt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có thanh nhiệt, hoạt động tốt nhưng chưa có cảm biến ngắt khi vật liệu kẹt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Vật liệu đóng gói (nilon, giấy) đôi khi kẹt vào thanh nhiệt gây chảy/cháy nhỏ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thanh nhiệt hỏng thermostat, quá nhiệt liên tục, vật liệu đóng gói đã bị cháy nhiều lần", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực nạp điện cho xe nâng và thiết bị điện công nghiệp có được bố trí đúng không?", "options": [
            {"key": "A", "text": "Khu sạc riêng biệt, thông gió (khí hydro), sàn chống axit, bình chữa cháy, biển cấm lửa", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Khu sạc riêng nhưng thông gió chưa đủ, chưa có biển cấm lửa", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sạc xe nâng ngay trong kho hàng, gần hàng hóa dễ cháy, không thông gió", "score": 2, "risk": "high"},
            {"key": "D", "text": "Sạc ắc-quy xe nâng trong phòng kín, bộ sạc cũ hỏng, tia lửa khi sạc, khí hydro tích tụ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên sản xuất có được đào tạo nhận biết dấu hiệu cảnh báo sớm nguy cơ cháy nổ liên quan đến quy trình của mình không?", "options": [
            {"key": "A", "text": "Đào tạo chuyên sâu cho từng vị trí, nhận biết dấu hiệu cháy nổ riêng, thực tập định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đào tạo PCCC chung, chưa đi sâu vào nguy cơ đặc thù từng quy trình sản xuất", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ đào tạo cho quản lý, công nhân trực tiếp sản xuất chưa biết dấu hiệu cảnh báo", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chưa ai được đào tạo, công nhân không biết dấu hiệu nguy hiểm của quy trình mình làm", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP 2: Kho hàng, kho vật liệu (WH01–WH10) =======
SPECIFIC_CATEGORY_B = {
    "name": "Đặc thù: Kho hàng, kho vật liệu",
    "description": "Câu hỏi cho kho chứa hàng hóa, vật liệu xây dựng, nông sản, kho lạnh",
    "icon": "🏪", "color": "#f59e0b", "facility_type": "warehouse",
    "questions": [
        {"text": "Phân loại hàng hóa theo mức độ dễ cháy trong kho có được duy trì nhất quán không?", "options": [
            {"key": "A", "text": "Có bảng phân loại nguy hiểm cháy, hàng dễ cháy để kho riêng, nhãn cảnh báo rõ ràng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có phân loại sơ bộ nhưng chưa dán nhãn đầy đủ, đôi khi xếp lẫn lộn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không phân loại, hàng dễ cháy và hàng thường để chung trong cùng kho", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng nguy hiểm cháy nổ (aerosol, pin lithium, dung môi) để lẫn hàng thường, không nhãn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Lối đi chính trong kho và lối tiếp cận chữa cháy có luôn thông thoáng không?", "options": [
            {"key": "A", "text": "Lối đi chính ≥ 2m thông suốt, lối tiếp cận xe cứu hỏa ≥ 3.5m, kiểm tra hàng ngày", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Lối đi chính thông thoáng nhưng đôi khi có pallet tạm chiếm chỗ rồi dọn đi", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lối đi chính bị hàng hóa thu hẹp, xe nâng phải đi khó khăn, lối thoát nạn hẹp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Lối đi chính bị chặn hoàn toàn bởi hàng hóa, không thể đi qua khi khẩn cấp", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hàng hóa dễ cháy tồn kho ngoài giờ làm việc có được giám sát bởi hệ thống tự động không?", "options": [
            {"key": "A", "text": "Có hệ thống báo cháy tự động, camera nhiệt, kết nối trung tâm điều khiển 24/7", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có báo cháy tự động nhưng không có camera nhiệt, bảo vệ tuần tra ban đêm", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có bảo vệ tuần tra, không có hệ thống tự động phát hiện cháy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kho không có người trực ban đêm, không có bất kỳ hệ thống giám sát nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kệ hàng kim loại trong kho có được kiểm tra tải trọng và neo giữ chống đổ không?", "options": [
            {"key": "A", "text": "Kệ neo vào tường/sàn, tải trọng ghi rõ, không chất vượt tải, kiểm tra định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kệ có neo giữ nhưng tải trọng không ghi rõ, chất hàng theo kinh nghiệm", "score": 1, "risk": "low"},
            {"key": "C", "text": "Kệ không neo giữ, đã bị nghiêng do chất quá tải, xe nâng va chạm làm cong", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kệ hỏng cong vênh vẫn dùng, chất quá tải, đã từng đổ kệ gây hư hại", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hàng hóa nguy hiểm (pin lithium, aerosol, hàng dễ cháy đặc biệt) có được xác định và bảo quản riêng không?", "options": [
            {"key": "A", "text": "Khu vực riêng cho hàng nguy hiểm, tường ngăn cháy, sprinkler, biển cảnh báo đầy đủ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Để khu riêng nhưng không có tường ngăn cháy, có biển cảnh báo", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng nguy hiểm để chung với hàng thường, không nhãn cảnh báo đặc biệt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Pin lithium, aerosol để chung đống lớn sát tủ điện, không biện pháp bảo vệ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho lạnh hoặc kho đông có hệ thống phát hiện và ngắt an toàn khi xảy ra sự cố môi chất lạnh không?", "options": [
            {"key": "A", "text": "Không có kho lạnh; hoặc có, cảm biến rò môi chất, quạt sự cố, van ngắt khẩn cấp", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có kho lạnh, van ngắt tay nhưng chưa có cảm biến tự động phát hiện rò rỉ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Kho lạnh cũ dùng NH₃, đường ống ăn mòn, không có cảm biến rò khí", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kho lạnh NH₃ rò rỉ thường xuyên, không cảm biến, phòng máy kín, rất nguy hiểm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Ánh sáng chiếu sáng trong kho có được lắp đặt an toàn và không tiếp xúc với hàng hóa dễ cháy không?", "options": [
            {"key": "A", "text": "Đèn LED, cách hàng ≥ 0.5m, chao đèn bảo vệ, dây điện luồn ống đúng kỹ thuật", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đèn LED nhưng một số vị trí hàng xếp cao gần sát đèn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dùng đèn huỳnh quang/sợi đốt, hàng dễ cháy xếp sát đèn, ballast cũ nóng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đèn sợi đốt tỏa nhiệt chạm trực tiếp vào hàng vải/giấy/nhựa, đã có hiện tượng ố cháy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hàng hóa trả lại, hàng hỏng và phế phẩm có được quản lý riêng trong kho không?", "options": [
            {"key": "A", "text": "Có khu riêng cho hàng trả lại/hỏng, kiểm tra và xử lý trong ngày, không tích tụ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có khu riêng nhưng xử lý hàng tuần, đôi khi tích tụ nhiều", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng hỏng để lẫn trong kho chính, tích tụ lâu ngày không xử lý", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng hỏng (pin rò, aerosol méo, hóa chất đổ) chất đống trong kho không ai quản lý", "score": 3, "risk": "critical"},
        ]},
        {"text": "Việc sạc pin xe nâng và thiết bị điện trong kho được thực hiện ở khu vực được chỉ định an toàn không?", "options": [
            {"key": "A", "text": "Không sạc trong kho; hoặc sạc tại khu riêng thông gió, sàn chống axit, biển cấm lửa", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Sạc tại góc kho có thông gió nhưng cách hàng hóa chỉ vài mét", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sạc xe nâng giữa kho, gần hàng dễ cháy, không thông gió riêng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Sạc ắc-quy cũ rò axit giữa kho hàng dễ cháy, bộ sạc tóe tia lửa khi cắm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho có quy trình thực hành tốt để duy trì an toàn PCCC hàng ngày không?", "options": [
            {"key": "A", "text": "Có checklist PCCC hàng ngày: kiểm tra thoát hiểm, bình chữa cháy, tủ điện, cuối ngày ký xác nhận", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có nhắc nhở chung về PCCC nhưng không có checklist cụ thể hàng ngày", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có quy trình PCCC hàng ngày, chỉ kiểm tra khi có đoàn thanh tra", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bất kỳ quy trình PCCC nào, nhân viên kho không biết trách nhiệm PCCC", "score": 3, "risk": "critical"},
        ]},
    ]
}

# ======= GROUP 3: Nhà ở hỗn hợp (MX01–MX10) =======
SPECIFIC_CATEGORY_C = {
    "name": "Đặc thù: Nhà ở hỗn hợp (ở + kinh doanh)",
    "description": "Nhà phố vừa ở vừa kinh doanh, cửa hàng kết hợp nhà ở",
    "icon": "🏠", "color": "#22c55e", "facility_type": "mixed_residence",
    "questions": [
        {"text": "Khu vực kinh doanh và khu vực sinh hoạt gia đình có được ngăn cách bằng tường và cửa chống cháy không, hay chỉ phân biệt bằng nội thất?", "options": [
            {"key": "A", "text": "Ngăn cách bằng tường chịu lửa và cửa chống cháy tự đóng, lối đi riêng biệt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có tường ngăn thường (gạch), cửa thường, nhưng lối đi chung qua khu kinh doanh", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ phân biệt bằng nội thất, không có tường ngăn, hàng hóa tràn vào khu sinh hoạt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Toàn bộ nhà (kể cả phòng ngủ, cầu thang) đều chứa hàng hóa kinh doanh", "score": 3, "risk": "critical"},
        ]},
        {"text": "Lối thoát nạn từ tầng ở phía trên có hoàn toàn độc lập với lối ra vào của khu kinh doanh tầng dưới không?", "options": [
            {"key": "A", "text": "Có cầu thang thoát hiểm riêng hoặc ban công kết nối nhà bên, không qua khu kinh doanh", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cầu thang đi qua tầng kinh doanh nhưng bằng bê tông, có cửa ngăn tại mỗi tầng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cầu thang duy nhất đi qua khu kinh doanh đầy hàng hóa, không có cửa ngăn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Tầng trên hoàn toàn bị giam kín (chuồng cọp), chỉ có 1 lối duy nhất qua tầng dưới", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện phục vụ kinh doanh và điện sinh hoạt gia đình có được tách riêng mạch, riêng CB, có thể ngắt độc lập không?", "options": [
            {"key": "A", "text": "Mạch điện kinh doanh và sinh hoạt tách riêng hoàn toàn, CB riêng, ngắt độc lập", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có CB riêng cho khu kinh doanh nhưng chung công tơ, chung dây tổng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dùng chung mạch điện, thiết bị kinh doanh và gia đình cắm cùng ổ cắm", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chung mạch điện, thường xuyên quá tải do thiết bị kinh doanh, CB nhảy liên tục", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hàng hóa kinh doanh được để qua đêm trong cửa hàng có được sắp xếp cách xa nguồn điện, nguồn nhiệt và không chất vào khu sinh hoạt không?", "options": [
            {"key": "A", "text": "Hàng hóa xếp gọn tầng dưới, cách xa ổ cắm/tủ điện ≥ 1m, không chất lên tầng sinh hoạt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hàng hóa xếp gọn nhưng một số gần ổ cắm, không tràn lên tầng sinh hoạt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàng hóa dễ cháy xếp sát tủ điện, ổ cắm, một phần tràn vào khu sinh hoạt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng hóa dễ cháy chất khắp nhà kể cả cầu thang, phòng ngủ, sát thiết bị điện", "score": 3, "risk": "critical"},
        ]},
        {"text": "Có cảm biến khói được lắp đặt trong từng phòng ngủ của khu ở không?", "options": [
            {"key": "A", "text": "Có cảm biến khói trong mỗi phòng ngủ, kiểm tra pin hàng tháng, hoạt động tốt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cảm biến khói ở hành lang các tầng ngủ nhưng chưa lắp trong từng phòng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có 1 cảm biến ở tầng kinh doanh, tầng ngủ không có cảm biến", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bất kỳ cảm biến khói nào trong nhà", "score": 3, "risk": "critical"},
        ]},
        {"text": "Các thiết bị điện kinh doanh hoạt động 24/7 như tủ đông, tủ mát, biển hiệu LED có được bảo dưỡng định kỳ không?", "options": [
            {"key": "A", "text": "Bảo dưỡng 6 tháng/lần, mạch điện riêng có CB, kiểm tra dây điện và motor định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hoạt động bình thường, chỉ sửa khi hỏng, chưa bảo dưỡng chủ động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chạy liên tục nhiều năm không bảo dưỡng, motor kêu lạ, dây điện nóng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Tủ đông/tủ mát motor cháy khét vẫn chạy, biển hiệu LED cũ chập chờn, chưa sửa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bếp nấu ăn của gia đình và bếp chế biến phục vụ kinh doanh có được tách biệt về không gian và nguồn nhiệt không?", "options": [
            {"key": "A", "text": "Bếp gia đình và bếp kinh doanh ở phòng riêng, quạt hút riêng, bình gas riêng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cùng phòng bếp nhưng bếp kinh doanh có quạt hút mùi, bình gas đặt nơi thoáng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dùng chung bếp quá tải, nhiều bình gas cùng phòng nhỏ, thông gió kém", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bếp kinh doanh đặt ngay trong khu bán hàng hoặc gần kho hàng dễ cháy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Trẻ em trong gia đình có biết đường thoát nạn, biết điểm tập kết ngoài nhà và biết phải làm gì khi nghe chuông cảm biến khói kêu không?", "options": [
            {"key": "A", "text": "Trẻ em đã được dạy, biết đường thoát, biết điểm tập kết, đã diễn tập gia đình", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đã nói cho trẻ biết lối thoát nhưng chưa diễn tập thực tế", "score": 1, "risk": "low"},
            {"key": "C", "text": "Trẻ chưa được hướng dẫn về thoát nạn, gia đình chưa nghĩ đến việc này", "score": 2, "risk": "high"},
            {"key": "D", "text": "Trẻ nhỏ ngủ phòng kín trên tầng cao, không có lối thoát thứ hai, không ai hướng dẫn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cầu thang bộ trong nhà nhiều tầng có cửa ngăn khói tại mỗi tầng với cơ chế tự đóng, và không bị xe máy hay đồ đạc chiếm chỗ không?", "options": [
            {"key": "A", "text": "Cầu thang bê tông, cửa ngăn khói tự đóng mỗi tầng, không để đồ đạc, xe máy trên cầu thang", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cầu thang bê tông, không có cửa ngăn khói nhưng thông thoáng, không để đồ đạc", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cầu thang bị xe máy, đồ đạc chiếm chỗ, phải len qua khi đi, không có cửa ngăn khói", "score": 2, "risk": "high"},
            {"key": "D", "text": "Cầu thang gỗ duy nhất, chất đầy đồ đạc và xe máy, khi cháy tầng 1 không thể thoát", "score": 3, "risk": "critical"},
        ]},
        {"text": "Gia đình đã từng thực hành diễn tập thoát nạn, kể cả tình huống giả định cháy xảy ra vào ban đêm khi mọi người đang ngủ chưa?", "options": [
            {"key": "A", "text": "Đã diễn tập thoát nạn ban đêm, mọi người biết cách, có thang dây hoặc lối thoát phụ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đã bàn về kế hoạch thoát nạn nhưng chưa thực hành, có đèn pin sẵn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chưa bao giờ nghĩ đến việc diễn tập, không có kế hoạch thoát nạn gia đình", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nhà nhiều tầng, cửa khóa kín ban đêm, không ai biết phải làm gì nếu cháy lúc ngủ", "score": 3, "risk": "critical"},
        ]},
    ]
}

# Placeholder for Groups 4-12 — will be added
SPECIFIC_CATEGORY_D = {
    "name": "Đặc thù: Nhà hàng, khách sạn, chợ, TTTM",
    "description": "Câu hỏi cho nhà hàng, khách sạn, chợ, trung tâm thương mại",
    "icon": "🍽️", "color": "#f97316", "facility_type": "hospitality",
    "questions": [
        {"text": "Hệ thống ống hút khói và bộ lọc mỡ của bếp công nghiệp có được vệ sinh định kỳ không, hay đã có mùi khét và quạt chạy chậm hơn bình thường?", "options": [
            {"key": "A", "text": "Vệ sinh ống hút và bộ lọc mỡ mỗi 3 tháng bởi đơn vị chuyên nghiệp, có biên bản", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Tự vệ sinh 6 tháng/lần, quạt hoạt động bình thường, chưa mời đơn vị chuyên nghiệp", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lâu chưa vệ sinh, bộ lọc mỡ bám dày, quạt chạy chậm, có mùi khét khi nấu", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chưa bao giờ vệ sinh ống hút, mỡ nhỏ giọt ngược, quạt gần kẹt, đã có cháy mỡ nhỏ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Toàn bộ nhân viên có được đào tạo quy trình dẫn khách thoát nạn, và cơ sở đã tổ chức diễn tập sơ tán có sự tham gia của khách hàng thực tế chưa?", "options": [
            {"key": "A", "text": "100% nhân viên được đào tạo, có diễn tập sơ tán thực tế bao gồm khách, định kỳ 6 tháng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Nhân viên được đào tạo lý thuyết, chưa tổ chức diễn tập có khách tham gia", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ quản lý biết quy trình, nhân viên phục vụ không biết dẫn khách thoát nạn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không ai được đào tạo, cơ sở đông khách nhưng chưa từng diễn tập sơ tán", "score": 3, "risk": "critical"},
        ]},
        {"text": "Ban quản lý chợ/TTTM có thực sự kiểm tra và xử lý khi tiểu thương sử dụng bếp lửa, bếp gas hoặc bếp cồn ngay tại gian hàng không?", "options": [
            {"key": "A", "text": "Cấm tuyệt đối bếp lửa/gas tại gian hàng, kiểm tra hàng ngày, xử phạt vi phạm", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quy định cấm nhưng kiểm tra không thường xuyên, đôi khi bỏ qua vi phạm nhỏ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Biết tiểu thương dùng bếp gas nhưng không xử lý vì sợ mất mối quan hệ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nhiều gian hàng dùng bếp gas/cồn thoải mái, bình gas để trong gian hàng kín", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cửa phòng khách sạn có phải cửa chống cháy với cơ chế tự đóng không, và nhân viên có nhắc khách không được chèn cửa mở không?", "options": [
            {"key": "A", "text": "Cửa phòng chống cháy với tay gạt tự đóng, nhân viên nhắc khách không chèn cửa", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cửa phòng có tự đóng nhưng nhân viên không nhắc khách về quy định", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cửa phòng thường, không tự đóng, khách thường chèn cửa mở cho thoáng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Cửa gỗ mỏng không chống cháy, tay gạt hỏng, hành lang không có cửa ngăn khói", "score": 3, "risk": "critical"},
        ]},
        {"text": "Trong các dịp lễ tết khi bổ sung đèn trang trí, tải điện thực tế có được tính toán lại và kiểm tra không vượt quá công suất thiết kế không?", "options": [
            {"key": "A", "text": "Có tính toán tải trước khi lắp đèn trang trí, dùng đèn LED tiết kiệm, CB riêng cho đèn", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Dùng đèn LED nhưng chưa tính toán tải cụ thể, cắm vào ổ cắm hiện có", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lắp nhiều đèn sợi đốt/dây đèn nhấp nháy, dùng ổ cắm kéo dài nối chồng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đèn trang trí khắp nơi kể cả gần rèm/vải, nối điện chồng chéo, CB nhảy phải nối tắt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cửa kho hàng trong TTTM/siêu thị có luôn được đóng kín và có cơ chế tự đóng, hay thường xuyên bị chèn mở suốt ngày vì nhân viên đi lại?", "options": [
            {"key": "A", "text": "Cửa kho chống cháy tự đóng, có gắn nam châm giữ mở kết nối hệ thống báo cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cửa kho tự đóng nhưng nhân viên thỉnh thoảng chèn mở rồi đóng lại", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cửa kho luôn bị chèn mở bằng gạch/nêm suốt ngày vì nhân viên đi lại thường xuyên", "score": 2, "risk": "high"},
            {"key": "D", "text": "Cửa kho hỏng không đóng được, kho thông với sàn bán hàng, hàng hóa tràn ra ngoài", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khách sạn có danh sách phòng đang có khách được cập nhật real-time và quy trình kiểm tra từng phòng khi có báo động cháy không?", "options": [
            {"key": "A", "text": "Hệ thống quản lý phòng real-time, quy trình rõ ai kiểm tra phòng nào, master key sẵn sàng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Biết phòng nào có khách nhưng chưa có quy trình phân công kiểm tra cụ thể", "score": 1, "risk": "low"},
            {"key": "C", "text": "Danh sách phòng cập nhật thủ công, có thể sai lệch, chưa có quy trình kiểm tra", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không quản lý danh sách phòng có khách, khi cháy không biết phòng nào cần kiểm tra", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bếp nhà hàng có hệ thống chữa cháy tự động chuyên dụng cho cháy dầu mỡ (wet chemical system), hay chỉ trang bị bình CO₂ thông thường?", "options": [
            {"key": "A", "text": "Có hệ thống dập cháy bếp tự động (wet chemical/ANSUL), kiểm tra 6 tháng/lần", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có bình chữa cháy bếp chuyên dụng (loại K/F) nhưng chưa có hệ thống tự động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có bình CO₂ hoặc bột ABC cho bếp, không phù hợp cho cháy dầu mỡ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bình chữa cháy nào trong bếp, dập cháy dầu bằng nước (rất nguy hiểm)", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bảo vệ cuối ngày có thực hiện kiểm tra từng gian hàng theo checklist cụ thể trước khi đóng cửa chợ/TTTM không, hay chỉ tắt đèn và khóa cổng?", "options": [
            {"key": "A", "text": "Có checklist kiểm tra: điện từng gian hàng, bình gas, lối thoát, ký xác nhận mỗi tối", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Bảo vệ đi qua từng khu nhưng không có checklist, kiểm tra bằng mắt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bảo vệ chỉ tắt đèn chung và khóa cổng, không kiểm tra từng gian hàng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không kiểm tra gì, tiểu thương tự khóa gian hàng, đôi khi quên tắt điện/bếp", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cơ sở có tính toán và kiểm soát số người tối đa được phép có mặt theo thiết kế thoát nạn, đặc biệt trong các sự kiện đông người không?", "options": [
            {"key": "A", "text": "Có biển ghi sức chứa tối đa, kiểm soát số người vào, đóng cửa khi đạt giới hạn", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Biết sức chứa thiết kế nhưng chưa kiểm soát đếm người ra vào", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không biết sức chứa tối đa, sự kiện đông nghịt nhưng không giới hạn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đông vượt xa sức chứa, lối thoát kẹt cứng người, đã xảy ra chen lấn nguy hiểm", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_E = {
    "name": "Đặc thù: Bệnh viện, trường học, cơ sở y tế",
    "description": "Câu hỏi cho bệnh viện, trường học, cơ sở giáo dục, cơ sở y tế",
    "icon": "🏥", "color": "#ec4899", "facility_type": "medical_education",
    "questions": [
        {"text": "Cơ sở y tế có phương án và thiết bị sơ tán chuyên dụng cho bệnh nhân không thể tự di chuyển hoặc đang phụ thuộc vào thiết bị hỗ trợ sự sống không?", "options": [
            {"key": "A", "text": "Có phương án chi tiết, xe lăn sơ tán, tấm trượt, phân công cụ thể, đã diễn tập", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có phương án chung nhưng chưa có thiết bị sơ tán chuyên dụng, chưa diễn tập", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có phương án cho người tự đi, bệnh nhân nặng chưa có kế hoạch sơ tán cụ thể", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có phương án sơ tán nào, bệnh nhân nằm liệt tầng cao không có thang máy cứu hỏa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Trường học có tổ chức diễn tập sơ tán phù hợp với từng độ tuổi học sinh, kể cả tình huống không báo trước không?", "options": [
            {"key": "A", "text": "Diễn tập sơ tán 2 lần/năm, phù hợp từng lứa tuổi, bao gồm tình huống không báo trước", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Diễn tập 1 lần/năm có báo trước, tất cả học sinh biết lối thoát", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ phổ biến lý thuyết, chưa tổ chức diễn tập thực tế cho học sinh", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chưa bao giờ tổ chức diễn tập, học sinh không biết lối thoát nạn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho lưu trữ hồ sơ bệnh án giấy có được bảo vệ bằng hệ thống phát hiện và chữa cháy chuyên dụng không?", "options": [
            {"key": "A", "text": "Kho riêng có báo cháy sớm, bình CO₂, tường chống cháy, có bản sao lưu số", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kho riêng có bình chữa cháy, chưa có báo cháy riêng, đang số hóa dần", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hồ sơ giấy để trong phòng làm việc chung, không có PCCC riêng, chưa sao lưu số", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hồ sơ giấy chất đống trong kho kín không PCCC, là bản gốc duy nhất", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cồn y tế, formalin và các hóa chất dễ cháy trong phòng xét nghiệm có được bảo quản trong tủ chuyên dụng chống cháy không?", "options": [
            {"key": "A", "text": "Bảo quản trong tủ chống cháy chuyên dụng, phân loại tương thích, SDS đầy đủ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Để trong tủ riêng có khóa nhưng không phải tủ chống cháy chuyên dụng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cồn, formalin để lẫn lộn trên kệ chung, gần bồn rửa và ổ cắm điện", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hóa chất dễ cháy để tràn lan trên bàn, gần nguồn nhiệt, chai hở nắp", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thiết bị điện y tế (máy X-quang, máy MRI, máy thở) có được kiểm tra và bảo dưỡng theo lịch riêng không?", "options": [
            {"key": "A", "text": "Bảo dưỡng theo lịch nhà sản xuất, mạch điện riêng, phòng đặt có thông gió tản nhiệt tốt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Bảo dưỡng khi có lỗi, mạch điện riêng, phòng có ĐHKK nhưng chưa kiểm tra tản nhiệt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thiết bị y tế dùng chung mạch điện, phòng đặt chật, thông gió kém, nóng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thiết bị y tế cũ chạy quá tải, phòng kín nóng, dây điện nóng bất thường", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực phòng mổ và phòng hồi sức sử dụng khí oxy, khí gây mê có hệ thống phát hiện rò rỉ khí không?", "options": [
            {"key": "A", "text": "Có cảm biến rò rỉ khí oxy/gây mê, van ngắt khẩn cấp, kiểm tra đường ống định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra đường ống định kỳ nhưng chưa lắp cảm biến rò rỉ tự động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Đường ống khí cũ, chưa kiểm tra gần đây, không có cảm biến rò rỉ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đường ống oxy bị rò rỉ, nồng độ oxy cao trong phòng kín, nguy cơ cháy bùng rất lớn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng học có đủ ít nhất hai lối thoát nạn, cửa mở ra phía ngoài và không bị khóa hoặc chất đồ trong giờ học không?", "options": [
            {"key": "A", "text": "Có ≥ 2 cửa mở ra ngoài, thanh đẩy khẩn cấp, không bị chất đồ, đèn EXIT hoạt động", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có 2 cửa nhưng 1 cửa mở vào trong, không bị khóa", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có 1 cửa ra vào, cửa mở vào trong, bàn ghế xếp chật", "score": 2, "risk": "high"},
            {"key": "D", "text": "Cửa lớp khóa từ bên ngoài trong giờ học, cửa sổ có song sắt, không thoát được", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên y tế trực ca đêm có nắm rõ quy trình báo động, ngắt điện cục bộ và dẫn bệnh nhân sơ tán không?", "options": [
            {"key": "A", "text": "100% nhân viên trực đêm biết quy trình, đã diễn tập, biết rõ vị trí CB và lối thoát", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Nhân viên biết quy trình chung nhưng chưa diễn tập ca đêm cụ thể", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ bác sĩ trực biết, điều dưỡng và hộ lý chưa nắm quy trình sơ tán", "score": 2, "risk": "high"},
            {"key": "D", "text": "Ca đêm ít người, không ai biết quy trình sơ tán, không biết cầu dao ở đâu", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống oxy trung tâm và bình oxy lưu động trong bệnh viện có được kiểm tra áp suất, van an toàn định kỳ không?", "options": [
            {"key": "A", "text": "Kiểm tra áp suất và van an toàn hàng tháng, bình oxy cách nguồn nhiệt ≥ 3m, buộc cố định", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra khi nạp bình, bình oxy buộc cố định nhưng chưa kiểm tra van định kỳ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bình oxy để lung tung, không buộc cố định, van an toàn lâu chưa kiểm tra", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bình oxy không buộc, gần nguồn nhiệt/điện, van hỏng, đã từng rò rỉ oxy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhà trẻ, mầm non có tường ngăn cháy giữa các phòng học, cửa mở ra ngoài dễ dàng và đủ nhân viên để bế/dẫn trẻ thoát nạn không?", "options": [
            {"key": "A", "text": "Tường chống cháy, cửa mở ra ngoài, tỷ lệ cô/trẻ đủ, đã diễn tập sơ tán với trẻ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cửa mở ra ngoài, tỷ lệ cô/trẻ đủ nhưng chưa tổ chức diễn tập cháy với trẻ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cửa mở vào trong, ít nhân viên so với số trẻ, chưa diễn tập thoát nạn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Phòng trẻ tầng cao, cửa khóa, song sắt kín, ít cô giáo, không thể sơ tán nhanh", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_F = {
    "name": "Đặc thù: Xăng dầu, khí gas, vật liệu nổ",
    "description": "Câu hỏi cho cơ sở xăng dầu, khí gas, vật liệu nổ",
    "icon": "⛽", "color": "#b91c1c", "facility_type": "fuel_gas",
    "questions": [
        {"text": "Cửa hàng xăng dầu có kiểm tra rò rỉ đường ống ngầm và bể ngầm định kỳ không?", "options": [
            {"key": "A", "text": "Kiểm tra rò rỉ bể ngầm và đường ống hàng năm bằng thiết bị chuyên dụng, có biên bản", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra bằng quan sát mắt thường hàng tháng, chưa dùng thiết bị đo chuyên dụng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lâu chưa kiểm tra, đôi khi thấy vết dầu loang trên mặt sân nhưng chưa điều tra", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đã phát hiện rò rỉ dầu từ bể ngầm, dầu ngấm ra xung quanh nhưng chưa sửa chữa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên cây xăng có thực sự yêu cầu khách tắt máy xe, không sử dụng điện thoại và không hút thuốc trong khu vực bơm xăng không?", "options": [
            {"key": "A", "text": "Thực thi nghiêm: yêu cầu tắt máy, cấm điện thoại và hút thuốc, có biển cấm đầy đủ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có biển cấm và nhắc nhở nhưng không phải lúc nào cũng kiểm soát được 100%", "score": 1, "risk": "low"},
            {"key": "C", "text": "Có biển cấm nhưng nhân viên ngại nhắc khách, nhiều khách vẫn dùng điện thoại", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không kiểm soát, khách thoải mái dùng điện thoại, hút thuốc, nổ máy khi bơm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống nối đất chống tĩnh điện cho bồn chứa xăng dầu và vòi bơm có được đo kiểm định kỳ không?", "options": [
            {"key": "A", "text": "Đo kiểm điện trở nối đất hàng năm, đạt tiêu chuẩn ≤ 10Ω, có biên bản kiểm định", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có hệ thống nối đất nhưng lâu chưa đo kiểm, giả định vẫn đạt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hệ thống nối đất đã lắp nhưng dây nối bị đứt/gỉ ở một số vị trí", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có hệ thống nối đất chống tĩnh điện cho bồn chứa và vòi bơm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho LPG và trạm nạp bình gas có cảm biến phát hiện rò rỉ khí, van ngắt khẩn cấp và hệ thống thông gió cơ học hoạt động 24/7 không?", "options": [
            {"key": "A", "text": "Có cảm biến gas LPG, van ngắt khẩn cấp tự động, quạt thông gió cơ học 24/7", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có van ngắt tay và quạt thông gió nhưng chưa có cảm biến phát hiện gas tự động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có cảm biến, thông gió tự nhiên, phát hiện rò rỉ bằng mũi", "score": 2, "risk": "high"},
            {"key": "D", "text": "Kho gas kín, không thông gió, có mùi gas nhưng chưa xử lý, không van ngắt khẩn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên giao nhận bình gas có được đào tạo phát hiện bình méo, van hỏng và quy trình xử lý khi phát hiện rò rỉ không?", "options": [
            {"key": "A", "text": "100% nhân viên được đào tạo kiểm tra bình, loại bỏ bình lỗi, biết quy trình rò rỉ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Nhân viên kiểm tra bằng kinh nghiệm, chưa qua đào tạo chính thức bài bản", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ kiểm tra sơ qua, đôi khi giao bình van lỏng hoặc dây dẫn nứt cho khách", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không kiểm tra, giao bình cũ méo van hỏng, chưa ai biết xử lý rò rỉ gas", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực bơm xăng và bể ngầm có được phân vùng nguy hiểm và toàn bộ thiết bị điện trong vùng đó có đạt cấp Ex không?", "options": [
            {"key": "A", "text": "Phân vùng theo TCVN/IEC, toàn bộ thiết bị điện trong vùng nguy hiểm đạt cấp Ex", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thiết bị chính (trụ bơm, đèn) đạt Ex, nhưng ổ cắm phụ dùng loại thường", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dùng thiết bị điện thông thường trong khu vực bơm, chưa phân vùng chính thức", "score": 2, "risk": "high"},
            {"key": "D", "text": "Có ổ cắm, công tắc thường trong vùng hơi xăng, đã xảy ra tia lửa điện gần trụ bơm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe bồn chở xăng dầu khi vào cơ sở có thực hiện nối đất chống tĩnh điện trước khi bơm không?", "options": [
            {"key": "A", "text": "Có quy trình bắt buộc: nối đất xe bồn, kiểm tra dây nối, có nút dừng khẩn cấp", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có dây nối đất nhưng đôi khi tài xế quên nối, nhân viên nhắc không thường xuyên", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dây nối đất cũ hỏng, không thay mới, bơm xăng mà không nối đất", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có dây nối đất, không có nút dừng khẩn cấp, bơm xăng ban đêm không giám sát", "score": 3, "risk": "critical"},
        ]},
        {"text": "Vật liệu nổ (nếu có) được bảo quản trong kho đúng tiêu chuẩn với đầy đủ giấy phép không?", "options": [
            {"key": "A", "text": "Không có vật liệu nổ; hoặc kho đúng tiêu chuẩn, xa khu dân cư, giấy phép còn hiệu lực", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có kho đúng tiêu chuẩn, giấy phép sắp hết hạn đang gia hạn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Kho chưa đạt chuẩn khoảng cách an toàn, giấy phép đã hết hạn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bảo quản vật liệu nổ trái phép, không kho chuyên dụng, gần khu dân cư", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cơ sở có phương án ứng phó sự cố tràn đổ xăng dầu quy mô lớn không?", "options": [
            {"key": "A", "text": "Có phương án ứng phó tràn đổ, vật liệu thấm dầu sẵn sàng, van ngăn tràn vào cống", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có vật liệu thấm dầu nhưng chưa có phương án chi tiết và diễn tập", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có vật liệu thấm dầu, xăng tràn chảy tự do vào cống thoát nước", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bất kỳ biện pháp nào, xăng dầu tràn đã chảy vào khu dân cư gần đó", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên trực ca đêm tại cây xăng có biết quy trình ngắt điện toàn bộ, đóng van bể khẩn cấp khi phát hiện rò rỉ ban đêm không?", "options": [
            {"key": "A", "text": "Biết rõ: vị trí nút ngắt khẩn, van bể, quy trình sơ tán, số điện thoại khẩn cấp", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Biết vị trí nút ngắt nhưng chưa thực hành quy trình khẩn cấp bao giờ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Nhân viên trực đêm là lao động mới, chưa biết quy trình khẩn cấp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Ca đêm chỉ 1 người, không biết quy trình, ngủ gật, có nguy cơ không phát hiện rò rỉ", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_G = {
    "name": "Đặc thù: Phương tiện giao thông",
    "description": "Xe khách, xe tải, tàu thuyền, phương tiện giao thông",
    "icon": "🚌", "color": "#0891b2", "facility_type": "transport",
    "questions": [
        {"text": "Xe khách, xe buýt có được kiểm tra hệ thống nhiên liệu, ống dẫn gas (nếu chạy CNG/LPG) định kỳ không?", "options": [
            {"key": "A", "text": "Kiểm tra hệ thống nhiên liệu theo lịch nhà sản xuất, có biên bản, bình PCCC trên xe", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra trước mỗi chuyến nhưng không có biên bản chi tiết", "score": 1, "risk": "low"},
            {"key": "C", "text": "Kiểm tra khi bảo dưỡng lớn, giữa các lần không kiểm tra hệ thống nhiên liệu", "score": 2, "risk": "high"},
            {"key": "D", "text": "Xe cũ, hệ thống nhiên liệu rò rỉ, bình PCCC hết hạn hoặc không có", "score": 3, "risk": "critical"},
        ]},
        {"text": "Búa thoát hiểm, cửa thoát hiểm trên xe khách có đủ số lượng, ở đúng vị trí và hành khách biết cách sử dụng không?", "options": [
            {"key": "A", "text": "Đủ búa, cửa thoát hiểm hoạt động, có hướng dẫn sử dụng, tài xế thông báo trước chuyến", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có búa và cửa thoát hiểm nhưng tài xế không thông báo cho hành khách", "score": 1, "risk": "low"},
            {"key": "C", "text": "Búa thoát hiểm thiếu hoặc bị giấu đi, cửa thoát hiểm bị kẹt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có búa, cửa thoát hiểm bị hàn kín hoặc chất hàng che khuất", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện trên phương tiện (dây điện, cầu chì, ắc quy) có được bảo dưỡng và kiểm tra chuyên sâu không?", "options": [
            {"key": "A", "text": "Kiểm tra hệ thống điện mỗi 6 tháng, cầu chì đúng ampe, dây không hở, ắc quy tốt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra khi bảo dưỡng định kỳ, chưa kiểm tra riêng hệ thống điện chuyên sâu", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dây điện xe cũ, một số đoạn nối tạm bằng băng keo, cầu chì thay bằng dây đồng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hệ thống điện hỏng nặng, đã có hiện tượng chập cháy, vẫn chạy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Tàu thuyền có đầy đủ phao cứu sinh, áo phao và đã diễn tập sơ tán cho thuyền viên và hành khách không?", "options": [
            {"key": "A", "text": "Không có tàu thuyền; hoặc có đủ phao/áo phao, diễn tập cứu nạn định kỳ, hành khách được hướng dẫn", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Đủ phao và áo phao nhưng chưa tổ chức diễn tập cho hành khách", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thiếu phao/áo phao so với số hành khách, chưa diễn tập bao giờ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không đủ phao, áo phao hỏng, thuyền viên không biết quy trình cứu nạn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe ô tô/xe tải của cơ sở có được trang bị bình chữa cháy đúng loại, còn hạn và tài xế biết sử dụng không?", "options": [
            {"key": "A", "text": "Mỗi xe có bình chữa cháy còn hạn, đúng loại, tài xế biết sử dụng, kiểm tra hàng tháng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có bình chữa cháy trên xe nhưng tài xế chưa thực hành sử dụng bao giờ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bình chữa cháy hết hạn hoặc để trong cốp xe khó lấy khi khẩn cấp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bình chữa cháy trên xe, hoặc bình đã hỏng van không sử dụng được", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe chở hàng nguy hiểm (xăng dầu, hóa chất, khí gas) có đầy đủ biển báo, trang thiết bị PCCC và giấy phép vận chuyển không?", "options": [
            {"key": "A", "text": "Không chở hàng nguy hiểm; hoặc có đủ biển báo, giấy phép, bộ ứng phó sự cố trên xe", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có biển báo và giấy phép nhưng bộ ứng phó sự cố chưa đầy đủ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Biển báo mờ, giấy phép sắp hết hạn, thiếu dụng cụ ứng phó sự cố", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chở hàng nguy hiểm không phép, không biển báo, không có PCCC trên xe", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực sạc pin xe điện (ô tô điện, xe máy điện) tại bãi đỗ có được bố trí an toàn với hệ thống PCCC phù hợp không?", "options": [
            {"key": "A", "text": "Không có sạc xe điện; hoặc khu sạc riêng biệt, sprinkler, bình chữa cháy, nền chống cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có khu sạc riêng, bình chữa cháy nhưng chưa có sprinkler riêng cho khu sạc", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sạc xe điện trong bãi đỗ xe chung, gần xe xăng dầu, không có PCCC riêng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Sạc xe điện trong tầng hầm kín, không thông gió, không PCCC, sạc qua đêm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Tài xế xe tải/xe khách có được huấn luyện quy trình xử lý khi phát hiện cháy xe trên đường không?", "options": [
            {"key": "A", "text": "Đào tạo bài bản: dừng xe an toàn, sơ tán hành khách, dùng bình chữa cháy, gọi 114", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Biết cơ bản nhưng chưa thực hành diễn tập tình huống cháy xe thực tế", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ biết gọi cứu hỏa, không biết sử dụng bình chữa cháy trên xe", "score": 2, "risk": "high"},
            {"key": "D", "text": "Tài xế không được đào tạo PCCC, không biết bình chữa cháy ở đâu trên xe", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thùng hàng xe tải có lắp cảm biến nhiệt hoặc báo cháy cho các chuyến hàng có nguy cơ cháy cao không?", "options": [
            {"key": "A", "text": "Không chở hàng nguy hiểm; hoặc có cảm biến nhiệt/khói trong thùng, cảnh báo cab tài xế", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Không có cảm biến nhưng tài xế kiểm tra hàng mỗi trạm dừng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chở hàng dễ cháy nhưng không có giám sát thùng hàng, chỉ phát hiện khi cháy ra ngoài", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chở hóa chất/hàng nguy hiểm trong thùng kín, không giám sát, đường dài không kiểm tra", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phương tiện giao thông có khu vực riêng cho hành lý và hàng hóa tách biệt với khoang hành khách, với vách ngăn chống cháy không?", "options": [
            {"key": "A", "text": "Khoang hành lý tách biệt hoàn toàn, có vách ngăn, không thông với khoang hành khách", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Khoang hành lý riêng nhưng vách ngăn bằng vật liệu thường, không chống cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hành lý để lẫn trong khoang khách, hàng hóa chất trên lối đi", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàng hóa dễ cháy, bình gas, xăng để lẫn trong khoang hành khách", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_H = {
    "name": "Đặc thù: Khu dân cư, nhà ở, nhà trọ",
    "description": "Câu hỏi cho nhà ở đơn lẻ, nhà trọ, chung cư mini",
    "icon": "🏘️", "color": "#059669", "facility_type": "residential",
    "questions": [
        {"text": "Nhà trọ, chung cư mini có mấy lối thoát nạn độc lập, và các lối thoát có thông thoáng 24/7 không?", "options": [
            {"key": "A", "text": "Có ≥ 2 lối thoát nạn độc lập, luôn thông thoáng, đèn EXIT hoạt động, có thang thoát hiểm phụ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có 2 lối nhưng 1 lối phụ (ban công, cửa sổ), lối chính thông thoáng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có 1 cầu thang duy nhất, cửa thoát hiểm phụ bị khóa hoặc chặn đồ", "score": 2, "risk": "high"},
            {"key": "D", "text": "1 lối duy nhất, bị khóa cổng sắt ban đêm, không ai có chìa khóa dự phòng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu nhà trọ có hệ thống báo cháy (ít nhất cảm biến khói độc lập) lắp tại hành lang và từng phòng không?", "options": [
            {"key": "A", "text": "Cảm biến khói trong mỗi phòng trọ và hành lang, kiểm tra pin hàng tháng, có chuông báo chung", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cảm biến khói ở hành lang mỗi tầng nhưng chưa lắp trong từng phòng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ lắp ở cầu thang tầng 1, các tầng trên không có cảm biến", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bất kỳ cảm biến khói hay chuông báo cháy nào trong toàn bộ nhà trọ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cổng sắt, chuồng cọp, lưới chống trộm có được thiết kế lối mở khẩn cấp khi xảy ra sự cố cháy không?", "options": [
            {"key": "A", "text": "Không có chuồng cọp; hoặc có lối mở khẩn cấp bản lề, chìa khóa để cạnh, mọi người biết", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có cửa mở khẩn cấp trên chuồng cọp nhưng chìa khóa cất trong phòng, phải tìm", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chuồng cọp hàn kín, chỉ có 1 cửa ra vào chính, chưa có lối mở khẩn cấp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chuồng cọp hàn kín toàn bộ cửa sổ và ban công, không có bất kỳ lối mở nào", "score": 3, "risk": "critical"},
        ]},
        {"text": "Mỗi phòng trọ có mạch điện riêng với CB riêng, để khi 1 phòng có sự cố thì ngắt được mà không ảnh hưởng phòng khác không?", "options": [
            {"key": "A", "text": "Mỗi phòng có CB riêng, tổng có CB chống rò, công tơ riêng, sơ đồ mạch rõ ràng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có CB riêng mỗi phòng nhưng chưa có CB chống rò (ELCB) tổng", "score": 1, "risk": "low"},
            {"key": "C", "text": "2-3 phòng dùng chung CB, quá tải CB nhảy thì mất điện cả mấy phòng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Toàn bộ nhà trọ dùng chung 1 CB, dây điện nối tạm, nào CB nhảy nối tắt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bình nước nóng điện (máy nóng lạnh) trong các phòng trọ/phòng tắm được lắp đặt và sử dụng an toàn không?", "options": [
            {"key": "A", "text": "Bình nước nóng có ELCB riêng 30mA, nối đất đúng, bảo dưỡng hàng năm, còn bảo hành", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Bình nước nóng có ELCB nhưng lần lắp đặt đã lâu, chưa kiểm tra nối đất", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bình nước nóng cũ không có ELCB riêng, dùng chung CB với ổ cắm phòng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bình nước nóng rỉ sét, dây điện hở trong môi trường ẩm ướt, không ELCB, rất nguy hiểm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xe máy, xe đạp điện có được sạc tại khu vực riêng an toàn hay sạc ngay trong phòng trọ/phòng ngủ?", "options": [
            {"key": "A", "text": "Khu sạc xe riêng tầng trệt, thông thoáng, ổ cắm chuyên dụng, bình chữa cháy gần đó", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Sạc ở tầng trệt khu chung nhưng chưa có ổ cắm chuyên dụng hay bình chữa cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sạc xe máy/xe đạp điện trong phòng trọ, gần đồ dùng cá nhân", "score": 2, "risk": "high"},
            {"key": "D", "text": "Sạc xe điện qua đêm trong phòng ngủ kín, pin xe cũ phồng, dùng sạc kém chất lượng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Chủ nhà trọ có phổ biến quy tắc PCCC cho người thuê, niêm yết nội quy và sơ đồ thoát nạn mỗi tầng không?", "options": [
            {"key": "A", "text": "Nội quy PCCC lồng khung kính mỗi tầng, sơ đồ thoát nạn dán mỗi tầng, phổ biến cho người thuê mới", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có phổ biến miệng cho người thuê nhưng chưa niêm yết sơ đồ và nội quy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chưa phổ biến PCCC cho người thuê, niêm yết nội quy nhưng chữ mờ cũ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có nội quy, sơ đồ, phổ biến gì, người thuê không biết lối thoát nạn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Người thuê trọ có được phép nấu ăn bằng bếp gas trong phòng không? Nếu có, quản lý bình gas như thế nào?", "options": [
            {"key": "A", "text": "Cấm nấu gas trong phòng, có bếp chung hoặc bếp điện từ thay thế", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Cho phép dùng bếp gas mini nhỏ, dây dẫn mới, bình gas nhỏ, phòng thông thoáng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Dùng bếp gas trong phòng trọ nhỏ kín, bình gas 12kg, thông gió kém", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bếp gas trong phòng trọ kín, dây gas cũ nứt, bình gas để dưới gầm giường", "score": 3, "risk": "critical"},
        ]},
        {"text": "Có ai giữ chìa khóa tổng (master key) của toàn bộ phòng trọ và chìa khóa cổng khẩn cấp không?", "options": [
            {"key": "A", "text": "Chủ nhà/quản lý giữ master key 24/7, chìa khóa cổng khẩn cấp đặt trong hộp kính phá vỡ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Chủ nhà giữ master key nhưng không ở tại chỗ 24/7, ban đêm phải gọi điện", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chìa khóa tổng chỉ chủ nhà có, chủ nhà ở xa, ban đêm không liên lạc được", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có master key, mỗi phòng khóa riêng, cổng khóa xích, khi cháy không mở được", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu dân cư, hẻm nhỏ có trụ nước cứu hỏa gần nhất trong phạm vi bao nhiêu mét, và xe cứu hỏa có vào được không?", "options": [
            {"key": "A", "text": "Trụ nước cứu hỏa trong phạm vi 150m, đường rộng ≥ 3.5m xe cứu hỏa vào được", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Trụ nước cứu hỏa gần nhưng đường hẻm hơi hẹp, xe cứu hỏa phải đỗ ngoài", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không biết trụ nước gần nhất ở đâu, hẻm nhỏ xe cứu hỏa không vào được", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có trụ nước cứu hỏa gần đây, hẻm cụt xe cứu hỏa không thể tiếp cận", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_I = {
    "name": "Đặc thù: Công trình xây dựng đang thi công",
    "description": "Công trình đang xây dựng, cải tạo, sửa chữa lớn",
    "icon": "🏗️", "color": "#78716c", "facility_type": "construction",
    "questions": [
        {"text": "Công trình có quy trình cấp giấy phép hàn cắt (Hot Work Permit) cho mọi hoạt động phát sinh tia lửa không?", "options": [
            {"key": "A", "text": "Có giấy phép bắt buộc, kiểm tra hiện trường, dọn vật dễ cháy 10m, canh lửa sau 30 phút", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có giấy phép nhưng không phải lúc nào cũng kiểm tra hiện trường trước khi hàn", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hàn cắt tự do không cần giấy phép, đôi khi dọn vật dễ cháy xung quanh", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hàn cắt không kiểm soát, tia lửa bắn vào vật liệu dễ cháy, đã có cháy nhỏ nhiều lần", "score": 3, "risk": "critical"},
        ]},
        {"text": "Vật liệu xây dựng dễ cháy (gỗ ván khuôn, xốp cách nhiệt, bạt che, sơn) được bảo quản tại công trình như thế nào?", "options": [
            {"key": "A", "text": "Kho riêng, cách khu thi công ≥ 10m, biển cấm lửa, bình chữa cháy gần đó", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Để khu riêng nhưng gần khu thi công, có bình chữa cháy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Để rải rác khắp công trình, gần khu hàn cắt, không có biện pháp bảo vệ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Gỗ, xốp, sơn chất đống lẫn lộn sát khu hàn cắt và thiết bị điện tạm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống điện tạm thi công có được thiết kế và lắp đặt bởi thợ điện có chứng chỉ không?", "options": [
            {"key": "A", "text": "Hệ thống điện tạm do thợ điện có chứng chỉ lắp, tủ điện tạm có CB, ELCB, nối đất", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thợ điện lắp nhưng chưa có ELCB chống rò, chỉ có CB thông thường", "score": 1, "risk": "low"},
            {"key": "C", "text": "Công nhân tự kéo điện, nối tạm, dây vắt qua khung thép, không có CB riêng", "score": 2, "risk": "high"},
            {"key": "D", "text": "Điện kéo tạm bằng dây trần, nối bằng băng keo, ngâm nước khi mưa, rất nguy hiểm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Tầng hầm và khu vực kín của công trình có hệ thống thông gió đủ khi sử dụng sơn, keo, dung môi không?", "options": [
            {"key": "A", "text": "Có quạt thông gió cưỡng bức, đo nồng độ VOC, thiết bị điện phòng nổ trong vùng kín", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quạt thông gió nhưng không đo nồng độ hơi  dung môi", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có thông gió cơ học, chỉ mở cửa tự nhiên, hơi dung môi tích tụ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Phun sơn/keo trong tầng hầm kín, không thông gió, dùng đèn sợi đốt chiếu sáng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bình gas phục vụ thi công (hàn hơi, cắt gas) được bảo quản và sử dụng tại công trình như thế nào?", "options": [
            {"key": "A", "text": "Bình gas đứng, buộc cố định, nắp bảo vệ van, cách nguồn nhiệt ≥ 3m, kho riêng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Bình gas buộc cố định khi dùng, cất trong khu riêng khi không dùng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bình gas để nằm, không buộc, nắp bảo vệ van bị mất, gần khu hàn cắt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bình gas oxy và bình gas axetylen để sát nhau, nằm trên sàn, không buộc, rất dễ nổ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Công nhân trên công trình có được đào tạo PCCC, biết vị trí bình chữa cháy và lối thoát nạn tại công trình không?", "options": [
            {"key": "A", "text": "100% công nhân được đào tạo PCCC trước khi vào công trình, biết vị trí bình chữa cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Chỉ đội trưởng và kỹ sư được đào tạo, công nhân được phổ biến sơ qua", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có đào tạo PCCC, công nhân không biết bình chữa cháy ở đâu", "score": 2, "risk": "high"},
            {"key": "D", "text": "Công nhân thời vụ vào ra tự do, không đào tạo, không biết lối thoát nạn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Rác thải xây dựng dễ cháy (gỗ vụn, xốp thừa, bao bì, vải bạt cũ) có được thu gom và xử lý kịp thời không?", "options": [
            {"key": "A", "text": "Thu gom cuối mỗi ngày, đổ tại bãi rác riêng xa công trình, không đốt tại chỗ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thu gom 2-3 ngày/lần, chất tại góc công trình chờ xe đến lấy", "score": 1, "risk": "low"},
            {"key": "C", "text": "Rác xây dựng tích nhiều ngày, chất đống gần khu thi công, gần dây điện tạm", "score": 2, "risk": "high"},
            {"key": "D", "text": "Công nhân tự đốt rác xây dựng tại công trình, gần kho vật tư và bình gas", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhà tạm của công nhân (lán trại) tại công trình có đáp ứng yêu cầu PCCC không?", "options": [
            {"key": "A", "text": "Lán trại bằng vật liệu khó cháy, cách công trình ≥ 10m, có cảm biến khói và bình chữa cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Lán trại tôn thiếc, cách công trình, có bình chữa cháy nhưng không có cảm biến khói", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lán trại bằng gỗ/bạt dựng sát công trình, không bình chữa cháy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Lán trại bạt/gỗ dễ cháy, nấu ăn bếp gas trong lán, sạc điện thoại tạm, rất nguy hiểm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Giàn giáo có che bạt chống bụi/nắng bằng vật liệu dễ cháy không? Bạt có tiếp xúc với nguồn nhiệt không?", "options": [
            {"key": "A", "text": "Không dùng bạt; hoặc dùng bạt chống cháy, cách xa khu hàn cắt, có biện pháp chống tia lửa", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Bạt PE thường nhưng cách xa khu hàn cắt, không tiếp xúc nguồn nhiệt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bạt PE phủ giàn giáo gần khu hàn cắt, tia lửa có thể bắn tới", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bạt dễ cháy bao quanh toàn bộ công trình, hàn cắt bên trong, tia lửa bắn vào bạt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cần trục, thang máy xây dựng (vận thăng) có nguy cơ chập cháy hệ thống điện điều khiển không?", "options": [
            {"key": "A", "text": "Không có cần trục/vận thăng; hoặc kiểm tra hệ thống điện hàng tuần, bảo dưỡng đúng lịch", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra khi bảo dưỡng định kỳ, hoạt động bình thường", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hệ thống điện cần trục cũ, dây cáp điều khiển mòn, chưa thay thế", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hệ thống điện cần trục hỏng, chập cháy, motor bốc khói vẫn vận hành", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_J = {
    "name": "Đặc thù: Cơ quan, văn phòng, trụ sở",
    "description": "Câu hỏi cho cơ quan hành chính, văn phòng làm việc",
    "icon": "🏛️", "color": "#4f46e5", "facility_type": "office",
    "questions": [
        {"text": "Kho lưu trữ hồ sơ, giấy tờ, tài liệu tại cơ quan có được bảo vệ bằng hệ thống PCCC chuyên dụng không?", "options": [
            {"key": "A", "text": "Kho riêng, tường chống cháy, cửa chống cháy, báo cháy sớm, bình CO₂, hồ sơ có sao lưu số", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kho riêng có bình chữa cháy nhưng chưa có hệ thống báo cháy riêng cho kho", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hồ sơ giấy chất đống trong phòng làm việc, gần ổ cắm điện và máy photocopy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hồ sơ giấy chất đống trong kho kín không PCCC, là bản gốc duy nhất, mất là mất", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên có thói quen rút phích cắm các thiết bị điện (ấm nước, máy pha cà phê, quạt sưởi) trước khi ra về không?", "options": [
            {"key": "A", "text": "Có quy định bắt buộc rút phích cắm, người cuối cùng kiểm tra và ký xác nhận", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có nhắc nhở nhưng phụ thuộc ý thức cá nhân, đôi khi quên rút ấm nước", "score": 1, "risk": "low"},
            {"key": "C", "text": "Nhiều thiết bị để chế độ chờ qua đêm, ấm nước điện cắm suốt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Quạt sưởi, ấm đun nước chạy suốt đêm không ai tắt, đã có ấm cạn nước bốc khói", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng máy photocopy, máy in chuyên dụng có thông gió tốt và được kiểm soát nhiệt độ không?", "options": [
            {"key": "A", "text": "Phòng riêng có ĐHKK, thông gió tốt, bình chữa cháy CO₂, CB riêng cho máy in", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Máy photocopy đặt trong phòng làm việc chung, ĐHKK hoạt động bình thường", "score": 1, "risk": "low"},
            {"key": "C", "text": "Máy in/photocopy cũ tỏa nhiệt nhiều, đặt trong phòng kín nhỏ, giấy chất xung quanh", "score": 2, "risk": "high"},
            {"key": "D", "text": "Máy cũ nóng bất thường, bốc mùi nhựa khét, giấy chất đống sát máy, chưa sửa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hành lang và cầu thang thoát nạn trong tòa nhà văn phòng có được duy trì thông thoáng và đèn chiếu sáng sự cố hoạt động không?", "options": [
            {"key": "A", "text": "Hành lang và cầu thang thông thoáng, cửa ngăn khói tự đóng, đèn sự cố hoạt động, test hàng tháng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Hành lang thông thoáng, đèn sự cố có nhưng lâu chưa test, không rõ hoạt động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hành lang để bàn ghế, tủ hồ sơ, đèn sự cố một số đã hỏng chưa thay", "score": 2, "risk": "high"},
            {"key": "D", "text": "Cầu thang thoát nạn bị khóa, hành lang chất đầy đồ, đèn sự cố không có", "score": 3, "risk": "critical"},
        ]},
        {"text": "Tòa nhà văn phòng có hệ thống quản lý ra vào (access control) kết hợp với hệ thống PCCC (tự mở cửa khi báo cháy) không?", "options": [
            {"key": "A", "text": "Có access control kết nối hệ thống báo cháy, tự mở khóa cửa thoát nạn khi báo cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có access control nhưng chưa kết nối hệ thống báo cháy, cửa thoát nạn luôn mở từ trong", "score": 1, "risk": "low"},
            {"key": "C", "text": "Cửa thoát nạn bị khóa điện, khi mất điện hoặc cháy phải mở bằng tay từ phòng bảo vệ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Cửa thoát nạn khóa cơ, chỉ bảo vệ có chìa, ban đêm không ai mở được", "score": 3, "risk": "critical"},
        ]},
        {"text": "Bếp ăn tập thể, phòng ăn nhân viên trong cơ quan có hệ thống hút khói bếp và bình chữa cháy phù hợp không?", "options": [
            {"key": "A", "text": "Có quạt hút khói, bình chữa cháy loại K/F cho bếp, bếp điện từ, không dùng gas", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Dùng bếp gas có quạt hút, bình chữa cháy bột ABC gần bếp", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bếp gas trong phòng nhỏ ít thông gió, bình chữa cháy ở hành lang, xa bếp", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nhân viên tự nấu bằng bếp cồn/bếp gas mini tại bàn làm việc, không có PCCC", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng hội nghị, hội trường có lắp đặt đèn EXIT, đèn chiếu sáng sự cố và kiểm soát số người tối đa không?", "options": [
            {"key": "A", "text": "Đèn EXIT hoạt động, đèn sự cố tại lối thoát, biển ghi sức chứa tối đa, kiểm tra định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có đèn EXIT nhưng chưa có biển ghi sức chứa tối đa", "score": 1, "risk": "low"},
            {"key": "C", "text": "Đèn EXIT hỏng một số, đèn sự cố không có, không biết sức chứa tối đa", "score": 2, "risk": "high"},
            {"key": "D", "text": "Phòng hội nghị kín, không đèn EXIT, không đèn sự cố, chứa vượt sức chứa thiết kế", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cơ quan có quy trình ứng phó khi có tin nhắn đe dọa cháy nổ hoặc phát hiện vật thể lạ nghi ngờ không?", "options": [
            {"key": "A", "text": "Có quy trình rõ ràng: báo bảo vệ, sơ tán, cách ly vật thể, gọi Cảnh sát, đã diễn tập", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có quy trình trên giấy nhưng chưa diễn tập và phổ biến cho toàn bộ nhân viên", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có quy trình cụ thể, phụ thuộc vào phán đoán cá nhân bảo vệ", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có quy trình, không ai biết phải làm gì, cơ quan là mục tiêu có nguy cơ", "score": 3, "risk": "critical"},
        ]},
        {"text": "Thang máy trong tòa nhà văn phòng có chế độ vận hành đặc biệt khi có cháy (Firefighter Mode) không?", "options": [
            {"key": "A", "text": "Thang máy có Firefighter Mode, tự về tầng 1 khi báo cháy, chìa khóa cho lực lượng PCCC", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thang máy ngắt khi báo cháy nhưng không có chế độ Firefighter dành cho lực lượng PCCC", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thang máy không kết nối hệ thống báo cháy, vẫn chạy bình thường khi có cháy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thang máy cũ, đôi khi kẹt giữa chừng, không có chế độ cháy, người dùng khi cháy có thể bị kẹt", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cơ quan có bảo dưỡng hệ thống ĐHKK trung tâm và kiểm tra nguy cơ cháy từ dàn nóng/dàn lạnh định kỳ không?", "options": [
            {"key": "A", "text": "Bảo dưỡng ĐHKK 6 tháng/lần bởi đơn vị chuyên nghiệp, kiểm tra hệ thống điện và gas lạnh", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Vệ sinh filter hàng năm, chưa kiểm tra chuyên sâu hệ thống điện và gas lạnh", "score": 1, "risk": "low"},
            {"key": "C", "text": "ĐHKK chạy liên tục nhiều năm, chưa bảo dưỡng, dàn nóng rung lắc bất thường", "score": 2, "risk": "high"},
            {"key": "D", "text": "ĐHKK cũ rò gas lạnh, dàn nóng bốc mùi khét, dây điện nóng bất thường, vẫn chạy", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_K = {
    "name": "Đặc thù: Nghiên cứu, phòng thí nghiệm",
    "description": "Câu hỏi cho cơ sở nghiên cứu khoa học, phòng thí nghiệm",
    "icon": "🔬", "color": "#7c3aed", "facility_type": "laboratory",
    "questions": [
        {"text": "Hóa chất trong phòng thí nghiệm có được bảo quản theo bảng tương thích hóa chất (Chemical Compatibility Chart) không?", "options": [
            {"key": "A", "text": "Có bảng tương thích, hóa chất phân loại theo nhóm, tách riêng axit-bazơ-oxy hóa-dễ cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Phân loại sơ bộ nhưng chưa tách riêng hoàn toàn, bảng tương thích chưa niêm yết", "score": 1, "risk": "low"},
            {"key": "C", "text": "Hóa chất để lẫn lộn, axit gần bazơ, chất oxy hóa gần chất dễ cháy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hóa chất không phân loại, để tràn lan, đã xảy ra phản ứng ngoài ý muốn", "score": 3, "risk": "critical"},
        ]},
        {"text": "Tủ hút khí độc (fume hood) trong phòng thí nghiệm có hoạt động đúng và được kiểm tra định kỳ không?", "options": [
            {"key": "A", "text": "Tủ hút kiểm tra lưu lượng gió hàng năm, đạt ≥ 0.5 m/s, có báo lỗi khi quạt hỏng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Tủ hút hoạt động nhưng lâu chưa đo lưu lượng gió, không rõ có đạt chuẩn không", "score": 1, "risk": "low"},
            {"key": "C", "text": "Tủ hút lực hút yếu, cửa kính lên xuống nặng, hơi hóa chất có thoát ra ngoài", "score": 2, "risk": "high"},
            {"key": "D", "text": "Tủ hút hỏng không sử dụng được, vẫn thao tác hóa chất dễ bay hơi ngoài tủ hút", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng thí nghiệm có hệ thống rửa mắt khẩn cấp (eyewash) và vòi sen khẩn cấp (safety shower) hoạt động không?", "options": [
            {"key": "A", "text": "Có eyewash và safety shower trong vòng 10 giây đi bộ, test hàng tuần, nước xả thông", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có nhưng lâu chưa test, không rõ nước có chảy thông hay không", "score": 1, "risk": "low"},
            {"key": "C", "text": "Có eyewash nhưng không có safety shower, hoặc vị trí quá xa", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có eyewash hay safety shower nào trong phòng thí nghiệm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Nhân viên phòng thí nghiệm có được đào tạo về xử lý sự cố đổ tràn hóa chất (spill response) không?", "options": [
            {"key": "A", "text": "100% được đào tạo, có bộ kit xử lý tràn đổ (spill kit), biết khi nào phải sơ tán", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có spill kit nhưng chỉ quản phòng biết sử dụng, nhân viên mới chưa được đào tạo", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có spill kit, khi đổ hóa chất thì lau bằng giẻ thường", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không ai biết xử lý khi đổ tràn, đã từng đổ axit mà không biết trung hòa", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khí nén, gas thí nghiệm (H₂, O₂, N₂, Ar, He) có được buộc cố định vào tường và có van ngắt khẩn cấp ngoài phòng không?", "options": [
            {"key": "A", "text": "Bình gas buộc cố định, van ngắt ngoài phòng, kiểm tra rò rỉ hàng tháng, nhãn đầy đủ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Bình gas buộc cố định nhưng van ngắt chung ở trong phòng, chưa kiểm tra rò rỉ", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bình gas không buộc, đứng tự do, van ngắt ở trên bình, phải vào phòng để ngắt", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bình H₂ hoặc O₂ không buộc, nằm nghiêng, gần nguồn nhiệt, không van ngắt ngoài", "score": 3, "risk": "critical"},
        ]},
        {"text": "Tủ bảo quản hóa chất dễ cháy trong phòng thí nghiệm có phải tủ chống cháy chuyên dụng (flammable storage cabinet) không?", "options": [
            {"key": "A", "text": "Tủ chống cháy đạt chuẩn FM/UL, tự đóng, thông gió, dung tích đúng quy định", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Tủ kim loại có khóa nhưng không phải tủ chống cháy chuyên dụng", "score": 1, "risk": "low"},
            {"key": "C", "text": "Để hóa chất dễ cháy trong tủ gỗ hoặc ngăn kéo bàn làm việc", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hóa chất dễ cháy để ngoài bàn, gần bếp đun/nguồn nhiệt, chai hở nắp", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng thí nghiệm có bình chữa cháy phù hợp (CO₂ cho thiết bị, bột cho hóa chất, cát cho kim loại hoạt tính) không?", "options": [
            {"key": "A", "text": "Có bình phù hợp từng loại nguy cơ, vị trí rõ ràng, kiểm tra hàng tháng, nhân viên biết dùng", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có bình chữa cháy bột ABC, chưa có bình riêng cho thiết bị điện và kim loại", "score": 1, "risk": "low"},
            {"key": "C", "text": "Chỉ có 1 bình chữa cháy ở hành lang, trong phòng thí nghiệm không có bình", "score": 2, "risk": "high"},
            {"key": "D", "text": "Không có bình chữa cháy, chỉ có nước vòi (không phù hợp cho nhiều loại cháy hóa chất)", "score": 3, "risk": "critical"},
        ]},
        {"text": "Chất thải hóa chất nguy hại có được thu gom, phân loại và xử lý đúng quy định không?", "options": [
            {"key": "A", "text": "Thu gom trong thùng chuyên dụng có nhãn, phân loại theo nhóm, hợp đồng xử lý với đơn vị có phép", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Thu gom riêng nhưng chưa phân loại chi tiết, đang tìm đơn vị xử lý", "score": 1, "risk": "low"},
            {"key": "C", "text": "Đổ chất thải hóa chất xuống bồn rửa hoặc thùng rác thường", "score": 2, "risk": "high"},
            {"key": "D", "text": "Chất thải nguy hại chất đống trong phòng, chai lọ hở nắp, nguy cơ phản ứng", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng thí nghiệm có nguy cơ cháy nổ do sử dụng laser, lò nung mẫu, bếp cách thủy hoặc thiết bị gia nhiệt không?", "options": [
            {"key": "A", "text": "Thiết bị gia nhiệt có thermostat, ngắt quá nhiệt, cách xa hóa chất dễ cháy, có giám sát", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có thermostat nhưng đôi khi để chạy không giám sát khi ra ngoài nghỉ trưa", "score": 1, "risk": "low"},
            {"key": "C", "text": "Lò nung/bếp cách thủy chạy qua đêm không ai giám sát, gần hóa chất trên bàn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thiết bị gia nhiệt tự chế, không thermostat, chạy liên tục, gần dung môi dễ cháy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Phòng thí nghiệm có quy trình khóa/mở (Lock-Out/Tag-Out) cho thiết bị đang bảo dưỡng để ngăn vận hành ngoài ý muốn không?", "options": [
            {"key": "A", "text": "Có quy trình LOTO đầy đủ, khóa chuyên dụng, biển cảnh báo, nhân viên được đào tạo", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có ghi chú 'đang sửa chữa' nhưng không có khóa chuyên dụng ngăn vận hành", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có quy trình LOTO, đôi khi người khác bật thiết bị đang sửa ngoài ý muốn", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đã xảy ra sự cố do bật thiết bị đang sửa, chưa có biện pháp khắc phục", "score": 3, "risk": "critical"},
        ]},
    ]
}
SPECIFIC_CATEGORY_L = {
    "name": "Đặc thù: Nông nghiệp, chế biến nông lâm sản",
    "description": "Xưởng xay xát, kho thóc, xưởng chế biến gỗ, trại chăn nuôi",
    "icon": "🌾", "color": "#65a30d", "facility_type": "agriculture",
    "questions": [
        {"text": "Xưởng xay xát, xưởng chế biến lúa gạo có hệ thống hút bụi và kiểm soát nguy cơ nổ bụi ngũ cốc không?", "options": [
            {"key": "A", "text": "Có hệ thống hút bụi cyclone, van xả áp nổ, vệ sinh bụi hàng ngày, thiết bị Ex", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có hút bụi nhưng chưa có van xả áp, vệ sinh bụi hàng tuần", "score": 1, "risk": "low"},
            {"key": "C", "text": "Bụi ngũ cốc tích dày trên máy, trần, tường, không có hệ thống hút bụi", "score": 2, "risk": "high"},
            {"key": "D", "text": "Bụi lơ lửng dày đặc khi máy chạy, đã xảy ra cháy nhỏ do bụi, chưa khắc phục", "score": 3, "risk": "critical"},
        ]},
        {"text": "Kho thóc, kho gạo, kho nông sản có kiểm tra nhiệt độ bên trong đống hàng để phát hiện tự phát nhiệt không?", "options": [
            {"key": "A", "text": "Có que đo nhiệt hoặc cảm biến nhiệt cắm trong đống, kiểm tra hàng tuần, kho thông gió tốt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Kiểm tra định kỳ nhưng bằng sờ tay, kho thông gió tự nhiên", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không kiểm tra nhiệt, kho kín thông gió kém, nông sản ẩm khi nhập kho", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nông sản ẩm chất đống lớn trong kho kín, đã bốc nóng/mốc nhưng chưa xử lý", "score": 3, "risk": "critical"},
        ]},
        {"text": "Xưởng chế biến gỗ (cưa, bào, chà nhám) có hệ thống hút mùn cưa và kiểm soát nguy cơ cháy nổ bụi gỗ không?", "options": [
            {"key": "A", "text": "Có hệ thống hút mùn cưa tập trung, silo chứa có van xả áp, vệ sinh hàng ngày", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có hút bụi cục bộ tại máy, quét mùn cưa cuối ngày nhưng chưa có silo chứa", "score": 1, "risk": "low"},
            {"key": "C", "text": "Mùn cưa tích đống quanh máy, trên nóc máy, không hút bụi đúng cách", "score": 2, "risk": "high"},
            {"key": "D", "text": "Mùn cưa phủ dày khắp xưởng, máy móc nóng, đã cháy mùn cưa gần motor máy", "score": 3, "risk": "critical"},
        ]},
        {"text": "Lò sấy nông sản (sấy cà phê, tiêu, lúa, gỗ) có thermostat tự động và ngắt quá nhiệt dự phòng không?", "options": [
            {"key": "A", "text": "Lò sấy có thermostat tự động, ngắt quá nhiệt độc lập, bảo dưỡng định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có thermostat nhưng ngắt quá nhiệt chưa được test, sấy theo kinh nghiệm", "score": 1, "risk": "low"},
            {"key": "C", "text": "Sấy thủ công, điều chỉnh nhiệt bằng tay, phải canh suốt quá trình sấy", "score": 2, "risk": "high"},
            {"key": "D", "text": "Lò sấy tự chế, không thermostat, sấy qua đêm không ai canh, đã cháy sản phẩm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Hệ thống biogas (nếu có) tại trại chăn nuôi có cảm biến rò rỉ khí methane và van an toàn không?", "options": [
            {"key": "A", "text": "Không có biogas; hoặc có, cảm biến CH₄, van an toàn, kiểm tra đường ống định kỳ", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có van an toàn nhưng không có cảm biến khí, kiểm tra đường ống bằng mắt", "score": 1, "risk": "low"},
            {"key": "C", "text": "Đường ống biogas cũ, mối nối lỏng, không van an toàn, phát hiện rò bằng mùi", "score": 2, "risk": "high"},
            {"key": "D", "text": "Hệ  thống biogas rò rỉ nghiêm trọng, mùi gas quanh trại, gần bếp nấu ăn công nhân", "score": 3, "risk": "critical"},
        ]},
        {"text": "Máy xay, máy nghiền, máy ép có lắp thiết bị phát hiện kim loại hoặc dị vật để ngăn tia lửa va chạm không?", "options": [
            {"key": "A", "text": "Có đầu dò kim loại tự động, ngắt máy khi phát hiện dị vật, nam châm bẫy sắt", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có nam châm bẫy sắt nhưng không có đầu dò tự động", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có thiết bị phát hiện, đôi khi đá, sắt vào máy gây tia lửa", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thường xuyên có dị vật gây tia lửa trong máy xay, trong môi trường bụi ngũ cốc", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực phun thuốc trừ sâu, phân bón hóa học có được cách ly khỏi kho nông sản và khu sinh hoạt không?", "options": [
            {"key": "A", "text": "Kho thuốc riêng biệt, có khóa, tường chống cháy, cách kho nông sản và nhà ở ≥ 10m", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có khu riêng nhưng chưa có tường ngăn cháy, cách kho nông sản vài mét", "score": 1, "risk": "low"},
            {"key": "C", "text": "Thuốc trừ sâu để chung kho nông sản, không nhãn riêng, gần khu ở", "score": 2, "risk": "high"},
            {"key": "D", "text": "Thuốc trừ sâu dạng dung môi dễ cháy để lẫn kho gạo, gần bếp nấu, rất nguy hiểm", "score": 3, "risk": "critical"},
        ]},
        {"text": "Trại chăn nuôi có biện pháp phòng cháy cho khu chuồng trại (quạt thông gió, đèn sưởi gia súc, hệ thống điện) không?", "options": [
            {"key": "A", "text": "Điện chuồng trại có CB riêng, ELCB, đèn sưởi có bảo vệ, cách rơm ≥ 1m, bình chữa cháy", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có CB nhưng đèn sưởi để gần rơm hơn quy định, vẫn theo dõi", "score": 1, "risk": "low"},
            {"key": "C", "text": "Đèn sưởi treo sát rơm/cỏ khô, dây điện kéo qua chuồng, không ELCB", "score": 2, "risk": "high"},
            {"key": "D", "text": "Dây điện bị chuột gặm trong chuồng, đèn sưởi chạm rơm khô, đã cháy nhỏ 1 lần", "score": 3, "risk": "critical"},
        ]},
        {"text": "Khu vực phơi sấy nông sản ngoài trời (sân phơi, giàn phơi) gần đường dây điện cao thế hoặc nguồn phát tia lửa không?", "options": [
            {"key": "A", "text": "Sân phơi cách xa đường dây điện cao thế, không gần nguồn lửa, có rào chắn", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Sân phơi gần dây điện hạ thế nhưng cách an toàn, không có nguồn lửa gần", "score": 1, "risk": "low"},
            {"key": "C", "text": "Phơi sấy nông sản ngay dưới đường dây điện, gần khu đốt rác thải", "score": 2, "risk": "high"},
            {"key": "D", "text": "Nông sản khô phơi sát đường dây điện rủ võng, gần lò đốt/bếp, mùa gió lốc", "score": 3, "risk": "critical"},
        ]},
        {"text": "Cơ sở nông nghiệp có phương án PCCC phù hợp mùa khô hanh khi nguy cơ cháy đồng, cháy rừng cao không?", "options": [
            {"key": "A", "text": "Có kế hoạch mùa khô: tăng cường tuần tra, đường ngăn lửa, liên lạc lực lượng C.sát PCCC", "score": 0, "risk": "safe"},
            {"key": "B", "text": "Có nhận thức về nguy cơ mùa khô nhưng chưa có kế hoạch cụ thể văn bản", "score": 1, "risk": "low"},
            {"key": "C", "text": "Không có kế hoạch, mùa khô vẫn đốt rơm rạ trên đồng gần kho nông sản", "score": 2, "risk": "high"},
            {"key": "D", "text": "Đốt rơm mùa khô gần kho, trại, đường dây điện, đã cháy lan 1 lần trước đây", "score": 3, "risk": "critical"},
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
