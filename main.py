from naver_bot import NaverBlogBot
import time
import random
import os
from dotenv import load_dotenv

# .env 파일에서 로그인 정보 로드
load_dotenv()

def main():
    bot = None
    try:
        bot = NaverBlogBot()
        print("\n=== 네이버 블로그 자동 댓글/좋아요 프로그램 ===")
        
        # 환경 변수에서 로그인 정보 가져오기
        naver_id = os.getenv('NAVER_ID')
        naver_pw = os.getenv('NAVER_PW')
        
        if not naver_id or not naver_pw:
            print("로그인 정보를 찾을 수 없습니다.")
            return
            
        # 로그인 시도
        if not bot.login(naver_id, naver_pw):
            return
            
        while True:
            print("\n1. URL 입력하기")
            print("2. 서로이웃 신청하기")
            print("3. PDF로 저장하기")
            print("4. 프로그램 종료")
            choice = input("\n선택해주세요 (1-4): ")
            
            if choice == "4":
                print("프로그램을 종료합니다.")
                break
                
            elif choice == "1":
                url = input("\n블로그 포스트 URL을 입력해주세요: ")
                
                try:
                    # 좋아요 시도
                    print("좋아요 시도 중...")
                    try:
                        bot.like_post(url)
                        print("✅ 좋아요 완료!")
                    except Exception as like_error:
                        print("ℹ️ 공감 버튼을 찾을 수 없거나 이미 공감한 글입니다.")
                    
                    time.sleep(random.uniform(1, 2))
                    
                    # 댓글
                    comments = [
                        "좋은 글 잘 보고 갑니다 😊",
                        "정말 유익한 정보네요! 감사합니다 👍",
                        "잘 보고 갑니다~ 좋은 하루 되세요 ✨",
                        "공감하며 읽었습니다 💕",
                        "좋은 정보 감사합니다! 도움이 많이 되네요 🙏",
                        "잘 보고 가요! 오늘도 행복한 하루 되세요 ⭐",
                        "너무 좋은 글이에요! 공감하고 갑니다 💖",
                        "정성스러운 포스팅 감사합니다 😍",
                        "이런 좋은 정보 공유해주셔서 감사해요 👍",
                        "구독하고 갑니다! 앞으로도 좋은 글 기대할게요 🌟",
                        "오늘도 좋은 글 잘 읽었습니다 💫",
                        "항상 유익한 글 감사드려요 😊",
                        "공감 누르고 갑니다! 좋은 하루 보내세요 ❤️"
                    ]
                    print("댓글 작성 중...")
                    bot.comment_post(url, random.choice(comments))
                    print("✅ 댓글 작성 완료!")
                    
                except Exception as e:
                    print(f"\n❌ 오류 발생: {str(e)}")
                    
                continue
                
            elif choice == "2":
                url = input("\n서로이웃 신청할 블로그 URL을 입력해주세요: ")
                try:
                    print("서로이웃 신청 중...")
                    bot.add_neighbor(url)
                    print("\n✅ 처리 완료!")
                    
                except Exception as e:
                    print(f"\n❌ 오류 발생: {str(e)}")
                    
                continue
                
            elif choice == "3":
                url = input("\n저장할 블로그 포스트 URL을 입력해주세요: ")
                try:
                    print("PDF 저장 중...")
                    bot.save_as_pdf(url)
                    print("\n✅ 처리 완료!")
                    
                except Exception as e:
                    print(f"\n❌ 오류 발생: {str(e)}")
                    
                continue
                
            else:
                print("\n잘못된 선택입니다. 다시 선택해주세요.")
                
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {str(e)}")
        
    finally:
        if bot and bot.driver:
            bot.driver.quit()
            print("\n브라우저가 종료되었습니다.")

if __name__ == "__main__":
    main() 