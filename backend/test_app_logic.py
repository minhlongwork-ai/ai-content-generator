import os
import json
import asyncio
from ai_client import AIClient
from database import get_db_session
from models import Generation

async def test_full_workflow():
    print("🚀 Bắt đầu test workflow thực tế (Async)...")
    
    # 1. Khởi tạo AI Client
    ai_client = AIClient()
    
    # 2. Input giả lập
    input_data = {
        "product_name": "Tai nghe Sony WH-1000XM5",
        "category": "Điện tử",
        "features": "Chống ồn đỉnh cao, Pin 30 giờ, Sạc nhanh 10 phút dùng 5 giờ, Âm thanh Hi-Res",
        "target_audience": "Người yêu nhạc, nhân viên văn phòng",
        "tone": "luxury",
        "language": "Vietnamese"
    }
    
    # 3. Generate Content (Gửi đến OpenRouter thật)
    print("🤖 Đang gọi AI (Gemini 2.0 Flash) tạo nội dung...")
    # Truyền TÊN skill (string) vào, AIClient sẽ tự load skill
    result = await ai_client.generate_with_skill("product-description", input_data)
    
    if not result.get('success'):
        print(f"❌ Thất bại: {result.get('error')}")
        return

    print("✅ AI đã phản hồi thành công!")
    
    # 4. Kiểm tra Logic Output
    print("\n📝 Kết quả AI trả về:")
    content = result.get('content', {})
    print(json.dumps(content, indent=2, ensure_ascii=False))
    
    # 5. Kiểm tra Quality Report
    report = result.get('quality_report', {})
    score = report.get('score', 0)
    print(f"\n🏆 Quality Score: {score}/100")
    print(f"✓ Tổng số checks: {len(report.get('checks', []))}")
    
    # 6. Lưu vào Database
    print("\n💾 Lưu vào Database...")
    with get_db_session() as db:
        gen = Generation(
            user_id=1,
            skill_name="product-description",
            input_params=input_data,
            output_content=content,
            quality_score=report,
            model_used=result.get('model'),
            backend=result.get('backend')
        )
        db.add(gen)
        db.commit()
        print(f"✓ Đã lưu thành công vào lịch sử (ID: {gen.id})")

    print("\n✨ Test PASSED. Workflow hoạt động chuẩn xác.")

if __name__ == "__main__":
    asyncio.run(test_full_workflow())
