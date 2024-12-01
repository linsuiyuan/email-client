## email client

一个简单易用的邮件客户端，支持发送和接收邮件，可以处理附件、设置过滤条件等功能。支持 QQ 邮箱、163邮箱等邮箱

## 支持的邮箱

- QQ邮箱
- 163邮箱(网易邮箱)
- 139邮箱
- iCloud
- Gmail
- Outlook/Hotmail

## 安装

```bash
pip install emlclient
```

## 使用示例

### 1. 读取未读邮件

```python
from emlclient import EmailClient

# 初始化邮件客户端
client = EmailClient(
    username="your_email@example.com",
    password="your_password"
)

# 读取最新的3封未读邮件
emails = client.read_emails(
    criteria="UNSEEN",
    limit=3,
    seen=True  # 设置为已读
)

# 打印邮件内容
for email in emails:
    print(f"发件人: {email['sender']}")
    print(f"主题: {email['subject']}")
    print(f"内容: {email['body']}\n")
```

### 2. 发送带附件的邮件

```python
from emlclient import EmailClient

client = EmailClient(
    username="your_email@example.com",
    password="your_password"
)

# 发送带附件的邮件
result = client.send_email(
    to="recipient@example.com",
    subject="测试邮件",
    content="这是一封测试邮件",
    attachments=["document.pdf", "image.jpg"]
)
```

### 3. 按条件搜索邮件

```python
from emlclient import EmailClient

client = EmailClient(
    username="your_email@example.com",
    password="your_password"
)

# 搜索2024年1月1日之后的包含"发票"的邮件
emails = client.read_emails(
    criteria='SINCE "01-Jan-2024" SUBJECT "发票"',
    limit=5
)

# 打印搜索结果
for email in emails:
    print(f"日期: {email['date']}")
    print(f"主题: {email['subject']}")
```

## 搜索条件说明

支持的搜索条件包括：
- `ALL`: 所有邮件
- `UNSEEN`: 未读邮件
- `SEEN`: 已读邮件
- `FROM "someone@example.com"`: 来自特定发件人的邮件
- `TO "someone@example.com"`: 发送给特定收件人的邮件
- `SUBJECT "test"`: 主题包含特定文字的邮件
- `SINCE "01-Jan-2020"`: 某个日期之后的邮件
- `BEFORE "01-Jan-2020"`: 某个日期之前的邮件
- `LARGER 1000`: 大于1000字节的邮件
- `SMALLER 1000`: 小于1000字节的邮件

多个条件可以组合使用，如: `UNSEEN SUBJECT "test"`

## 注意事项

1. 部分邮箱服务商可能需要特殊配置，请参考各自的文档(比如一些邮箱密码需要使用授权码而不是登录密码)

## License

MIT
