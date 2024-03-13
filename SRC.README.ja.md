# Chat-CodeReview(Gitlab)

>   ChatGPT は GitLab のコードを自動的にコードレビューします。 

翻訳版: [ENGLISH](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.md) | [中文简体](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.zh-CN.md) | [中文繁體](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.zh-TW.md) | [한국어](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.ko.md) | [日本語](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.ja.md) 

## 特徴

 **ChatGPTはGitLabと統合し、自動的にコード監査を行い、コメントを追加します。ソフトウェア開発チームに効率的でスマートなコード監査のソリューションを提供します。** 

> 1. 自動トリガーとリアルタイムな応答：GitLabのWebhook機能を利用して、コードのコミット、マージリクエスト、タグ作成などのイベントを自動的にトリガーします。新しいコードのコミットがあると、システムは即座に応答し、自動的に監査プロセスを開始します。手動で干渉する必要はありません。
> 2. GitLab API インタフェースの活用：GitLabのAPIインタフェースと統合することで、将来的な機能の拡張や拡充が容易になります。この統合方法により、GitLabとのやり取りが柔軟になり、より多様なカスタム監査要件をサポートできます。
> 3. 全自動のコード監査：ChatGPTは、GitLabのコードを自動的に監査し、コミット（push）、マージリクエスト（合流リクエスト）、タグ（タグ作成）など、3つのコード提出方法をカバーしています。新しいコードの提出やコードのマージに関わらず、システムは自動的にチェックを行い、監査コメントを提供します。
> 4. リトライメカニズム：ネットワークの問題やその他の問題に対応するため、システムにはリトライメカニズムが実装されています。ネットワークの問題によりリクエストが成功しなかった場合、システムは自動的にリトライを行い、監査プロセスの信頼性と安定性を確保します。

## 审计原理

![1689647943933](images/1689647943933.png)

 **達成すべき次のステップ：** 

> 1. GitLabのWebhookイベント通知：GitLabはWebhookを設定でき、コードのコミットやマージリクエストなどのイベントが発生した際に通知をトリガーします。新しいコードのコミットやマージリクエストがある場合、GitLabは事前に設定されたURLに対してPOSTリクエストを送信し、関連するイベントデータを含めます。
> 2. Diff内容の解析とChatGPTへの送信：GitLabがWebhookイベントを受信すると、Diff内容を解析できます。これは新しく提出されたコードと既存のコードとの差分です。そして、これらの差分をChatGPTのAPIエンドポイントに送信し、ChatGPTがコードの変更内容を理解できるようにします。
> 3. ChatGPTの処理と結果の返信：ChatGPTは強力な自然言語処理モデルであり、自然言語テキストを理解し、処理することができます。ChatGPTがDiff内容を受信すると、コードの変更内容を解析し、問題点、脆弱性、または最適化の提案に対して分析と回答を行います。ChatGPTは処理された結果をWebhookをトリガーしたGitLabインスタンスに返信します。
> 4. ChatGPTが処理した結果をコメントで表示：GitLabはChatGPTからの処理結果を受け取り、それを対応するコミットやマージリクエストにコメントとして追加できます。これにより、コードの提出者や他のチームメンバーはChatGPTのレビュー結果を確認し、提案に基づいて適切な改善や修正を行うことができます。

 GitLabのコードレビューをChatGPTと組み合わせることで、コードの品質を自動的にチェックし、レビューすることができます。これにより、チームは潜在的な問題や脆弱性、改善の機会を見つけるのに役立ちます。（以上、参考までに）。 





## prompt

### 上級リーダー

```python
    messages = [
        {"role": "system",
         "content": "私はプログラミングのエキスパートではありませんが、提供されるGitLabのコミットコード変更は、変更のスコアを「変更評価：実際のスコア」の形式で示し、スコアの範囲は0〜100ポイントとします。出力形式は、厳格な言葉で、問題を指摘し、必要な場合は直接修正内容を提供します。フィードバック内容は厳格なMarkdown形式を使用する必要があります。"
         },
        {"role": "user",
         "content": f"请review这部分代码变更{content}",
         },
    ]
```

###  ツンデレ少女 👧

```python
{
    "role": "system",
    "content": "あなたはプログラムに長けた天才の少女で、高慢で傲慢な性格を持ち、前輩のコード変更を審査する責任があります。若々しい態度と元気な方法で問題を指摘します。Markdown形式を使用して、絵文字も使って構いません。"
}
```

## 環境変数

> -  gitlab_server_url: GitlabサーバーのURLアドレス
> -  gitlab_private_token: Gitlab APIにアクセスするためのプライベートトークン
> -  openai_api_key: OpenAIのAPIにアクセスするためのAPIキー



##  GitLabのWebhook（ウェブフック） 

GitLabのWebhookは、特定のイベントが発生した際にGitLabから指定したURLに対してHTTPリクエストが送信され、関連するイベントデータがあなたのアプリケーションに渡されるイベント通知メカニズムです。これにより、イベントデータに基づいてカスタムの操作や応答を実行することができます。

Webhookは、コードのコミット、マージリクエスト、タグの作成、ブランチ操作など、さまざまなイベントをGitLabで監視し、応答するために使用することができます。Webhookを活用することで、さまざまな自動化タスクや統合、継続的インテグレーション/継続的デリバリー（CI/CD）プロセスを実現することができます。

以下は、GitLabのWebhookの主な特徴と用途です：

> 1. イベントトリガー：GitLabでWebhookを設定し、有効にすると、特定のイベント（コードのコミット、マージリクエストなど）が発生した際に、GitLabが自動的にWebhookをトリガーします。
> 2. HTTPリクエスト：イベントがトリガーされると、GitLabは事前に設定したURLに対してHTTPリクエストを送信します。通常はPOSTリクエストであり、関連するイベントのデータをJSON形式で含んでいます。
> 3. カスタム操作：Webhookリクエストを受け取るスクリプトやサービスを作成することで、受け取ったイベントデータを解析し処理し、カスタムの操作（自動ビルド、自動テスト、自動デプロイなど）を実行することができます。
> 4. 他のサービスとの統合：Webhookにより、GitLabは他のサービスやツールとの統合が可能となります。例えば、コードの自動同期を継続的インテグレーションプラットフォームに行ったり、チームメンバーに自動通知を送ったり、タスクトラッキングシステムを自動更新したりすることができます。
> 5. 柔軟な設定：GitLabのWebhookには豊富な設定オプションがあり、監視するイベントのタイプを選択したり、トリガー条件を設定したり、リクエストの内容や形式を定義したりすることができます。

![1689651530556](images/1689651530556.png)

![1689651554862](images/1689651554862.png)

------

### テストデータ（プッシュ）

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



## インストールして実行する

### 1. コードをダウンロードする

```python
git clone https://github.com/nangongchengfeng/chat-review.git
```

### 2. インストールの依存関係

![1689663745702](images/1689663745702.png)

```python
python deal_package.py
```

### 3、構成を更新する

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

### 4、app.pyファイルを実行する

```python
简单
nohup python3 app.py & 
```

### 5、Gitlab 設定 Webhook

```python
http://192.168.96.19:5000/git/webhook 
実行マシンのIPアドレスを変更したり、ドメイン名を変更したりすることができます。
http://gitlab.ownit.top/git/webhook 
```



![1689651530556](images/1689651530556.png)



## 難病

### diff処理

![1689661104194](images/1689661104194.png)

#### 方法1  （シンプルな方法） 

​		1、diffの内容をすべてChatGPTに渡して処理を行います（追加行、削除行を含む）。

利点：簡単で迅速です。

デメリット：内容が長すぎる場合、ChatGPTの処理に失敗し、コードの一部や論理の整合性が失われる可能性があります。



#### 方法2 ( 推奨方法） 

​		2、diffの内容を処理し、削除行と+記号のタグを削除します。

利点：簡単で迅速であり、一定の長さを節約できます。

デメリット：内容が長すぎる場合、ChatGPTの処理に失敗し、コードの一部や論理の整合性が失われる可能性があります。

```python
def filter_diff_content(diff_content):
    filtered_content = re.sub(r'(^-.*\n)|(^@@.*\n)', '', diff_content, flags=re.MULTILINE)
    processed_code = '\n'.join([line[1:] if line.startswith('+') else line for line in filtered_content.split('\n')])
    return processed_code
```

![1689661743140](images/1689661743140.png)



#### 方法3 ( 複雑な方法）- 未調整、コードは完成しています 

​		3、diffの内容を処理し、削除行と+記号のタグを削除します。修正された元のファイルを取得し、JavaParserを使用して解析します。対応するコードブロックを取得してレビューをアップロードします。

利点：長さを節約でき、メソッドが完了し、ロジックが多少整合しています。

デメリット：非常に手間がかかり、面倒で、Javaのみをサポートしています。

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



## デモ

![1689663598079](images/1689663598079.png)



## 助ける

プロジェクトへのサポートとインスピレーションを与えてくれた [ anc95  小安大佬](https://github.com/anc95) に感謝します

 https://github.com/anc95/ChatGPT-CodeReview.git

 ![Avatar](images/13167934.jpg) 



