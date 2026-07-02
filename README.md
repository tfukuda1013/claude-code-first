# claude-code-first

Claude Code入門用のリポジトリです。

## calculator.py

シンプルな電卓CLIツール。

```
python3 calculator.py 3 + 5
python3 calculator.py 2 ^ 10
```

対応演算子: `+` `-` `*` `/` `^`

## テスト

```
pip install pytest
python3 -m pytest test_calculator.py -v
```