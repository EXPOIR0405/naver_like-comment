# 네이버 블로그 자동화 봇

네이버 블로그의 자동 좋아요/댓글 작성을 자동화하는 Python 스크립트입니다.

## 기능

- 네이버 자동 로그인 (실패시 수동 로그인 가능)


### 공감하기 (`like_post`)
- 블로그 포스트 페이지 접속
- 공감 버튼 찾기 및 클릭
- 성공 여부 확인

### 댓글 작성 (`comment_post`)
- 블로그 포스트 페이지 접속
- 댓글 작성 영역 활성화
- 댓글 내용 입력
- 등록 버튼 클릭


## 설치 방법

1. 필요한 패키지 설치:

```bash
pip install selenium webdriver_manager python-dotenv
```

2. Chrome 웹 드라이버는 자동으로 설치됩니다.

### 가상환경 설정 (필수)

Windows:
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate
```

Mac/Linux:
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```

## 환경 설정

1. `.env` 파일을 프로젝트 루트 디렉토리에 생성:

```bash
NAVER_ID=your_naver_id
NAVER_PW=your_naver_password
```

## 개발 환경

- Python 3.8+
- Selenium 4.x
- Chrome 브라우저

## 사용 방법

1. 프로그램 실행:

```bash
python main.py
```

2. 메뉴 선택:
   - 1: URL 입력하기
   - 2: 프로그램 종료

3. URL 입력 시 자동으로:
   - 좋아요 클릭
   - 랜덤 댓글 작성 
   ("좋은 글 잘 보고 갑니다 😊" 등 미리 설정된 댓글 중 랜덤 선택)

## 주의사항

- 네이버의 이용약관을 준수하여 사용해주세요
- 과도한 자동화는 계정 제재의 원인이 될 수 있습니다
- 개인정보 보호를 위해 `.env`는 반드시 `.gitignore`에 포함시켜주세요

## ⭐ 이 프로젝트가 도움이 되셨나요?

네이버 블로그 자동화 봇이 마음에 드셨다면 Star를 눌러주세요! 
당신의 ⭐는 제가 더 열심히 코딩하게 만드는 연료가 됩니다 🚀

(네이버 블로그에 자동으로 좋아요를 누르는 것처럼, 
GitHub에서는 수동으로 Star 부탁드립니다 😉)
