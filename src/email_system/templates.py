from datetime import datetime

def create_sales_report_email(report_data):
    """매출 보고서 이메일 HTML 템플릿을 생성합니다."""
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
            .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; }}
            .highlight {{ background-color: #e7f3ff; padding: 10px; border-radius: 3px; }}
            .summary {{ background-color: #d4edda; padding: 15px; border-radius: 5px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 자판기 매출 보고서</h1>
            <p>생성일시: {report_data['report_date']}</p>
        </div>
        
        <div class="section">
            <h2>📈 일일 매출 요약</h2>
            <div class="highlight">
                <p><strong>기간:</strong> {report_data['daily_summary']['period']}</p>
                <p><strong>매출액:</strong> {report_data['daily_summary']['sales_amount']:,}원</p>
                <p><strong>판매 상품 수:</strong> {report_data['daily_summary']['product_count']}개</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📦 재고 현황</h2>
            <div class="highlight">
                <p><strong>재고 상태:</strong> {report_data['total_summary']['inventory_status']}</p>
                <!-- 재고 상세 정보는 실제 데이터에 따라 추가 -->
            </div>
        </div>
        
        <div class="section">
            <h2>📅 월 누적 매출</h2>
            <div class="highlight">
                <p><strong>월:</strong> {report_data['monthly_summary']['month']}월</p>
                <p><strong>누적 매출:</strong> {report_data['monthly_summary']['total_sales']:,}원</p>
                <p><strong>일평균 매출:</strong> {report_data['monthly_summary']['daily_average']:,}원</p>
            </div>
        </div>
        
        <div class="summary">
            <h2>💰 총계</h2>
            <table>
                <tr>
                    <th>구분</th>
                    <th>금액</th>
                </tr>
                <tr>
                    <td>일일 매출</td>
                    <td>{report_data['total_summary']['total_daily_sales']:,}원</td>
                </tr>
                <tr>
                    <td>월 누적 매출</td>
                    <td>{report_data['total_summary']['total_monthly_sales']:,}원</td>
                </tr>
            </table>
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
            <p><em>이 보고서는 자동으로 생성되었습니다.</em></p>
            <p><em>문의사항이 있으시면 관리자에게 연락해주세요.</em></p>
        </div>
    </body>
    </html>
    """
    
    return html_template

def create_simple_text_email(report_data):
    """간단한 텍스트 이메일을 생성합니다."""
    
    text_template = f"""
자판기 매출 보고서
생성일시: {report_data['report_date']}

=== 일일 매출 요약 ===
기간: {report_data['daily_summary']['period']}
매출액: {report_data['daily_summary']['sales_amount']:,}원
판매 상품 수: {report_data['daily_summary']['product_count']}개

=== 재고 현황 ===
재고 상태: {report_data['total_summary']['inventory_status']}

=== 월 누적 매출 ===
월: {report_data['monthly_summary']['month']}월
누적 매출: {report_data['monthly_summary']['total_sales']:,}원
일평균 매출: {report_data['monthly_summary']['daily_average']:,}원

=== 총계 ===
일일 매출: {report_data['total_summary']['total_daily_sales']:,}원
월 누적 매출: {report_data['total_summary']['total_monthly_sales']:,}원

---
이 보고서는 자동으로 생성되었습니다.
    """
    
    return text_template 