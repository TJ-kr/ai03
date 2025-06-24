#!/usr/bin/env python3
"""
프로젝트 진행 상황 대시보드
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def get_project_stats():
    """프로젝트 통계 정보 수집"""
    stats = {
        'total_files': 0,
        'python_files': 0,
        'config_files': 0,
        'docs_files': 0,
        'total_lines': 0,
        'python_lines': 0
    }
    
    # 프로젝트 루트 디렉토리
    project_root = Path(".")
    
    for file_path in project_root.rglob("*"):
        if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
            stats['total_files'] += 1
            
            # 파일 확장자별 분류
            if file_path.suffix == '.py':
                stats['python_files'] += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        stats['python_lines'] += lines
                        stats['total_lines'] += lines
                except:
                    pass
            elif file_path.suffix in ['.md', '.txt', '.rst']:
                stats['docs_files'] += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        stats['total_lines'] += len(f.readlines())
                except:
                    pass
            elif file_path.suffix in ['.json', '.yaml', '.yml', '.ini', '.cfg']:
                stats['config_files'] += 1
    
    return stats

def get_milestone_progress():
    """마일스톤 진행 상황 파악"""
    milestone_file = Path("MILESTONES.md")
    
    if not milestone_file.exists():
        return None
    
    with open(milestone_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 진행 상황 테이블에서 완료율 추출
    import re
    table_pattern = r'(\| 마일스톤 \| 상태 \| 완료율 \| 완료일 \| 비고 \|\n\|-+\|-+\|-+\|-+\|-+\|\n)(.*?)(\n\n---)'
    table_match = re.search(table_pattern, content, re.DOTALL)
    
    if not table_match:
        return None
    
    table_body = table_match.group(2)
    milestones = []
    
    for row in table_body.strip().split('\n'):
        if row.strip() and '|' in row:
            parts = [part.strip() for part in row.split('|')]
            if len(parts) >= 5:
                milestone_name = parts[0]
                status = parts[1]
                completion_rate = parts[2].replace('%', '')
                completion_date = parts[3]
                notes = parts[4]
                
                try:
                    completion_rate = int(completion_rate)
                except:
                    completion_rate = 0
                
                milestones.append({
                    'name': milestone_name,
                    'status': status,
                    'completion_rate': completion_rate,
                    'completion_date': completion_date,
                    'notes': notes
                })
    
    return milestones

def display_dashboard():
    """대시보드 표시"""
    print("=" * 80)
    print("🎯 자판기 매출 관리 시스템 - 프로젝트 대시보드")
    print("=" * 80)
    print(f"📅 생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 프로젝트 통계
    stats = get_project_stats()
    print("📊 프로젝트 통계:")
    print(f"   📁 총 파일 수: {stats['total_files']}개")
    print(f"   🐍 Python 파일: {stats['python_files']}개")
    print(f"   ⚙️  설정 파일: {stats['config_files']}개")
    print(f"   📚 문서 파일: {stats['docs_files']}개")
    print(f"   📝 총 코드 라인: {stats['total_lines']:,}줄")
    print(f"   🐍 Python 코드 라인: {stats['python_lines']:,}줄")
    print()
    
    # 마일스톤 진행 상황
    milestones = get_milestone_progress()
    if milestones:
        print("🎯 마일스톤 진행 상황:")
        total_completion = 0
        
        for milestone in milestones:
            status_icon = "✅" if "완료" in milestone['status'] else "🔄" if "진행중" in milestone['status'] else "⏳"
            completion_bar = "█" * (milestone['completion_rate'] // 10) + "░" * (10 - milestone['completion_rate'] // 10)
            
            print(f"   {status_icon} {milestone['name']}")
            print(f"      진행률: {milestone['completion_rate']}% [{completion_bar}]")
            if milestone['completion_date'] != '-':
                print(f"      완료일: {milestone['completion_date']}")
            if milestone['notes']:
                print(f"      비고: {milestone['notes']}")
            print()
            
            total_completion += milestone['completion_rate']
        
        overall_completion = total_completion / len(milestones)
        overall_bar = "█" * int(overall_completion // 10) + "░" * (10 - int(overall_completion // 10))
        print(f"📈 전체 진행률: {overall_completion:.1f}% [{overall_bar}]")
        print()
    
    # 다음 단계 안내
    print("🚀 다음 단계:")
    if milestones:
        incomplete_milestones = [m for m in milestones if m['completion_rate'] < 100]
        if incomplete_milestones:
            next_milestone = incomplete_milestones[0]
            print(f"   다음 마일스톤: {next_milestone['name']}")
            print(f"   현재 진행률: {next_milestone['completion_rate']}%")
            print(f"   목표: 100% 완료")
        else:
            print("   🎉 모든 마일스톤이 완료되었습니다!")
    print()
    
    # 빠른 명령어 안내
    print("⚡ 빠른 명령어:")
    print("   python scripts/update_milestone.py show                    # 마일스톤 상태 확인")
    print("   python scripts/update_milestone.py update 2 완료 100 '설명'  # 마일스톤 업데이트")
    print("   python src/main.py --test                                  # 연결 테스트")
    print("   python src/main.py                                         # 즉시 실행")
    print("   python src/main.py --schedule                              # 스케줄러 모드")
    print()

def check_project_health():
    """프로젝트 상태 점검"""
    print("🔍 프로젝트 상태 점검:")
    
    # 필수 파일 확인
    required_files = [
        "src/main.py",
        "src/config/settings.py",
        "requirements.txt",
        "README.md",
        "MILESTONES.md",
        ".gitignore"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("   ❌ 누락된 파일:")
        for file_path in missing_files:
            print(f"      - {file_path}")
    else:
        print("   ✅ 모든 필수 파일이 존재합니다.")
    
    # 환경변수 파일 확인
    if not Path(".env").exists():
        print("   ⚠️  .env 파일이 없습니다. env.example을 복사하여 설정하세요.")
    else:
        print("   ✅ .env 파일이 존재합니다.")
    
    # credentials.json 확인
    if not Path("credentials.json").exists():
        print("   ⚠️  credentials.json 파일이 없습니다. Google API 설정이 필요합니다.")
    else:
        print("   ✅ credentials.json 파일이 존재합니다.")
    
    print()

def main():
    """메인 함수"""
    if len(sys.argv) > 1 and sys.argv[1] == "--health":
        check_project_health()
    else:
        display_dashboard()
        check_project_health()

if __name__ == "__main__":
    main() 