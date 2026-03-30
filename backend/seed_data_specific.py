"""
FRAS Question Database - Specific Questions by Facility Type
AUTO-GENERATED from danh_sach_cau_hoi_duyet.txt
DO NOT EDIT MANUALLY - Edit the txt file and re-run sync_questions_from_txt.py
"""

SPECIFIC_CATEGORY_A = {
    "name": "Đặc thù: SẢN XUẤT CÔNG NGHIỆP",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: sản xuất công nghiệp",
    "facility_type": "A",
    "icon": "🏭",
    "color": "#e74c3c",
    "questions": [
        {
            "text": "Khu vực sơn, phun sơn có mùi dung môi nồng, hơi dung môi nhìn thấy được trong không khí không?",
            "options": [
                {
                    "key": "A",
                    "text": "Buồng sơn kín có quạt hút, không mùi ngoài buồng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có quạt hút nhưng thoáng mùi dung môi lúc mở cửa",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Sơn trong xưởng mở, hơi dung môi lan tỏa, mùi nồng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Phun sơn trong phòng kín, không thông gió, nồng độ hơi cao, có ổ cắm thường",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hệ thống hút bụi, ống dẫn bụi, silo chứa bụi có tích bụi dày hoặc đã phồng ống không?",
            "options": [
                {
                    "key": "A",
                    "text": "Vệ sinh định kỳ, ống sạch, silo có van xả áp",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Vệ sinh hàng tháng nhưng chưa kiểm tra nguy cơ nổ bụi",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Bụi tích dày trong ống, silo chưa có van xả áp",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Đã phồng ống hoặc cháy nhỏ trong hệ thống hút bụi",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Phoi kim loại dính dầu cắt gọt có tích đống gần máy đang chạy hoặc nguồn nhiệt không?",
            "options": [
                {
                    "key": "A",
                    "text": "Phoi thu gom ngay, dầu hứng khay, xử lý hàng ngày",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Thu gom cuối ca, dính dầu nhưng lượng nhỏ, xa nguồn nhiệt",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Phoi dính dầu tích đống nhiều ngày gần máy đang chạy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Phoi dính dầu chất đống gần khu hàn cắt, đã bốc khói",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hệ thống điện nhà xưởng có dấu hiệu quá tải: dây nóng, CB nhảy thường xuyên?",
            "options": [
                {
                    "key": "A",
                    "text": "Hệ thống đủ tải, dây không nóng, CB không nhảy",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Đủ tải hiện tại nhưng không còn dự phòng cho máy mới",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Thêm nhiều máy mới, CB thỉnh thoảng nhảy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Dây nóng ran khi chạy, CB nhảy phải nối tắt",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Khu nạp axit, pha hóa chất có hơi axit ăn mòn thiết bị điện xung quanh không?",
            "options": [
                {
                    "key": "A",
                    "text": "Không có hóa chất, hoặc có quạt hút cục bộ, thiết bị được bảo vệ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có quạt hút nhưng công suất nhỏ, thoáng mùi hóa chất",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Không hút hơi, axit bay hơi ăn mòn thiết bị điện gần đó",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Hơi axit ăn mòn dây điện và tủ điện, đã gây chập",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Thanh nhiệt trong dây chuyền đóng gói có bị kẹt vật liệu (nilon, giấy) gây cháy chảy không?",
            "options": [
                {
                    "key": "A",
                    "text": "Không có thanh nhiệt, hoặc có cảm biến ngắt khi kẹt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Hoạt động tốt nhưng chưa có cảm biến ngắt khi kẹt",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Vật liệu đôi khi kẹt vào thanh nhiệt gây chảy/cháy nhỏ",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Thanh nhiệt hỏng tự ngắt, quá nhiệt, đã cháy nhiều lần",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Khu sạc xe nâng/ắc-quy có thông gió không? Có mùi axit hoặc khí gas không?",
            "options": [
                {
                    "key": "A",
                    "text": "Khu sạc riêng, thông gió tốt, biển cấm lửa",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Khu sạc riêng nhưng thông gió chưa đủ",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Sạc ngay trong kho hàng, gần hàng dễ cháy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Sạc phòng kín, bộ sạc cũ tóe tia lửa, khí hydro tích tụ",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Thiết bị gia nhiệt (lò nung, sấy, nhiệt đóng gói) có dấu hiệu quá nhiệt không kiểm soát?",
            "options": [
                {
                    "key": "A",
                    "text": "Có tự ngắt quá nhiệt, nhiệt kế kiểm tra định kỳ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có nhiệt kế nhưng chưa hiệu chuẩn gần đây",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Điều chỉnh nhiệt bằng tay, không tự ngắt, công nhân canh bằng mắt",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Thiết bị tự chế, không kiểm soát nhiệt, đã quá nhiệt gây hỏng",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Motor quạt tháp giải nhiệt, chiller có rung lắc, nóng bất thường, mùi khét không?",
            "options": [
                {
                    "key": "A",
                    "text": "Không có tháp/chiller, hoặc hoạt động êm, bảo trì tốt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Hoạt động bình thường, chưa kiểm tra gần đây",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Motor nóng, rung lắc mạnh hơn trước",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Motor quá tải thường xuyên, tấm tản nhiệt PVC dễ cháy",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Công nhân có nhận biết được dấu hiệu cảnh báo sớm (mùi khét, khói, tiếng lạ) từ quy trình mình làm không?",
            "options": [
                {
                    "key": "A",
                    "text": "Được đào tạo nhận biết dấu hiệu riêng cho từng vị trí",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Được đào tạo PCCC chung, chưa đi sâu dấu hiệu đặc thù",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ quản lý biết, công nhân chưa nhận ra dấu hiệu",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không ai biết dấu hiệu nguy hiểm của quy trình mình làm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_B = {
    "name": "Đặc thù: KHO HÀNG, KHO VẬT LIỆU",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: kho hàng, kho vật liệu",
    "facility_type": "B",
    "icon": "📦",
    "color": "#e67e22",
    "questions": [
        {
            "text": "Hàng dễ cháy (aerosol, pin lithium, dung môi) có đang để lẫn với hàng thường, không nhãn cảnh báo?",
            "options": [
                {
                    "key": "A",
                    "text": "Khu riêng cho hàng nguy hiểm, biển cảnh báo rõ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Để khu riêng nhưng chưa có biển cảnh báo đầy đủ",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Hàng nguy hiểm để chung hàng thường, không nhãn",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Pin lithium, aerosol chất đống sát tủ điện, không bảo vệ",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Lối đi chính trong kho có đang bị hàng hóa chặn, xe nâng không qua được?",
            "options": [
                {
                    "key": "A",
                    "text": "Lối đi thông suốt ≥2m, kiểm tra hàng ngày",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Đôi khi có pallet tạm chiếm chỗ rồi dọn đi",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Lối đi bị thu hẹp, xe nâng đi khó, lối thoát hẹp",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Lối đi bị chặn hoàn toàn, không thể đi qua khi khẩn cấp",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Kho ban đêm có hệ thống báo cháy tự động hoặc camera giám sát không?",
            "options": [
                {
                    "key": "A",
                    "text": "Báo cháy tự động, camera nhiệt, kết nối trung tâm 24/7",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Báo cháy có nhưng không camera nhiệt, bảo vệ tuần tra",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ bảo vệ tuần tra, không hệ thống tự động",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Ban đêm không ai trực, không hệ thống giám sát nào",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Đèn chiếu sáng trong kho có loại nào tỏa nhiệt cao (sợi đốt) chạm vào hàng dễ cháy không?",
            "options": [
                {
                    "key": "A",
                    "text": "Đèn LED, cách hàng ≥0.5m, có chao bảo vệ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Đèn LED nhưng hàng xếp cao gần sát đèn",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Đèn huỳnh quang/sợi đốt, hàng dễ cháy sát đèn, ballast nóng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Đèn sợi đốt chạm trực tiếp vải/giấy/nhựa, đã ố cháy",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Kệ hàng có bị nghiêng, cong vênh do chất quá tải hoặc xe nâng va chạm không?",
            "options": [
                {
                    "key": "A",
                    "text": "Kệ neo chắc, tải trọng ghi rõ, không chất vượt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Kệ neo nhưng tải không ghi rõ, chất theo kinh nghiệm",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Kệ không neo, nghiêng do quá tải, đã bị xe nâng va cong",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Kệ cong vênh vẫn dùng, đã từng đổ gây hư hại",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hàng hỏng (pin rò, aerosol méo, hóa chất đổ) có đang tích đống trong kho không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có khu riêng, kiểm tra xử lý trong ngày",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có khu riêng nhưng xử lý hàng tuần, đôi khi tích nhiều",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Hàng hỏng để lẫn kho chính, tích lâu ngày",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Hàng hỏng (pin rò, hóa chất đổ) chất đống không ai quản lý",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Cuối ngày, bảo vệ có kiểm tra điện từng khu vực kho trước khi khóa cửa không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có checklist kiểm tra: điện, lối thoát, bình chữa cháy",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Đi qua kiểm tra bằng mắt, không checklist",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ tắt đèn chung và khóa cổng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không kiểm tra gì, đôi khi quên tắt điện",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_C = {
    "name": "Đặc thù: NHÀ Ở KẾT HỢP KINH DOANH",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: nhà ở kết hợp kinh doanh",
    "facility_type": "C",
    "icon": "🏠",
    "color": "#f39c12",
    "questions": [
        {
            "text": "Khu bán hàng/sản xuất tầng dưới có ngăn cách với khu ngủ tầng trên bằng tường và cửa chắn không?",
            "options": [
                {
                    "key": "A",
                    "text": "Tường chịu lửa, cửa chắn tự đóng, lối đi riêng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có tường gạch, cửa thường, nhưng lối đi chung qua khu kinh doanh",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ phân biệt bằng nội thất, hàng hóa tràn vào khu ở",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Toàn bộ nhà kể cả phòng ngủ, cầu thang đều chứa hàng",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Từ phòng ngủ tầng trên có lối thoát nào KHÔNG đi qua khu hàng hóa tầng dưới không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có cầu thang thoát riêng hoặc ban công nối nhà bên",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Cầu thang bê tông qua tầng kinh doanh, có cửa ngăn mỗi tầng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Cầu thang duy nhất qua khu hàng hóa đầy ắp, không cửa ngăn",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Tầng trên bị giam kín (chuồng cọp), chỉ 1 lối qua tầng dưới",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Điện kinh doanh và điện sinh hoạt có riêng mạch, riêng aptomat (CB) không?",
            "options": [
                {
                    "key": "A",
                    "text": "Tách riêng hoàn toàn, CB riêng, ngắt độc lập được",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có CB riêng cho kinh doanh nhưng chung dây tổng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Dùng chung mạch, thiết bị kinh doanh và gia đình cắm cùng ổ",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Chung mạch, thường quá tải, CB nhảy liên tục",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hàng hóa kinh doanh có đang xếp sát ổ cắm, tủ điện hoặc tràn vào khu ngủ không?",
            "options": [
                {
                    "key": "A",
                    "text": "Hàng gọn tầng dưới, cách xa ổ cắm/tủ điện >1m",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Hàng gọn nhưng gần ổ cắm, không tràn lên tầng ngủ",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Hàng dễ cháy sát tủ điện, tràn vào khu sinh hoạt",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Hàng chất khắp nhà kể cả cầu thang, phòng ngủ, sát thiết bị điện",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Phòng ngủ có cảm biến khói không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có cảm biến khói trong mỗi phòng ngủ, hoạt động tốt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có ở hành lang tầng ngủ nhưng chưa lắp trong phòng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ có ở tầng kinh doanh, tầng ngủ không có",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không có cảm biến khói nào trong nhà",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Tủ đông, tủ mát, biển hiệu LED chạy 24/7 có tiếng kêu lạ, motor nóng, mùi khét không?",
            "options": [
                {
                    "key": "A",
                    "text": "Hoạt động bình thường, bảo dưỡng định kỳ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Hoạt động bình thường nhưng chỉ sửa khi hỏng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chạy nhiều năm không bảo dưỡng, motor kêu, dây nóng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Motor cháy khét vẫn chạy, biển hiệu chập chờn, chưa sửa",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Bếp kinh doanh và bếp gia đình có cùng phòng nhỏ, nhiều bình gas, ít thông gió không?",
            "options": [
                {
                    "key": "A",
                    "text": "Bếp riêng biệt, quạt hút riêng, thoáng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Cùng phòng bếp nhưng thoáng, bình gas đặt nơi thông gió",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chung bếp quá tải, nhiều bình gas phòng nhỏ, thông gió kém",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Bếp kinh doanh ngay khu bán hàng hoặc gần kho dễ cháy",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Trẻ em trong nhà có biết đường thoát khi cháy và biết làm gì khi nghe chuông báo cháy không?",
            "options": [
                {
                    "key": "A",
                    "text": "Trẻ đã được dạy, biết đường thoát, đã diễn tập",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Đã nói cho trẻ biết lối thoát nhưng chưa diễn tập",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Trẻ chưa được hướng dẫn về thoát nạn",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Trẻ nhỏ ngủ phòng kín tầng cao, không lối thoát thứ hai",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Cầu thang có bị xe máy, hàng hóa chiếm chỗ không? Có cửa ngăn khói mỗi tầng không?",
            "options": [
                {
                    "key": "A",
                    "text": "Cầu thang thông thoáng, có cửa ngăn khói tự đóng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Không cửa ngăn khói nhưng thông thoáng, không để đồ",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Xe máy, đồ đạc chiếm chỗ, phải len qua",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Cầu thang gỗ duy nhất, chất đầy đồ, khi cháy tầng 1 kẹt",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Gia đình đã từng diễn tập thoát nạn ban đêm chưa? Nhà có thang dây hoặc lối phụ không?",
            "options": [
                {
                    "key": "A",
                    "text": "Đã diễn tập, có thang dây hoặc lối thoát phụ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Đã bàn kế hoạch nhưng chưa thực hành, có đèn pin",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chưa nghĩ đến, không có kế hoạch",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Nhà nhiều tầng, khóa kín ban đêm, không ai biết phải làm gì",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_D = {
    "name": "Đặc thù: NHÀ HÀNG, KHÁCH SẠN, CHỢ, TTTM",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: nhà hàng, khách sạn, chợ, tttm",
    "facility_type": "D",
    "icon": "🏪",
    "color": "#2ecc71",
    "questions": [
        {
            "text": "Ống hút khói bếp có mùi khét, quạt chạy chậm, mỡ nhỏ giọt ngược không?",
            "options": [
                {
                    "key": "A",
                    "text": "Vệ sinh mỗi 3 tháng, hoạt động tốt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Tự vệ sinh, quạt bình thường",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Bộ lọc mỡ bám dày, quạt chậm, mùi khét",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Chưa bao giờ vệ sinh, mỡ nhỏ ngược, đã cháy mỡ nhỏ",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Tiểu thương có dùng bếp gas/bếp cồn ngay tại gian hàng trong chợ/TTTM không?",
            "options": [
                {
                    "key": "A",
                    "text": "Cấm tuyệt đối, kiểm tra hàng ngày",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có quy tắc cấm nhưng kiểm tra không thường xuyên",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Biết tiểu thương dùng nhưng không xử lý",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Nhiều gian hàng dùng bếp gas thoải mái, bình gas trong gian hàng kín",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Cửa kho hàng trong TTTM có luôn bị chèn mở suốt ngày không?",
            "options": [
                {
                    "key": "A",
                    "text": "Cửa chống cháy tự đóng, kết nối hệ thống báo cháy",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Tự đóng nhưng thỉnh thoảng chèn mở rồi đóng lại",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Luôn bị chèn mở bằng gạch/nêm suốt ngày",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Cửa kho hỏng, kho thông sàn bán hàng, hàng tràn ra",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Bếp nhà hàng có hệ thống dập cháy dầu mỡ chuyên dụng hay chỉ có bình bột thường?",
            "options": [
                {
                    "key": "A",
                    "text": "Có hệ thống dập cháy bếp tự động, kiểm tra 6 tháng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có bình chữa cháy bếp chuyên dụng, chưa có hệ thống tự động",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ có bình bột ABC, không phù hợp cho cháy dầu mỡ",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không bình nào trong bếp, dập cháy dầu bằng nước",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Lối thoát có bị đông nghịt vượt sức chứa trong sự kiện/giờ cao điểm không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có biển sức chứa, kiểm soát số người, đóng cửa khi đạt giới hạn",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Biết sức chứa nhưng chưa đếm người ra vào",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Không biết sức chứa, sự kiện đông không giới hạn",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Đông vượt sức chứa, lối thoát kẹt cứng, chen lấn nguy hiểm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_E = {
    "name": "Đặc thù: BỆNH VIỆN, TRƯỜNG HỌC, CƠ SỞ Y TẾ",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: bệnh viện, trường học, cơ sở y tế",
    "facility_type": "E",
    "icon": "🏥",
    "color": "#3498db",
    "questions": [
        {
            "text": "Có phương án sơ tán cho bệnh nhân không tự đi (nằm liệt, máy trợ sự sống) không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có phương án, thiết bị sơ tán, đã diễn tập",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có phương án chung, chưa có thiết bị chuyên dụng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ có kế hoạch cho người tự đi, bệnh nhân nặng chưa có",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không có phương án, bệnh nhân liệt tầng cao không thang cứu hỏa",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Cồn y tế, formalin, hóa chất dễ cháy có đang để lẫn lộn gần ổ cắm, bồn rửa không?",
            "options": [
                {
                    "key": "A",
                    "text": "Để trong tủ chống cháy, phân loại tương thích",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Tủ riêng có khóa nhưng không phải tủ chống cháy",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Để lẫn trên kệ chung, gần bồn rửa và ổ cắm",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Để tràn lan trên bàn, gần nguồn nhiệt, chai hở nắp",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Đường ống oxy trong bệnh viện có dấu hiệu rò rỉ (mùi lạ, tiếng xì) không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có cảm biến rò, van ngắt khẩn, kiểm tra ống định kỳ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Kiểm tra ống định kỳ nhưng chưa lắp cảm biến tự động",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Ống cũ, chưa kiểm tra gần đây, không cảm biến",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Ống rò rỉ, nồng độ oxy cao phòng kín, nguy cơ cháy bùng lớn",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Phòng học có ≥2 cửa thoát? Cửa có bị khóa hoặc chất đồ trong giờ học không?",
            "options": [
                {
                    "key": "A",
                    "text": "≥2 cửa mở ra ngoài, thanh đẩy khẩn cấp, đèn EXIT",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "2 cửa nhưng 1 mở vào trong, không khóa",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ 1 cửa, mở vào trong, bàn ghế chật",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Cửa khóa từ ngoài trong giờ, cửa sổ song sắt, không thoát được",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Trường có tổ chức diễn tập sơ tán cho học sinh, kể cả tình huống không báo trước không?",
            "options": [
                {
                    "key": "A",
                    "text": "Diễn tập 2 lần/năm, phù hợp lứa tuổi, kể cả không báo trước",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "1 lần/năm có báo trước, học sinh biết lối thoát",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ phổ biến lý thuyết, chưa diễn tập thực tế",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Chưa bao giờ diễn tập, học sinh không biết lối thoát",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_F = {
    "name": "Đặc thù: XĂNG DẦU, KHÍ GAS, VẬT LIỆU NỔ",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: xăng dầu, khí gas, vật liệu nổ",
    "facility_type": "F",
    "icon": "⛽",
    "color": "#9b59b6",
    "questions": [
        {
            "text": "Có vết dầu loang trên mặt sân cây xăng gợi ý rò rỉ bể ngầm/đường ống không?",
            "options": [
                {
                    "key": "A",
                    "text": "Kiểm tra rò rỉ hàng năm bằng thiết bị, không vết dầu",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Kiểm tra bằng mắt hàng tháng, chưa thấy bất thường",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Đôi khi thấy vết dầu loang trên sân chưa điều tra",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Dầu rò rỉ từ bể ngầm, ngấm ra xung quanh, chưa sửa",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Kho gas/LPG có mùi gas, cảm biến khí hoạt động, hệ thống thông gió chạy tốt không?",
            "options": [
                {
                    "key": "A",
                    "text": "Cảm biến gas, van ngắt tự động, quạt thông gió 24/7",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Van ngắt tay, quạt thông gió, chưa có cảm biến tự động",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Không cảm biến, thông gió tự nhiên, phát hiện rò bằng mũi",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Kho kín, mùi gas rõ, chưa xử lý, không van ngắt khẩn cấp",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Khách có tắt máy xe và không dùng điện thoại khi bơm xăng không?",
            "options": [
                {
                    "key": "A",
                    "text": "Nhân viên yêu cầu nghiêm, biển cấm đầy đủ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có biển cấm, nhắc nhở nhưng chưa kiểm soát 100%",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Có biển nhưng nhân viên ngại nhắc, nhiều khách dùng điện thoại",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không kiểm soát, khách vẫn nổ máy, hút thuốc khi bơm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Dây nối đất chống tĩnh điện bồn chứa và vòi bơm có bị đứt, gỉ sét không?",
            "options": [
                {
                    "key": "A",
                    "text": "Kiểm tra hàng năm, dây tốt, điện trở đạt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có hệ thống nhưng lâu chưa kiểm tra",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Dây nối đứt/gỉ ở một số vị trí",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không có hệ thống nối đất chống tĩnh điện",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Nhân viên ca đêm có biết cách ngắt điện khẩn cấp, đóng van bể khi rò rỉ không?",
            "options": [
                {
                    "key": "A",
                    "text": "Biết rõ: nút ngắt, van bể, quy trình sơ tán, số khẩn cấp",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Biết nút ngắt nhưng chưa thực hành bao giờ",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Nhân viên mới, chưa biết quy trình khẩn cấp",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Ca đêm 1 người, không biết quy trình, ngủ gật",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_G = {
    "name": "Đặc thù: PHƯƠNG TIỆN GIAO THÔNG",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: phương tiện giao thông",
    "facility_type": "G",
    "icon": "🚌",
    "color": "#1abc9c",
    "questions": [
        {
            "text": "Xe khách/xe buýt có bình chữa cháy, búa thoát hiểm đầy đủ, hành khách biết vị trí không?",
            "options": [
                {
                    "key": "A",
                    "text": "Đủ búa, cửa thoát hoạt động, tài xế thông báo trước chuyến",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có búa và cửa thoát nhưng tài xế không thông báo",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Búa thiếu hoặc giấu đi, cửa thoát bị kẹt",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không có búa, cửa thoát hàn kín hoặc chất hàng che",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hệ thống điện xe (dây, cầu chì, ắc-quy) có dấu hiệu chạm chập: khói, mùi khét?",
            "options": [
                {
                    "key": "A",
                    "text": "Kiểm tra mỗi 6 tháng, dây tốt, cầu chì đúng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Bảo dưỡng theo km, chưa kiểm tra điện riêng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Xe cũ, dây nối tạm băng keo, cầu chì dùng dây đồng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Đã có khói/tia lửa từ khoang điện, vẫn chạy",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Khu sạc xe điện tại bãi đỗ có thông gió, bình chữa cháy, cách xa xe xăng không?",
            "options": [
                {
                    "key": "A",
                    "text": "Khu sạc riêng, sprinkler, bình chữa cháy, sàn chống cháy",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Khu riêng, có bình chữa cháy nhưng chưa có sprinkler",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Sạc trong bãi chung, gần xe xăng, không PCCC riêng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Sạc tầng hầm kín, không thông gió, không PCCC, qua đêm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hàng hóa dễ cháy (bình gas, xăng) có đang để lẫn trong khoang hành khách không?",
            "options": [
                {
                    "key": "A",
                    "text": "Khoang hành lý tách biệt, vách ngăn, không hàng nguy hiểm",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Khoang riêng nhưng vách ngăn bằng vật liệu thường",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Hành lý để lẫn khoang khách, hàng chất trên lối đi",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Bình gas, xăng để lẫn khoang hành khách",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Xe tải chở hàng nguy hiểm có biển báo, bộ ứng phó sự cố trên xe không?",
            "options": [
                {
                    "key": "A",
                    "text": "Không chở hàng nguy hiểm, hoặc đủ biển báo, bộ ứng phó",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có biển báo nhưng bộ ứng phó chưa đầy đủ",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Biển mờ, thiếu dụng cụ ứng phó",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Chở hàng nguy hiểm không biển, không PCCC trên xe",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_H = {
    "name": "Đặc thù: KHU DÂN CƯ, NHÀ TRỌ, NHÀ Ở",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: khu dân cư, nhà trọ, nhà ở",
    "facility_type": "H",
    "icon": "🏘️",
    "color": "#e74c3c",
    "questions": [
        {
            "text": "Nhà trọ/chung cư mini có bao nhiêu lối thoát nạn? Các lối thoát có thông thoáng 24/7 không?",
            "options": [
                {
                    "key": "A",
                    "text": "≥2 lối thoát độc lập, luôn thông, có thang thoát phụ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "2 lối nhưng 1 lối phụ (ban công, cửa sổ), lối chính thông",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ 1 cầu thang duy nhất, cửa phụ bị khóa hoặc chặn đồ",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "1 lối duy nhất, khóa cổng sắt ban đêm, không ai có chìa dự phòng",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Chuồng cọp, lưới chống trộm có lối mở khẩn cấp không? Mọi người có biết cách mở không?",
            "options": [
                {
                    "key": "A",
                    "text": "Không có chuồng cọp, hoặc có lối mở, chìa để cạnh, mọi người biết",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có cửa mở nhưng chìa cất trong phòng, phải tìm",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chuồng cọp hàn kín, chỉ 1 cửa ra vào chính",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Hàn kín toàn bộ cửa sổ và ban công, không lối mở nào",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Mỗi phòng trọ có aptomat (CB) riêng không? Hay nhiều phòng dùng chung?",
            "options": [
                {
                    "key": "A",
                    "text": "Mỗi phòng CB riêng, có CB chống rò tổng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "CB riêng mỗi phòng nhưng chưa có CB chống rò tổng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "2-3 phòng chung CB, quá tải thì mất điện cả mấy phòng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Toàn nhà chung 1 CB, dây nối tạm, CB nhảy thì nối tắt",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Bình nước nóng trong phòng tắm có bị rỉ sét, dây điện hở trong môi trường ẩm ướt không?",
            "options": [
                {
                    "key": "A",
                    "text": "Bình tốt, có thiết bị chống giật riêng, nối đất đúng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có thiết bị chống giật nhưng lắp đã lâu, chưa kiểm tra",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Bình cũ không có thiết bị chống giật, chung CB với ổ cắm phòng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Bình rỉ sét, dây hở trong phòng tắm ẩm, rất nguy hiểm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Người thuê có nấu gas trong phòng trọ kín không? Bình gas để ở đâu?",
            "options": [
                {
                    "key": "A",
                    "text": "Cấm gas trong phòng, có bếp chung hoặc bếp điện từ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Dùng bếp gas mini nhỏ, phòng thông thoáng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Bếp gas trong phòng nhỏ kín, bình gas 12kg, ít thông gió",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Bếp gas phòng kín, dây nứt, bình gas dưới gầm giường",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Có ai giữ chìa khóa tổng (master key) và chìa cổng khẩn cấp 24/7 không?",
            "options": [
                {
                    "key": "A",
                    "text": "Chủ nhà giữ master key 24/7, chìa cổng trong hộp kính phá vỡ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Chủ nhà giữ nhưng không ở tại chỗ 24/7, phải gọi điện",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ chủ nhà có chìa, chủ ở xa, ban đêm không liên lạc được",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không master key, mỗi phòng khóa riêng, cổng khóa xích",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Xe cứu hỏa có vào được hẻm/ngõ nơi nhà trọ tọa lạc không?",
            "options": [
                {
                    "key": "A",
                    "text": "Đường rộng ≥3.5m, xe cứu hỏa vào tận nơi",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Hẻm hơi hẹp, xe cứu hỏa phải đỗ ngoài kéo vòi",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Không biết, hẻm nhỏ xe cứu hỏa không vào được",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Hẻm cụt, xe cứu hỏa không thể tiếp cận",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Chủ nhà trọ có dán sơ đồ thoát nạn mỗi tầng và phổ biến cho người thuê không?",
            "options": [
                {
                    "key": "A",
                    "text": "Sơ đồ dán mỗi tầng, phổ biến cho người thuê mới",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Phổ biến miệng nhưng chưa dán sơ đồ",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chưa phổ biến, nội quy cũ mờ chữ",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không nội quy, sơ đồ, người thuê không biết lối thoát",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Nhà trọ có cảm biến khói ở hành lang và phòng trọ không?",
            "options": [
                {
                    "key": "A",
                    "text": "Cảm biến khói trong mỗi phòng và hành lang, có chuông",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Ở hành lang mỗi tầng nhưng chưa lắp trong phòng",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chỉ ở tầng 1, các tầng trên không có",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không có cảm biến hay chuông báo cháy nào",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Xe máy, xe đạp điện có sạc trong phòng trọ/phòng ngủ kín qua đêm không?",
            "options": [
                {
                    "key": "A",
                    "text": "Khu sạc riêng tầng trệt thông thoáng, có bình chữa cháy",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Sạc tầng trệt khu chung, chưa có bình chữa cháy",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Sạc trong phòng trọ gần đồ dùng cá nhân",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Sạc qua đêm phòng kín, pin cũ phồng, sạc kém chất lượng",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_I = {
    "name": "Đặc thù: CÔNG TRÌNH XÂY DỰNG ĐANG THI CÔNG",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: công trình xây dựng đang thi công",
    "facility_type": "I",
    "icon": "🏗️",
    "color": "#e67e22",
    "questions": [
        {
            "text": "Công trình có hàn cắt tự do không cần kiểm tra hiện trường, tia lửa bắn vào vật dễ cháy?",
            "options": [
                {
                    "key": "A",
                    "text": "Có kiểm tra hiện trường trước, dọn vật cháy 10m, canh lửa sau",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có kiểm tra nhưng không phải lúc nào cũng thực hiện",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Hàn cắt tự do, đôi khi dọn vật dễ cháy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Hàn cắt không kiểm soát, tia lửa bắn vào vật cháy, đã cháy nhỏ",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Gỗ ván khuôn, xốp cách nhiệt, sơn có đang chất đống sát khu hàn cắt và thiết bị điện tạm?",
            "options": [
                {
                    "key": "A",
                    "text": "Kho riêng cách khu thi công ≥10m, có bình chữa cháy",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Khu riêng nhưng gần khu thi công, có bình chữa cháy",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Rải rác khắp công trình, gần khu hàn cắt",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Gỗ, xốp, sơn chất lẫn lộn sát khu hàn cắt và điện tạm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Điện tạm thi công có dây trần, nối băng keo, CB không có, ngâm nước khi mưa?",
            "options": [
                {
                    "key": "A",
                    "text": "Thợ điện chứng chỉ lắp, tủ tạm có CB, ELCB, nối đất",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Thợ điện lắp, có CB nhưng chưa ELCB",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Công nhân tự kéo, nối tạm, vắt qua khung thép, không CB",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Dây trần, nối băng keo, ngâm nước khi mưa",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Lán trại công nhân có bằng bạt/gỗ dễ cháy, nấu bếp gas trong lán, sạc điện tạm?",
            "options": [
                {
                    "key": "A",
                    "text": "Lán vật liệu khó cháy, cách công trình, có cảm biến khói",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Lán tôn thiếc, cách công trình, có bình chữa cháy",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Lán gỗ/bạt sát công trình, không bình chữa cháy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Lán bạt dễ cháy, nấu gas trong lán, sạc điện tạm, rất nguy hiểm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Rác xây dựng (gỗ vụn, xốp, bạt cũ) có đang tích đống gần dây điện tạm hoặc bình gas?",
            "options": [
                {
                    "key": "A",
                    "text": "Thu gom cuối ngày, đổ bãi rác xa công trình",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Thu gom 2-3 ngày, chất góc công trình chờ xe lấy",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Tích nhiều ngày, gần khu thi công, gần dây điện tạm",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Công nhân tự đốt rác tại công trình, gần kho vật tư, bình gas",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_J = {
    "name": "Đặc thù: CƠ QUAN, VĂN PHÒNG, TRỤ SỞ",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: cơ quan, văn phòng, trụ sở",
    "facility_type": "J",
    "icon": "🏢",
    "color": "#3498db",
    "questions": [
        {
            "text": "Ấm nước, quạt sưởi, máy pha cà phê có đang cắm suốt đêm không ai tắt không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có nhắc rút phích cắm, người cuối kiểm tra",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có nhắc nhưng phụ thuộc ý thức, đôi khi quên",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Nhiều thiết bị chế độ chờ qua đêm, ấm nước cắm suốt",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Quạt sưởi, ấm chạy suốt đêm, đã có ấm cạn bốc khói",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hồ sơ giấy tờ có chất đống gần ổ cắm, máy photocopy, không có bản sao lưu số?",
            "options": [
                {
                    "key": "A",
                    "text": "Kho riêng, có PCCC, hồ sơ sao lưu số",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Kho riêng, bình chữa cháy, chưa sao lưu số",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chất đống phòng làm việc, gần ổ cắm, chưa sao lưu",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Chất đống kho kín không PCCC, bản gốc duy nhất",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hành lang, cầu thang thoát nạn có bị bàn ghế, tủ hồ sơ chiếm chỗ không?",
            "options": [
                {
                    "key": "A",
                    "text": "Hành lang thông, cửa ngăn khói tự đóng, đèn sự cố tốt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Thông thoáng, đèn sự cố có nhưng lâu chưa test",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Để bàn ghế, tủ hồ sơ, đèn sự cố một số hỏng",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Cầu thang khóa, hành lang chất đầy đồ, không đèn sự cố",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Máy photocopy, máy in cũ có tỏa nhiệt, bốc mùi nhựa khét, giấy chất sát máy không?",
            "options": [
                {
                    "key": "A",
                    "text": "Phòng riêng thông gió, CB riêng, hoạt động bình thường",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Đặt phòng chung, ĐHKK bình thường",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Máy cũ tỏa nhiệt nhiều, phòng kín nhỏ, giấy chất xung quanh",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Máy nóng bất thường, mùi nhựa khét, giấy đống sát máy, chưa sửa",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Thang máy văn phòng có tự về tầng 1 khi báo cháy không?",
            "options": [
                {
                    "key": "A",
                    "text": "Có chế độ cháy, tự về tầng 1 khi báo cháy",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Ngắt khi báo cháy nhưng không có chế độ riêng cho PCCC",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Không kết nối báo cháy, chạy bình thường khi cháy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Thang cũ, đôi khi kẹt, không chế độ cháy, nguy cơ kẹt người",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_K = {
    "name": "Đặc thù: NGHIÊN CỨU, PHÒNG THÍ NGHIỆM",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: nghiên cứu, phòng thí nghiệm",
    "facility_type": "K",
    "icon": "🔬",
    "color": "#9b59b6",
    "questions": [
        {
            "text": "Hóa chất dễ cháy có đang để lẫn lộn không phân loại (axit gần bazơ, oxy hóa gần dễ cháy)?",
            "options": [
                {
                    "key": "A",
                    "text": "Phân loại theo nhóm tương thích, tách riêng rõ ràng",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Phân loại sơ bộ, chưa tách hoàn toàn",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Để lẫn lộn, axit gần bazơ, oxy hóa gần dễ cháy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Không phân loại, tràn lan, đã xảy ra phản ứng ngoài ý muốn",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Tủ hút khí độc (fume hood) có lực hút yếu, hơi hóa chất thoát ra ngoài không?",
            "options": [
                {
                    "key": "A",
                    "text": "Kiểm tra lưu lượng gió hàng năm, đạt yêu cầu",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Hoạt động nhưng lâu chưa đo, không rõ còn đạt không",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Lực hút yếu, hơi hóa chất thoát ra ngoài",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Tủ hút hỏng, vẫn thao tác hóa chất bay hơi ngoài tủ",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Bình gas thí nghiệm (H₂, O₂) có buộc cố định không? Có van ngắt ngoài phòng không?",
            "options": [
                {
                    "key": "A",
                    "text": "Buộc cố định, van ngắt ngoài phòng, kiểm tra rò rỉ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Buộc cố định, van ngắt trong phòng, chưa kiểm tra rò",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Không buộc, đứng tự do, phải vào phòng mới ngắt",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "H₂/O₂ không buộc, nghiêng, gần nguồn nhiệt, không van ngoài",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Lò nung mẫu, bếp cách thủy có chạy qua đêm không ai giám sát, gần hóa chất?",
            "options": [
                {
                    "key": "A",
                    "text": "Có tự ngắt quá nhiệt, cách xa hóa chất, có giám sát",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có nhiệt kế nhưng đôi khi chạy không giám sát",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Chạy qua đêm không giám sát, gần hóa chất trên bàn",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Thiết bị tự chế, không tự ngắt, chạy liên tục gần dung môi",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Chất thải hóa chất có đang đổ bồn rửa hoặc chất đống trong phòng, chai hở nắp?",
            "options": [
                {
                    "key": "A",
                    "text": "Thu gom thùng chuyên dụng có nhãn, xử lý đúng cách",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Thu gom riêng nhưng chưa phân loại chi tiết",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Đổ xuống bồn rửa hoặc thùng rác thường",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Chất thải nguy hại đống trong phòng, chai hở, nguy cơ phản ứng",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

SPECIFIC_CATEGORY_L = {
    "name": "Đặc thù: NÔNG NGHIỆP, CHẾ BIẾN NÔNG LÂM SẢN",
    "description": "Dấu hiệu nguy cơ cháy nổ - đặc thù: nông nghiệp, chế biến nông lâm sản",
    "facility_type": "L",
    "icon": "🌾",
    "color": "#27ae60",
    "questions": [
        {
            "text": "Xưởng xay xát, chế biến gỗ có bụi ngũ cốc/mùn cưa tích dày, lơ lửng trong không khí?",
            "options": [
                {
                    "key": "A",
                    "text": "Có hệ thống hút bụi, vệ sinh hàng ngày",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có hút bụi nhưng vệ sinh hàng tuần",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Bụi tích dày trên máy, trần, tường, không hút bụi",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Bụi dày đặc khi máy chạy, đã cháy nhỏ do bụi, chưa khắc phục",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Nông sản trong kho có bốc nóng, mốc ẩm nhưng chưa xử lý?",
            "options": [
                {
                    "key": "A",
                    "text": "Có kiểm tra nhiệt, kho thông gió tốt",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Kiểm tra bằng sờ tay, kho thông gió tự nhiên",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Không kiểm tra, kho kín, nông sản ẩm khi nhập",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Nông sản ẩm bốc nóng/mốc trong kho kín, chưa xử lý",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Lò sấy nông sản có chạy qua đêm không ai canh? Có dấu hiệu quá nhiệt?",
            "options": [
                {
                    "key": "A",
                    "text": "Có tự ngắt quá nhiệt, bảo dưỡng định kỳ",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có nhiệt kế nhưng chưa test tự ngắt, sấy theo kinh nghiệm",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Sấy thủ công, canh suốt quá trình sấy",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Lò sấy tự chế, không tự ngắt, sấy qua đêm, đã cháy sản phẩm",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Đèn sưởi gia súc có treo sát rơm, cỏ khô? Dây điện chuồng trại có bị chuột gặm?",
            "options": [
                {
                    "key": "A",
                    "text": "Đèn sưởi có bảo vệ, cách rơm >1m, CB riêng, ELCB",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Có CB nhưng đèn sưởi gần rơm, vẫn theo dõi",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Đèn sưởi treo sát rơm/cỏ, dây kéo qua chuồng, không ELCB",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Dây bị chuột gặm, đèn sưởi chạm rơm, đã cháy nhỏ 1 lần",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        },
        {
            "text": "Hệ thống biogas có mùi gas quanh trại, mối nối ống lỏng, van an toàn có hoạt động không?",
            "options": [
                {
                    "key": "A",
                    "text": "Không biogas, hoặc cảm biến CH₄, van an toàn, kiểm tra ống",
                    "score": 0,
                    "risk": "safe"
                },
                {
                    "key": "B",
                    "text": "Van an toàn có, kiểm tra ống bằng mắt, không cảm biến",
                    "score": 1,
                    "risk": "low"
                },
                {
                    "key": "C",
                    "text": "Ống cũ, mối lỏng, không van an toàn, phát hiện rò bằng mùi",
                    "score": 2,
                    "risk": "high"
                },
                {
                    "key": "D",
                    "text": "Rò rỉ nghiêm trọng, mùi gas quanh trại, gần bếp nấu ăn",
                    "score": 3,
                    "risk": "critical"
                }
            ]
        }
    ]
}

ALL_SPECIFIC_CATEGORIES = [
    SPECIFIC_CATEGORY_A,
    SPECIFIC_CATEGORY_B,
    SPECIFIC_CATEGORY_C,
    SPECIFIC_CATEGORY_D,
    SPECIFIC_CATEGORY_E,
    SPECIFIC_CATEGORY_F,
    SPECIFIC_CATEGORY_G,
    SPECIFIC_CATEGORY_H,
    SPECIFIC_CATEGORY_I,
    SPECIFIC_CATEGORY_J,
    SPECIFIC_CATEGORY_K,
    SPECIFIC_CATEGORY_L,
]
