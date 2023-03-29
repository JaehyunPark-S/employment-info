# 📌 채용 정보 SNS

자료 수집(데이터 크롤링)을 이용해 많은 채용정보를 쉽게 접근할 수 있도록 하여 사용자들이 시간과 비용을 절감하여 효율적인 취업준비를 할 수 있게 도와주는 웹 서비스
</br></br>

# 1. 제작 기간 & 참여 인원

- 개인 프로젝트
- 2021.03.07 ~ 2021.06.18
  </br></br>

# 2. 사용 기술

#### `Backend`

- Python3
- Django
- SqLite3
- RabbitMQ
- BeautifulSoup

#### `Frontend`

- Django-template
- Tailwind-CSS
- SCSS
- JQuery
  </br></br>

# 3. ERD 설계

![image](https://user-images.githubusercontent.com/56579736/228511620-b66d7851-cf6a-4542-9c16-280f01263d22.png)
</br></br>

# 4. DFD 설계

![sns dfd](https://user-images.githubusercontent.com/56579736/228522609-9118a636-135f-457b-a085-b4e81a300ce4.png)
</br></br>

# 5. 핵심 기능

<details>
<summary>매일 자정 스택오버플로우에서 채용 정보 크롤링</summary>

1. Celery를 이용하여 매일 자정에 크롤링 기능이 수행한다.(개발당시 크롤링이 오랜 시간 실행되어 RabbitMQ에서 실행되도록 하였음)
2. 크롤링 기능이 수행될 때 DB에 같은 공고가 없을 때만 DB에 저장한다.
</details>
</br>
<details>
<summary>각 테이블 별 CRUD</summary>

1. 사용자 CRUD
2. 댓글 CRUD
3. 게시판 CRUD
4. 채용공고 CRUD
5. 채팅(채팅방, 메세지) CRUD
</details>
</br>
<details>
<summary>팔로우 기눙</summary>

- 팔로우, 언팔로우 기능(INSERT, DELETE)
</details>
</br></br>

# 6. 화면 구성

![채용정보 화면](https://user-images.githubusercontent.com/56579736/228511988-4f6d9e6f-f83a-4e66-badf-7183b988782a.png)
</br></br>
