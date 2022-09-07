# 뉴뉴 (Knewnew)::PC버전 🍭

<img src="https://user-images.githubusercontent.com/104430030/188837571-d895300c-0e2b-4cb9-907d-015b96852369.JPG" alt="teamKnewnew" width="500px" />

## 개발 인원 및 기간

- 개발 기간 : 2022/8/16 ~ 2022/9/7 (3주)
- 개발 인원 : FE 3명, BE 3명
  - Front-end : 김광희, 손민지, 정훈조
  - Back-end : 손찬규(PM), 안상현, 음정민

## 프로젝트 소개

모바일 어플리케이션 뉴뉴(Knewnew)의 PC버전 페이지 제작을 위한 프로젝트 입니다.<br>
[뉴뉴(Knewnew)](https://play.google.com/store/apps/details?id=com.mealing.knewnnew)는 수많은 온라인 식품 선택지 속에서 유저 간 추천을 통해 원하는 식품을 손쉽게 발견할 수 있는 **데이터 기반 푸드 포털 플랫폼**입니다.<br>
식품에 대한 후기를 카테고리 별로 게시하고 조회하며 소통하는 **커뮤니티 기능에 중점**을 두고 있습니다.<br>
기존 어플리케이션 '뉴뉴(Knewnew)'는 React Native로 구현되었으나 PC버전은 React.js로 구현되어<br>
디자인 모티브만 가져왔을 뿐 개발은 초기 세팅부터 모두 직접 구현하였습니다.<br>

## 사용기술 스택

### Front-end<br>
![React Badge](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=React&logoColor=white)&nbsp;
![JavaScript Badge](https://img.shields.io/badge/Javascript-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=white)&nbsp;
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)&nbsp;
![Redux](https://img.shields.io/badge/Redux-764ABC?style=for-the-badge&logo=redux&logoColor=white)&nbsp;
![React Query Badge](https://img.shields.io/badge/ReactQuery-FF4154?style=for-the-badge&logo=React&logoColor=white)&nbsp;
![StyledComponents Badge](https://img.shields.io/badge/styled--components-DB7093?style=for-the-badge&logo=styled-components&logoColor=white)

### Back-end<br>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=MySQL&logoColor=white"/>&nbsp;

## 협업 툴
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=MySQL&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Trello-0052CC?style=for-the-badge&logo=Trello&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;


## 구현 

### Sign in : 로그인 페이지
- 소셜 로그인
    - 카카오
    - 네이버

### Option Info : 추가 정보 페이지
- 로그인 이후 추가 정보 수집 후 저장

### My : 마이 페이지
- 로그인한 사용자의 정보 조회
- 로그아웃

### Main(=List) : 리스트 페이지
- 게시글 리스트 조회
- 무한스크롤

### Posting : 글쓰기 페이지
- Form data를 이용한 입력 데이터 전송
- S3 - pre signed URL을 이용한 이미지 파일 업로드

### Detail : 상세 페이지
- 게시글
    - 조회 GET
    - 삭제 DELETE
- 댓글
    - 조회 GET
    - 생성 POST
    - 수정 PATCH
    - 삭제 DELETE

### 기타 페이지
- 모바일 앱 연계 모달창
- Nav / Footer
- 잘못된 접근 시 활용 가능한 404 페이지

## 시연 영상

[🍭뉴뉴 (Knewnew)](http://www.youtube.com/)

### 메인(=리스트) 페이지
- 비로그인 사용자도 조회는 가능하나 수정, 삭제 등의 조작은 로그인 사용자만 가능하도록 구현 

### 소셜 로그인 및 로그아웃
- Kakao / Naver OAuth 2.0 API를 이용한 소셜 로그인 기능 구현
- JWT를 이용한 인증
- Refresh Token을 이용한 토큰 보안 강화
- 전역에서 Token의 상태 관리를 하기 위해 Redux 활용
- 로그아웃 기능 구현

### 글쓰기 페이지
- Form Data를 활용한 게시글 전송 기능 구현
- S3와 pre signed URL을 이용한 이미지 파일 업로드 기능 구현

### 게시글 상세 페이지
- 게시글 조회, 삭제 기능 구현
- 댓글 및 대댓글의 생성, 삭제 기능 구현

