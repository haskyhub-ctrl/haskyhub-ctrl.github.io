"""
FRAS Question Database - Common Questions
AUTO-GENERATED from danh_sach_cau_hoi_duyet.txt
DO NOT EDIT MANUALLY - Edit the txt file and re-run sync_questions_from_txt.py

Scoring logic v2:
  - "high" (default): A=0, B=1, C=2, D=3 (nguy co truc tiep)
  - "medium":         A=0, B=1, C=2, D=2 (anh huong gian tiep)
  - "low":            A=0, B=0, C=1, D=2 (phong ngua, hieu biet)
"""

FACILITY_TYPES = [
    {
        "name": "Cơ sở sản xuất công nghiệp",
        "code": "A"
    },
    {
        "name": "Kho hàng, kho vật liệu",
        "code": "B"
    },
    {
        "name": "Nhà ở kết hợp kinh doanh",
        "code": "C"
    },
    {
        "name": "Nhà hàng, khách sạn, chợ, TTTM",
        "code": "D"
    },
    {
        "name": "Bệnh viện, trường học, cơ sở y tế",
        "code": "E"
    },
    {
        "name": "Xăng dầu, khí gas, vật liệu nổ",
        "code": "F"
    },
    {
        "name": "Phương tiện giao thông",
        "code": "G"
    },
    {
        "name": "Khu dân cư, nhà trọ, nhà ở",
        "code": "H"
    },
    {
        "name": "Công trình xây dựng đang thi công",
        "code": "I"
    },
    {
        "name": "Cơ quan, văn phòng, trụ sở",
        "code": "J"
    },
    {
        "name": "Nghiên cứu, phòng thí nghiệm",
        "code": "K"
    },
    {
        "name": "Nông nghiệp, chế biến nông lâm sản",
        "code": "L"
    }
]

COMMON_CATEGORIES = [
    {
        "name": "Dấu hiệu nguy cơ từ hệ thống điện",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - dấu hiệu nguy cơ từ hệ thống điện",
        "icon": "⚡",
        "color": "#e74c3c",
        "order_index": 1,
        "max_score": 37
    },
    {
        "name": "Nguy cơ từ nguồn lửa/nhiệt",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - nguy cơ từ nguồn lửa/nhiệt",
        "icon": "🔥",
        "color": "#e67e22",
        "order_index": 2,
        "max_score": 20
    },
    {
        "name": "Lối thoát nạn và trang bị PCCC",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - lối thoát nạn và trang bị pccc",
        "icon": "🚪",
        "color": "#2ecc71",
        "order_index": 3,
        "max_score": 17
    },
    {
        "name": "Dấu hiệu bất thường từ máy móc",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - dấu hiệu bất thường từ máy móc",
        "icon": "⚙️",
        "color": "#3498db",
        "order_index": 4,
        "max_score": 21
    },
    {
        "name": "Tác động từ thiên nhiên",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - tác động từ thiên nhiên",
        "icon": "🌿",
        "color": "#27ae60",
        "order_index": 5,
        "max_score": 13
    },
    {
        "name": "Nguy cơ tự cháy",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - nguy cơ tự cháy",
        "icon": "💥",
        "color": "#9b59b6",
        "order_index": 6,
        "max_score": 20
    },
    {
        "name": "Phương tiện giao thông",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - phương tiện giao thông",
        "icon": "🚗",
        "color": "#1abc9c",
        "order_index": 7,
        "max_score": 12
    },
    {
        "name": "Nguy cơ bổ sung",
        "description": "Các dấu hiệu nhận biết sớm nguy cơ cháy nổ - nguy cơ bổ sung",
        "icon": "⚠️",
        "color": "#f39c12",
        "order_index": 8,
        "max_score": 12
    }
]

GROUP1_QUESTIONS = [
    {
        "text": "Bạn có ngửi thấy mùi khét (nhựa cháy, cao su) phát ra từ ổ cắm, công tắc, tủ điện hoặc bảng điện không?",
        "options": [
            {
                "key": "A",
                "text": "Không có mùi khét bất thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Thỉnh thoảng thoáng có mùi khét nhẹ nhưng nhanh hết",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Có mùi khét rõ ràng từ ổ cắm hoặc tủ điện, xuất hiện thường xuyên",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Mùi khét nồng kèm khói mỏng từ thiết bị điện",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Ổ cắm, phích cắm hoặc công tắc điện có bị nóng bất thường khi chạm tay vào không?",
        "options": [
            {
                "key": "A",
                "text": "Không nóng, nhiệt độ bình thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Ấm nhẹ khi dùng thiết bị công suất lớn, hết ấm khi rút phích",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nóng rõ rệt dù chỉ cắm thiết bị nhỏ, phích cắm bị biến dạng",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Nóng bỏng tay, nhựa ổ cắm bị chảy méo, có vết cháy đen",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Quanh ổ cắm, công tắc hoặc bảng điện có xuất hiện vết xém, ố vàng hoặc muội đen không?",
        "options": [
            {
                "key": "A",
                "text": "Không có vết ố hay cháy xém",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có vết ố vàng nhẹ quanh 1-2 ổ cắm cũ",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nhiều ổ cắm/công tắc có vết xém đen, nhựa sậm màu",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Vết cháy lan rộng trên tường quanh bảng điện, có dấu tia lửa",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Đèn chiếu sáng có bị chập chờn, nhấp nháy hoặc tối đi bất thường không?",
        "options": [
            {
                "key": "A",
                "text": "Đèn sáng ổn định, không nhấp nháy",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Thỉnh thoảng 1-2 bóng nhấp nháy khi bật nhiều thiết bị cùng lúc",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nhiều đèn nhấp nháy thường xuyên, tối đi rõ rệt khi bật thêm thiết bị",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đèn chập chờn liên tục kèm tiếng kêu từ bảng điện, đã từng tắt đột ngột",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Có tiếng kêu lạ (vo ve, lạch cạch, xì xì) phát ra từ ổ cắm, hộp điện hoặc tủ điện không?",
        "options": [
            {
                "key": "A",
                "text": "Không có tiếng kêu bất thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có tiếng vo nhẹ từ ballast đèn huỳnh quang cũ",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Tiếng lạch cạch hoặc xì xì từ ổ cắm/hộp nối khi dùng thiết bị",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Tiếng nổ lách tách kèm tia lửa nhỏ nhìn thấy được",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Tần suất aptomat (cầu dao tự động) bị ngắt điện khi cơ sở vận hành các thiết bị điện như thế nào?",
        "options": [
            {
                "key": "A",
                "text": "Hoạt động ổn định, hầu như không bao giờ bị ngắt điện do quá tải",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Thỉnh thoảng ngắt 1-2 lần khi cùng lúc bật nhiều thiết bị công suất cao",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Thường xuyên bị ngắt điện hàng tuần, phải bật lại aptomat nhiều lần",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Aptomat ngắt liên tục do quá tải hoặc đang phải đấu nối tạm để duy trì hoạt động",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Hiện trạng lắp đặt và tình trạng vỏ cách điện của hệ thống dây dẫn điện tại cơ sở ra sao?",
        "options": [
            {
                "key": "A",
                "text": "Dây điện vỏ nguyên vẹn, luồn ống hoặc máng cáp gọn gàng",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có một vài chỗ dây đi nổi trên tường, lớp vỏ ngoài còn nguyên vẹn",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Có một số đoạn dây đi nối thêm hoặc có quấn băng dính cách điện",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Nhiều đoạn dây đã cũ theo thời gian, có vết trầy xước hoặc đi sát mép kim loại",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Ổ cắm kéo dài (dây nối dài) có bị nóng, chân cắm lỏng hoặc nối chồng nhiều cái không?",
        "options": [
            {
                "key": "A",
                "text": "Không dùng ổ kéo dài, hoặc dùng ít, không nóng",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có dùng nhưng không nối chồng, dây không nóng",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nối chồng 2-3 ổ, cắm nhiều thiết bị, dây ấm khi dùng",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Ổ cắm cũ hỏng, chân lỏng, dây nóng ran khi dùng, vẫn dùng hàng ngày",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Hóa đơn tiền điện có tăng đột biến (trên 20-30%) mà không sử dụng thêm thiết bị mới không?",
        "options": [
            {
                "key": "A",
                "text": "Tiền điện ổn định, tăng giảm theo mùa bình thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có tăng nhẹ nhưng giải thích được (thêm ĐHKK, mùa nóng)",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Tăng bất thường >20% mà không rõ lý do",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Tăng đột biến >50% kèm theo dây điện nóng hoặc CB nhảy",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Dây điện có bị chuột, côn trùng gặm nhấm làm hở lớp vỏ bảo vệ không?",
        "options": [
            {
                "key": "A",
                "text": "Không có dấu hiệu chuột/côn trùng gặm dây điện",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có thấy chuột trong nhà nhưng chưa phát hiện gặm dây",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Đã thấy dây điện bị gặm hở vỏ 1-2 chỗ",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Chuột gặm nhiều dây, đã từng chập điện do chuột",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Khoảng cách giữa các vật liệu dễ cháy (hàng hóa, giấy, vải...) với ổ cắm và bảng điện ra sao?",
        "options": [
            {
                "key": "A",
                "text": "Bảng điện và ổ cắm đều thông thoáng, cách vật dễ cháy trên 1 mét",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Đôi chỗ có đồ đạc gần ổ cắm nhưng không che khuất bảng điện",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Hàng hóa để khá gần bảng điện hoặc che khuất một phần ổ cắm",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Hàng hóa xếp sát kín xung quanh bảng điện, khó tiếp cận nhanh",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Thiết bị điện nung nóng (bếp, bàn ủi, lò sưởi, ấm nước) có đang đặt gần vật dễ cháy hoặc chạy không giám sát không?",
        "options": [
            {
                "key": "A",
                "text": "Luôn cách xa vật dễ cháy, rút phích khi không dùng",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Đôi khi quên rút phích nhưng thiết bị có tự ngắt",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Đặt gần rèm/vải, dùng chung ổ cắm với thiết bị khác",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Thiết bị cũ không tự ngắt, chạy liên tục không ai trông",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Điều hòa, tủ lạnh, tủ đông có tiếng kêu bất thường, rung mạnh hoặc mùi khét không?",
        "options": [
            {
                "key": "A",
                "text": "Hoạt động êm ái, không mùi, không rung lắc lạ",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Thỉnh thoảng kêu nhẹ khi khởi động, nhanh hết",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Rung lắc mạnh, kêu liên tục, dây điện nóng khi chạy",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Bốc mùi khét, motor cháy, vẫn cắm điện chạy",
                "score": 3,
                "risk": "critical"
            }
        ]
    }
]

GROUP2_QUESTIONS = [
    {
        "text": "Có đốt rác, lá khô, phế thải lộ thiên trong khuôn viên không?",
        "options": [
            {
                "key": "A",
                "text": "Không đốt rác lộ thiên",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có đốt trong thùng kim loại có nắp, có người trông",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Đốt lộ thiên gần hàng rào, cây khô, không trông liên tục",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đốt gần kho hàng hoặc nhà xưởng, kể cả khi gió lớn",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Bàn thờ, nến, đèn dầu, vàng mã có đặt gần vật dễ cháy (rèm, gỗ, giấy) không?",
        "options": [
            {
                "key": "A",
                "text": "Không dùng lửa thờ cúng, hoặc dùng nến LED thay thế",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Bàn thờ cách trần và vật dễ cháy >0.5m, có người trông",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Bàn thờ gỗ sát trần, tàn hương/nến rơi xuống đồ giấy/vải",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đốt vàng mã lộ thiên, nến cháy qua đêm không ai trông",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Có người hút thuốc trong nhà, trong kho hàng hoặc gần vật liệu dễ cháy không?",
        "options": [
            {
                "key": "A",
                "text": "Không ai hút thuốc trong khuôn viên",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Hút ngoài trời, xa vật dễ cháy, có gạt tàn",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Hút trong nhà, vứt tàn vào thùng rác thường",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Hút trong kho hàng hoặc gần nhiên liệu/hóa chất",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Bếp gas, bình gas có dấu hiệu bất thường (mùi gas, dây dẫn cũ nứt, van khó khóa) không?",
        "options": [
            {
                "key": "A",
                "text": "Bếp gas hoạt động tốt, dây mới, không mùi gas",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Dây dẫn hơi cũ nhưng chưa nứt, không mùi gas",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Thoáng có mùi gas khi mở bếp, dây cũ trên 3 năm, van hơi cứng",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Mùi gas rõ, dây nứt vá băng keo, bình gas đặt trong phòng kín",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Xăng dầu, cồn, dung môi dễ cháy có đang được để trong nhà/phòng ngủ/gần bếp không?",
        "options": [
            {
                "key": "A",
                "text": "Không lưu trữ chất dễ cháy, hoặc để tủ chuyên dụng",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Lượng nhỏ trong can kim loại có nắp, xa nguồn nhiệt",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Để trong kho chung gần thiết bị điện",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Để trong chai nhựa hở, trong phòng ngủ hoặc gần bếp",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Có hoạt động hàn cắt kim loại gần vật liệu dễ cháy không?",
        "options": [
            {
                "key": "A",
                "text": "Không có hàn cắt, hoặc hàn tại khu riêng cách xa vật dễ cháy",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Hàn tại khu riêng, có bình chữa cháy gần đó",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Hàn cắt ngay khu sản xuất, chưa dọn vật dễ cháy xung quanh",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Hàn cắt cạnh vật dễ cháy, tia lửa bắn tự do, không giám sát",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Có than hoa, lửa trại, nướng lộ thiên gần nhà hoặc kho hàng không?",
        "options": [
            {
                "key": "A",
                "text": "Không dùng lửa ngoài trời",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Nướng ngoài sân rộng, cách xa nhà, có nước dập sẵn",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nướng trên ban công hoặc gần mái hiên dễ cháy",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đốt lửa gần kho hàng, bãi xe, cỏ khô",
                "score": 2,
                "risk": "high"
            }
        ]
    }
]

GROUP3_QUESTIONS = [
    {
        "text": "Từ khu vực sinh hoạt hoặc làm việc chính, hiện có bao nhiêu lối có thể trực tiếp đi hoặc thoát ra ngoài an toàn (cửa chính, cửa phụ, ban công, lối thoát khẩn cấp)?",
        "options": [
            {
                "key": "A",
                "text": "Có từ 2 lối thoát độc lập trở lên, cửa luôn mở sẵn sàng",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có 2 lối thoát nhưng 1 lối phụ thường khép hoặc cần chìa khóa để ngay gần",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Chỉ có 1 lối thoát chính duy nhất, dọc lối đi có để một số xe cộ hoặc đồ đạc",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Chỉ có 1 lối thoát duy nhất và lối đi hẹp hoặc cửa thường xuyên khóa nhiều lớp",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Tại cơ sở hoặc gia đình của bạn, phương tiện chữa cháy tại chỗ (như bình chữa cháy xách tay) hiện được bố trí như thế nào?",
        "options": [
            {
                "key": "A",
                "text": "Có sẵn bình chữa cháy ở nơi dễ thấy dễ lấy, kim đồng hồ chỉ vạch xanh",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có bình chữa cháy nhưng đang để ở góc khuất hoặc lâu chưa kiểm tra kim áp",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Hiện dùng các phương tiện thay thế (vòi nước, xô cát, chăn dập lửa)",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Chưa trang bị bình chữa cháy hoặc bình đã quá cũ chưa bảo dưỡng",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Khi xảy ra sự cố mất điện vào ban đêm, phương án chiếu sáng chỉ dẫn lối ra tại cơ sở hiện như thế nào?",
        "options": [
            {
                "key": "A",
                "text": "Có hệ thống đèn EXIT và đèn sự cố tự sáng khi mất điện (hoặc công trình nhỏ không thuộc diện trang bị)",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có đèn chiếu sáng sự cố nhưng lâu rồi chưa kiểm tra pin lưu điện",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Dùng đèn pin hoặc một số đèn chỉ dẫn đã mờ, chưa thay thế",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Chưa có phương án chiếu sáng dự phòng khi mất điện ban đêm",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Đầu phun sprinkler (nếu có) có bị hàng hóa che khuất hoặc sơn phủ lên không?",
        "options": [
            {
                "key": "A",
                "text": "Không có sprinkler, hoặc có và đầu phun đều thông thoáng, không thuộc diện phải trang bị đầu phun sprinkler",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Hầu hết thông thoáng, 1-2 chỗ hàng xếp gần sát",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nhiều đầu phun bị kệ hàng che khuất hoặc bị sơn phủ",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đầu phun bị chôn vùi trong hàng hóa, không thể phun được",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Khi có tình huống khẩn cấp, mức độ nắm rõ phương hướng thoát hiểm của các thành viên hoặc nhân sự tại đây ra sao?",
        "options": [
            {
                "key": "A",
                "text": "Mọi người đều thuộc rõ đường thoát hiểm và có bảng sơ đồ chỉ dẫn rõ ràng",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Mọi người biết đường đi ra ngoài nhưng chưa có sơ đồ chỉ dẫn",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "C",
                "text": "Chỉ một số người quen thuộc địa hình, khách hoặc người mới khó định hình",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "D",
                "text": "Chưa từng hướng dẫn hay trao đổi về phương hướng thoát nạn khi có sự cố",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Khoảng cách giữa các lối đi lại và khả năng tiếp cận khu vực tủ điện, bảng điện hiện nay như thế nào?",
        "options": [
            {
                "key": "A",
                "text": "Lối đi rộng rãi thông thoáng, bảng điện luôn trống trải dễ thao tác ngay",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Lối đi đủ người qua lại, bảng điện vẫn với tay ngắt aptomat được",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Lối đi hơi hẹp do tận dụng để đồ, cần dịch chuyển đồ đạc mới tới được bảng điện",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Hàng hóa xếp sát kín xung quanh bảng điện, khó tiếp cận nhanh",
                "score": 3,
                "risk": "critical"
            }
        ]
    }
]

GROUP4_QUESTIONS = [
    {
        "text": "Vỏ máy, ổ bi, hộp số hoặc bộ phận chuyển động có nóng bất thường khi chạm vào không?",
        "options": [
            {
                "key": "A",
                "text": "Không nóng bất thường, nhiệt độ trong phạm vi bình thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Ấm hơn bình thường ở 1-2 vị trí, đã lưu ý theo dõi",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nóng rõ rệt khi chạm, có mùi dầu cháy nhẹ",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Nóng bỏng tay, có khói hoặc mùi khét từ ổ bi/hộp số",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Máy móc có phát ra tiếng kêu lạ (rít, gõ, lục cục) hoặc rung mạnh hơn bình thường không?",
        "options": [
            {
                "key": "A",
                "text": "Hoạt động êm ái, không tiếng lạ hay rung bất thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Tiếng kêu nhẹ khi khởi động, hết khi chạy ổn định",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Tiếng rít hoặc gõ liên tục, rung lắc mạnh hơn trước",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Va đập mạnh, rung dữ dội làm lỏng bu lông, chưa sửa",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Có vết dầu mỡ rò rỉ, nhỏ giọt xuống sàn hoặc bám trên vỏ máy không?",
        "options": [
            {
                "key": "A",
                "text": "Không rò rỉ, sàn sạch, máy khô ráo",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Rỉ nhẹ tại khớp nối, đã dùng khay hứng và lau dọn",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Dầu nhỏ giọt xuống sàn tạo vũng, sàn trơn, chưa xử lý",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Dầu loang rộng trên sàn gần nguồn nhiệt/thiết bị điện",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Dây đai truyền động, băng chuyền có bốc mùi khét hoặc nóng bất thường không?",
        "options": [
            {
                "key": "A",
                "text": "Không có dây đai/băng chuyền, hoặc hoạt động bình thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Thỉnh thoảng dây đai trượt phát sinh nhiệt nhẹ",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Dây đai cũ, kẹt gây nóng, bụi vải tích quanh bộ phận ma sát",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Mùi khét từ dây đai, bụi dễ cháy tích dày, nóng bất thường",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Ống dẫn thủy lực, khí nén có bị phồng rộp, rỉ dầu tại khớp nối không?",
        "options": [
            {
                "key": "A",
                "text": "Không có hoặc ống tốt, khớp nối chắc, không rò rỉ",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "1-2 khớp rỉ nhẹ đã siết lại",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Ống cũ mòn mỏng, khớp lỏng gây rò dầu áp lực",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Ống phồng rộp có nguy cơ vỡ, dầu phun ra khi vận hành",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Xe nâng hoặc phương tiện nội bộ có rò rỉ nhiên liệu, dầu nhớt trên sàn không?",
        "options": [
            {
                "key": "A",
                "text": "Không có vết dầu dưới xe, sàn sạch",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Vết dầu nhỏ tại chỗ đỗ, lau dọn thường xuyên",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Vết dầu loang dưới xe trong kho, chưa xác định nguồn",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Xe rò rỉ rõ ràng, vẫn đỗ trong kho hàng dễ cháy, mùi xăng",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Lò nung, lò sấy (nếu có) có dấu hiệu quá nhiệt: vỏ ngoài nóng rát, lớp cách nhiệt bong tróc?",
        "options": [
            {
                "key": "A",
                "text": "Không có lò nung/sấy, hoặc vỏ ngoài mát, cách nhiệt tốt",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Vỏ ấm nhẹ, cách nhiệt nguyên vẹn",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Vỏ nóng, cách nhiệt bong 1-2 chỗ, đặt gần vật dễ cháy",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Vỏ nóng bỏng, cách nhiệt hư hỏng nặng, sát vật dễ cháy",
                "score": 3,
                "risk": "critical"
            }
        ]
    }
]

GROUP5_QUESTIONS = [
    {
        "text": "Cơ sở có nằm gần rừng, đồng cỏ khô hoặc khu vực hay xảy ra cháy rừng không?",
        "options": [
            {
                "key": "A",
                "text": "Nằm trong khu đô thị, không gần rừng/đồng cỏ",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Gần đồi núi nhưng có khoảng cách an toàn và đường ngăn lửa",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "C",
                "text": "Gần bìa rừng/đồng cỏ, mùa khô có nguy cơ cháy lan",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "D",
                "text": "Giáp rừng, vùng cháy rừng thường xuyên, không có biện pháp ngăn",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Mái nhà, tường có bằng vật liệu dễ cháy (gỗ, lá, tôn nhựa, xốp) không?",
        "options": [
            {
                "key": "A",
                "text": "Xây bằng bê tông, gạch, tôn thép - khó cháy",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Phần lớn bê tông, có một số vách ngăn bằng gỗ/nhựa",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Mái tôn nhựa, vách gỗ, xốp cách nhiệt dễ cháy",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Toàn bộ bằng gỗ/lá/bạt, nằm vùng nắng nóng kéo dài",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Thiết bị điện ngoài trời có bị gỉ sét, vỡ vỏ bảo vệ hoặc nước mưa xâm nhập không?",
        "options": [
            {
                "key": "A",
                "text": "Vỏ nguyên vẹn chống nước, không gỉ sét",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Gỉ sét nhẹ bên ngoài, vỏ bảo vệ còn nguyên",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Vỏ tủ điện ngoài trời bị thủng, nắp hộp vỡ, cáp lộ lõi",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Nước mưa đã xâm nhập vào tủ điện, gây chập",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Bụi (xi măng, kim loại, than) có tích tụ dày trên thiết bị điện, tủ điện không?",
        "options": [
            {
                "key": "A",
                "text": "Thiết bị được vệ sinh định kỳ, không tích bụi",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Lớp bụi mỏng, vệ sinh mỗi tháng",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Bụi tích dày trên tủ điện, ổ cắm, đầu báo khói",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Bụi dẫn điện (kim loại/than) phủ dày trên thanh dẫn điện",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Tủ điện, ổ cắm có đặt ở vùng thấp dễ bị ngập nước khi mưa lớn không?",
        "options": [
            {
                "key": "A",
                "text": "Vùng cao không ngập, tủ điện đặt trên cao",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Thỉnh thoảng ngập nhẹ, ổ cắm tầng trệt chưa có nắp chống nước",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Hay ngập, tủ điện đặt thấp dưới 1m, dây đi sát sàn",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Tầng hầm có thiết bị điện, đã từng ngập gây chập điện",
                "score": 3,
                "risk": "critical"
            }
        ]
    }
]

GROUP6_QUESTIONS = [
    {
        "text": "Có đống rơm, trấu, than, gỗ vụn lớn nào đang bốc nóng, bốc hơi hoặc có mùi cháy không?",
        "options": [
            {
                "key": "A",
                "text": "Không có vật liệu tự cháy, hoặc đống nhỏ nơi thoáng mát",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có bảo quản nhưng đống nhỏ, kho thông gió, chưa nóng",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Đống lớn trong kho kín, thông gió kém, chưa kiểm tra nhiệt",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đống đã tự nóng, bốc khói hoặc có mùi cháy âm ỉ",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Giẻ lau dính dầu (dầu ăn, dầu máy) có đang chất đống hoặc vứt gần nguồn nhiệt không?",
        "options": [
            {
                "key": "A",
                "text": "Giẻ dính dầu được thu gom vào thùng kim loại có nắp",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có thu gom nhưng thùng hở nắp, chưa xử lý hàng ngày",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Giẻ dính dầu chất đống, thùng dầu hở trong kho nóng",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Giẻ dính dầu vứt bừa gần nguồn nhiệt, đã nóng hoặc bốc khói",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Bụi gỗ, bụi ngũ cốc, bụi kim loại có tích tụ dày trong không gian kín không?",
        "options": [
            {
                "key": "A",
                "text": "Không phát sinh bụi, hoặc có hệ thống hút bụi tốt",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có bụi nhưng vệ sinh hàng ngày, không tích dày",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Bụi tích dày trên máy, tường, trần, không hút bụi",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Bụi lơ lửng dày đặc tạo mây bụi, đã có cháy nhỏ do bụi",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Pin lithium (điện thoại, laptop, xe điện) có bị phồng, nóng hoặc sạc bằng sạc kém chất lượng không?",
        "options": [
            {
                "key": "A",
                "text": "Pin tốt, sạc chính hãng, không sạc qua đêm",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Sạc chính hãng, đôi khi sạc qua đêm nơi thoáng",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Pin một số thiết bị phồng, sạc không chính hãng, phòng kín",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Pin phồng vẫn dùng, sạc qua đêm trong phòng ngủ kín",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Hóa chất dễ cháy hoặc tự phản ứng có đang để lẫn với nhau hoặc gần nguồn nhiệt không?",
        "options": [
            {
                "key": "A",
                "text": "Không có hóa chất, hoặc tách riêng theo nhóm tương thích",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có tách nhóm nhưng chưa hoàn toàn, kho thông gió",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Hóa chất oxy hóa để chung vật dễ cháy, không kho riêng",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Hóa chất lượng lớn bảo quản kém, gần nguồn nhiệt",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Phân bón, phế phẩm hữu cơ có ủ đống lớn trong không gian kín, bốc nóng không?",
        "options": [
            {
                "key": "A",
                "text": "Không có đống ủ, hoặc ủ nhỏ ngoài trời có đảo trộn",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Ủ quy mô nhỏ ngoài trời, đảo trộn không thường xuyên",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Đống lớn trong khu kín, bốc mùi nóng, chưa xử lý",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đống ủ tự phát nhiệt, bốc khói hoặc âm ỉ cháy",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Xe máy, xe đạp điện có đang sạc trong phòng ngủ kín hoặc pin đã phồng không?",
        "options": [
            {
                "key": "A",
                "text": "Sạc ở khu riêng thông thoáng, pin còn tốt",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Sạc tầng trệt khu chung, pin bình thường",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Sạc trong phòng trọ/ngủ, gần đồ dùng cá nhân",
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

GROUP7_QUESTIONS = [
    {
        "text": "Xe ô tô, xe máy đỗ trong nhà có dấu hiệu rò rỉ xăng dầu (mùi xăng, vết dầu dưới xe) không?",
        "options": [
            {
                "key": "A",
                "text": "Xe không đỗ trong nhà, hoặc không rò rỉ, sàn sạch",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Đỗ trong nhà, kiểm tra thường, chưa phát hiện rò rỉ",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Có vết dầu loang dưới xe, chưa xác định nguồn",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Xe rò xăng rõ ràng, mùi xăng nồng, vẫn đỗ trong nhà",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Vào ban đêm hoặc giờ cao điểm, khu vực để xe máy/ô tô tại tầng 1 (hoặc sân trước) được sắp xếp như thế nào so với lối di chuyển ra cửa?",
        "options": [
            {
                "key": "A",
                "text": "Khu để xe tách biệt với lối đi hoặc cơ sở có từ 2 cửa ra vào độc lập",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Xe để gọn một bên, vẫn còn khoảng trống rộng trên 0.8m để đi lại dễ dàng",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Xe để khá chật, cần phải lách người qua các tay lái để đi ra cửa",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Xe xếp kín khu vực tầng 1 từ cửa ra vào tới cầu thang",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Can xăng, dầu nhớt dự trữ có đang để trong nhà gần ổ cắm điện không?",
        "options": [
            {
                "key": "A",
                "text": "Không dự trữ xăng dầu, hoặc để khu riêng xa nhà",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Để riêng ngoài trời, thùng có nắp kín, xa nguồn nhiệt",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Để trong nhà gần thiết bị điện",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Can nhựa hở, trong garage chung nhiều xe, gần ổ cắm",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Hệ thống điện xe (dây điện, ắc-quy) có dấu hiệu chạm chập: khói, mùi khét, tia lửa?",
        "options": [
            {
                "key": "A",
                "text": "Hệ thống điện xe hoạt động bình thường",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Xe cũ, chưa kiểm tra điện gần đây nhưng chưa có dấu hiệu lạ",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Dây điện xe một số chỗ nối tạm, cầu chì thay bằng dây đồng",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đã có hiện tượng khói/tia lửa từ khoang động cơ, vẫn chạy",
                "score": 3,
                "risk": "critical"
            }
        ]
    }
]

GROUP8_QUESTIONS = [
    {
        "text": "Cơ sở lân cận (nhà hàng xóm, xưởng bên cạnh) có hoạt động dễ gây cháy lan không?",
        "options": [
            {
                "key": "A",
                "text": "Có tường ngăn, hàng xóm hoạt động ít nguy cơ",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Liền kề nhưng hàng xóm ít nguy cơ (văn phòng, trường)",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Liền kề xưởng gỗ/kho hàng, không tường ngăn cháy",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Sát cơ sở kinh doanh xăng dầu/gas, mái nhà thông nhau",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Rác thải, phế liệu dễ cháy có đang tích tụ thành đống lớn gần nguồn nhiệt/điện không?",
        "options": [
            {
                "key": "A",
                "text": "Thu gom rác hàng ngày, khu rác sạch, thùng có nắp",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Thu gom 2-3 ngày/lần, đôi khi đầy tràn",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Phế liệu tích đống trong góc xưởng, nhiều ngày chưa xử lý",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Phế liệu dễ cháy chất đống gần nguồn nhiệt/điện, lâu ngày",
                "score": 3,
                "risk": "critical"
            }
        ]
    },
    {
        "text": "Khuôn viên có camera, hàng rào, khóa cổng để ngăn người lạ xâm nhập không?",
        "options": [
            {
                "key": "A",
                "text": "Có camera 24/7, hàng rào kín, bảo vệ trực",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Có camera và khóa cổng nhưng không bảo vệ ngoài giờ",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "C",
                "text": "Không camera, cổng lỏng, người lạ dễ vào",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "D",
                "text": "Khuôn viên mở, đã có dấu hiệu bị phá hoại",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Trong dịp lễ, sự kiện, có lắp nhiều đèn trang trí gây nóng dây điện, quá tải không?",
        "options": [
            {
                "key": "A",
                "text": "Dùng đèn LED ít, CB riêng cho đèn trang trí",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Dùng đèn LED, cắm ổ cắm hiện có, chưa tính tải",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "C",
                "text": "Nhiều đèn sợi đốt, nối chồng ổ cắm kéo dài",
                "score": 2,
                "risk": "high"
            },
            {
                "key": "D",
                "text": "Đèn khắp nơi gần rèm/vải, nối chéo, CB nhảy phải nối tắt",
                "score": 2,
                "risk": "high"
            }
        ]
    },
    {
        "text": "Mọi người trong gia đình hoặc nhân sự tại cơ sở đã từng thao tác bình chữa cháy hoặc tham gia buổi hướng dẫn PCCC nào chưa?",
        "options": [
            {
                "key": "A",
                "text": "Đã từng thực hành sử dụng bình chữa cháy và nắm rõ cách gọi 114",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "B",
                "text": "Nhớ số khẩn cấp 114 nhưng chưa trực tiếp cầm bình xịt thao tác lần nào",
                "score": 0,
                "risk": "safe"
            },
            {
                "key": "C",
                "text": "Mới chỉ xem hướng dẫn qua truyền hình, mạng xã hội hoặc tờ rơi",
                "score": 1,
                "risk": "low"
            },
            {
                "key": "D",
                "text": "Chưa có dịp tiếp cận hay tham gia hướng dẫn kỹ năng PCCC thực tế",
                "score": 2,
                "risk": "high"
            }
        ]
    }
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
