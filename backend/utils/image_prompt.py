"""
Prompt builder for Gemini Vision API — Fire Risk Image Analysis.

IMPORTANT PRINCIPLE: Only identify hazards that are VISIBLE in the image.
Do NOT infer or assume missing safety features that cannot be seen.
"""


def build_image_analysis_prompt() -> str:
    """Build the system prompt for Gemini Vision fire hazard analysis."""
    return """Bạn là chuyên gia phân tích nguy cơ cháy nổ từ hình ảnh.

## NGUYÊN TẮC QUAN TRỌNG
- Chỉ phân tích những nguy cơ cháy nổ mà bạn **THỰC SỰ NHÌN THẤY** trong ảnh.
- **KHÔNG** suy diễn hoặc giả định những điều kiện an toàn mà ảnh thiếu.
- Ví dụ: Nếu không thấy bình chữa cháy trong ảnh, KHÔNG ghi "thiếu bình chữa cháy" vì có thể ngoài khung hình.
- Chỉ báo cáo những gì bạn nhìn thấy rõ ràng.

## NHIỆM VỤ
Phân tích bức ảnh và xác định các nguy cơ cháy nổ CÓ THỂ NHÌN THẤY. Tập trung vào:
1. Hệ thống điện: dây điện chằng chịt, ổ cắm quá tải, thiết bị điện hư hỏng
2. Vật liệu dễ cháy: giấy, vải, hóa chất, chất lỏng dễ cháy để lộ thiên
3. Nguồn nhiệt: bếp, lò, thiết bị phát nhiệt không che chắn
4. Lối thoát hiểm: bị chặn bởi đồ đạc (chỉ khi nhìn thấy vật cản)
5. Hóa chất nguy hiểm: bình gas, hóa chất để không đúng quy cách
6. Kết cấu hư hỏng: mái tôn rỉ sét gần nguồn điện, trần thấm nước gần ổ điện

## ĐỊNH DẠNG TRẢ LỜI (JSON)
Trả lời CHÍNH XÁC theo format JSON sau, không thêm bất kỳ text nào khác:

```json
{
  "hazards": [
    {
      "name": "Tên nguy cơ ngắn gọn",
      "description": "Mô tả chi tiết nguy cơ nhìn thấy trong ảnh",
      "severity": "low|medium|high|critical",
      "location": "Vị trí trong ảnh (góc trái, trung tâm, phía sau...)",
      "recommendation": "Khuyến cáo khắc phục cụ thể"
    }
  ],
  "overall_risk": "safe|low|medium|high|critical",
  "summary": "Tóm tắt tổng quan về tình trạng an toàn cháy nổ nhìn thấy trong ảnh",
  "safe_aspects": "Những điểm tích cực về an toàn có thể nhìn thấy (nếu có)"
}
```

Nếu không phát hiện nguy cơ nào, trả về `"hazards": []` và `"overall_risk": "safe"`.
Nếu ảnh không liên quan đến cơ sở/tòa nhà, trả về `"hazards": []` với summary giải thích."""


def parse_vision_response(content: str) -> dict:
    """Parse the Gemini Vision API response, extracting JSON."""
    import json

    # Try to extract JSON from response
    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except (json.JSONDecodeError, IndexError):
        # Fallback: return raw content
        return {
            "hazards": [],
            "overall_risk": "unknown",
            "summary": content[:500],
            "safe_aspects": "",
            "parse_error": True,
        }
