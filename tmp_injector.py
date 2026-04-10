import re
import json

raw_text = """
Câu hỏi 1: Anh/chị hãy cho biết có mấy cách nhận biết đám cháy qua các dấu hiệu ban đầu?
a)  Khói, mùi.
b)  Ánh lửa, khói.
c)  Khói, ánh lửa - tiếng nổ - mùi sản phẩm cháy.
Đáp án: c
Câu hỏi 2: Khi phát hiện cháy, anh/chị cần thực hiện các động tác theo trình tự nào dưới đây:
a) Hô to: Cháy! Cháy! Cháy!, cúp cầu dao điện, tham gia chữa cháy, đồng thời gọi điện thoại báo lực lượng chữa cháy chuyên nghiệp.
b) Gọi điện thoại báo lực lượng chữa cháy chuyên nghiệp, cúp cầu dao điện, hô to: Cháy! Cháy! Cháy!, tham gia chữa cháy.
c) Hô to: Cháy! Cháy! Cháy!, cúp cầu dao điện, đồng thời gọi điện thoại báo lực lượng chữa cháy chuyên nghiệp.
Đáp án: a
Câu hỏi 3: Người phát hiện cháy phải bằng mọi cách báo ngay cho 01 hoặc tất cả các đơn vị:
a) Đội dân phòng hoặc Đội PCCC cơ sở nơi xảy ra hỏa hoạn.
b) Đơn vị Cảnh sát PCCC gần nhất.
c) Chính quyền địa phương sở tại hoặc cơ quan Công an nơi gần nhất.
d) Tất cả a, b, c đều đúng.
Đáp án: d
Câu hỏi 4: Khi đang ở trong siêu thị, nếu phát hiện siêu thị đang bị cháy, anh/chị sẽ làm gì?
a) Hô hoán cho mọi người chạy
b) Tới nơi có cháy để chữa cháy
c) Gọi điện cho lực lượng Cảnh sát PCCC
d) Bình tĩnh, báo động có cháy, ngắt cầu giao điện, dùng phương tiện chữa cháy tại chỗ chữa cháy và gọi điện báo cho lực lượng Cảnh sát PCCC.
Đáp án: d
Câu hỏi 5: Khi đang ở trên tầng 18 của chung cư, mà ở tầng 17 bị cháy không thể xuống phía dưới được, anh/chị sẽ làm gì?
a) Nhảy xuống
b) Cố chạy xuống
c) Chạy lên trên tầng cao nhất, dùng khăn ướt bịt mũi và gọi điện để lực lượng Cảnh sát PCCC ứng cứu.
d) Ở trong phòng căn hộ đóng kín cửa lại
Đáp án: c
Câu hỏi 6: Khi bị cháy ở nhà cao tầng, anh/chị sẽ thoát nạn như thế nào?
a) Chạy lên
b) Đi bằng thang máy
c) Chạy xuống bằng cầu thang bộ theo biển chỉ dẫn thoát nạn trong tòa nhà.
d) Ở trong phòng đóng kín cửa lại
Đáp án: c
Câu hỏi 7: Trong các ký túc xá, nhà trọ, người ta thường dùng bếp dầu để đun nấu. Khi xảy cháy, bếp dầu do chế dầu lúc đun nấu, phạm vi cháy mới chỉ xung quanh bếp dầu, tại chỗ không có bình chữa cháy, chỉ có: nước, cát, chăn (mền). Anh/chị xử lý thế nào?
a) Xối nước.
b) Tạt cát.
c) Lấy chăn (mền) nhúng nước trùm lên.
Đáp án: c
Câu hỏi 8: Anh, chị hãy cho biết khi cháy xảy ra xử lý như thế nào?
a) Cắt điện, dùng phương tiện chữa cháy dập tắt đám cháy
b) Báo động, cắt điện, dùng phương tiện chữa cháy dập tắt đám cháy, gọi điện thoại cho lực lượng chữa cháy số  điện thoại 114
c) Dùng phương tiện chữa cháy dập tắt đám cháy
Đáp án: b
Câu hỏi 9: Trong đêm, anh A đang ngủ thì phát hiện có mùi gas bên trong nhà mình. Theo anh/chị, anh A cần tiến hành xử lý trình tự như thế nào là đúng nhất?
a) Mở đèn chiếu sáng, khóa bình gas, mở cửa thông thoáng gió.
b) Mở cửa thông thoáng gió, mở đèn chiếu sáng, khóa bình gas.
c) Mở cửa thông thoáng gió, khóa bình gas, không bật các thiết bị tiêu thụ điện.
Đáp án: c
Câu hỏi 10: Cách tránh ngộ độc khí trong đám cháy?
a) Phải ngay lập tức mở tất cả các cửa ở hướng không có cháy để giảm áp suất.
b) Không được mở cửa ở hướng có cháy và khói xông vào phòng.
c) Các phương pháp phòng khói khẩn cấp như khăn ướt luôn có tác dụng tốt vì vậy bạn nên luôn để 1 chai nước trong phòng.
d) Cả a,b,c,d đều đúng.
Đáp án: d
Câu hỏi 11: Điều kiện an toàn về PCCC đối với hộ gia đình là:
a) Nơi đun nấu, nơi thờ cúng, nơi có sử dụng nguồn gây cháy phải đảm bảo an toàn về PCCC.
b) Tài sản, vật tư, chất cháy phải bố trí, sắp xếp, bảo quản, sử dụng đúng quy định an toàn PCCC.
c) Có dự kiến tình huống cháy thoát nạn và biện pháp chữa cháy có phương tiện chữa cháy ban đầu phù hợp.
d) Tất cả a, b, c đều đúng.
Đáp án: d
Câu hỏi 12: Phương án chữa cháy của cơ sở được tổ chức thực tập như thế nào?
a) Ít nhất mỗi tháng/lần
b) Ít nhất mỗi quý/lần
c) Ít nhất 6 tháng/lần
d) Ít nhất mỗi năm/lần
Đáp án: d
Câu hỏi 13: Cảnh sát phòng cháy và chữa cháy có trách nhiệm kiểm tra an toàn PCCC đối với cơ sở có nguy hiểm về cháy, nổ mấy lần trong 01 năm?
a) 01 lần/năm
b) 02 lần/năm
c) 03 lần/năm
d) 04 lần/năm
Đáp án: d
Câu hỏi 14: Điều 5 Luật PCCC quy định trách nhiệm PCCC như thế nào?
a) Trách nhiệm của Cơ quan, tổ chức
b) Trách nhiệm của cá nhân và hộ gia đình
c) Cả a và b
Đáp án: c
Câu hỏi 15: Anh/chị hãy cho biết khi xảy ra cháy, điện thoại cho lực lượng Cảnh sát PCCC theo số điện thoại nào?
a) 113
b) 114
c) 115
Đáp án: b
Câu hỏi 16: Anh/chị hãy cho biết hành vi tổ chức thi công, xây dựng công trình thuộc diện phải thẩm duyệt về phòng cháy và chữa cháy khi chưa có giấy chứng nhận thẩm duyệt về phòng cháy và chữa cháy sẽ xử phạt hành chính như thế nào?
a) Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng
b) Phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng
c) Phạt tiền từ 15.000.000 đồng đến 25.000.000 đồng
Đáp án: c
Câu hỏi 17: Anh/chị hãy cho biết hành vi không trang bị phương tiện chữa cháy thông dụng cho nhà, công trình theo quy định sẽ xử phạt hành chính như thế nào?
a) Phạt tiền từ 3.000.000 đồng đến 5.00.000 đồng
b) Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng
c) Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng
Đáp án: b
Câu hỏi 18: Hành vi làm mất tác dụng hoặc để nội quy, tiêu lệnh, biển báo, biển cấm, biển chỉ dẫn về PCCC cũ, mờ, không nhìn rõ chữ, ký hiệu chỉ dẫn sẽ xử phạt như thế nào?
a) Phạt cảnh cáo
b) Phạt tiền từ 100.000 đồng đến 300.000 đồng
c) Phạt cảnh cáo hoặc phạt tiền từ 100.000 đồng đến 300.000 đồng
Đáp án: c
Câu hỏi 19: Anh, chị hãy cho biết hành vi không xuất trình hồ sơ, tài liệu phục vụ cho kiểm tra an toàn phòng cháy và chữa cháy sẽ xử phạt như thế nào?
a) Phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng
b) Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng
c) Phạt cảnh cáo
Đáp án: a
Câu hỏi 20: Anh, chị hãy cho biết hành vi không lập hồ sơ quản lý, theo dõi phòng cháy và chữa cháy sẽ xử phạt hành chính như thế nào?
a) Phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng
b) Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng
c) Phạt tiền từ 2.000.000 đồng đến 5.000.000 đồng
Đáp án: c
Câu hỏi 21: Anh, chị hãy cho biết hành vi vận chuyển chất, hàng nguy hiểm về cháy, nổ mà không có giấy phép vận chuyển chất, hàng nguy hiểm về cháy, nổ sẽ xử phạt hành chính như thế nào?
a) Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng
b) Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng
c) Phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng
Đáp án: b
Câu hỏi 22: Anh, chị hãy cho biết hành vi sử dụng nguồn lửa, các thiết bị điện tử hoặc các thiết bị, dụng cụ sinh lửa, sinh nhiệt khác ở những nơi có quy định cấm sẽ xử phạt hành chính như thế nào?
a) Phạt tiền từ 2.000.000 đồng đến 5.000.000 đồng
b) Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng
c) Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng
Đáp án: a
Câu hỏi 23: Anh, chị hãy cho biết các trường hợp nào sau đây bị tạm đình chỉ hoạt động đối với cơ sở, phương tiện giao thông cơ giới, hộ gia đình, cá nhân không đảm bảo an toàn về phòng cháy và chữa cháy?
a) Trong môi trường nguy hiểm cháy, nổ xuất hiện nguồn lửa, nguồn nhiệt hoặc khi đang có nguồn lửa, nguồn nhiệt mà xuất hiện môi trường nguy hiểm cháy, nổ (sau đây gọi là nguy cơ trực tiếp phát sinh cháy, nổ).
b) Vi phạm quy định về phòng cháy và chữa cháy nếu không được ngăn chặn kịp thời thì có thể dẫn đến nguy cơ trực tiếp phát sinh cháy, nổ và có thể gây hậu quả đặc biệt nghiêm trọng.
c)  Vi phạm quy định về phòng cháy và chữa cháy đã được cơ quan Cảnh sát phòng cháy và chữa cháy yêu cầu khắc phục mà không khắc phục hoặc đã bị xử phạt vi phạm hành chính về phòng cháy và chữa cháy mà tiếp tục vi phạm.
d) Cả a, b, c
Đáp án: d
Câu hỏi 24: Anh/chị hãy cho biết hành vi nào bị nghiêm cấm theo Điều 13, Luật phòng cháy và chữa cháy?
a) Báo cháy giả
b) Làm hư hỏng, tự ý thay đổi, di chuyển phương tiện, thiết bị phòng cháy và chữa cháy, biển báo, biển chỉ dẫn và lối thoát nạn
c) Làm hư hỏng các trang thiết bị phòng cháy và chữa cháy
d) Cả a và b
Đáp án: d
Câu hỏi 25: Anh, chị hãy cho biết hành vi nào sau đây là vi phạm các quy định về PCCC?
a) Gọi điện thoại khi đang đổ xăng
b) Không trang bị bình chữa cháy tại nhà ở
c) Khoá, chèn, chặn cửa thoát nạn
d) Cả 3 phương án trên
Đáp án: d
Câu hỏi 26: Nhà Văn phòng, khách sạn, Nhà nghỉ cao 5 tầng có thuộc diện phải thẩm duyệt về PCCC?
a) Có                                                           
b) Không
c) Tùy nhu cầu của Văn phòng, khách sạn, Nhà nghỉ
d) Chỉ có khách sạn, Nhà nghỉ là thuộc diện phải thẩm duyệt về PCCC.
Đáp án: a
Câu hỏi 27: Cơ sở như thế nào phải mua bảo hiểm cháy nổ bắt buộc?
a) Hộ gia đình
b) Phương tiện giao thông cơ giới
c) Người dân
d) Cơ sở có nguy hiểm về cháy, nổ
Đáp án: d
Câu hỏi 28: Cơ sở sản xuất và kinh doanh hóa chất nguy hiểm về cháy, nổ với diện tích 1000m2 có phải xây dựng phương án chữa cháy không?
a) Có
b) Không
c) Tùy vào nhu cầu của các cơ sở
d) Trên 2000m2 mới cần phải xây dựng phương án chữa cháy
Đáp án: a
Câu hỏi 29: Công dân từ bao nhiêu tuổi trở lên, đủ sức khoẻ có trách nhiệm tham gia vào đội dân phòng, đội phòng cháy và chữa cháy cơ sở được lập ở nơi cư trú hoặc nơi làm việc khi có yêu cầu?
a) 16 tuổi
b) 17 tuổi
c) 18 tuổi
d) 19 tuổi
Đáp án: c
Câu hỏi 30: Bình chữa cháy có ký hiệu MT5 là bình chữa cháy loại gì?
a) Loại bột 5kg.
b) Loại khí 5kg.
c) Loại bột 50kg.
d) Loại khí 50kg.
Đáp án: b
Câu hỏi 31: Bình chữa cháy có ký hiệu MT3 là bình chữa cháy loại gì?
a) Loại bột 5kg.
b) Loại khí 5kg.
c) Loại bột 3kg.
d) Loại khí 3kg.
Đáp án: d
Câu hỏi 32: Bình chữa cháy có ký hiệu MFZ5 là bình chữa cháy loại gì?
a) Loại bột 5kg.
b) Loại khí 5kg.
c) Loại bột 3kg.
d) Loại khí 3kg.
Đáp án: a
Câu hỏi 33: Bình chữa cháy có ký hiệu MFZ3 là bình chữa cháy loại gì?
a) Loại bột 5kg.
b) Loại khí 5kg.
c) Loại bột 3kg.
d) Loại khí 3kg.
Đáp án: c
Câu hỏi 34: Cách sử dụng bình chữa cháy bằng bột như thế nào?
a) Ném cả bình vào đám cháy.
b) Lắc bình, rút chốt, hướng loa phun vào ngọn lửa, bóp cò.
c) Đứng tại chỗ phun chất chữa cháy.
d) cả a,b,c đều đúng.
Đáp án: b
Câu hỏi 35: Bình chữa cháy bằng bột chữa cháy không hiệu quả đối với đám cháy nào?
a) Chất rắn
b) Chất lỏng
c) Chất khí.
d) Các kim loại đang nóng đỏ và thiết bị điện tử
Đáp án: d
Câu hỏi 36: Bình chữa cháy bằng khí chữa cháy hiệu quả ở khu vực nào?
a) Ngoài trời
b) Nơi có gió
c) Nơi kín gió
d) Tất cả các đáp án trên
Đáp án: c
Câu hỏi 37: Anh/chị hãy cho biết kiểm tra an toàn về phòng cháy và chữa cháy gồm những nội dung nào?
a) Điều kiện an toàn về phòng cháy và chữa cháy của cơ sở.
b) Việc thực hiện trách nhiệm phòng cháy và chữa cháy.
c) Việc chấp hành các quy định của Luật Phòng cháy và chữa cháy.
d) Cả a, b, c
Đáp án: d
Câu hỏi 38: Khi có cháy xảy ra do điện, đầu tiên, ta phải làm gì?
a) Báo động cho mọi người xung quanh biết, đồng thời gọi 114.
b) Ngắt cầu dao điện.
c) Nhanh chóng dùng phương tiện chữa cháy tại chỗ để chữa cháy.
d) Tất cả đều đúng.
Đáp án: d
Câu hỏi 39: Các biện pháp phòng cháy điện trong hộ gia đình?
a) Không dùng đồ kém chất lượng.
b) Không đặt chất gây cháy gần ổ cắm.
c) Không để người tâm thần, trẻ nhỏ dùng bếp điện.
d) Tất cả đều đúng.
Đáp án: d
Câu hỏi 40: Để đảm bảo an toàn khi sử dụng khí gas trong gia đình, anh/chị sẽ phải làm gì?
a) Khóa van an toàn sau mỗi lần sử dụng.
b) Thường xuyên vệ sinh bếp và khu vực nấu ăn.
c) Trang bị thiết bị cảnh báo rò rỉ khí gas.
d) cả a,b,c đều đúng.
Đáp án: d
Câu hỏi 41: Luật PCCC quy định một trong những biện pháp cơ bản đầu tiên trong công tác phòng cháy là gì?
a) Sử dụng an toàn các chất cháy, chất nổ.
b) Quản lý chặt chẽ.
c) Quản lý chặt chẽ và sử dụng an toàn các chất cháy, nguồn lửa, thiết bị sinh nhiệt.
d) Tự tổ chức kiểm tra.
Đáp án: c
Câu hỏi 42: Khi ngửi thấy mùi khét, khói hoặc thấy lửa thì gọi cho lực lượng nào?
a) Lực lượng PCCC, qua số 114.
b) Lực lượng Cảnh sát 113.
c) UBND Phường.
d) Cả ba đáp án.
Đáp án: a
Câu hỏi 43: Khi nào thì nên kiểm tra định kỳ bình cứu hỏa?
a) Cứ sau 6 tháng hoặc khi mốc ở kim chỉ đỏ.
b) Cứ sau 1 năm.
c) Cứ sau 2 năm.
d) Câu b và c đúng.
Đáp án: a
Câu hỏi 44: Bạn nên để bình chữa cháy ở đâu?
a) Tại nơi dễ thấy, dễ lấy, gần cửa ra vào.
b) Để cao khỏi tầm tay trẻ em.
c) Cất kín đáo để bảo quản.
d) Câu a và b đúng.
Đáp án: a
Câu hỏi 45: Khi ngoài cửa căn hộ đã bị bao vây bởi lửa không thể thoát ra ngoài, bạn làm thế nào?
a) Ở yên trong phòng, chờ người đến cứu.
b) Ra ban công/sân thượng ra hiệu, tuyệt đối không nhảy.
c) Chạy đại qua mảng lửa để thoát.
d) Dùng chăn quấn chạy nhảy qua ban công.
Đáp án: b
Câu hỏi 46: Xác định vị trí của khói. Nếu khói xuất phát từ tầng dưới phòng bạn thì sao?
a) Ở yên trong phòng.
b) Nhanh chóng di chuyển ra thang bộ để lên thượng hoặc xuống dưới.
c) Dùng thang máy.
d) Nhảy ra ngoài sổ.
Đáp án: b
Câu hỏi 47: Phương tiện PCCC gồm những loại phương tiện nào?
a) Bình chữa cháy.
b) Báo cháy tự động.
c) Chữa cháy tự động.
d) Phương tiện cơ giới, thiết bị chuyên PCCC, thô sơ chuyên dụng.
Đáp án: d
Câu hỏi 48: Người đứng đầu khi xảy ra cháy nổ thì chịu hình thức?
a) Hình sự.
b) Phạt tiền.
c) Không bị gì.
d) Tùy mức độ có thể phạt tiền hoặc truy cứu trách nhiệm hình sự.
Đáp án: d
Câu hỏi 49: Các hành vi bị nghiêm cấm theo quy định của Luật PCCC?
a) Cố ý gây cháy nổ.
b) Cản trở PCCC chống người thi hành công vụ.
c) Lợi dụng PCCC xâm hại tài sản.
d) Cả a, b, c.
Đáp án: d
Câu hỏi 50: Trách nhiệm phòng cháy và chữa cháy là của ai?
a) Cảnh sát PCCC
b) Lực lượng dân phòng
c) Lực lượng PCCC chuyên ngành
d) Mỗi cơ quan, tổ chức, hộ gia đình và cá nhân
Đáp án: d
"""

import re
import json

questions = []
# Match pattern: Câu hỏi X: [question]\n[options]\nĐáp án: [answer]
blocks = re.split(r'Câu hỏi \d+:', raw_text)
for block in blocks:
    block = block.strip()
    if not block:
        continue
    
    # Extract 'Đáp án: <char>'
    ans_match = re.search(r'Đáp án:\s*([a-dzA-Z])', block)
    if not ans_match:
        # Xử lý ngoại lệ Câu 25: Đáp án: a và c => gộp vào 1
        continue
        
    ans_letter = ans_match.group(1).lower()
    correct_idx = ord(ans_letter) - ord('a')
    
    # Tách dòng text
    lines = block.split('\n')
    q_text = lines[0].strip()
    
    options = []
    for line in lines[1:]:
        if line.startswith('Đáp án:'):
            break
        # Match "a) " or similar
        opt_match = re.match(r'^[a-d]\s*[\)\.]\s*(.*)', line, re.IGNORECASE)
        if opt_match:
            options.append(opt_match.group(1).strip())
        elif len(options) == 0 and line.strip() != "":
             # missing a) b)
             pass
             
    if not options:
        # Fallback for questions without explicit a) b) 
        opt_lines = [l for l in lines[1:] if l.strip() and not l.startswith('Đáp án:')]
        for opt in opt_lines:
            options.append(opt.strip())
            
    # Fix for questions where the parsing logic resulted in weird options
    if len(options) >= 2:
        formatted_options = []
        for i, opt_text in enumerate(options):
            formatted_options.append({
                "text": opt_text,
                "isCorrect": (i == correct_idx)
            })
        
        questions.append({
            "q": q_text,
            "options": formatted_options
        })

# Dữ liệu xuất sang json js code
js_array_str = json.dumps(questions, ensure_ascii=False, indent=4)

# Replace in game_quiz.html
import os
file_path = os.path.join(os.path.dirname(__file__), "frontend", "game-quiz.html")

with open(file_path, "r", encoding="utf-8") as f:
     content = f.read()
     
# Regex replace ALL_QUESTIONS = [...]
new_js = f"const ALL_QUESTIONS = {js_array_str};\n"
content = re.sub(r'const ALL_QUESTIONS = \[.*?\];', new_js, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
    
print(f"Updated JS with {len(questions)} high quality questions.")
