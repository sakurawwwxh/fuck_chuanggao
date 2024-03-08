## 逆向login接口全过程

### 1. 找到接口
```java
@POST("api/f/v6/login")
@FormUrlEncoded
Observable<ApiResult<Object>> m4864(@Field("username") String str, @Field("password") String str2, @Field("version") String str3, @Field("userAgent") String str4, @Field("provinceCode") String str5, @Field("randomCode") String str6);
```

### 2. 追溯password, username字段哪来的

```java
public void mo2102(String str, String str2, String str3, String str4, String str5, String str6) {
    if (this == null) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    ((LoginContract.InterfaceC1119) this.mView).showLoading();
    addDisposable(((SchoolService) RetrofitFactory
        // common.m4366可破解翻译
        .m4419(SchoolService.class, Common.m4366()))
        .m4864(str, str2, str3, str4, str5, str6)
        .compose(SchedulerUtils.m4451())
        .subscribe(new Consumer(this) {
            private final /* synthetic */ LoginPresenter f33099a;
            {
                if (this == null) {
                    Ffd45ff93.access$0();
                }
                Exist.started();
                this.f33099a = this;
            }

            @Override // 礕萻谪繘埱拎帞那泒鐁閗麣.櫼螉彬彆.阙蔬.Consumer
            public final void accept(Object obj) {
                if (this == null) {
                    Ffd45ff93.access$0();
                }
                Exist.started();
                Exist.started = Exist.enabled ? 1 : 0;
                this.f33099a.m2107((ApiResult) obj);
            }
        }, new Consumer(this) {
            private final /* synthetic */ LoginPresenter f33049a;
            {
                if (this == null) {
                    Ffd45ff93.access$0();
                }
                Exist.started();
                this.f33049a = this;
            }
            @Override // 礕萻谪繘埱拎帞那泒鐁閗麣.櫼螉彬彆.阙蔬.Consumer
            public final void accept(Object obj) {
                if (this == null) {
                    Ffd45ff93.access$0();
                }
                Exist.started();
                Exist.started = Exist.enabled ? 1 : 0;
                this.f33049a.m2112((Throwable) obj);
            }
        })
    );
}
```

### 3. 继续追溯

```java
@OnClick({R.id.btn_login, R.id.tv_forget_password, R.id.btn_schoolIn_login, R.id.btn_schoolOut_login})
public void onClickView(View view) {
    if (this == null) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    switch (view.getId()) {
        case R.id.btn_login /* 2131296407 */:
            if (m1455()) {
                return;
            }
            // username
            String obj = this.mEtUser.getText().toString();
            // m5011是password的加密算法，应该重点破解
            String m5011 = C0694.m5011(this.mEtPassword.getText().toString());
            List<SchoolList> m24509 = new DBHelper(BaseApplication.getContext()).m5395().m23917().m24443().m24509();
            if (m24509 != null && m24509.size() != 0) {
                // this.f1132是version号
                ((LoginPresenter) this.mPresenter).mo2102(obj, m5011, this.f1132, BaseApplication.setUserAgent(), this.f1135.getProvinceCode(), this.f1135.getRandomCode());
                return;
            } else {
                ToastUtil.m4944(this, "请确保网络正常，等待数据加载完成");
                return;
            }
        case R.id.btn_schoolIn_login /* 2131296416 */:
            if (m1455()) {
                return;
            }
            m1460(false);
            return;
        case R.id.btn_schoolOut_login /* 2131296417 */:
            m1460(true);
            return;
        case R.id.tv_forget_password /* 2131297548 */:
            if (TextUtils.isEmpty(this.f1141) || this.f1141 == null) {
                return;
            }
            Intent intent = new Intent(this, WebViewActivity.class);
            intent.putExtra("url", this.f1141);
            intent.putExtra("title", "密码找回");
            intent.putExtra("uid", SpfUtil.m5118(this));
            intent.putExtra("tokenUrl", "");
            startActivity(intent);
            return;
        default:
            return;
    }
}
```

### 4. 找到password的加密算法

```java
public static String m5011(String str) {
    if (str != str) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    try {
        // AES加密str,密钥为BuildUtils.m4606()
        return new String(BackAES.m22125(str, BuildUtils.m4606(), 0));
    } catch (Exception e4) {
        e4.printStackTrace();
        return "";
    }
}

// 返回login password的加密密钥
public static String m4606() {
    if (0 != 0) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    // "6d31" + "21b6" + "50e4" + "2855"
    // BuildConfig.f32015g + "21b6" + BaseApplication.getContext().getResources().getString(R.string.ak3) + ?
    return m4591() + m4593() + m4602() + ((Object) m4600());
}

// 密钥的一最后部分
public static StringBuffer m4600() {
    if (0 != 0) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    StringBuffer stringBuffer = new StringBuffer();
    // m4576(5, 571)
    stringBuffer.append(ConfigUtils.m4576(5, R2.C1322.tj));
    return stringBuffer;
}
```

计算结果为2855

```java
public static int m4576(int i4, int i5) {
    // password密钥 i4=5, i5=571
    // sign密钥 i4=5, i5=112
    if (i4 != i4) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    int i6 = 1;
    while (true) {
        int i7 = i4 * i5;
        if (i6 > i7) {
            return i7;
        }
        if (i6 % i4 == 0 && i6 % i5 == 0) {
            return i6;
        }
        i6++;
    }
    // password密钥 2855
    // sign密钥 560
}
```

### 5. 因此密钥最终为6d3121b650e42855

### 总结

以6d3121b650e42855为密钥AES非对称加密password

## 寻找sign的踪迹

### 1. 搜索"sign"

```java
private C3859.C3860 m4383(C3859 c3859) {
    if (this == null) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    return c3859.m22705()
        .m22723("Content-Type", "application/json;charset=UTF-8")
        .m22723("imei", DeviceUtils.m4569())
        .m22723(c.f11898b, DeviceUtils.m4566())
        .m22723("timestamp", this.f32023c)
        .m22723("sign", this.f32022b)
        .m22723("cgAuthorization", SPUtils.m18092(Common.f31998e).m18119("TOKEN"))
        .m22723("User-Agent", BaseApplication.setUserAgent())
        .m22723("client", DeviceUtils.m4565());
}
```

```java
private void m4382(String str) {
    if (this == null) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    String[] split = ChingoEncrypt
        .cgapiEnrypt(
            SPUtils
            .m18092(Common.f31998e) // "HEADER"
            .m18119(Common.f32005l), str) // "SECRET"
        .split("\\|");
    if (split.length > 3) {
        this.f32022b = split[3];
        this.f32023c = split[1];
    }
}
```

```java
// 返回sign值
public static String m4605() {
    if (0 != 0) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    // "262b6c001ea05beceb9d560be1dbf14f"
    // "262b6c001ea05" + "beceb9d" + "560" + "be1dbf14f"
    return m4595() + m4590() + ((Object) m4596()) + m4594();
}
```
