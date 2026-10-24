# Random malformed-SQL fuzz used in the Agent 2 review of sqlparse #885/#886 (2026-10-24).
# Usage: python3 -I fuzz.py <sqlparse checkout> <seed> <count>
import sys, itertools, random, traceback
sys.path.insert(0, sys.argv[1])
import sqlparse
atoms = ["::", "(", ")", "AS", "CASE", "WHEN", "THEN", "ELSE", "END", "WHERE", "SELECT", "a", "'a'", ":=", "1", "GO", "#", "->>", ",", "--c\n", "/*c*/", " ", "  "]
opts = [dict(strip_whitespace=True), dict(reindent=True), dict(reindent_aligned=True), dict(reindent_aligned=True, strip_whitespace=True)]
random.seed(int(sys.argv[2]))
seen = {}
for n in range(int(sys.argv[3])):
    k = random.randint(1, 8)
    sql = " ".join(random.choice(atoms) for _ in range(k))
    for o in opts:
        try:
            sqlparse.format(sql, **o)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)[-1]
            key = (type(e).__name__, tb.name, tb.lineno)
            if key not in seen:
                seen[key] = (sql, o)
for k, v in sorted(seen.items()):
    print(k, repr(v[0]), v[1])
