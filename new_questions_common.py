# === NHÓM 1: DẤU HIỆU NGUY CƠ TỪ HỆ THỐNG ĐIỆN (12 câu) ===
GROUP1 = [
    {"text": "Bạn có ngửi thấy mùi khét (nhựa cháy, cao su) phát ra từ ổ cắm, công tắc, tủ điện hoặc bảng điện không?",
     "options": [
        {"key": "A", "text": "Không có mùi khét bất thường", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thỉnh thoảng thoáng có mùi khét nhẹ nhưng nhanh hết", "score": 1, "risk": "low"},
        {"key": "C", "text": "Có mùi khét rõ ràng từ ổ cắm hoặc tủ điện, xuất hiện thường xuyên", "score": 2, "risk": "high"},
        {"key": "D", "text": "Mùi khét nồng kèm khói mỏng từ thiết bị điện", "score": 3, "risk": "critical"},
    ]},
    {"text": "Ổ cắm, phích cắm hoặc công tắc điện có bị nóng bất thường khi chạm tay vào không?",
     "options": [
        {"key": "A", "text": "Không nóng, nhiệt độ bình thường", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Ấm nhẹ khi dùng thiết bị công suất lớn, hết ấm khi rút phích", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nóng rõ rệt dù chỉ cắm thiết bị nhỏ, phích cắm bị biến dạng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Nóng bỏng tay, nhựa ổ cắm bị chảy méo, có vết cháy đen", "score": 3, "risk": "critical"},
    ]},
    {"text": "Quanh ổ cắm, công tắc hoặc bảng điện có xuất hiện vết cháy xém, ố vàng hoặc muội đen không?",
     "options": [
        {"key": "A", "text": "Không có vết ố hay cháy xém", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có vết ố vàng nhẹ quanh 1-2 ổ cắm cũ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhiều ổ cắm/công tắc có vết cháy đen, nhựa sậm màu", "score": 2, "risk": "high"},
        {"key": "D", "text": "Vết cháy lan rộng trên tường quanh bảng điện, có dấu tia lửa", "score": 3, "risk": "critical"},
    ]},
    {"text": "Đèn chiếu sáng có bị chập chờn, nhấp nháy hoặc tối đi bất thường không?",
     "options": [
        {"key": "A", "text": "Đèn sáng ổn định, không nhấp nháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thỉnh thoảng 1-2 bóng nhấp nháy khi bật nhiều thiết bị cùng lúc", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhiều đèn nhấp nháy thường xuyên, tối đi rõ rệt khi bật thêm thiết bị", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đèn chập chờn liên tục kèm tiếng kêu từ bảng điện, đã từng tắt đột ngột", "score": 3, "risk": "critical"},
    ]},
    {"text": "Có tiếng kêu lạ (vo ve, lạch cạch, xì xì) phát ra từ ổ cắm, hộp điện hoặc tủ điện không?",
     "options": [
        {"key": "A", "text": "Không có tiếng kêu bất thường", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có tiếng vo nhẹ từ ballast đèn huỳnh quang cũ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Tiếng lạch cạch hoặc xì xì từ ổ cắm/hộp nối khi dùng thiết bị", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tiếng nổ lách tách kèm tia lửa nhỏ nhìn thấy được", "score": 3, "risk": "critical"},
    ]},
    {"text": "Aptomat (CB) hoặc cầu chì có tự nhảy (ngắt) thường xuyên không?",
     "options": [
        {"key": "A", "text": "Chưa bao giờ tự nhảy, hoặc rất hiếm khi", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Nhảy 1-2 lần/tháng khi bật nhiều thiết bị cùng lúc", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhảy thường xuyên hàng tuần, phải đóng lại liên tục", "score": 2, "risk": "high"},
        {"key": "D", "text": "CB nhảy liên tục nên đã phải nối tắt (bypass) hoặc dùng dây đồng thay cầu chì", "score": 3, "risk": "critical"},
    ]},
    {"text": "Dây điện có bị bong tróc, nứt vỏ cách điện, lộ lõi đồng hoặc có mối nối quấn băng keo không?",
     "options": [
        {"key": "A", "text": "Dây điện vỏ nguyên vẹn, luồn ống hoặc máng cáp gọn gàng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có 1-2 chỗ vỏ hơi cũ nhưng chưa lộ lõi", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhiều chỗ bong tróc, lộ lõi đồng, mối nối quấn băng keo điện", "score": 2, "risk": "high"},
        {"key": "D", "text": "Dây cũ nát, lõi lộ nhiều chỗ, rỉ sét mối nối, đã có dấu hiệu chạm chập", "score": 3, "risk": "critical"},
    ]},
    {"text": "Ổ cắm kéo dài (dây nối dài) có bị nóng, chân cắm lỏng hoặc nối chồng nhiều cái không?",
     "options": [
        {"key": "A", "text": "Không dùng ổ kéo dài, hoặc dùng ít, không nóng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có dùng nhưng không nối chồng, dây không nóng", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nối chồng 2-3 ổ, cắm nhiều thiết bị, dây ấm khi dùng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Ổ cắm cũ hỏng, chân lỏng, dây nóng ran khi dùng, vẫn dùng hàng ngày", "score": 3, "risk": "critical"},
    ]},
    {"text": "Hóa đơn tiền điện có tăng đột biến (trên 20-30%) mà không sử dụng thêm thiết bị mới không?",
     "options": [
        {"key": "A", "text": "Tiền điện ổn định, tăng giảm theo mùa bình thường", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có tăng nhẹ nhưng giải thích được (thêm ĐHKK, mùa nóng)", "score": 1, "risk": "low"},
        {"key": "C", "text": "Tăng bất thường >20% mà không rõ lý do", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tăng đột biến >50% kèm theo dây điện nóng hoặc CB nhảy", "score": 3, "risk": "critical"},
    ]},
    {"text": "Dây điện có bị chuột, côn trùng gặm nhấm làm hở lớp vỏ bảo vệ không?",
     "options": [
        {"key": "A", "text": "Không có dấu hiệu chuột/côn trùng gặm dây điện", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có thấy chuột trong nhà nhưng chưa phát hiện gặm dây", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đã thấy dây điện bị gặm hở vỏ 1-2 chỗ", "score": 2, "risk": "high"},
        {"key": "D", "text": "Chuột gặm nhiều dây, đã từng chập điện do chuột", "score": 3, "risk": "critical"},
    ]},
    {"text": "Vật liệu dễ cháy (giấy, vải, hàng hóa) có đang chất gần hoặc sát ổ cắm, tủ điện không?",
     "options": [
        {"key": "A", "text": "Tủ điện và ổ cắm đều thông thoáng, cách vật dễ cháy >1m", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Đôi chỗ có đồ gần ổ cắm nhưng không che khuất tủ điện", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hàng hóa xếp sát tủ điện và ổ cắm, che khuất một phần", "score": 2, "risk": "high"},
        {"key": "D", "text": "Tủ điện bị chôn vùi trong hàng hóa dễ cháy, không thể tiếp cận", "score": 3, "risk": "critical"},
    ]},
    {"text": "Thiết bị điện nung nóng (bếp, bàn ủi, lò sưởi, ấm nước) có đang đặt gần vật dễ cháy hoặc chạy không giám sát không?",
     "options": [
        {"key": "A", "text": "Luôn cách xa vật dễ cháy, rút phích khi không dùng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Đôi khi quên rút phích nhưng thiết bị có tự ngắt", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đặt gần rèm/vải, dùng chung ổ cắm với thiết bị khác", "score": 2, "risk": "high"},
        {"key": "D", "text": "Thiết bị cũ không tự ngắt, chạy liên tục không ai trông", "score": 3, "risk": "critical"},
    ]},
]

# === NHÓM 2: NGUY CƠ TỪ NGUỒN LỬA/NHIỆT (8 câu) ===
GROUP2 = [
    {"text": "Có đốt rác, lá khô, phế thải lộ thiên trong khuôn viên không?",
     "options": [
        {"key": "A", "text": "Không đốt rác lộ thiên", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có đốt trong thùng kim loại có nắp, có người trông", "score": 1, "risk": "low"},
        {"key": "C", "text": "Đốt lộ thiên gần hàng rào, cây khô, không trông liên tục", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đốt gần kho hàng hoặc nhà xưởng, kể cả khi gió lớn", "score": 3, "risk": "critical"},
    ]},
    {"text": "Bàn thờ, nến, đèn dầu, vàng mã có đặt gần vật dễ cháy (rèm, gỗ, giấy) không?",
     "options": [
        {"key": "A", "text": "Không dùng lửa thờ cúng, hoặc dùng nến LED thay thế", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Bàn thờ cách trần và vật dễ cháy >0.5m, có người trông", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bàn thờ gỗ sát trần, tàn hương/nến rơi xuống đồ giấy/vải", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đốt vàng mã lộ thiên, nến cháy qua đêm không ai trông", "score": 3, "risk": "critical"},
    ]},
    {"text": "Có người hút thuốc trong nhà, trong kho hàng hoặc gần vật liệu dễ cháy không?",
     "options": [
        {"key": "A", "text": "Không ai hút thuốc trong khuôn viên", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Hút ngoài trời, xa vật dễ cháy, có gạt tàn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hút trong nhà, vứt tàn vào thùng rác thường", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hút trong kho hàng hoặc gần nhiên liệu/hóa chất", "score": 3, "risk": "critical"},
    ]},
    {"text": "Bếp gas, bình gas có dấu hiệu bất thường (mùi gas, dây dẫn cũ nứt, van khó khóa) không?",
     "options": [
        {"key": "A", "text": "Bếp gas hoạt động tốt, dây mới, không mùi gas", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Dây dẫn hơi cũ nhưng chưa nứt, không mùi gas", "score": 1, "risk": "low"},
        {"key": "C", "text": "Thoáng có mùi gas khi mở bếp, dây cũ trên 3 năm, van hơi cứng", "score": 2, "risk": "high"},
        {"key": "D", "text": "Mùi gas rõ, dây nứt vá băng keo, bình gas đặt trong phòng kín", "score": 3, "risk": "critical"},
    ]},
    {"text": "Xăng dầu, cồn, dung môi dễ cháy có đang được để trong nhà/phòng ngủ/gần bếp không?",
     "options": [
        {"key": "A", "text": "Không lưu trữ chất dễ cháy, hoặc để tủ chuyên dụng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Lượng nhỏ trong can kim loại có nắp, xa nguồn nhiệt", "score": 1, "risk": "low"},
        {"key": "C", "text": "Để trong kho chung gần thiết bị điện", "score": 2, "risk": "high"},
        {"key": "D", "text": "Để trong chai nhựa hở, trong phòng ngủ hoặc gần bếp", "score": 3, "risk": "critical"},
    ]},
    {"text": "Có hoạt động hàn cắt kim loại gần vật liệu dễ cháy không?",
     "options": [
        {"key": "A", "text": "Không có hàn cắt, hoặc hàn tại khu riêng cách xa vật dễ cháy", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Hàn tại khu riêng, có bình chữa cháy gần đó", "score": 1, "risk": "low"},
        {"key": "C", "text": "Hàn cắt ngay khu sản xuất, chưa dọn vật dễ cháy xung quanh", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hàn cắt cạnh vật dễ cháy, tia lửa bắn tự do, không giám sát", "score": 3, "risk": "critical"},
    ]},
    {"text": "Có than hoa, lửa trại, nướng lộ thiên gần nhà hoặc kho hàng không?",
     "options": [
        {"key": "A", "text": "Không dùng lửa ngoài trời", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Nướng ngoài sân rộng, cách xa nhà, có nước dập sẵn", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nướng trên ban công hoặc gần mái hiên dễ cháy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đốt lửa gần kho hàng, bãi xe, cỏ khô", "score": 3, "risk": "critical"},
    ]},
    {"text": "Điều hòa, tủ lạnh, tủ đông có tiếng kêu bất thường, rung mạnh hoặc mùi khét không?",
     "options": [
        {"key": "A", "text": "Hoạt động êm ái, không mùi, không rung lắc lạ", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Thỉnh thoảng kêu nhẹ khi khởi động, nhanh hết", "score": 1, "risk": "low"},
        {"key": "C", "text": "Rung lắc mạnh, kêu liên tục, dây điện nóng khi chạy", "score": 2, "risk": "high"},
        {"key": "D", "text": "Bốc mùi khét, motor cháy, vẫn cắm điện chạy", "score": 3, "risk": "critical"},
    ]},
]

# === NHÓM 3: LỐI THOÁT NẠN & TRANG BỊ PCCC (6 câu) ===
GROUP3 = [
    {"text": "Lối thoát nạn (cửa thoát hiểm, cầu thang bộ) có đang bị chặn bởi hàng hóa, xe máy hoặc khóa cứng không?",
     "options": [
        {"key": "A", "text": "Tất cả lối thoát thông thoáng, cửa mở dễ dàng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Lối thoát chính thông, có đồ đạc nhẹ bên cạnh nhưng không cản trở", "score": 1, "risk": "low"},
        {"key": "C", "text": "Lối thoát bị thu hẹp bởi hàng hóa/xe máy, phải len qua", "score": 2, "risk": "high"},
        {"key": "D", "text": "Lối thoát duy nhất bị chặn hoàn toàn hoặc cửa bị khóa cứng", "score": 3, "risk": "critical"},
    ]},
    {"text": "Bạn có nhìn thấy bình chữa cháy gần nhất không? Nó có dễ lấy không?",
     "options": [
        {"key": "A", "text": "Nhìn thấy ngay, dễ lấy, kim đồng hồ ở vùng xanh", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có bình nhưng hơi xa hoặc để dưới thấp khó thấy", "score": 1, "risk": "low"},
        {"key": "C", "text": "Bình bị hàng hóa che khuất, phải dọn mới lấy được", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không thấy bình nào, hoặc bình hết hạn/hỏng van", "score": 3, "risk": "critical"},
    ]},
    {"text": "Đèn EXIT (chỉ lối thoát) và đèn chiếu sáng khẩn cấp có sáng không?",
     "options": [
        {"key": "A", "text": "Đèn EXIT sáng rõ, đèn khẩn cấp hoạt động khi test", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Đèn EXIT sáng nhưng chưa test đèn khẩn cấp gần đây", "score": 1, "risk": "low"},
        {"key": "C", "text": "Một số đèn EXIT đã tắt/hỏng, chưa thay", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không có đèn EXIT hoặc tất cả đã hỏng", "score": 3, "risk": "critical"},
    ]},
    {"text": "Đầu phun sprinkler (nếu có) có bị hàng hóa che khuất hoặc sơn phủ lên không?",
     "options": [
        {"key": "A", "text": "Không có sprinkler, hoặc có và đầu phun đều thông thoáng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Hầu hết thông thoáng, 1-2 chỗ hàng xếp gần sát", "score": 1, "risk": "low"},
        {"key": "C", "text": "Nhiều đầu phun bị kệ hàng che khuất hoặc bị sơn phủ", "score": 2, "risk": "high"},
        {"key": "D", "text": "Đầu phun bị chôn vùi trong hàng hóa, không thể phun được", "score": 3, "risk": "critical"},
    ]},
    {"text": "Bạn có biết đường thoát nạn gần nhất từ vị trí hiện tại không? Có sơ đồ dán trên tường không?",
     "options": [
        {"key": "A", "text": "Biết rõ, có sơ đồ thoát nạn rõ ràng dán mỗi tầng", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Biết đường đi nhưng sơ đồ cũ/mờ chữ", "score": 1, "risk": "low"},
        {"key": "C", "text": "Không chắc đường nào, không thấy sơ đồ", "score": 2, "risk": "high"},
        {"key": "D", "text": "Không biết, không có sơ đồ, chưa ai chỉ lối thoát", "score": 3, "risk": "critical"},
    ]},
    {"text": "Hàng hóa, vật tư trong kho có đang xếp chật tràn lan, che khuất tủ điện không?",
     "options": [
        {"key": "A", "text": "Xếp gọn gàng, lối đi thông, tủ điện dễ tiếp cận", "score": 0, "risk": "safe"},
        {"key": "B", "text": "Có lối đi nhưng hơi hẹp, tủ điện vẫn tiếp cận được", "score": 1, "risk": "low"},
        {"key": "C", "text": "Lối đi bị thu hẹp, hàng dễ cháy để lẫn lộn, tủ điện bị chắn", "score": 2, "risk": "high"},
        {"key": "D", "text": "Hàng chất tràn lan, không lối đi, tủ điện bị chôn vùi", "score": 3, "risk": "critical"},
    ]},
]

print(f"Nhóm 1: {len(GROUP1)} câu")
print(f"Nhóm 2: {len(GROUP2)} câu")
print(f"Nhóm 3: {len(GROUP3)} câu")
print(f"Tổng: {len(GROUP1)+len(GROUP2)+len(GROUP3)} câu")
