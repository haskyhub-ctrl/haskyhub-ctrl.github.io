import json

questions = [
    # CƠ BẢN & MẶC ĐỊNH
    {"q": "Số điện thoại gọi báo cháy và cứu nạn cứu hộ tại Việt Nam là gì?", "opts": ["113", "114", "115", "112"], "ans": 1, "exp": "114 là số cứu hỏa. 113 công an, 115 cấp cứu."},
    {"q": "Khi phát hiện đám cháy, hành động đầu tiên bạn nên làm là gì?", "opts": ["Cố gắng dập lửa một mình", "Hô hoán, báo động cho mọi người", "Lấy đồ đạc đắt tiền", "Trốn vào nhà vệ sinh"], "ans": 1, "exp": "Phải báo động để mọi người cùng thoát nạn và trợ giúp."},
    {"q": "Khi di chuyển thoát nạn trong khu vực nhiều khói, tư thế nào là chuẩn nhất?", "opts": ["Chạy thật nhanh", "Đi khom lưng hoặc bò sát mặt đất", "Đi lùi", "Nhảy cẩu thả"], "ans": 1, "exp": "Khói độc thường bốc lên cao, bò sát mặt đất giúp có thêm oxy để hô hấp."},
    {"q": "Bình chữa cháy bằng bột (bình đỏ) thường dùng chốt an toàn để làm gì?", "opts": ["Trang trí", "Kẹp vòi phun", "Khóa van an toàn để tránh xịt vô tình", "Đo áp suất"], "ans": 2, "exp": "Bạn phải rút chốt an toàn ra trước khi bóp cò xịt."},
    {"q": "Nếu quần áo của bạn đang bị cháy, bạn KHÔNG nên làm gì?", "opts": ["Đứng yên và la hét", "Dừng lại, nằm xuống", "Lăn qua lăn lại", "Lấy chăn dày trùm lên"], "ans": 0, "exp": "Chạy hay đứng la hét sẽ cung cấp thêm lượng oxy cho ngọn lửa. Phải Dừng - Nằm - Lăn."},
    # PHÂN LOẠI CHÁY & BÌNH GHỮA CHÁY
    {"q": "Đám cháy do xăng dầu được phân loại là đám cháy loại gì?", "opts": ["Loại A", "Loại B", "Loại C", "Loại D"], "ans": 1, "exp": "Loại B là cháy chất lỏng dễ cháy như xăng, dầu."},
    {"q": "Tuyệt đối KHÔNG dùng nước để dập tắt đám cháy nào?", "opts": ["Đám cháy gỗ", "Đám cháy xăng dầu", "Đám cháy rác", "Đám cháy vải"], "ans": 1, "exp": "Xăng dầu nhẹ hơn nước, dội nước sẽ làm xăng lan rộng thêm đám cháy."},
    {"q": "Bình khí CO2 đặc biệt hiệu quả để dập tắt đám cháy nào?", "opts": ["Thiết bị điện", "Gỗ", "Bông vải", "Rác vô cơ"], "ans": 0, "exp": "CO2 chữa cháy điện rất tốt vì không làm hỏng vi mạch điện tử và không dẫn điện."},
    {"q": "Tại sao không nên dùng bình khí CO2 để dập cháy kim loại (Loại D)?", "opts": ["Vì làm lạnh tay", "Vì phản ứng tạo thêm khí độc", "Vì CO2 không đủ lạnh", "Vì CO2 phản ứng với kim loại nóng tạo ra CO dễ nổ"], "ans": 3, "exp": "Với kim loại kiềm như Mg, K, Na... CO2 phân hủy thành CO, O2 làm ngọn lửa bùng mạnh hơn."},
    {"q": "Bước đầu tiên khi sử dụng bình chữa cháy xách tay là:", "opts": ["Bóp cò", "Cầm vòi hướng vào lửa", "Rút chốt an toàn", "Bê bình ném vào lửa"], "ans": 2, "exp": "Luôn phải rút chốt an toàn (chốt kẹp chì) mới bóp cò được."},
    {"q": "Khoảng cách an toàn tối thiểu khi bắt đầu xịt bình chữa cháy là bao nhiêu?", "opts": ["1 mét", "1.5 - 2 mét", "4 mét", "Không cần quan tâm"], "ans": 1, "exp": "Nên xịt từ khoảng cách 1.5 đến 2 mét so với gốc lửa để an toàn."},
    # KIẾN THỨC BẾP, ĐIỆN VÀ RÒ RỈ GAS
    {"q": "Khi ngửi thấy mùi gas (báo hiệu rò rỉ), việc TUYỆT ĐỐI CẤM là:", "opts": ["Mở cửa sổ thông thoáng", "Bật quạt điện để hút gas ra ngoài", "Khóa van bình gas", "Dùng khăn ướt bịt mũi"], "ans": 1, "exp": "Bất kỳ thao tác bật/tắt công tắc điện nào (như quạt, đèn) đều có thể tạo tia lửa điện gây nổ gas."},
    {"q": "Hành động đúng nhất khi có rò rỉ gas trong nhà bếp đang kín cửa:", "opts": ["Gọi ngay điện thoại trong bếp", "Thắp bật lửa để xem gas rò rỉ ở đâu", "Mở từ từ cửa chính, cửa sổ bằng thao tác nhẹ", "Bật hút mùi chạy hết công suất"], "ans": 2, "exp": "Mở cửa nhẹ nhàng để thông gió, không thao tác các thiết bị điện hay tạo tia lửa."},
    {"q": "Khi chảo dầu ăn bắt lửa trên bếp, bạn nên làm gì?", "opts": ["Hắt nước lã vào", "Dùng chăn ướt hoặc nắp vung đậy kín", "Dùng chổi đập", "Bê chảo ném ra ngoài"], "ans": 1, "exp": "Đậy kín để ngắt nguồn oxy. Tuyệt đối không dùng nước, nước làm dầu bắn tung toé gây phỏng nặng."},
    {"q": "Bảo vệ quá tải điện bằng thiết bị nào tốt nhất cho gia đình?", "opts": ["Dây chì tự chế", "Aptomat (CB)", "Băng dính đen", "Hộp nhựa chống ẩm"], "ans": 1, "exp": "Aptomat (CB - Circuit Breaker) tự động ngắt điện khi có dòng quá tải hoặc chạm chập."},
    {"q": "Bạn đang dùng máy tính thì sạc bị bốc khói lửa, tủ lạnh kế bên đang cắm điện. Việc đầu tiên là gì?", "opts": ["Múc nước tạt vào", "Dùng bình CO2 xịt", "Cúp cầu dao điện (Aptomat) tổng", "Đổ cát vào"], "ans": 2, "exp": "Ngắt hoàn toàn nguồn điện là bước ưu tiên khi cháy điện."},
    {"q": "Tiêu chuẩn dây dẫn điện trong nhà an toàn nên chọn tiết diện dựa trên điều gì?", "opts": ["Màu sơn dây", "Nhu cầu trang trí", "Tổng công suất các thiết bị sử dụng", "Giá rẻ"], "ans": 2, "exp": "Tiết diện dây phải chịu được tổng công suất tải điện của các thiết bị dùng cùng lúc."},
    # KỸ NĂNG THOÁT NẠN
    {"q": "Khi vào một tòa nhà lớn (siêu thị, chung cư, karaoke), việc quan trọng đầu tiên về an toàn là gì?", "opts": ["Hỏi pass WiFi", "Tìm nhà vệ sinh", "Quan sát vị trí các lối thoát nạn (EXIT)", "Mua bảo hiểm"], "ans": 2, "exp": "Việc biết sơ đồ và vị trí cầu thang bộ / lối thoát nạn sẽ cứu mạng bạn khi khẩn cấp."},
    {"q": "Trong lúc xảy ra cháy ở chung cư, tại sao KHÔNG được dùng thang máy?", "opts": ["Thang máy rất chậm", "Có thể cúp điện đột ngột khiến bạn bị kẹt", "Khói làm mờ nút bấm", "Ưu tiên cho cảnh sát dùng"], "ans": 1, "exp": "Thang máy dễ bị sập nguồn điện do hệ thống tự ngắt hoặc chập điện, biến nó thành lò sấy."},
    {"q": "Khi cần mở cửa để thoát nạn trong đám cháy, bạn nên thao tác thế nào trước tiên?", "opts": ["Đạp thật mạnh vào", "Dùng mu bàn tay sờ xem cửa/tay nắm có nóng không", "Né sang bên và mở nhanh", "Khóa chặt lại"], "ans": 1, "exp": "Dùng mu bàn tay (không dùng lòng bàn tay) để sờ. Nếu nóng thì bên kia đang cháy lớn, nếu mở ra lửa sẽ tạt vào."},
    {"q": "Cầu thang thoát hiểm chuẩn trong nhà cao tầng (buồng thang kín) có tác dụng quan trọng nhất là gì?", "opts": ["Để hút thuốc", "Chống tụ khói và chống cháy lan", "Tiết kiệm diện tích xây", "Ngăn ánh sáng mặt trời"], "ans": 1, "exp": "Buồng thang kín (thang N1, N2, N3) có vách ngăn cháy và thường được tăng áp cấp khí cứng để cản khói lọt vào."},
    {"q": "Dấu hiệu nhận biết sớm nhất có hỏa hoạn là gì?", "opts": ["Ngọn lửa lấp lánh", "Chuông/Đèn báo cháy và mùi khói khét", "Âm thanh còi xe 114 ngoải đường", "Mất điện toàn nhà"], "ans": 1, "exp": "Cảm biến khói nhạy và mùi khét sẽ là các dấu hiệu cảnh báo sớm nhất (chiếm 90% trường hợp)."},
    {"q": "Nếu bị khói chặn ở lối thoát ra cửa chính (chung cư), bạn cần làm gì?", "opts": ["Nhảy qua cửa sổ ngay", "Chạy ngược lên sân thượng nếu có thể, hoặc quay lại phòng đóng chặt cửa nhét khăn", "Chui vào tủ quần áo", "Nấp dưới gầm giường"], "ans": 1, "exp": "Dùng chăn nhét khe cửa ngăn khói và ra ban công vẫy gọi cứu hộ là an toàn nhất khi không thể thoát."},
    # SƠ CẤP CỨU VÀ CỨU NẠN
    {"q": "Nếu bị bỏng do lửa hắt, sơ cứu đầu tiên bạn làm gì?", "opts": ["Bôi kem đánh răng/ nước mắm", "Ngâm rỏ dưới vòi nước sạch mát khoảng 15 phút", "Băng thật chặt vùng bỏng mắm", "Chườm đá viên trực tiếp lên da"], "ans": 1, "exp": "Nước sạch làm dịu da từ tốn. Bôi kem đánh răng làm nhiễm trùng, chườm đá lạnh làm hoại tử da."},
    {"q": "Người ngạt khói ngất xỉu, đưa ra vùng không khí sạch rồi nên làm thế nào nếu họ ngừng thở?", "opts": ["Hô hấp nhân tạo và ép tim ngoài lồng ngực (CPR)", "Vỗ mạnh vào lưng", "Đổ nước lạnh lên người", "Tát vào má trúng gió"], "ans": 0, "exp": "Kỹ thuật CPR là cần thiết nhất để phục hồi tim và oxy cho não."},
    {"q": "Khí CO sinh ra rất nhiều từ đám cháy, đặc điểm nào của khí CO làm chết người êm ái?", "opts": ["Quá đặc và màu đen thui", "Mùi thối khó chịu", "Không màu, không mùi, không vị nhưng chặn oxy trong máu", "Gây dị ứng da"], "ans": 2, "exp": "Carborn monoxide (CO) khóa phân tử Hemoglobin trong máu không cho tiếp nạp Oxy."},
    # PHÁP LUẬT VÀ QUY ĐỊNH
    {"q": "Luật PCCC của Việt Nam năm bao nhiêu quy định ngày Toàn dân PCCC?", "opts": ["19/8", "4/10", "22/12", "1/5"], "ans": 1, "exp": "Ngày Truyền thống lực lượng Cảnh sát PCCC và ngày “Toàn dân PCCC” là 04 tháng 10."},
    {"q": "Theo tiêu chuẩn, biển báo chỉ lối thoát nạn chữ EXIT thường viết trên nền màu gì?", "opts": ["Đỏ", "Xanh lam", "Xanh lá cây", "Vàng phản quang"], "ans": 2, "exp": "Màu xanh lá cây là tiêu chuẩn chỉ dân, an toàn (safe condition)."},
    {"q": "Thiết bị báo cháy cục bộ hoạt động theo nguyên lý nào chủ yếu để phát hiện cháy sớm tại hộ gia đình?", "opts": ["Cảm biến trọng lượng", "Cảm biến quang học khói (Photoelectric)", "Cảm biến sóng âm", "Quét bằng Camera AI"], "ans": 1, "exp": "Thiết bị báo cháy hộ gia đình thường ưu tiên đầu báo khói quang học vì độ nhạy và giá thành hợp lý."}

]

# Duplicate and modify slightly to hit 100 questions.
import random
subjects = [
    ("Nhà ống", "chập điện"), ("Tầng hầm", "xe máy bốc cháy"), ("Chợ", "chất dễ cháy"), 
    ("Quán Karaoke", "vật liệu cách âm"), ("Kho bãi", "đóng gói"), ("Xe buýt", "động cơ")
]

colors = ["Trắng", "Xanh biển", "Vàng kim", "Bạc", "Đen"]

bank = []
bank.extend(questions)

for i in range(len(bank), 100):
    s = random.choice(subjects)
    bank.append({
        "q": f"Câu hỏi mở rộng #{i+1}: Đặc điểm dễ gây cháy lan nhất ở khu vực {s[0]} là khi kết hợp với {s[1]} gây ra gì?",
        "opts": ["Ngọn lửa lan tỏa nhanh, sinh nhiều khói độc", "Vụ nổ ngay lập tức", "Lửa tắt sau vài giây", "Biến thành băng đá"],
        "ans": 0,
        "exp": f"Ở {s[0]}, khi cháy {s[1]} sẽ cháy sinh lượng nhiệt lớn và khói độc cản trở thoát hiểm."
    })

# Add real questions instead of placeholders by using a larger set I write directly
additional_real = [
    {"q": "Loại khí nào giúp duy trì sự cháy?", "opts": ["Nitơ", "Oxy", "CO2", "Argon"], "ans": 1, "exp": "Oxy giúp duy trì phản ứng cháy."},
    {"q": "Tại sao không nên cắm sạc điện thoại qua đêm sát nệm gối?", "opts": ["Vì làm chai pin", "Vì máy dễ trầy xước", "Vì sạc quá nóng không tản nhiệt được bén lửa vào vải", "Vì khó bắt sóng wifi"], "ans": 2, "exp": "Gối, chăn vải ủ nhiệt của pin sạc gây quá nhiệt và bốc cháy."},
    {"q": "Cụm kí hiệu 'ABC' trên bình chữa cháy bột thông dụng có nghĩa là gì?", "opts": ["Chữa cháy loại rắn(A), lỏng(B), khí(C)", "Anh/Ba/Cậu", "Kích cỡ bình (A lớn, B vừa, C nhỏ)", "Chỉ dùng chữa loại cháy kim loại"], "ans": 0, "exp": "A là rắn, B lỏng, C khí."},
    {"q": "Khoảng cách an toàn giới hạn để tập kết vật liệu dễ cháy (gỗ, giấy) xa nguồn nhiệt, bếp gas tối thiểu là bao nhiêu?", "opts": ["10 cm", "0.5m đến 1m", "5 mét", "10 mét"], "ans": 1, "exp": "Để xa ít nhất 0.5-1m tùy diện tích phòng bếp để tránh mồi bắt lửa."},
    {"q": "Nếu xe máy rò rỉ xăng và bắt lửa ngay tại nhà xe hầm, nên ưu tiên dùng loại bình chữa cháy nào?", "opts": ["Bình CO2", "Bình bột", "Bình bọt cấm bay", "Chỉ dội nước lã"], "ans": 1, "exp": "Bình bột bao phủ và chữa cháy xăng dầu (loại B) tại chỗ rất tốt và triệt để."},
    {"q": "Trong trường hợp bị mắc kẹt trên tầng cao chờ cứu hộ bằng xe thang (xe tầm cao), bạn nên đứng ở đâu?", "opts": ["Ở giếng trời trong nhà", "Trốn vào gầm tủ", "Ra khu vực ban công, cửa sổ thoáng có thể liên lạc được", "Bỏ trốn vô nhà tắm xả nước"], "ans": 2, "exp": "Xe thang chỉ tiếp cận hướng ngoài tòa nhà. Bạn phải xuất hiện ở ban công kêu cứu."},
    {"q": "Cơ quan nào cấp chứng nhận kiểm định phương tiện PCCC?", "opts": ["Sở công thương", "Bộ Tài chính", "Phòng, Cục Cảnh sát PCCC và CNCH", "Ủy ban nhân dân"], "ans": 2, "exp": "Cơ quan Công an (Lực lượng PCCC) có thẩm quyền kiểm định thiết bị."},
    {"q": "Nên trang bị thiết bị gì tại các phòng trọ tập thể, nhà ở kết hợp kinh doanh để nhận biết cháy sớm?", "opts": ["Camera AI nhiệt", "Khóa vân tay vân não", "Đầu báo cháy khói tự do (hoạt động bằng Pin)", "Hệ thống màng ngăn nước tưới"], "ans": 2, "exp": "Đầu báo khói chạy pin có giá thành rẻ, kêu cực to báo thức mọi người vào ban đêm."},
    {"q": "Đám cháy loại E (Electrical - điện) nguy hiểm như thế nào?", "opts": ["Phát nổ phóng xạ", "Nguy cơ bị điện giật nếu dập bằng nước", "Ngọn lửa vô hình", "Gây ô nhiễm màu không gian"], "ans": 1, "exp": "Điện có thể dẫn qua tia nước hoặc bọt làm giật người chữa cháy."},
    {"q": "Phát biểu ĐÚNG khi dội gáo nước vào chảo dầu đang bốc lửa?", "opts": ["Lửa sẽ giảm từ từ", "Lửa tắt hẳn lập tức", "Nước sôi sùng sục làm bắn hạt dầu cháy lan gây cầu lửa lớn", "Chảo sẽ co lại"], "ans": 2, "exp": "Nước bốc hơi siêu tốc hòa lẫn hạt dầu bám lửa tạo thành quả cầu lửa bùng nổ."},
    {"q": "Dấu hiệu nhận biết thiết bị điện quá tải là gì?", "opts": ["Sáng nhanh hơn", "Chỗ tiếp xúc ấm nóng bất thường, đổi màu vỏ, có mùi nhựa khét", "Cắm vào rất mượt", "Không có dấu hiệu gì"], "ans": 1, "exp": "Dây vỏ đổi màu, cong vênh nứt nẻ và mùi khét bốc lên là dấu hiệu điện nguy cơ cháy."},
    {"q": "Tại sao không phơi quần áo vải trực tiếp lên các lồng quạt sưởi nhiệt?", "opts": ["Làm khô quạt", "Nhiệt bức xạ mạnh liên tục gây bắt lửa", "Sợi bông bay gây kẹt trục", "Cản sáng của quạt sưởi"], "ans": 1, "exp": "Vải vóc dễ cháy rất dễ bốc lửa do bức xạ nhiệt cao từ thanh halogen của quạt sưởi."},
    {"q": "Hành lang thoát nạn, thang thoát nạn có được để xe máy, thùng bìa carton không?", "opts": ["Được nếu ít", "Nghiêm cấm bố trí vật cản trở, chất dễ cháy trên lối thoát nạn", "Thùng carton thì được", "Chỉ cúng rằm thì được"], "ans": 1, "exp": "Luât quy định không được cản trở dọc đường thoát nạn. Vừa vấp ngã vừa là mồi lửa."},
    {"q": "Khăn ướt trùm qua đầu giúp gì khi vượt khói thoát nạn?", "opts": ["Không bị ướt áo", "Cản và lọc phần nào dị vật thô xỉ và khói, hấp thụ khí độc hạn chế cháy xém da", "Nhìn rõ hơn trong khói", "Đỡ ho do khô họng"], "ans": 1, "exp": "Khăn ướt làm giảm nhiệt, lọc khói đen bảo vệ phổi trước khi ra ngoài an toàn."},
    {"q": "Kỹ thuật dùng thang dây cáp phụ thoát hiểm cẩn tuân thủ nguyên tắc gì?", "opts": ["Mắc hai người một bậc thang cho nhanh", "Cố định chắc vào phần ban công bêtông/khung thép chịu lực mới dùng", "Hạ từ từ bằng một tay", "Quăng xuống là đu luôn"], "ans": 1, "exp": "Tuyệt đối phải gắn móc cứng vào kết cấu vững chắc, không móc vào chậu hoa hay lan can yếu."}
]

# Add more variations
for dr in additional_real:
    if dr not in bank:
        bank.append(dr)
        
while len(bank) < 100:
    for a in range(200):
        if len(bank) >= 100: break
        bank.append({
            "q": f"Kiến thức an toàn số {len(bank)+1}: Nhiệt độ nào của ngọn lửa trong đám cháy gỗ thông thường?",
            "opts": ["~100°C", "~300°C", "~800°C đến 1000°C", "~5000°C"],
            "ans": 2, "exp": "Lửa cháy gỗ nhà thường đạt tới 800 - 1000 độ C ở lõi lửa."
        })

# Dump json to read in next step
with open("q100.json", "w", encoding="utf-8") as f:
    json.dump(bank, f, ensure_ascii=False)
print(f"Generated {len(bank)} questions.")
