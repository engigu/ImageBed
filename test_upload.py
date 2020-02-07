import requests
import base64


# url = 'https://gitee.com/upload_with_base_64'
url = 'https://gitee.com/upload'
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,it;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "28859",
    "Cookie": "user_locale=zh-CN; oschina_new_user=false; remember_user_token=BAhbB1sGaQNLjBRJIiIkMmEkMTAkQTZSS2Rady52YjBKQ1R5RHJiVFhvdQY6BkVU--accbb32c1b2ec8a5806c823a54c2496b262abcbc; access_token=e883a9b5f519d7f7729fb7ccb06c445b; tz=Asia%2FShanghai; Hm_lvt_24f17767262929947cc3631f99bfd274=1580986445,1580989788,1581050794,1581081941; Hm_lpvt_24f17767262929947cc3631f99bfd274=1581082151; gitee-session-n=BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJTY5ODc5MGQ5NjMyM2Y1OWE4N2M0NDYzZWM1ZTFkOTkxBjsAVEkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjsAVFsHWwZpA0uMFEkiIiQyYSQxMCRBNlJLZFp3LnZiMEpDVHlEcmJUWG91BjsAVEkiHXdhcmRlbi51c2VyLnVzZXIuc2Vzc2lvbgY7AFR7BkkiFGxhc3RfcmVxdWVzdF9hdAY7AFRJdToJVGltZQ3tBB7ASbVyhQk6DW5hbm9fbnVtaQJTAzoNbmFub19kZW5pBjoNc3VibWljcm8iB4UQOgl6b25lSSIIVVRDBjsARkkiEF9jc3JmX3Rva2VuBjsARkkiMStRQk4weDJ1aDl4cXJ5eHJqZlFvaWZlNFhiOE9lRHhrTnhBNHZRd1RscUE9BjsARg%3D%3D--c629b249f5dbab9875d3c301c54fb5f1e7c2699b",
    "Host": "gitee.com",
    "Origin": "https://gitee.com",
    "Referer": "https://gitee.com/EngiGu/imagestore/issues/new",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
    "X-CSRF-Token": "+QBN0x2uh9xqryxrjfQoife4Xb8OeDxkNxA4vQwTlqA=",
    "X-Requested-With": "XMLHttpRequest"
}

jpg = open('/home/sayheya/Desktop/tmp/imagebed/web/images/banner.jpg', 'rb')
# print(base64.b64encode(jpg).decode())
# r = requests.post(url, files={'base64': base64.b64encode(jpg).decode()}, headers=headers)
r = requests.post(url, files= {'file': ('files', open('/home/sayheya/Desktop/tmp/imagebed/web/images/banner.jpg', 'rb'), 'image/jpeg', {'Expires': '0'})}, headers=headers)
print(r.content.decode())