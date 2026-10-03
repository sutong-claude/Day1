#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d /tmp/bag_selftest_XXXXXX)"
trap 'rm -rf "$TMP"' EXIT
cp -a "$HERE/." "$TMP/"
cd "$TMP"
rm -rf samples .work .check failcase sample_fail bin obj; mkdir samples
cat > main.cpp <<'CPP'
#include <bits/stdc++.h>
using namespace std; int main(){long long n,x,s=0;if(!(cin>>n))return 0;while(n--&&cin>>x)s+=x;cout<<s<<'\n';}
CPP
cp main.cpp AC.cpp
cat > gen.cpp <<'CPP'
#include <bits/stdc++.h>
using namespace std;int main(){unsigned long long s=getenv("SEED")?strtoull(getenv("SEED"),0,10):1;mt19937_64 r(s);int n=1+r()%20;cout<<n<<'\n';for(int i=0;i<n;i++)cout<<(long long)(r()%201)-100<<(i+1==n?'\n':' ');}
CPP
printf '5\n1 2 3 4 5\n' > samples/basic.in
printf '15\n' > samples/basic.out
bash run.sh >/dev/null
python3 stress_runner.py 100 --progress 0 >/dev/null
python3 runner.py --sanitize --limit 1 >/dev/null
python3 - <<'PY'
import xml.etree.ElementTree as ET
p=ET.parse('AC.cbp'); units=[u.attrib.get('filename') for u in p.getroot().find('Project').findall('Unit')]
assert units==['main.cpp'], units
PY
CB="SKIP"
if command -v codeblocks >/dev/null 2>&1 && [ -n "${DISPLAY:-}" ]; then
    rm -rf bin obj
    if timeout 30 codeblocks --no-splash-screen --build --target=Debug AC.cbp >/tmp/bag_codeblocks_selftest.log 2>&1; then
        if [ -x bin/Debug/main ]; then CB="PASS"; else CB="FAIL(no binary)"; fi
    else
        CB="FAIL(build command)"
        cat /tmp/bag_codeblocks_selftest.log >&2 || true
        exit 1
    fi
fi
echo "SELFTEST: PASS (sample runner + 100 stress tests + ASan/UBSan + project XML; Code::Blocks=$CB)"
