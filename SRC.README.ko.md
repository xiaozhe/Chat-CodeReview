# Chat-CodeReview(Gitlab)

>  ChatGPT는 GitLab 코드의 코드 검토를 자동화합니다.

번역된 버전: [ENGLISH](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.md) | [中文简体](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.zh-CN.md) | [中文繁體](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.zh-TW.md) | [한국어](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.ko.md) | [日本語](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.ja.md) 

## 특징

 **ChatGPT가 Gitlab을 통합하여 자동 코드 리뷰와 주석을 수행하여 소프트웨어 개발 팀에 효율적이고 지능적인 코드 검토 솔루션을 제공합니다.** 

> 
>
> 1. 자동 트리거 및 즉시 응답: GitLab의 Webhook 기능을 활용하여 코드 제출, 병합 요청, 태그 생성 등의 이벤트를 자동으로 트리거합니다. 새로운 코드가 제출되면 시스템은 즉시 응답하여 감사 프로세스를 자동으로 시작하며 수동 개입이 필요하지 않습니다.
>
> 2. GitLab API 인터페이스 활용: GitLab API 인터페이스와 통합하여 향후 기능 확장과 확장을 용이하게 합니다. 이러한 통합 방식은 GitLab과의 상호 작용을 더 유연하게 만들며 더 많은 사용자 정의 감사 요구를 지원할 수 있습니다.
>
> 3. 전체 자동 감사: ChatGPT는 GitLab의 코드를 자동으로 감사하며, 커밋, 병합 요청 및 태그 생성과 같은 세 가지 코드 제출 방식을 포함합니다. 새로운 코드 제출이든 코드 병합이든 시스템은 자동으로 검사하고 감사 코멘트를 제공합니다.
>
> 4. 재시도 메커니즘: 네트워크 문제 또는 기타 문제에 대응하기 위해 시스템에 재시도 메커니즘을 구현했습니다. 네트워크 문제로 인해 요청이 성공하지 않으면 시스템이 자동으로 재시도하여 감사 프로세스의 신뢰성과 안정성을 보장합니다.

## 감사의 원칙

![1689647943933](images/1689647943933.png)

 **달성 단계:** 

> 1. Gitlab의 웹훅 이벤트 푸시: Gitlab은 코드 커밋, 머지 리퀘스트 등 이벤트 발생 시 알림을 트리거하기 위해 웹훅을 설정할 수 있습니다. 새로운 코드 커밋이나 머지 리퀘스트가 있을 때 Gitlab은 미리 설정된 URL로 POST 요청을 보내고 관련 이벤트 데이터를 함께 보냅니다.
> 2. diff 내용을 해석하고 ChatGPT로 전송: Gitlab은 웹훅 이벤트를 받으면 diff 내용을 해석할 수 있습니다. 이 diff는 새로운 커밋된 코드와 기존 코드 간의 차이점입니다. 그런 다음 이러한 차이점을 ChatGPT의 API 엔드포인트에 전송하여 ChatGPT가 코드 변경 내용을 이해할 수 있도록 합니다.
> 3. ChatGPT 처리 및 결과 반환: ChatGPT는 강력한 자연어 처리 모델로써 자연어 텍스트를 이해하고 처리할 수 있습니다. ChatGPT는 diff 내용을 받으면 코드 변경을 분석하고 잠재적인 문제점, 취약점 또는 최적화 제안을 분석하고 응답합니다. ChatGPT는 처리된 결과를 웹훅을 트리거한 Gitlab 인스턴스에 반환합니다.
> 4. ChatGPT 처리 결과를 코멘트로 표시: Gitlab은 ChatGPT의 처리 결과를 받아 해당하는 커밋이나 머지 리퀘스트에 코멘트로 추가할 수 있습니다. 이렇게 하면 코드 제출자와 다른 팀 멤버들은 ChatGPT의 감사 결과를 확인하고 해당 제안에 따라 개선이나 수정을 할 수 있습니다.

 Gitlab 코드 검토와 ChatGPT를 결합함으로써 코드 품질의 자동 검사와 리뷰를 실현하여 팀이 잠재적인 문제, 취약점 또는 개선 기회를 발견하는 데 도움을 줄 수 있습니다. 





## prompt

### 고위 지도자

```python
    messages = [
        {"role": "system",
         "content": "저는 숙련된 프로그래밍 전문가입니다. GitLab의 커밋 코드 변경은 git diff 문자열 형식으로 제공되며, "변경 평가: 실제 점수" 형식으로 점수를 매깁니다. 점수 범위는 0에서 100까지입니다. 출력 형식은 다음과 같습니다. 문제를 간결한 언어로 엄격하게 지적합니다. 필요한 경우 수정된 내용을 직접 제시합니다. 피드백 내용은 엄격한 Markdown 형식을 사용해야 합니다."
         },
        {"role": "user",
         "content": f"이 코드 변경을 검토하십시오 {content}",
         },
    ]
```

### 츤데레 소녀👧

```python
{
    "role": "system",
    "content": "저는 천재 소녀로, 프로그래밍 작업을 능숙하게 다루며, 거만하고 고집 센 성격을 가지고 있습니다. 전배의 코드 변경을 검토하고, 코미디적이고 경쾌한 태도로 문제를 지적합니다. 피드백은 마크다운 형식을 사용하며 이모지를 포함할 수 있습니다."
}
```

 

## 환경 변수

> -  gitlab_server_url: Gitlab 서버의 URL 주소
> -  gitlab_private_token: Gitlab API에 접근하기 위해 사용되는 개인 액세스 토큰 (private token)
> -  openai_api_key: OpenAI API에 접근하기 위해 사용되는 키



## Gitlab 웹후크

Gitlab의 웹훅(Webhook)은 특정 이벤트가 발생할 때 Gitlab이 지정된 URL로 HTTP 요청을 보내고, 관련 이벤트 데이터를 애플리케이션으로 전달하는 이벤트 알림 메커니즘입니다. 이를 통해 애플리케이션은 이벤트 데이터를 기반으로 사용자 정의 작업이나 응답을 수행할 수 있습니다.

웹훅은 Gitlab에서 코드 커밋, 머지 요청, 태그 생성, 브랜치 작업 등 다양한 이벤트를 모니터링하고 응답하는 데 사용될 수 있습니다. 웹훅을 활용하면 자동화된 작업, 통합 및 CI/CD (지속적 통합/지속적 배포) 프로세스를 구현할 수 있습니다.

다음은 Gitlab Webhook의 주요 기능 및 용도입니다.

> 1. 이벤트 트리거: Gitlab에서 Webhook을 구성하고 활성화한 후, 특정 이벤트(코드 커밋, 머지 요청 등)가 발생하면 Gitlab이 자동으로 Webhook을 트리거합니다.
> 2. HTTP 요청: 이벤트가 트리거되면 Gitlab은 미리 구성한 URL로 HTTP 요청을 보내며, 해당 이벤트의 데이터를 전송합니다. 일반적으로 POST 요청이며, JSON 형식의 데이터를 함께 전송합니다.
> 3. 사용자 정의 작업: Webhook 요청을 수신하는 스크립트나 서비스를 작성함으로써 수신한 이벤트 데이터를 구문 분석하고 처리하여 자신만의 사용자 정의 작업(자동 빌드, 자동 테스트, 자동 배포 등)을 수행할 수 있습니다.
> 4. 다른 서비스 통합: Webhook을 통해 Gitlab은 다른 서비스나 도구와 통합할 수 있으며, 예를 들어 코드를 CI 플랫폼으로 자동 동기화하거나 팀 멤버에게 자동 알림을 보내거나 작업 추적 시스템을 자동으로 업데이트하는 등의 작업을 수행할 수 있습니다.
> 5. 구성 가능성: Gitlab의 Webhook은 다양한 구성 옵션을 제공하며, 모니터링할 이벤트 유형을 선택하고 트리거 조건을 설정하며, 요청의 내용과 형식을 정의할 수 있습니다.



![1689651530556](images/1689651530556.png)

![1689651554862](images/1689651554862.png)

------

### 테스트 데이터(푸시)

**Request URL:** POST http://192.168.96.19:5000/git/webhook 200

**Trigger:** Push Hook

**Elapsed time:** 0.01 sec

**Request time:** 刚刚

------

##### Request headers:

```
Content-Type: application/jsonX-Gitlab-Event: Push HookX-Gitlab-Token: asdhiqbryuwfqodwgeayrgfbsifbd
```

##### Request body:

```
{
  "object_kind": "push",
  "event_name": "push",
  "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
  "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "ref": "refs/heads/master",
  "checkout_sha": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "message": "Hello World",
  "user_id": 4,
  "user_name": "John Smith",
  "user_email": "john@example.com",
  "user_avatar": "https://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=8://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=80",
  "project_id": 15,
  "project": {
    "id": 15,
    "name": "gitlab",
    "description": "",
    "web_url": "http://test.example.com/gitlab/gitlab",
    "avatar_url": "https://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=8://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=80",
    "git_ssh_url": "git@test.example.com:gitlab/gitlab.git",
    "git_http_url": "http://test.example.com/gitlab/gitlab.git",
    "namespace": "gitlab",
    "visibility_level": 0,
    "path_with_namespace": "gitlab/gitlab",
    "default_branch": "master"
  },
  "commits": [
    {
      "id": "c5feabde2d8cd023215af4d2ceeb7a64839fc428",
      "message": "Add simple search to projects in public area",
      "timestamp": "2013-05-13T18:18:08+00:00",
      "url": "https://test.example.com/gitlab/gitlab/-/commit/c5feabde2d8cd023215af4d2ceeb7a64839fc428",
      "author": {
        "name": "Test User",
        "email": "test@example.com"
      }
    }
  ],
  "total_commits_count": 1,
  "push_options": {
    "ci": {
      "skip": true
    }
  }
}
```

##### Response headers:

```
Server: Werkzeug/2.3.6 Python/3.8.0Date: Tue, 18 Jul 2023 03:39:51 GMTContent-Type: application/jsonContent-Length: 26Connection: close
```

##### Response body:

```
{
  "status": "success"
}
```



## 설치 및 실행

### 1、코드 다운로드

```python
git clone https://github.com/nangongchengfeng/chat-review.git
```

### 2、종속성 설치

![1689663745702](images/1689663745702.png)

```python
python deal_package.py
```

### 3、업데이트 구성

**config/config.py**

```python

"""
这个文件是用来从apollo配置中心获取配置的，
如果没有apollo配置中心，可以直接在这里配置
"""

WEBHOOK_VERIFY_TOKEN = "asdhiqbryuwfqodwgeayrgfbsifbd"
gitlab_server_url = gitlab_server_url
gitlab_private_token = gitlab_private_token
openai_api_key = openai_api_key

```

### 4、app.py 파일 실행

```python
简单
nohup python3 app.py & 
```

### 5、Gitlab 구성 Webhook

```python
http://192.168.96.19:5000/git/webhook 
실행 중인 컴퓨터의 IP 주소를 변경할 수 있으며 도메인 이름도 변경할 수 있습니다.
http://gitlab.ownit.top/git/webhook 
```



![1689651530556](images/1689651530556.png)



## 질문

### diff다루다

![1689661104194](images/1689661104194.png)

#### 방법 1(간결)



​	1、diff 내용을 ChatGPT에 전달하여 처리합니다. (추가된 라인 및 삭제된 라인 포함)

장점: 편리하고 빠릅니다.

단점: 내용이 너무 길 경우, ChatGPT 처리에 실패하고 일부 코드가 불완전하거나 불일치할 수 있습니다.



#### 방법 2(권장)

​	2、diff 내용을 처리하고, 삭제된 라인과 + 기호 표시를 제거합니다.

장점: 편리하고 빠르며 길이를 절약할 수 있습니다.

단점: 내용이 너무 길 경우, ChatGPT 처리에 실패하고 일부 코드가 불완전하거나 불일치할 수 있습니다.

```python
def filter_diff_content(diff_content):
    filtered_content = re.sub(r'(^-.*\n)|(^@@.*\n)', '', diff_content, flags=re.MULTILINE)
    processed_code = '\n'.join([line[1:] if line.startswith('+') else line for line in filtered_content.split('\n')])
    return processed_code
```

![1689661743140](images/1689661743140.png)



#### 방법 3(복잡함) 공동 디버깅이 아니라 코드를 덮어썼습니다.

​	3、diff 내용을 처리하여 삭제된 라인과 + 기호 표시를 제거한 후, JavaParser를 사용하여 수정된 원본 파일을 가져와서 해당 코드 블록을 추출하고 리뷰를 업로드합니다.

장점: 길이를 절약하고, 작업은 완료되며, 약간의 논리성이 보입니다.

단점: 매우 귀찮고 번거롭습니다. Java만 지원됩니다.

```json
[{
	'code': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	'name': 'SettlementDetailController'
}, {
	'code': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	'name': 'queryRecord'
}, {
	'code': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	'name': 'populateBatchItemVO'
}]
```



## 데모

![1689663598079](images/1689663598079.png)



## 기여하다

프로젝트의 지원과 영감을 주신 [anc95 Xiaoan](https://github.com/anc95)에게 감사드립니다.
 https://github.com/anc95/ChatGPT-CodeReview.git

 ![Avatar](images/13167934.jpg) 



