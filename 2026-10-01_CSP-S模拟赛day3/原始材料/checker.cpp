// Local construction checker: checker <input_file> <output_file>
// NO is skipped. This program does not decide whether a solution exists.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

using namespace std;

// Read a whole integer token; reject overflow and tokens such as "12abc".
bool read_integer(istream& stream, long long& value) {
    string token;
    if (!(stream >> token)) return false;
    istringstream parser(token);
    return bool(parser >> value) && parser.eof();
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <input_file> <output_file>\n";
        return 2;
    }
    ifstream fin(argv[1]), fout(argv[2]);
    if (!fin || !fout) {
        cerr << "Error: Cannot open " << (!fin ? "input" : "output") << " file.\n";
        return 2;
    }

    long long tests;
    if (!read_integer(fin, tests) || tests < 1 || tests > 10000) {
        cerr << "Error: Invalid test case count.\n";
        return 2;
    }
    int checked = 0, skipped = 0;
    long long total_length = 0;
    for (int tc = 1; tc <= tests; ++tc) {
        long long n;
        string s;
        if (!read_integer(fin, n) || n < 1 || n > 1000000 ||
            !(fin >> s) || s.size() != static_cast<size_t>(n) ||
            s.find_first_not_of("abcdefghijklmnopqrstuvwxyz") != string::npos ||
            (total_length += n) > 1000000) {
            cerr << "Error: Invalid input at test case #" << tc << ".\n";
            return 2;
        }

        cout << "Test Case #" << tc << ": ";
        string verdict;
        if (!(fout >> verdict)) {
            cout << "WA (Unexpected end of output)\n";
            return 1;
        }
        if (verdict == "NO") {
            cout << "Skipped (NO is not verified)\n";
            ++skipped;
            continue;
        }
        if (verdict != "YES") {
            cout << "WA (Expected uppercase YES or NO)\n";
            return 1;
        }
        long long l, r;
        if (!read_integer(fout, l) || !read_integer(fout, r)) {
            cout << "WA (Expected two integers after YES)\n";
            return 1;
        }
        if (l < 1 || l > r || r > n) {
            cout << "WA (Interval must satisfy 1 <= l <= r <= n)\n";
            return 1;
        }

        reverse(s.begin() + l - 1, s.begin() + r);
        string remaining;
        remaining.reserve(s.size());
        for (char c : s) {
            if (!remaining.empty() && remaining.back() == c)
                remaining.pop_back();
            else
                remaining.push_back(c);
        }
        if (!remaining.empty()) {
            cout << "WA (The reversed string cannot be fully erased; "
                 << remaining.size() << " characters remain)\n";
            return 1;
        }
        cout << "AC (Construction valid)\n";
        ++checked;
    }

    string extra;
    if (fin >> extra) {
        cerr << "Error: Extra data in input file.\n";
        return 2;
    }
    if (fout >> extra) {
        cout << "WA (Extra output after the last test case)\n";
        return 1;
    }
    cout << "Checked " << checked << " YES construction(s); skipped "
         << skipped << " NO answer(s).\n";
    if (checked) cout << "All checked constructions are valid.\n";
    else cout << "No constructions were checked.\n";
    if (skipped) cout << "NO answers are not verified; this is not a full verdict.\n";
    return 0;
}