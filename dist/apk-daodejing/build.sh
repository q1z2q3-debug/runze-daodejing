#!/usr/bin/env bash
# 本地出包：aapt2 → javac → d8 → zipalign → apksigner，不经 gradle。
# 用法：在 dist/apk-<slug>/ 内执行  SDK_ROOT=/home/user/apkbuild/sdk ./build.sh
# 依赖：JDK 17（javac/d8 需要）、build-tools 35.0.0、platforms/android-35。
set -euo pipefail
cd "$(dirname "$0")"

SDK_ROOT=${SDK_ROOT:-/home/user/apkbuild/sdk}
JAR="$SDK_ROOT/platforms/android-35/android.jar"
BT="$SDK_ROOT/build-tools/35.0.0"

read -r CODE NAME PKG OUT < <(python3 - <<'PY'
import json
c = json.load(open('apk-config.json', encoding='utf-8'))
print(c['version_code'], c['version_name'], c['package'], c.get('out', 'apk'))
PY
)
OUTFILE="../../dist/${OUT}-v${NAME}.apk"

rm -rf build && mkdir -p build/res build/gen build/classes build/dex

# 源 Manifest 不带 package（供 gradle 的 namespace）；aapt2 手工链必须有
sed 's|<manifest xmlns:android="http://schemas.android.com/apk/res/android">|<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="'"$PKG"'">|' \
  app/src/main/AndroidManifest.xml > build/AndroidManifest.xml

"$BT/aapt2" compile --dir app/src/main/res -o build/res/resources.zip
"$BT/aapt2" link -o build/unsigned.apk \
  -I "$JAR" --manifest build/AndroidManifest.xml -A app/src/main/assets \
  --java build/gen --min-sdk-version 21 --target-sdk-version 35 \
  --version-code "$CODE" --version-name "$NAME" build/res/resources.zip

# 注意：JDK 17 的 javac 不接受 -bootclasspath 与 -target 11 并用，只用 -classpath
javac -source 11 -target 11 -encoding UTF-8 -classpath "$JAR" \
  -d build/classes $(find app/src/main/java -name '*.java')

"$BT/d8" --lib "$JAR" --min-api 21 --release --output build/dex $(find build/classes -name '*.class')

python3 - <<'PY'
import os, zipfile
src = 'build/dex/classes.dex'
with zipfile.ZipFile('build/unsigned.apk', 'a', zipfile.ZIP_DEFLATED) as z:
    z.write(src, 'classes.dex')
PY

"$BT/zipalign" -p -f 4 build/unsigned.apk build/aligned.apk

KS=.debug.keystore
if [ ! -f "$KS" ]; then
  keytool -genkeypair -keystore "$KS" -alias androiddebugkey -storepass android -keypass android \
    -dname "CN=Runze, O=Daokedao, C=CN" -keyalg RSA -keysize 2048 -validity 10000 >/dev/null 2>&1
fi

"$BT/apksigner" sign --ks "$KS" --ks-pass pass:android --key-pass pass:android \
  --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
  --out "$OUTFILE" build/aligned.apk

"$BT/apksigner" verify --print-certs "$OUTFILE" | head -4
ls -l "$OUTFILE"
sha256sum "$OUTFILE"
