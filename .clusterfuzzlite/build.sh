#!/bin/bash -eu

# Package every *_fuzzer.py with pyinstaller into $OUT using the
# Python 3.12 venv installed by the Dockerfile. Pure-Python project:
# no sanitizer preload needed in the execution wrapper.
PYBIN=/opt/fuzz-venv/bin

for fuzzer in $(find "$SRC" -name '*_fuzzer.py'); do
  fuzzer_basename=$(basename -s .py "$fuzzer")
  fuzzer_package="${fuzzer_basename}.pkg"

  "$PYBIN/pyinstaller" --distpath "$OUT" --onefile --name "$fuzzer_package" "$fuzzer"

  echo "#!/bin/sh
# LLVMFuzzerTestOneInput for fuzzer detection.
this_dir=\$(dirname \"\$0\")
\$this_dir/$fuzzer_package \$@" > "$OUT/$fuzzer_basename"
  chmod +x "$OUT/$fuzzer_basename"
done
