let android_log_write = new NativeFunction(
    Module.getExportByName(null, '__android_log_write'),
    'int',
    ['int', 'pointer', 'pointer']
);

let tag = Memory.allocUtf8String("[frida-script]");
let i = 0;
let work = function() {
    setTimeout(function() {
        android_log_write(3, tag, Memory.allocUtf8String(`[${Date.now()}] Hello from frida + madgadget`));
        if (i++ < 99) {
            work();
        }
    }, 1000);
}

work();
