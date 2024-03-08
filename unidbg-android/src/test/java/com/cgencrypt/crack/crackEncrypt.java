package com.cgencrypt.crack;

import com.github.unidbg.Module;
import com.github.unidbg.arm.ARMEmulator;
import com.github.unidbg.arm.backend.Unicorn2Factory;
import com.github.unidbg.linux.android.AndroidARMEmulator;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.AbstractJni;
import com.github.unidbg.linux.android.dvm.DalvikModule;
import com.github.unidbg.linux.android.dvm.DvmClass;
import com.github.unidbg.linux.android.dvm.VM;
import com.github.unidbg.memory.Memory;

import java.io.File;
import java.io.IOException;

public class crackEncrypt extends AbstractJni {
    private final ARMEmulator emulator; // ARM模拟器
    private final VM vm; // vm
    private final Module module; // 载入的模块
    private final DvmClass TTEncryptUtils;
    private String arg1;
    private String arg2;

    public crackEncrypt(String arg1, String arg2) throws IOException {
        this.arg1 = arg1;
        this.arg2 = arg2;
        // 需要调用的so文件所在路径
        String soFilePath = getPath() + "/src/test/resources/myso/libAMapSDK_Location_v6_6_0.so";
        // 需要调用函数所在的Java类完整路径，比如a/b/c/d等等，注意需要用/代替.
        String classPath = "net/crigh/api/encrypt/ChingoEncrypt";
        // 创建app进程
        String apkPath = getPath() + "/src/test/resources/创高体育_2.9.8.apk";
        // 创建模拟器实例,进程名建议依照实际进程名填写，可以规避针对进程名的校验
        emulator = AndroidEmulatorBuilder.for32Bit()
                .setProcessName("com.wubba.labba.dub.dub")
                .addBackendFactory(new Unicorn2Factory(true))
                .build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        // 获取模拟器的内存操作接口
        Memory memory = emulator.getMemory();
        // 设置系统类库解析: 作者支持19和23两个sdk
        memory.setLibraryResolver(new AndroidResolver(23));
        // 创建Android虚拟机，传入APK，Unidbg可以替我们做部分签名校验的工作
//        vm = ((AndroidARMEmulator) emulator).createDalvikVM((File) null);
        vm = ((AndroidARMEmulator) emulator).createDalvikVM(new File(apkPath));
        // 打印日志
        vm.setVerbose(true);
        // 设置JNI
        vm.setJni(this);
        // （关键处1）加载so，填写so的文件路径
        DalvikModule dm = vm.loadLibrary(new File(soFilePath), false);
        // 调用JNI OnLoad
        dm.callJNI_OnLoad(emulator);
        module = dm.getModule();
        // （关键处2）加载so文件中的哪个类，填写完整的类路径
        TTEncryptUtils = vm.resolveClass(classPath);
    }

    public static void main(String[] args) throws IOException {
        // 在这里定义需要从python传过来的值
        String arg1 = System.getProperty("arg1");
        String arg2 = System.getProperty("arg2");
        crackEncrypt chingoCrackEncrypt = new crackEncrypt(arg1, arg2);
        // 输出调用结果 result
        System.out.println(chingoCrackEncrypt.calc());
        System.out.println("--------------------------");
    }

    public static String getPath() {
        String path = crackEncrypt.class.getProtectionDomain().getCodeSource().getLocation().getPath();
        if (System.getProperty("os.name").contains("dows")) {
            path = path.substring(1);
        }
        if (path.contains("jar")) {
            path = path.substring(0, path.lastIndexOf("."));
            return path.substring(0, path.lastIndexOf("/"));
        }

        return path.replace("/target/test-classes/", "");
    }

    public String calc() throws IOException {
        if (this.arg1 == null || this.arg2 == null) {
            this.arg1 = "AAAANECTVm4Fm9JozjVjXJKKPo/+/zpAtocm0RKClXOlCwmRJhIck/2PqzN/1i2cuU/8zw==";
            this.arg2 = "/api/l/v6/prejudgment?jsonsports=";
        }
        // 需要调用方法,再jadx中找到对应的方法，然后点击下面的Smail,复制方法的Smail代码。
        String methodSign = "cgapiEnrypt(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;";
        // 调用so里面的方法
        String result = this.myJni(methodSign, this.arg1, this.arg2);
        this.destroy();
        System.out.println("--------------------------");
        return result;
    }

    /**
     * 调用so文件中的指定函数
     *
     * @param methodSign 传入你要执行的函数信息，需要完整的smali语法格式的函数签名
     * @param args       是即将调用的函数需要的参数
     * @return 函数调用结果
     */
    private String myJni(String methodSign, Object... args) {
        // 使用jni调用传入的函数签名对应的方法（）
        Object value = TTEncryptUtils.callStaticJniMethodObject(emulator, methodSign, args).getValue();
        return value.toString();
    }

    /**
     * 关闭模拟器
     *
     * @throws IOException
     */
    private void destroy() throws IOException {
        emulator.close();
        System.out.println("emulator destroy...");
    }
}
