#!/usr/bin/env python3
"""
Google Cloud Scheduler 설정 스크립트
매일 정기적으로 Cloud Function을 트리거하도록 설정
"""

import os
import json
from google.cloud import scheduler_v1
from google.cloud.scheduler_v1 import Job
from google.protobuf import timestamp_pb2
import datetime

def create_cloud_scheduler_job():
    """Cloud Scheduler 작업 생성"""
    
    # 클라이언트 생성
    client = scheduler_v1.CloudSchedulerClient()
    
    # 프로젝트 및 위치 설정
    project_id = "your-project-id"  # 실제 프로젝트 ID로 변경
    location_id = "asia-northeast3"  # 서울 리전
    parent = f"projects/{project_id}/locations/{location_id}"
    
    # 작업 이름
    job_id = "toygo-data-collector"
    job_path = f"{parent}/jobs/{job_id}"
    
    # HTTP 타겟 설정
    target = scheduler_v1.HttpTarget()
    target.uri = f"https://{location_id}-{project_id}.cloudfunctions.net/collect-data"
    target.http_method = scheduler_v1.HttpMethod.POST
    target.headers = {
        "Content-Type": "application/json"
    }
    
    # 스케줄 설정 (매일 오전 9시)
    schedule = "0 9 * * *"  # Cron 표현식
    
    # 작업 생성
    job = Job(
        name=job_path,
        http_target=target,
        schedule=schedule,
        time_zone="Asia/Seoul"
    )
    
    try:
        # 기존 작업 삭제 (있다면)
        try:
            client.delete_job(name=job_path)
            print(f"기존 작업 삭제: {job_id}")
        except:
            pass
        
        # 새 작업 생성
        result = client.create_job(
            request={
                "parent": parent,
                "job": job
            }
        )
        
        print(f"✅ Cloud Scheduler 작업 생성 완료!")
        print(f"📅 작업 이름: {result.name}")
        print(f"⏰ 실행 시간: 매일 오전 9시 (한국 시간)")
        print(f"🌐 타겟 URL: {target.uri}")
        
        return result
        
    except Exception as e:
        print(f"❌ Cloud Scheduler 작업 생성 실패: {str(e)}")
        return None

def list_scheduler_jobs():
    """등록된 스케줄러 작업 목록 조회"""
    client = scheduler_v1.CloudSchedulerClient()
    project_id = "your-project-id"  # 실제 프로젝트 ID로 변경
    location_id = "asia-northeast3"
    parent = f"projects/{project_id}/locations/{location_id}"
    
    try:
        request = scheduler_v1.ListJobsRequest(parent=parent)
        page_result = client.list_jobs(request=request)
        
        print("📋 등록된 Cloud Scheduler 작업:")
        for job in page_result:
            print(f"  - {job.name}")
            print(f"    스케줄: {job.schedule}")
            print(f"    상태: {job.state}")
            print()
            
    except Exception as e:
        print(f"❌ 작업 목록 조회 실패: {str(e)}")

def delete_scheduler_job(job_name="toygo-data-collector"):
    """스케줄러 작업 삭제"""
    client = scheduler_v1.CloudSchedulerClient()
    project_id = "your-project-id"  # 실제 프로젝트 ID로 변경
    location_id = "asia-northeast3"
    job_path = f"projects/{project_id}/locations/{location_id}/jobs/{job_name}"
    
    try:
        client.delete_job(name=job_path)
        print(f"✅ 작업 삭제 완료: {job_name}")
    except Exception as e:
        print(f"❌ 작업 삭제 실패: {str(e)}")

def main():
    """메인 함수"""
    print("☁️ Google Cloud Scheduler 설정")
    print("=" * 50)
    
    while True:
        print("\n📋 선택하세요:")
        print("1. 스케줄러 작업 생성")
        print("2. 작업 목록 조회")
        print("3. 작업 삭제")
        print("4. 종료")
        
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == "1":
            create_cloud_scheduler_job()
        elif choice == "2":
            list_scheduler_jobs()
        elif choice == "3":
            job_name = input("삭제할 작업 이름 (기본: toygo-data-collector): ").strip()
            if not job_name:
                job_name = "toygo-data-collector"
            delete_scheduler_job(job_name)
        elif choice == "4":
            print("종료합니다.")
            break
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main() 