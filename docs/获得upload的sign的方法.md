这是登录数据：
```json
{
    "code": 200,
    "data": {
        "info": {
            "userStatus": "",
            "zyId": "",
            "faceFileIcon": null,
            "idCardNo": "",
            "roles": "1",
            "lastLoginDate": "2024-03-03 12:57:31",
            "pic": "",
            "uid": "5122174845",
            "password": "9967c006e23df34873431e8c7acf6da1",
            "isManager": false,
            "id": 15000108,
            "classbh": "",
            "njmc": "",
            "nickName": "",
            "xb": "1",
            "loginStatus": "",
            "zymc": "",
            "deviceToken": "AoPmeEdCuxbo5tphAJPhd3xcebNzcJrr9pjj6lMVvs4a",
            "xymc": "",
            "bjmc": "",
            "xh": "2022181640245",
            "unit": "",
            "faceCodeImageUrl": "",
            "phoneNumber": "",
            "xm": "胡宗尧",
            "fileIcon": null,
            "grade": "",
            "faceCode": "",
            "imei": "",
            "xybh": ""
        },
        "token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyMDIyMTgxNjQwMjQ1Iiwic2Nob29sX2lkIjoiMjEiLCJleHAiOjE3MTAzMDYxNDYsImlhdCI6MTcwOTQ0MjE0NiwianRpIjoiMjhhNTc3YWEtODQxOC00Yjg4LWFhMTEtOTExYjM2OTliNWYyIn0.gv0krKeNq61hwEYtU99weaX6NhrqJayQmyP-1h8ngdQ.AAAANIqjCkjMe7S0gm/Bd9RfyIbForoTjhXtq/NGe3JSK5nDPuRON+jjq2Ukn6E27ch/mg==.1710306146000"
    },
    "message": "OK"
}
```

取 `token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyMDIyMTgxNjQwMjQ1Iiwic2Nob29sX2lkIjoiMjEiLCJleHAiOjE3MTAzMDYxNDYsImlhdCI6MTcwOTQ0MjE0NiwianRpIjoiMjhhNTc3YWEtODQxOC00Yjg4LWFhMTEtOTExYjM2OTliNWYyIn0.gv0krKeNq61hwEYtU99weaX6NhrqJayQmyP-1h8ngdQ.AAAANIqjCkjMe7S0gm/Bd9RfyIbForoTjhXtq/NGe3JSK5nDPuRON+jjq2Ukn6E27ch/mg==.1710306146000"`

按`.`分割成5份：

- eyJhbGciOiJIUzI1NiJ9
- eyJzdWIiOiIyMDIyMTgxNjQwMjQ1Iiwic2Nob29sX2lkIjoiMjEiLCJleHAiOjE3MTAzMDYxNDYsImlhdCI6MTcwOTQ0MjE0NiwianRpIjoiMjhhNTc3YWEtODQxOC00Yjg4LWFhMTEtOTExYjM2OTliNWYyIn0
- gv0krKeNq61hwEYtU99weaX6NhrqJayQmyP-1h8ngdQ
- AAAANIqjCkjMe7S0gm/Bd9RfyIbForoTjhXtq/NGe3JSK5nDPuRON+jjq2Ukn6E27ch/mg==
- 1710306146000

```java
arg1 = 第四项
arg2 = "/api/l/v6/prejudgment?jsonsports=" + AES(json)
encrypted = cgapiEnrypt(arg1, arg2)
cgAuthorization = 前三项
```

sign = encrypted (用`|`分割) 的最后一项


