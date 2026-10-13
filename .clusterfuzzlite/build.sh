#!/bin/bash -eu

# Build and install the project so the fuzz targets can import it.
pip3 install .

# Package every *_fuzzer.py with pyinstaller into $OUT. Pure-Python
# project: no sanitizer preload needed in the execution wrapper.
for fuzzer in $(find "$SRC" -name '*_fuzzer.py'); do
  fuzzer_basename=$(basename -s .py "$fuzzer")
  fuzzer_package="${fuzzer_basename}.pkg"

  pyinstaller --distpath "$OUT" --onefile --name "$fuzzer_package" "$fuzzer"

  echo "#!/bin/sh
# LLVMFuzzerTestOneInput for fuzzer detection.
this_dir=\$(dirname \"\$0\")
\$this_dir/$fuzzer_package \$@" > "$OUT/$fuzzer_basename"
  chmod +x "$OUT/$fuzzer_basename"
done
