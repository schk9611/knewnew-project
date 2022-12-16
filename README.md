# 뉴뉴 (Knewnew)

## 개발 인원 및 기간

- 개발 기간 : 2022/8/16 ~ 2022/9/7 (3주)
- 개발 인원 : FE 3명, BE 3명
  - Front-end : 김광희, 손민지, 정훈조
  - Back-end : 손찬규(PM), 안상현, 음정민

<br>

## 프로젝트 소개

모바일 어플리케이션 뉴뉴(Knewnew)의 PC버전 페이지 제작을 위한 프로젝트 입니다.<br>
[뉴뉴(Knewnew)](https://play.google.com/store/apps/details?id=com.mealing.knewnnew)는 수많은 온라인 식품 선택지 속에서 유저 간 추천을 통해 원하는 식품을 손쉽게 발견할 수 있는 **데이터 기반 푸드 포털 플랫폼**입니다.<br>
식품에 대한 후기를 카테고리 별로 게시하고 조회하며 소통하는 **커뮤니티 기능에 중점**을 두고 있습니다.<br>
기존 어플리케이션 '뉴뉴(Knewnew)'는 React Native로 구현되었으나 PC버전은 React.js로 구현되어<br>
디자인 모티브만 가져왔을 뿐 개발은 초기 세팅부터 모두 직접 구현하였습니다.<br>

<br>

## 시연 영상

[🍭뉴뉴 (Knewnew)](https://www.youtube.com/watch?v=T7NdgYqNdog)

<br>

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
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=Poetry&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=Amazon_S3&logoColor=white"/>&nbsp;

<br>

## 협업 툴
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=MySQL&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Trello-0052CC?style=for-the-badge&logo=Trello&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;

<br>

## 구현 

### ERD
![knewnew_ERD](https://user-images.githubusercontent.com/60742666/208109581-55ffae59-6da6-4309-b8c3-d833534194e1.png)

### API EndPoint

|URI|METHOD|DESC|
|---|---|---|
|/user/login/\<str:social_type\>|POST|소셜로그인|
|/user/mypage|GET|회원프로필|
|/user/introduction|POST|회원 추가정보 기입|
|/review|GET|리뷰 리스트보기|
|/review|POST|리뷰 작성하기|
|/review/\<id:int\>|GET|리뷰 상세보기|
|/review/\<id:int\>|PATCH|리뷰 수정하기|
|/review/\<id:int\>|DELETE|리뷰 삭제하기|
|/review/image-presigned-url|POST|이미지 presigned url 받기|
|/review/like|POST|리뷰 좋아요/해제|
|/review/bookmark|POST|리뷰 북마크/해제|
|/review/\<id:int\>/comment|GET|리뷰 댓글보기|
|/review/\<id:int\>/comment|POST|리뷰 댓글 생성하기|
|/review/\<id:int\>/comment/\<id:int\>|PATCH|리뷰 댓글 수정하기|
|/review/\<id:int\>/comment/\<id:int\>|DELETE|리뷰 댓글 삭제하기|

### 담당 역할(Back-end)

- review의 상세 페이지 구현 담당
- review의 댓글 기능 구현 담당

### 가상 환경 세팅

- poetry를 통해 가상환경 및 의존성&버전 관리를 진행하였습니다.

### 시크릿 키 및 보안 사항

- python-dotenv 패키지를 통해 `.env` 파일로 프로젝트의 시크릿 키와 DB 관련 사항들을 보안 처리하였습니다.

### 게시글 상세 페이지
- DRF의 특성을 이용하여 `settings.py` 에서 'REST_FRAMEWORK'의 'DEFAULT_PERMISSION_CLASSES'를 'rest_framework.permissions.IsAuthenticatedOrReadOnly'로 설정하여 비로그인 사용자도 조회는 가능하나 수정, 삭제 등의 조작은 로그인 사용자만 가능하도록 구현하였습니다.
- 사용자에 대한 관리는 JWT를 사용하여 access token과 refresh token을 통해 유저를 구분하도록 하였습니다.


### 댓글 기능 구현
- review의 `views.py`에서 `ListCreateAPIView'를 상속받아 댓글 기능을 구현하였습니다. 이 때 메소드의 분기를 설정하기 위해 'get_serialzier_class'를 작성하고 'GET' 메소드 요청일 때와 'POST' 메소드 요청일 때를 나누어 진행하였습니다.
- 댓글 기능 또한 사용자를 구분하여 조회 기능과 수정/삭제 기능을 진행할 수 있도록 구현하였습니다.
