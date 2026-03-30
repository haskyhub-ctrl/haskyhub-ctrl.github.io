# === CÁC NHÓM ĐẶC THÙ CÒN LẠI (mỗi nhóm 5 câu) ===

SPEC_D = {"name": "Đặc thù: Nhà hàng, khách sạn, chợ, TTTM", "description": "Dấu hiệu nguy cơ cháy nổ cho nhà hàng, khách sạn, chợ, TTTM",
    "questions": [
    {"text": "Ống hút khói bếp có mùi khét, quạt chạy chậm, mỡ nhỏ giọt ngược không?",
     "options": [{"key":"A","text":"Vệ sinh mỗi 3 tháng, hoạt động tốt","score":0,"risk":"safe"},{"key":"B","text":"Tự vệ sinh, quạt bình thường","score":1,"risk":"low"},{"key":"C","text":"Bộ lọc mỡ bám dày, quạt chậm, mùi khét","score":2,"risk":"high"},{"key":"D","text":"Chưa bao giờ vệ sinh, mỡ nhỏ ngược, đã cháy mỡ nhỏ","score":3,"risk":"critical"}]},
    {"text": "Tiểu thương có dùng bếp gas/bếp cồn ngay tại gian hàng trong chợ/TTTM không?",
     "options": [{"key":"A","text":"Cấm tuyệt đối, kiểm tra hàng ngày","score":0,"risk":"safe"},{"key":"B","text":"Có quy tắc cấm nhưng kiểm tra không thường xuyên","score":1,"risk":"low"},{"key":"C","text":"Biết tiểu thương dùng nhưng không xử lý","score":2,"risk":"high"},{"key":"D","text":"Nhiều gian hàng dùng bếp gas thoải mái, bình gas trong gian hàng kín","score":3,"risk":"critical"}]},
    {"text": "Cửa kho hàng trong TTTM có luôn bị chèn mở suốt ngày không?",
     "options": [{"key":"A","text":"Cửa chống cháy tự đóng, kết nối hệ thống báo cháy","score":0,"risk":"safe"},{"key":"B","text":"Tự đóng nhưng thỉnh thoảng chèn mở rồi đóng lại","score":1,"risk":"low"},{"key":"C","text":"Luôn bị chèn mở bằng gạch/nêm suốt ngày","score":2,"risk":"high"},{"key":"D","text":"Cửa kho hỏng, kho thông sàn bán hàng, hàng tràn ra","score":3,"risk":"critical"}]},
    {"text": "Bếp nhà hàng có hệ thống dập cháy dầu mỡ chuyên dụng hay chỉ có bình bột thường?",
     "options": [{"key":"A","text":"Có hệ thống dập cháy bếp tự động, kiểm tra 6 tháng","score":0,"risk":"safe"},{"key":"B","text":"Có bình chữa cháy bếp chuyên dụng, chưa có hệ thống tự động","score":1,"risk":"low"},{"key":"C","text":"Chỉ có bình bột ABC, không phù hợp cho cháy dầu mỡ","score":2,"risk":"high"},{"key":"D","text":"Không bình nào trong bếp, dập cháy dầu bằng nước","score":3,"risk":"critical"}]},
    {"text": "Lối thoát có bị đông nghịt vượt sức chứa trong sự kiện/giờ cao điểm không?",
     "options": [{"key":"A","text":"Có biển sức chứa, kiểm soát số người, đóng cửa khi đạt giới hạn","score":0,"risk":"safe"},{"key":"B","text":"Biết sức chứa nhưng chưa đếm người ra vào","score":1,"risk":"low"},{"key":"C","text":"Không biết sức chứa, sự kiện đông không giới hạn","score":2,"risk":"high"},{"key":"D","text":"Đông vượt sức chứa, lối thoát kẹt cứng, chen lấn nguy hiểm","score":3,"risk":"critical"}]},
]}

SPEC_E = {"name": "Đặc thù: Bệnh viện, trường học, cơ sở y tế", "description": "Dấu hiệu nguy cơ cho bệnh viện, trường học",
    "questions": [
    {"text": "Có phương án sơ tán cho bệnh nhân không tự đi (nằm liệt, máy trợ sự sống) không?",
     "options": [{"key":"A","text":"Có phương án, thiết bị sơ tán, đã diễn tập","score":0,"risk":"safe"},{"key":"B","text":"Có phương án chung, chưa có thiết bị chuyên dụng","score":1,"risk":"low"},{"key":"C","text":"Chỉ có kế hoạch cho người tự đi, bệnh nhân nặng chưa có","score":2,"risk":"high"},{"key":"D","text":"Không có phương án, bệnh nhân liệt tầng cao không thang cứu hỏa","score":3,"risk":"critical"}]},
    {"text": "Cồn y tế, formalin, hóa chất dễ cháy có đang để lẫn lộn gần ổ cắm, bồn rửa không?",
     "options": [{"key":"A","text":"Để trong tủ chống cháy, phân loại tương thích","score":0,"risk":"safe"},{"key":"B","text":"Tủ riêng có khóa nhưng không phải tủ chống cháy","score":1,"risk":"low"},{"key":"C","text":"Để lẫn trên kệ chung, gần bồn rửa và ổ cắm","score":2,"risk":"high"},{"key":"D","text":"Để tràn lan trên bàn, gần nguồn nhiệt, chai hở nắp","score":3,"risk":"critical"}]},
    {"text": "Đường ống oxy trong bệnh viện có dấu hiệu rò rỉ (mùi lạ, tiếng xì) không?",
     "options": [{"key":"A","text":"Có cảm biến rò, van ngắt khẩn, kiểm tra ống định kỳ","score":0,"risk":"safe"},{"key":"B","text":"Kiểm tra ống định kỳ nhưng chưa lắp cảm biến tự động","score":1,"risk":"low"},{"key":"C","text":"Ống cũ, chưa kiểm tra gần đây, không cảm biến","score":2,"risk":"high"},{"key":"D","text":"Ống rò rỉ, nồng độ oxy cao phòng kín, nguy cơ cháy bùng lớn","score":3,"risk":"critical"}]},
    {"text": "Phòng học có ≥2 cửa thoát? Cửa có bị khóa hoặc chất đồ trong giờ học không?",
     "options": [{"key":"A","text":"≥2 cửa mở ra ngoài, thanh đẩy khẩn cấp, đèn EXIT","score":0,"risk":"safe"},{"key":"B","text":"2 cửa nhưng 1 mở vào trong, không khóa","score":1,"risk":"low"},{"key":"C","text":"Chỉ 1 cửa, mở vào trong, bàn ghế chật","score":2,"risk":"high"},{"key":"D","text":"Cửa khóa từ ngoài trong giờ, cửa sổ song sắt, không thoát được","score":3,"risk":"critical"}]},
    {"text": "Trường có tổ chức diễn tập sơ tán cho học sinh, kể cả tình huống không báo trước không?",
     "options": [{"key":"A","text":"Diễn tập 2 lần/năm, phù hợp lứa tuổi, kể cả không báo trước","score":0,"risk":"safe"},{"key":"B","text":"1 lần/năm có báo trước, học sinh biết lối thoát","score":1,"risk":"low"},{"key":"C","text":"Chỉ phổ biến lý thuyết, chưa diễn tập thực tế","score":2,"risk":"high"},{"key":"D","text":"Chưa bao giờ diễn tập, học sinh không biết lối thoát","score":3,"risk":"critical"}]},
]}

SPEC_F = {"name": "Đặc thù: Xăng dầu, khí gas, vật liệu nổ", "description": "Dấu hiệu nguy cơ cho cây xăng, kho gas",
    "questions": [
    {"text": "Có vết dầu loang trên mặt sân cây xăng gợi ý rò rỉ bể ngầm/đường ống không?",
     "options": [{"key":"A","text":"Kiểm tra rò rỉ hàng năm bằng thiết bị, không vết dầu","score":0,"risk":"safe"},{"key":"B","text":"Kiểm tra bằng mắt hàng tháng, chưa thấy bất thường","score":1,"risk":"low"},{"key":"C","text":"Đôi khi thấy vết dầu loang trên sân chưa điều tra","score":2,"risk":"high"},{"key":"D","text":"Dầu rò rỉ từ bể ngầm, ngấm ra xung quanh, chưa sửa","score":3,"risk":"critical"}]},
    {"text": "Kho gas/LPG có mùi gas, cảm biến khí hoạt động, hệ thống thông gió chạy tốt không?",
     "options": [{"key":"A","text":"Cảm biến gas, van ngắt tự động, quạt thông gió 24/7","score":0,"risk":"safe"},{"key":"B","text":"Van ngắt tay, quạt thông gió, chưa có cảm biến tự động","score":1,"risk":"low"},{"key":"C","text":"Không cảm biến, thông gió tự nhiên, phát hiện rò bằng mũi","score":2,"risk":"high"},{"key":"D","text":"Kho kín, mùi gas rõ, chưa xử lý, không van ngắt khẩn cấp","score":3,"risk":"critical"}]},
    {"text": "Khách có tắt máy xe và không dùng điện thoại khi bơm xăng không?",
     "options": [{"key":"A","text":"Nhân viên yêu cầu nghiêm, biển cấm đầy đủ","score":0,"risk":"safe"},{"key":"B","text":"Có biển cấm, nhắc nhở nhưng chưa kiểm soát 100%","score":1,"risk":"low"},{"key":"C","text":"Có biển nhưng nhân viên ngại nhắc, nhiều khách dùng điện thoại","score":2,"risk":"high"},{"key":"D","text":"Không kiểm soát, khách vẫn nổ máy, hút thuốc khi bơm","score":3,"risk":"critical"}]},
    {"text": "Dây nối đất chống tĩnh điện bồn chứa và vòi bơm có bị đứt, gỉ sét không?",
     "options": [{"key":"A","text":"Kiểm tra hàng năm, dây tốt, điện trở đạt","score":0,"risk":"safe"},{"key":"B","text":"Có hệ thống nhưng lâu chưa kiểm tra","score":1,"risk":"low"},{"key":"C","text":"Dây nối đứt/gỉ ở một số vị trí","score":2,"risk":"high"},{"key":"D","text":"Không có hệ thống nối đất chống tĩnh điện","score":3,"risk":"critical"}]},
    {"text": "Nhân viên ca đêm có biết cách ngắt điện khẩn cấp, đóng van bể khi rò rỉ không?",
     "options": [{"key":"A","text":"Biết rõ: nút ngắt, van bể, quy trình sơ tán, số khẩn cấp","score":0,"risk":"safe"},{"key":"B","text":"Biết nút ngắt nhưng chưa thực hành bao giờ","score":1,"risk":"low"},{"key":"C","text":"Nhân viên mới, chưa biết quy trình khẩn cấp","score":2,"risk":"high"},{"key":"D","text":"Ca đêm 1 người, không biết quy trình, ngủ gật","score":3,"risk":"critical"}]},
]}

SPEC_G = {"name": "Đặc thù: Phương tiện giao thông", "description": "Dấu hiệu nguy cơ cháy nổ trên phương tiện giao thông",
    "questions": [
    {"text": "Xe khách/xe buýt có bình chữa cháy, búa thoát hiểm đầy đủ, hành khách biết vị trí không?",
     "options": [{"key":"A","text":"Đủ búa, cửa thoát hoạt động, tài xế thông báo trước chuyến","score":0,"risk":"safe"},{"key":"B","text":"Có búa và cửa thoát nhưng tài xế không thông báo","score":1,"risk":"low"},{"key":"C","text":"Búa thiếu hoặc giấu đi, cửa thoát bị kẹt","score":2,"risk":"high"},{"key":"D","text":"Không có búa, cửa thoát hàn kín hoặc chất hàng che","score":3,"risk":"critical"}]},
    {"text": "Hệ thống điện xe (dây, cầu chì, ắc-quy) có dấu hiệu chạm chập: khói, mùi khét?",
     "options": [{"key":"A","text":"Kiểm tra mỗi 6 tháng, dây tốt, cầu chì đúng","score":0,"risk":"safe"},{"key":"B","text":"Bảo dưỡng theo km, chưa kiểm tra điện riêng","score":1,"risk":"low"},{"key":"C","text":"Xe cũ, dây nối tạm băng keo, cầu chì dùng dây đồng","score":2,"risk":"high"},{"key":"D","text":"Đã có khói/tia lửa từ khoang điện, vẫn chạy","score":3,"risk":"critical"}]},
    {"text": "Khu sạc xe điện tại bãi đỗ có thông gió, bình chữa cháy, cách xa xe xăng không?",
     "options": [{"key":"A","text":"Khu sạc riêng, sprinkler, bình chữa cháy, sàn chống cháy","score":0,"risk":"safe"},{"key":"B","text":"Khu riêng, có bình chữa cháy nhưng chưa có sprinkler","score":1,"risk":"low"},{"key":"C","text":"Sạc trong bãi chung, gần xe xăng, không PCCC riêng","score":2,"risk":"high"},{"key":"D","text":"Sạc tầng hầm kín, không thông gió, không PCCC, qua đêm","score":3,"risk":"critical"}]},
    {"text": "Hàng hóa dễ cháy (bình gas, xăng) có đang để lẫn trong khoang hành khách không?",
     "options": [{"key":"A","text":"Khoang hành lý tách biệt, vách ngăn, không hàng nguy hiểm","score":0,"risk":"safe"},{"key":"B","text":"Khoang riêng nhưng vách ngăn bằng vật liệu thường","score":1,"risk":"low"},{"key":"C","text":"Hành lý để lẫn khoang khách, hàng chất trên lối đi","score":2,"risk":"high"},{"key":"D","text":"Bình gas, xăng để lẫn khoang hành khách","score":3,"risk":"critical"}]},
    {"text": "Xe tải chở hàng nguy hiểm có biển báo, bộ ứng phó sự cố trên xe không?",
     "options": [{"key":"A","text":"Không chở hàng nguy hiểm, hoặc đủ biển báo, bộ ứng phó","score":0,"risk":"safe"},{"key":"B","text":"Có biển báo nhưng bộ ứng phó chưa đầy đủ","score":1,"risk":"low"},{"key":"C","text":"Biển mờ, thiếu dụng cụ ứng phó","score":2,"risk":"high"},{"key":"D","text":"Chở hàng nguy hiểm không biển, không PCCC trên xe","score":3,"risk":"critical"}]},
]}

SPEC_I = {"name": "Đặc thù: Công trình xây dựng đang thi công", "description": "Dấu hiệu nguy cơ cho công trình xây dựng",
    "questions": [
    {"text": "Công trình có hàn cắt tự do không cần kiểm tra hiện trường, tia lửa bắn vào vật dễ cháy?",
     "options": [{"key":"A","text":"Có kiểm tra hiện trường trước, dọn vật cháy 10m, canh lửa sau","score":0,"risk":"safe"},{"key":"B","text":"Có kiểm tra nhưng không phải lúc nào cũng thực hiện","score":1,"risk":"low"},{"key":"C","text":"Hàn cắt tự do, đôi khi dọn vật dễ cháy","score":2,"risk":"high"},{"key":"D","text":"Hàn cắt không kiểm soát, tia lửa bắn vào vật cháy, đã cháy nhỏ","score":3,"risk":"critical"}]},
    {"text": "Gỗ ván khuôn, xốp cách nhiệt, sơn có đang chất đống sát khu hàn cắt và thiết bị điện tạm?",
     "options": [{"key":"A","text":"Kho riêng cách khu thi công ≥10m, có bình chữa cháy","score":0,"risk":"safe"},{"key":"B","text":"Khu riêng nhưng gần khu thi công, có bình chữa cháy","score":1,"risk":"low"},{"key":"C","text":"Rải rác khắp công trình, gần khu hàn cắt","score":2,"risk":"high"},{"key":"D","text":"Gỗ, xốp, sơn chất lẫn lộn sát khu hàn cắt và điện tạm","score":3,"risk":"critical"}]},
    {"text": "Điện tạm thi công có dây trần, nối băng keo, CB không có, ngâm nước khi mưa?",
     "options": [{"key":"A","text":"Thợ điện chứng chỉ lắp, tủ tạm có CB, ELCB, nối đất","score":0,"risk":"safe"},{"key":"B","text":"Thợ điện lắp, có CB nhưng chưa ELCB","score":1,"risk":"low"},{"key":"C","text":"Công nhân tự kéo, nối tạm, vắt qua khung thép, không CB","score":2,"risk":"high"},{"key":"D","text":"Dây trần, nối băng keo, ngâm nước khi mưa","score":3,"risk":"critical"}]},
    {"text": "Lán trại công nhân có bằng bạt/gỗ dễ cháy, nấu bếp gas trong lán, sạc điện tạm?",
     "options": [{"key":"A","text":"Lán vật liệu khó cháy, cách công trình, có cảm biến khói","score":0,"risk":"safe"},{"key":"B","text":"Lán tôn thiếc, cách công trình, có bình chữa cháy","score":1,"risk":"low"},{"key":"C","text":"Lán gỗ/bạt sát công trình, không bình chữa cháy","score":2,"risk":"high"},{"key":"D","text":"Lán bạt dễ cháy, nấu gas trong lán, sạc điện tạm, rất nguy hiểm","score":3,"risk":"critical"}]},
    {"text": "Rác xây dựng (gỗ vụn, xốp, bạt cũ) có đang tích đống gần dây điện tạm hoặc bình gas?",
     "options": [{"key":"A","text":"Thu gom cuối ngày, đổ bãi rác xa công trình","score":0,"risk":"safe"},{"key":"B","text":"Thu gom 2-3 ngày, chất góc công trình chờ xe lấy","score":1,"risk":"low"},{"key":"C","text":"Tích nhiều ngày, gần khu thi công, gần dây điện tạm","score":2,"risk":"high"},{"key":"D","text":"Công nhân tự đốt rác tại công trình, gần kho vật tư, bình gas","score":3,"risk":"critical"}]},
]}

SPEC_J = {"name": "Đặc thù: Cơ quan, văn phòng, trụ sở", "description": "Dấu hiệu nguy cơ cho văn phòng, cơ quan",
    "questions": [
    {"text": "Ấm nước, quạt sưởi, máy pha cà phê có đang cắm suốt đêm không ai tắt không?",
     "options": [{"key":"A","text":"Có nhắc rút phích cắm, người cuối kiểm tra","score":0,"risk":"safe"},{"key":"B","text":"Có nhắc nhưng phụ thuộc ý thức, đôi khi quên","score":1,"risk":"low"},{"key":"C","text":"Nhiều thiết bị chế độ chờ qua đêm, ấm nước cắm suốt","score":2,"risk":"high"},{"key":"D","text":"Quạt sưởi, ấm chạy suốt đêm, đã có ấm cạn bốc khói","score":3,"risk":"critical"}]},
    {"text": "Hồ sơ giấy tờ có chất đống gần ổ cắm, máy photocopy, không có bản sao lưu số?",
     "options": [{"key":"A","text":"Kho riêng, có PCCC, hồ sơ sao lưu số","score":0,"risk":"safe"},{"key":"B","text":"Kho riêng, bình chữa cháy, chưa sao lưu số","score":1,"risk":"low"},{"key":"C","text":"Chất đống phòng làm việc, gần ổ cắm, chưa sao lưu","score":2,"risk":"high"},{"key":"D","text":"Chất đống kho kín không PCCC, bản gốc duy nhất","score":3,"risk":"critical"}]},
    {"text": "Hành lang, cầu thang thoát nạn có bị bàn ghế, tủ hồ sơ chiếm chỗ không?",
     "options": [{"key":"A","text":"Hành lang thông, cửa ngăn khói tự đóng, đèn sự cố tốt","score":0,"risk":"safe"},{"key":"B","text":"Thông thoáng, đèn sự cố có nhưng lâu chưa test","score":1,"risk":"low"},{"key":"C","text":"Để bàn ghế, tủ hồ sơ, đèn sự cố một số hỏng","score":2,"risk":"high"},{"key":"D","text":"Cầu thang khóa, hành lang chất đầy đồ, không đèn sự cố","score":3,"risk":"critical"}]},
    {"text": "Máy photocopy, máy in cũ có tỏa nhiệt, bốc mùi nhựa khét, giấy chất sát máy không?",
     "options": [{"key":"A","text":"Phòng riêng thông gió, CB riêng, hoạt động bình thường","score":0,"risk":"safe"},{"key":"B","text":"Đặt phòng chung, ĐHKK bình thường","score":1,"risk":"low"},{"key":"C","text":"Máy cũ tỏa nhiệt nhiều, phòng kín nhỏ, giấy chất xung quanh","score":2,"risk":"high"},{"key":"D","text":"Máy nóng bất thường, mùi nhựa khét, giấy đống sát máy, chưa sửa","score":3,"risk":"critical"}]},
    {"text": "Thang máy văn phòng có tự về tầng 1 khi báo cháy không?",
     "options": [{"key":"A","text":"Có chế độ cháy, tự về tầng 1 khi báo cháy","score":0,"risk":"safe"},{"key":"B","text":"Ngắt khi báo cháy nhưng không có chế độ riêng cho PCCC","score":1,"risk":"low"},{"key":"C","text":"Không kết nối báo cháy, chạy bình thường khi cháy","score":2,"risk":"high"},{"key":"D","text":"Thang cũ, đôi khi kẹt, không chế độ cháy, nguy cơ kẹt người","score":3,"risk":"critical"}]},
]}

SPEC_K = {"name": "Đặc thù: Nghiên cứu, phòng thí nghiệm", "description": "Dấu hiệu nguy cơ cho phòng thí nghiệm",
    "questions": [
    {"text": "Hóa chất dễ cháy có đang để lẫn lộn không phân loại (axit gần bazơ, oxy hóa gần dễ cháy)?",
     "options": [{"key":"A","text":"Phân loại theo nhóm tương thích, tách riêng rõ ràng","score":0,"risk":"safe"},{"key":"B","text":"Phân loại sơ bộ, chưa tách hoàn toàn","score":1,"risk":"low"},{"key":"C","text":"Để lẫn lộn, axit gần bazơ, oxy hóa gần dễ cháy","score":2,"risk":"high"},{"key":"D","text":"Không phân loại, tràn lan, đã xảy ra phản ứng ngoài ý muốn","score":3,"risk":"critical"}]},
    {"text": "Tủ hút khí độc (fume hood) có lực hút yếu, hơi hóa chất thoát ra ngoài không?",
     "options": [{"key":"A","text":"Kiểm tra lưu lượng gió hàng năm, đạt yêu cầu","score":0,"risk":"safe"},{"key":"B","text":"Hoạt động nhưng lâu chưa đo, không rõ còn đạt không","score":1,"risk":"low"},{"key":"C","text":"Lực hút yếu, hơi hóa chất thoát ra ngoài","score":2,"risk":"high"},{"key":"D","text":"Tủ hút hỏng, vẫn thao tác hóa chất bay hơi ngoài tủ","score":3,"risk":"critical"}]},
    {"text": "Bình gas thí nghiệm (H₂, O₂) có buộc cố định không? Có van ngắt ngoài phòng không?",
     "options": [{"key":"A","text":"Buộc cố định, van ngắt ngoài phòng, kiểm tra rò rỉ","score":0,"risk":"safe"},{"key":"B","text":"Buộc cố định, van ngắt trong phòng, chưa kiểm tra rò","score":1,"risk":"low"},{"key":"C","text":"Không buộc, đứng tự do, phải vào phòng mới ngắt","score":2,"risk":"high"},{"key":"D","text":"H₂/O₂ không buộc, nghiêng, gần nguồn nhiệt, không van ngoài","score":3,"risk":"critical"}]},
    {"text": "Lò nung mẫu, bếp cách thủy có chạy qua đêm không ai giám sát, gần hóa chất?",
     "options": [{"key":"A","text":"Có tự ngắt quá nhiệt, cách xa hóa chất, có giám sát","score":0,"risk":"safe"},{"key":"B","text":"Có nhiệt kế nhưng đôi khi chạy không giám sát","score":1,"risk":"low"},{"key":"C","text":"Chạy qua đêm không giám sát, gần hóa chất trên bàn","score":2,"risk":"high"},{"key":"D","text":"Thiết bị tự chế, không tự ngắt, chạy liên tục gần dung môi","score":3,"risk":"critical"}]},
    {"text": "Chất thải hóa chất có đang đổ bồn rửa hoặc chất đống trong phòng, chai hở nắp?",
     "options": [{"key":"A","text":"Thu gom thùng chuyên dụng có nhãn, xử lý đúng cách","score":0,"risk":"safe"},{"key":"B","text":"Thu gom riêng nhưng chưa phân loại chi tiết","score":1,"risk":"low"},{"key":"C","text":"Đổ xuống bồn rửa hoặc thùng rác thường","score":2,"risk":"high"},{"key":"D","text":"Chất thải nguy hại đống trong phòng, chai hở, nguy cơ phản ứng","score":3,"risk":"critical"}]},
]}

SPEC_L = {"name": "Đặc thù: Nông nghiệp, chế biến nông lâm sản", "description": "Dấu hiệu nguy cơ cho nông nghiệp, chế biến",
    "questions": [
    {"text": "Xưởng xay xát, chế biến gỗ có bụi ngũ cốc/mùn cưa tích dày, lơ lửng trong không khí?",
     "options": [{"key":"A","text":"Có hệ thống hút bụi, vệ sinh hàng ngày","score":0,"risk":"safe"},{"key":"B","text":"Có hút bụi nhưng vệ sinh hàng tuần","score":1,"risk":"low"},{"key":"C","text":"Bụi tích dày trên máy, trần, tường, không hút bụi","score":2,"risk":"high"},{"key":"D","text":"Bụi dày đặc khi máy chạy, đã cháy nhỏ do bụi, chưa khắc phục","score":3,"risk":"critical"}]},
    {"text": "Nông sản trong kho có bốc nóng, mốc ẩm nhưng chưa xử lý?",
     "options": [{"key":"A","text":"Có kiểm tra nhiệt, kho thông gió tốt","score":0,"risk":"safe"},{"key":"B","text":"Kiểm tra bằng sờ tay, kho thông gió tự nhiên","score":1,"risk":"low"},{"key":"C","text":"Không kiểm tra, kho kín, nông sản ẩm khi nhập","score":2,"risk":"high"},{"key":"D","text":"Nông sản ẩm bốc nóng/mốc trong kho kín, chưa xử lý","score":3,"risk":"critical"}]},
    {"text": "Lò sấy nông sản có chạy qua đêm không ai canh? Có dấu hiệu quá nhiệt?",
     "options": [{"key":"A","text":"Có tự ngắt quá nhiệt, bảo dưỡng định kỳ","score":0,"risk":"safe"},{"key":"B","text":"Có nhiệt kế nhưng chưa test tự ngắt, sấy theo kinh nghiệm","score":1,"risk":"low"},{"key":"C","text":"Sấy thủ công, canh suốt quá trình sấy","score":2,"risk":"high"},{"key":"D","text":"Lò sấy tự chế, không tự ngắt, sấy qua đêm, đã cháy sản phẩm","score":3,"risk":"critical"}]},
    {"text": "Đèn sưởi gia súc có treo sát rơm, cỏ khô? Dây điện chuồng trại có bị chuột gặm?",
     "options": [{"key":"A","text":"Đèn sưởi có bảo vệ, cách rơm >1m, CB riêng, ELCB","score":0,"risk":"safe"},{"key":"B","text":"Có CB nhưng đèn sưởi gần rơm, vẫn theo dõi","score":1,"risk":"low"},{"key":"C","text":"Đèn sưởi treo sát rơm/cỏ, dây kéo qua chuồng, không ELCB","score":2,"risk":"high"},{"key":"D","text":"Dây bị chuột gặm, đèn sưởi chạm rơm, đã cháy nhỏ 1 lần","score":3,"risk":"critical"}]},
    {"text": "Hệ thống biogas có mùi gas quanh trại, mối nối ống lỏng, van an toàn có hoạt động không?",
     "options": [{"key":"A","text":"Không biogas, hoặc cảm biến CH₄, van an toàn, kiểm tra ống","score":0,"risk":"safe"},{"key":"B","text":"Van an toàn có, kiểm tra ống bằng mắt, không cảm biến","score":1,"risk":"low"},{"key":"C","text":"Ống cũ, mối lỏng, không van an toàn, phát hiện rò bằng mùi","score":2,"risk":"high"},{"key":"D","text":"Rò rỉ nghiêm trọng, mùi gas quanh trại, gần bếp nấu ăn","score":3,"risk":"critical"}]},
]}

for name, spec in [("NH-KS-Chợ", SPEC_D), ("BV-TH", SPEC_E), ("XD-Gas", SPEC_F), ("PTGT", SPEC_G), ("XD", SPEC_I), ("VP", SPEC_J), ("PTN", SPEC_K), ("NN", SPEC_L)]:
    print(f"{name}: {len(spec['questions'])} câu")
