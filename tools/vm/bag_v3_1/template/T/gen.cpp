#include <bits/stdc++.h>
#include <chrono>
using namespace std;

#define int long long

static uint64_t seed_value() {
    if (const char* s = getenv("SEED")) {
        try { return stoull(s); } catch (...) {}
    }
    return chrono::steady_clock::now().time_since_epoch().count();
}

mt19937_64 rng(seed_value());

long long Rand(long long l, long long r) {
    return l + (long long)(rng() % (uint64_t)(r - l + 1));
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    // Generate ONE non-empty test case.
    // TEST_ID is available during duipai.sh, if you want deterministic cases:
    // long long id = getenv("TEST_ID") ? atoll(getenv("TEST_ID")) : 0;

    return 0;
}
