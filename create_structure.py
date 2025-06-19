import os

def create_project_structure():
    """프로젝트 디렉토리 구조를 생성합니다."""
    
    # 기본 디렉토리들
    directories = [
        'src',
        'data',
        'logs', 
        'credentials',
        'tests',
        'data/downloads',
        'data/processed',
        'data/reports',
        'src/web_automation',
        'src/google_drive',
        'src/data_processing',
        'src/email_system',
        'src/utils'
    ]
    
    # 디렉토리 생성
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"생성됨: {directory}")
    
    # __init__.py 파일들 생성
    init_files = [
        'src/__init__.py',
        'src/web_automation/__init__.py',
        'src/google_drive/__init__.py',
        'src/data_processing/__init__.py',
        'src/email_system/__init__.py',
        'src/utils/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write('# Auto-generated __init__.py\n')
        print(f"생성됨: {init_file}")

if __name__ == "__main__":
    create_project_structure()
    print("\n프로젝트 구조 생성 완료!") 