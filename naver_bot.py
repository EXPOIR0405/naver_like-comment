from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

class NaverBlogBot:
    def __init__(self):
        # Chrome 옵션 설정
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않고 실행하려면 이 줄의 주석을 제거
        
        # WebDriver 설정
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)  # 암묵적 대기 시간 설정 
        
        # 우클릭 방지 해제를 위한 JavaScript 실행
        self.driver.execute_script("""
            // 우클릭 방지 해제
            document.addEventListener('contextmenu', function(e) {
                e.stopPropagation();
                return true;
            }, true);
            
            // 복사 방지 해제
            document.addEventListener('copy', function(e) {
                e.stopPropagation();
                return true;
            }, true);
            
            // 드래그 방지 해제
            document.addEventListener('selectstart', function(e) {
                e.stopPropagation();
                return true;
            }, true);
            
            // 개발자 도구 방지 해제
            Object.defineProperty(window, 'console', {
                value: console,
                writable: false,
                configurable: false
            });
        """)
        
        # 처리된 게시물 기록 파일 경로
        self.history_file = 'processed_posts.json'
        self.processed_posts = self.load_processed_posts()
    
    def load_processed_posts(self):
        """처리된 게시물 기록 불러오기"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_processed_post(self, url, action_type="both"):
        """처리된 게시물 저장"""
        self.processed_posts[url] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action_type  # "like", "comment", "both"
        }
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.processed_posts, f, ensure_ascii=False, indent=2)
    
    def is_already_processed(self, url, action_type="both"):
        """이미 처리된 게시물인지 확인"""
        return url in self.processed_posts and self.processed_posts[url]["action"] == action_type
    
    def get_blogger_posts(self, blogger_id, num_posts=5):
        """특정 블로거의 최근 게시물 URL 가져오기"""
        try:
            # 블로그 메인 페이지로 이동
            blog_url = f"https://blog.naver.com/{blogger_id}"
            self.driver.get(blog_url)
            time.sleep(3)
            
            # iframe 전환
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "mainFrame"))
            )
            self.driver.switch_to.frame(iframe)
            
            print("게시물 찾는 중...")
            
            # 새로운 선택자들 시도
            possible_selectors = [
                ".blog2_series .series_item a",           # 시리즈 글
                ".blog2_post .item a",                    # 일반 글 (새 레이아웃)
                "#postListBody .blog2_post a",            # 일반 글 (다른 형태)
                ".post_title > a",                        # 제목 직접 링크
                "#titleId_0",                            # 특정 글 ID
                ".list_content a"                         # 리스트 형태
            ]
            
            post_urls = []
            for selector in possible_selectors:
                try:
                    print(f"선택자 '{selector}' 시도 중...")
                    elements = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )
                    
                    for element in elements:
                        try:
                            # 요소가 보이는 위치로 스크롤
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.5)
                            
                            # href 속성 확인
                            url = element.get_attribute('href')
                            if url:
                                # 상대 URL을 절대 URL로 변환
                                if not url.startswith('http'):
                                    url = f"https://blog.naver.com/{blogger_id}/{url.split('/')[-1]}"
                                if 'blog.naver.com' in url:
                                    post_urls.append(url)
                                    print(f"Found URL: {url}")
                        except Exception as e:
                            print(f"개별 요소 처리 중 오류: {str(e)}")
                            continue
                    
                    if post_urls:
                        break
                        
                except Exception as e:
                    print(f"선택자 '{selector}' 실패: {str(e)}")
                    continue
            
            # 중복 제거 및 개수 제한
            post_urls = list(dict.fromkeys(post_urls))[:num_posts]
            
            print(f"총 {len(post_urls)}개의 게시물을 찾았습니다.")
            for url in post_urls:
                print(f"- {url}")
            
            return post_urls
            
        except Exception as e:
            print(f"블로그 접근 실패: {str(e)}")
            return []
        
        finally:
            try:
                self.driver.switch_to.default_content()
            except:
                pass
    
    def login(self, id, password):
        """네이버 자동 로그인"""
        try:
            print("로그인 시도 중...")
            self.driver.get("https://nid.naver.com/nidlogin.login")
            time.sleep(1)
            
            # JavaScript를 이용한 입력 방식 (보안 우회)
            self.driver.execute_script(f"document.getElementsByName('id')[0].value='{id}'")
            time.sleep(0.5)
            self.driver.execute_script(f"document.getElementsByName('pw')[0].value='{password}'")
            time.sleep(0.5)
            
            # 로그인 버튼 클릭
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".btn_login"))
            )
            login_button.click()
            
            # 로그인 성공 여부 확인
            time.sleep(3)
            if "로그인 정보가 아직 남아있습니다" in self.driver.page_source:
                # 보안 경고가 뜨면 확인 버튼 클릭
                continue_button = self.driver.find_element(By.CSS_SELECTOR, "#new.btn_login")
                continue_button.click()
            
            print("로그인 시도 완료")
            return True
            
        except Exception as e:
            print(f"로그인 실패: {str(e)}")
            print("수동 로그인으로 전환합니다.")
            
            # 수동 로그인으로 전환
            print("\n=== 주의사항 ===")
            print("1. 브라우저에서 직접 로그인을 진행해주세요.")
            print("2. 로그인 완료 후 엔터키를 눌러주시면 프로그램이 계속 진행됩니다.")
            input("로그인을 완료하신 후 엔터키를 눌러주세요...")
            return True
    
    def like_post(self, url):
        """블로그 포스트 공감"""
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # mainFrame으로 전환
            print("메인 프레임으로 전환 중...")
            main_frame = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "mainFrame"))
            )
            self.driver.switch_to.frame(main_frame)
            
            # 페이지 하단으로 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # 공감 버튼 찾기
            print("공감 버튼 찾는 중...")
            like_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    ".u_likeit_list_btn.off"  # 공감 안 한 상태의 버튼
                ))
            )
            print("공감 버튼 발견!")
            
            # JavaScript로 클릭
            self.driver.execute_script("arguments[0].click();", like_button)
            print("공감 처리 완료!")
            time.sleep(2)
            
        except Exception as e:
            print(f"공감 처리 실패: {str(e)}")
            raise e
        finally:
            self.driver.switch_to.default_content()
    
    def comment_post(self, url, comment_text):
        """블로그 포스트에 댓글 작성"""
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # mainFrame으로 전환
            print("메인 프레임으로 전환 중...")
            main_frame = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "mainFrame"))
            )
            self.driver.switch_to.frame(main_frame)
            print("메인 프레임 전환 완료")
            
            # 페이지 하단으로 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # 댓글 버튼 찾기
            print("댓글 버튼 찾는 중...")
            comment_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    "a.btn_comment._cmtList"
                ))
            )
            print("댓글 버튼 발견!")
            
            # 댓글 버튼 클릭
            self.driver.execute_script("arguments[0].click();", comment_button)
            print("댓글 버튼 클릭 완료")
            time.sleep(2)
            
            # contenteditable div 찾기
            print("댓글 입력창 찾는 중...")
            comment_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    "div.u_cbox_text[contenteditable='true']"
                ))
            )
            print("댓글 입력창 발견!")
            
            # JavaScript로 텍스트 입력
            self.driver.execute_script("""
                arguments[0].click();
                arguments[0].innerHTML = arguments[1];
                // 입력 이벤트 발생시키기
                var event = new Event('input', { bubbles: true });
                arguments[0].dispatchEvent(event);
            """, comment_div, comment_text)
            print("댓글 입력 완료")
            time.sleep(1)
            
            # 등록 버튼 찾기
            print("등록 버튼 찾는 중...")
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    "button.u_cbox_btn_upload"
                ))
            )
            print("등록 버튼 발견!")
            
            # 등록 버튼 클릭
            self.driver.execute_script("arguments[0].click();", submit_button)
            print("댓글 등록 완료!")
            time.sleep(2)
            
        except Exception as e:
            print(f"댓글 작성 실패: {str(e)}")
            raise e
        finally:
            self.driver.switch_to.default_content() 