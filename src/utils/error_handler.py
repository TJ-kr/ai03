import time
import functools
from ..utils.logger import get_logger

logger = get_logger()

def retry_on_error(max_retries=3, delay=1):
    """에러 발생 시 재시도하는 데코레이터"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"시도 {attempt + 1}/{max_retries} 실패: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        logger.error(f"최대 재시도 횟수 초과: {func.__name__}")
                        raise
            return None
        return wrapper
    return decorator

def safe_action(action_name="작업"):
    """안전한 작업 실행을 위한 데코레이터"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"{action_name} 시작")
                result = func(*args, **kwargs)
                logger.info(f"{action_name} 완료")
                return result
            except Exception as e:
                logger.error(f"{action_name} 실패: {e}")
                return None
        return wrapper
    return decorator

def handle_webdriver_error(func):
    """웹드라이버 관련 에러를 처리하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"웹드라이버 에러: {e}")
            # 웹드라이버 정리
            if 'driver' in kwargs and kwargs['driver']:
                try:
                    kwargs['driver'].quit()
                except:
                    pass
            return None
    return wrapper 