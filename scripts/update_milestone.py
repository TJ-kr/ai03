#!/usr/bin/env python3
"""
마일스톤 업데이트 스크립트
"""

import re
import sys
from datetime import datetime
from pathlib import Path

def update_milestone(milestone_number, status="완료", completion_rate=100, notes=""):
    """마일스톤 상태 업데이트"""
    
    milestone_file = Path("MILESTONES.md")
    
    if not milestone_file.exists():
        print("❌ MILESTONES.md 파일을 찾을 수 없습니다.")
        return False
    
    # 파일 읽기
    with open(milestone_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 진행 상황 추적 테이블 찾기
    table_pattern = r'(\| 마일스톤 \| 상태 \| 완료율 \| 완료일 \| 비고 \|\n\|-+\|-+\|-+\|-+\|-+\|\n)(.*?)(\n\n---)'
    table_match = re.search(table_pattern, content, re.DOTALL)
    
    if not table_match:
        print("❌ 진행 상황 테이블을 찾을 수 없습니다.")
        return False
    
    table_header = table_match.group(1)
    table_body = table_match.group(2)
    table_footer = table_match.group(3)
    
    # 테이블 행들을 분리
    rows = table_body.strip().split('\n')
    
    # 마일스톤 번호에 해당하는 행 찾기 및 업데이트
    updated_rows = []
    found = False
    
    for row in rows:
        if row.strip() and '|' in row:
            # 마일스톤 번호 확인
            if f"{milestone_number}." in row:
                found = True
                # 상태 업데이트
                if status == "완료":
                    status_icon = "✅"
                    completion_date = datetime.now().strftime("%Y-%m-%d")
                elif status == "진행중":
                    status_icon = "🔄"
                    completion_date = "-"
                else:
                    status_icon = "⏳"
                    completion_date = "-"
                
                # 행 업데이트
                parts = row.split('|')
                if len(parts) >= 5:
                    parts[1] = f" {status_icon} {status}"
                    parts[2] = f" {completion_rate}%"
                    parts[3] = f" {completion_date}"
                    parts[4] = f" {notes}"
                    updated_row = '|'.join(parts)
                    updated_rows.append(updated_row)
                else:
                    updated_rows.append(row)
            else:
                updated_rows.append(row)
    
    if not found:
        print(f"❌ 마일스톤 {milestone_number}을 찾을 수 없습니다.")
        return False
    
    # 업데이트된 테이블 생성
    updated_table = table_header + '\n'.join(updated_rows) + table_footer
    
    # 파일 내용 업데이트
    updated_content = re.sub(table_pattern, r'\1' + '\n'.join(updated_rows) + r'\3', content, flags=re.DOTALL)
    
    # 업데이트 기록 추가
    update_record = f"- **{datetime.now().strftime('%Y-%m-%d')}**: 마일스톤 {milestone_number} {status} - {notes}"
    
    # 업데이트 기록 섹션 찾기
    record_pattern = r'(## 📝 업데이트 기록\n\n)(.*?)(\n\n---)'
    record_match = re.search(record_pattern, updated_content, re.DOTALL)
    
    if record_match:
        record_header = record_match.group(1)
        record_body = record_match.group(2)
        record_footer = record_match.group(3)
        
        # 새로운 기록 추가
        updated_record_body = update_record + '\n' + record_body
        updated_content = re.sub(record_pattern, r'\1' + updated_record_body + r'\3', updated_content, flags=re.DOTALL)
    
    # 파일 저장
    with open(milestone_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ 마일스톤 {milestone_number} 업데이트 완료: {status}")
    return True

def show_milestones():
    """현재 마일스톤 상태 표시"""
    milestone_file = Path("MILESTONES.md")
    
    if not milestone_file.exists():
        print("❌ MILESTONES.md 파일을 찾을 수 없습니다.")
        return
    
    with open(milestone_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 진행 상황 테이블 찾기
    table_pattern = r'(\| 마일스톤 \| 상태 \| 완료율 \| 완료일 \| 비고 \|\n\|-+\|-+\|-+\|-+\|-+\|\n)(.*?)(\n\n---)'
    table_match = re.search(table_pattern, content, re.DOTALL)
    
    if table_match:
        table_body = table_match.group(2)
        print("📊 현재 마일스톤 상태:")
        print("=" * 80)
        print("| 마일스톤 | 상태 | 완료율 | 완료일 | 비고 |")
        print("|---------|------|--------|--------|------|")
        for row in table_body.strip().split('\n'):
            if row.strip() and '|' in row:
                print(row.strip())

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python scripts/update_milestone.py show                    # 현재 상태 표시")
        print("  python scripts/update_milestone.py update <번호> <상태>    # 마일스톤 업데이트")
        print("  python scripts/update_milestone.py update 2 완료 100 '웹사이트 자동화 완성'")
        return
    
    command = sys.argv[1]
    
    if command == "show":
        show_milestones()
    elif command == "update":
        if len(sys.argv) < 4:
            print("❌ 업데이트 명령어에 필요한 인수가 부족합니다.")
            print("사용법: python scripts/update_milestone.py update <번호> <상태> [완료율] [비고]")
            return
        
        milestone_number = sys.argv[2]
        status = sys.argv[3]
        completion_rate = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        notes = sys.argv[5] if len(sys.argv) > 5 else ""
        
        update_milestone(milestone_number, status, completion_rate, notes)
    else:
        print(f"❌ 알 수 없는 명령어: {command}")

if __name__ == "__main__":
    main() 