# Preserved recomputation negatives

1. **Initial range-hash attempt:** 0/17 under LF-joined UTF-8 with no final LF; guarded execution threw.
2. **False-positive shell text:** an unconditional `PASS` string was printed after the throw. It is not a successful result.
3. **Diagnostic shell syntax:** a separately entered `else` token failed as a PowerShell command; the subsequent combined `if/else` executed successfully.
4. **Transport serialization:** `git show | Set-Content -NoNewline` did not reproduce the Git blob; later raw `git cat-file blob ... > file` exports did.

None of these events changes Run 003 semantic findings. They are preserved because they expose transport and recomputation boundaries.
