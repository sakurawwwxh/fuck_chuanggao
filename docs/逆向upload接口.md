## 逆向"api/l/v6.1/prejudgment"接口全过程

### 1. 找到接口

```java
@POST("api/l/v6.1/prejudgment")
@FormUrlEncoded
Observable<ApiResult<List<Prejudgement>>> m4892(@Field("jsonsports") String str);
```

### 2. 追溯m4892

可以得到`BackAES.m22125()`用secret的前16位作为加密密钥:

```java
public Observable<ApiResult<List<Prejudgement>>> m1984(UploadJsonSports uploadJsonSports) {
    if (this == null) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    try {
        return ((SchoolService) RetrofitFactory.m4418(SchoolService.class, Common.m4366()))
            .m4892(
                new String(
                    // jsonsports加密字符串
                    BackAES.m22125(
                        new Gson().toJson(uploadJsonSports),
                        SPUtils
                            .m18092(Common.f31998e)
                            .m18119(Common.f32005l)
                            .substring(0, 16),
                        0
                    )
                )
            );
    } catch (Exception e4) {
        e4.printStackTrace();
        return null;
    }
}
```

### m4418

应该是返回一个以"cgapp-server/"结尾的url

```java
public static String m4366() {
    if (0 != 0) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    if (ConstantUtils.f32457f.equals(SPUtils.m18092("SCHOOL").m18119("SCHOOL_CODE"))) {
        return "http://ggtypt.xjtu.edu.cn/cgapp-server/";
    }
    String m18101 = SPUtils.m18092("SCHOOL").m18101("SERVERURL", "http://cgsoft.appdemo.chingo.cn/cgapp-server/");
    if (m18101.endsWith("/")) {
        return m18101;
    }
    return m18101 + "/";
}
```

## 逆向api/l/v7/savesports接口全过程

### 1. 找到接口

```java
@POST("api/l/v7/savesports")
@FormUrlEncoded
Observable<ApiResult<SportResult>> m4871(@Field("jsonsports") String str);

// 2. 追溯jsonsports字段哪来的, 可以得到BackAES.m22125()用secret的前16位作为加密密钥
public Observable<ApiResult<SportResult>> m2008(UploadJsonSports uploadJsonSports) {
    if (this == null) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    try {
        return ((SchoolService) RetrofitFactory.m4417(SchoolService.class, Common.m4366()))
            .m4871(
                // jsonsports加密字符串
                new String(
                    BackAES.m22125(
                        new GsonBuilder()
                            .addSerializationExclusionStrategy(
                                new LitepalFieldExclusionStategy())
                            .create()
                            .toJson(uploadJsonSports),
                        SPUtils
                            .m18092(Common.f31998e)
                            .m18119(Common.f32005l)
                            .substring(0, 16),
                        0
                    )
                )
            );
    } catch (Exception e4) {
        e4.printStackTrace();
        return null;
    }
}
```

### 分析加密字符串

```java
new String(
    // AES加密
    BackAES.m22125(
        // 待加密的str
        new GsonBuilder()
            .addSerializationExclusionStrategy(
                new LitepalFieldExclusionStategy()
            )
            .create()
            .toJson(uploadJsonSports),
        // 加密密钥，应重点分析
        SPUtils.m18092(Common.f31998e) // "HEADER"
            .m18119(Common.f32005l) // "SECRET"
            // 截取前16位
            .substring(0, 16),
        0 // 一般都是0
    )
)
```

```java
public static SPUtils m18092(String str) {
    // str = "HEADER"
    if (str != str) {
        F23e576ca.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    return m18094(str, 0);
}
```

```java
public static SPUtils m18094(String str, int i4) {
    // str = "HEADER"; i4 = 0
    if (str != str) {
        F23e576ca.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    // m18093: 判断str是否全为空格
    if (m18093(str)) {
        str = "spUtils";
    }
    // str = "HEADER"; i4 = 0
    // f4589 是一个 HashMap
    SPUtils sPUtils = f4589.get(str);
    if (sPUtils == null) {
        synchronized (SPUtils.class) {
            sPUtils = f4589.get(str);
            if (sPUtils == null) {
                sPUtils = new SPUtils(str, i4);
                f4589.put(str, sPUtils);
            }
        }
    }
    return sPUtils; // new SPUtils("HEADER", 0);
}
```

```java
public SPUtils(String str, int i4) {
    // str="HEADER",i4=0
    if (this == null) {
        F23e576ca.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    // getSharedPreferences("HEADER", 0)
    this.f4590 = Utils.m260().getSharedPreferences(str, i4);
}
```

```java
public String m18119(@NonNull String str) {
    // str = "SECRET"
    if (this == null) {
        F23e576ca.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    if (str != null) {
        return m18101(str, "");
    }
    throw new NullPointerException("Argument 'key' of type String (#0 out of 1, zero-based) is marked by @android.support.annotation.NonNull but got null for it");
}
```

```java
public String m18101(@NonNull String str, String str2) {
    // str = "SECRET"; str2 = ""
    if (this == null) {
        F23e576ca.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    if (str != null) {
        // getString("SECRET", "")
        return this.f4590.getString(str, str2);
    }
    throw new NullPointerException("Argument 'key' of type String (#0 out of 2, zero-based) is marked by @android.support.annotation.NonNull but got null for it");
}
```

```java
public static String getString(Context context, String str) {
    // context="SECRET"; str=""
    if (context != context) {
        Fd391efb3.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    return getSharedPreferences(context).getString(str, "");
}
```

### 解密sign签名认证

```java
public void mo2166(final SportBean sportBean) {
    if (this == null) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    DeviceUtils.f32142c = ActivityUtils.m18138().getLocalClassName();
    UploadJsonSports uploadJsonSports = new UploadJsonSports();
    uploadJsonSports.build(sportBean, true);
    addDisposable(this.f30168a.m2008(uploadJsonSports)
        .compose(C0657.m4442(this.f30169b, "正在上传..."))
        .flatMap(new InterfaceC2985(this) {

        private final /* synthetic */ SportUploadPresenter f33122a;
        {
            if (this == null) {
                Ffd45ff93.access$0();
            }
            Exist.started();
            this.f33122a = this;
        }

        @Override
        public final Object apply(Object obj) {
            return this.f33122a.m2170(sportBean, (SportResult) obj);
        }
    }).doFinally(C1036.f33085a).doOnComplete(new Action() {
        {
            if (this == null) {
                Ffd45ff93.access$0();
            }
            Exist.started();
        }

        @Override
        public final void run() {
            SportUploadPresenter.m2164(sportBean);
        }
    }).subscribe(new Consumer(this) {

        private final /* synthetic */ SportUploadPresenter f33100a;

        {
            if (this == null) {
                Ffd45ff93.access$0();
            }
            Exist.started();
            this.f33100a = this;
        }

        @Override
        public final void accept(Object obj) {
            this.f33100a.m2167(sportBean, (String) obj);
        }
    }, new Consumer(this) {

        private final /* synthetic */ SportUploadPresenter f33153a;

        {
            if (this == null) {
                Ffd45ff93.access$0();
            }
            Exist.started();
            this.f33153a = this;
        }

        @Override
        public final void accept(Object obj) {
            this.f33153a.m2169(sportBean, (Throwable) obj);
        }
    }));
}
```

### net.crigh.cgsport.model.UploadJsonSports很关键！！

```java
public static /* synthetic */ C3862 m4416(Interceptor.InterfaceC3865 interfaceC3865) throws IOException {
    if (interfaceC3865 != interfaceC3865) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    C3859.C3860 m22705 = interfaceC3865.mo22805().m22705();
    m22705.m22723("Content-Type", "application/json;charset=UTF-8")
        .m22723("imei", DeviceUtils.m4569())
        .m22723(c.f11898b, DeviceUtils.m4566())
        .m22723("timestamp", SPUtils.m18092(Common.f31998e)
        .m18119(Common.f32003j))
        // header.sign
        .m22723("sign", SPUtils.m18092(Common.f31998e).m18119(Common.f32000g))
        .m22723("User-Agent", BaseApplication.setUserAgent())
        .m22723("client", DeviceUtils.m4565());
    if (f32044b.contains("cgapp-server")) {
        m22705.m22723("app-key", BuildUtils.m4599());
    } else {
        m22705.m22723("app-key", BuildUtils.m4597());
    }
    return interfaceC3865.mo22808(m22705.m22726());
}
```

## app-key的计算

```java
public static String m4599() {
    if (0 != 0) {
        Ffd45ff93.access$0();
    }
    Exist.started();
    Exist.started = Exist.enabled ? 1 : 0;
    // "azk3t4jrcfm5772t"
    // "azk3t4" + "jrcfm" + m4576(481, 12) + "t"
    return m4607() + m4609() + ((Object) m4608()) + m4598();
}
```
