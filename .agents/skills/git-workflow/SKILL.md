---
name: git-workflow
description: Git/GitHubを使用した開発ワークフローの標準プロセス。ブランチ戦略、コミット規約、PR運用、バージョニングなど、業界標準に基づいた開発フローを定義する。
---

# Git/GitHub 開発ワークフロー標準

このスキルは、AIエージェントがGit/GitHubを使用した開発作業を行う際に従うべき標準プロセスを定義します。

## 1. 開発ワークフロー (Standard Development Flow)

すべての機能追加・バグ修正は以下の手順に従います。
GitHub との連携には `gh` CLI を使用します。

1. **要件分析**: Issue番号が提供された場合、`gh issue view <番号>` で要件を取得し、影響範囲を特定する。
2. **ブランチ作成**: `main` から命名規則（セクション2）に従いブランチを作成する。
   ```
   git checkout -b feature/customer-search
   ```
3. **実装**: 小さく論理的な単位でコードを修正する。
4. **テスト**: サーバー起動・動作確認を行い、エビデンスを記録する。
5. **コミット**: Conventional Commits 形式でコミットする（セクション3参照）。
6. **PR作成**: `gh pr create` でPull Requestを作成する（セクション5参照）。
7. **マージ**: ユーザーの承認後、`main` にマージし、作業ブランチを削除する。
   ```
   gh pr merge <PR番号> --merge && git branch -d <ブランチ名>
   ```

## 2. ブランチ命名規則 (Branch Naming)

### フォーマット
```
<type>/<短い説明（kebab-case）>
```

### type 一覧

| type | 用途 | 例 |
|------|------|-----|
| `feature` | 新機能の追加 | `feature/customer-search` |
| `fix` | バグ修正 | `fix/stock-calculation-error` |
| `hotfix` | 本番環境の緊急修正 | `hotfix/order-status-crash` |
| `refactor` | リファクタリング | `refactor/service-layer-cleanup` |
| `docs` | ドキュメント修正 | `docs/api-readme-update` |
| `chore` | 雑務（依存関係更新等） | `chore/update-dependencies` |

### ルール
- 小文字 + ハイフン区切り（`kebab-case`）を使用する。
- ベースブランチは `main` とする。
- ブランチ名は短く説明的にする（50文字以内目安）。

## 3. コミットメッセージ (Conventional Commits)

[Conventional Commits](https://www.conventionalcommits.org/) 仕様に従います。

### フォーマット
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### type 一覧

| type | 用途 |
|------|------|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメント |
| `style` | フォーマット変更（動作に影響なし） |
| `refactor` | リファクタリング |
| `test` | テスト追加・修正 |
| `chore` | ビルド・ツール・依存関係等 |

### ルール
- `description` は命令形・現在形で記述する（例: `add`, `fix`, `update`）。
- 1行目は72文字以内とする。
- 日本語での記述を許可する。

### 例
```
feat(customer): 顧客マスターに検索機能を追加

顧客名・顧客コードの部分一致検索を実装。
検索結果は10件ごとにページネーションで表示。
```

## 4. コミット粒度 (Commit Granularity)

### ガイドライン
- **1コミット = 1つの論理的変更**とする（機能追加、バグ修正、リファクタ等を混ぜない）。
- 動作する状態でコミットする（ビルドが壊れた状態をコミットしない）。

### 運用ルール
- コミット粒度のルールはガイドラインとして参照する。
- 実際のコミット実行タイミングは、ワークフロー（セクション1）の中でユーザーの承認・指示に従う。
- エージェントは適切なコミットポイントを提案するが、ユーザーの確認なしにコミットを実行しない。

## 5. PR（Pull Request）運用ルール

### PRタイトル
Conventional Commits 形式に揃える。
```
feat(customer): 顧客マスターに検索機能を追加
```

### PR本文に含める項目
- **変更の概要**: 何を、なぜ変えたか。
- **テスト内容**: どのように検証したか。
- **スクリーンショット/エビデンス**: UI変更がある場合は必ず添付。

### PR作成コマンド
```bash
gh pr create \
  --title "feat(customer): 顧客マスターに検索機能を追加" \
  --body "## 変更の概要
...

## テスト内容
...

Closes #42"
```

> [!NOTE]
> PR本文に `Closes #<Issue番号>` を含めると、マージ時に該当 Issue が自動的にクローズされます。

## 6. バージョニング (Semantic Versioning)

リリースタグには [Semantic Versioning 2.0.0](https://semver.org/) を適用します。

### フォーマット
```
v<MAJOR>.<MINOR>.<PATCH>
```

| 部位 | インクリメント条件 |
|------|-------------------|
| MAJOR | 破壊的変更 |
| MINOR | 後方互換の新機能追加 |
| PATCH | 後方互換のバグ修正 |

例: `v1.0.0`, `v1.1.0`, `v1.1.1`

## 7. `.gitignore` 管理

- 環境固有ファイル（`.env`, `venv/`, `__pycache__/`, `.DS_Store` 等）はコミットしない。
- `.gitignore` を適切に維持し、[GitHub 公式テンプレート](https://github.com/github/gitignore)を参考にする。
- シークレット情報（APIキー、パスワード等）は絶対にリポジトリに含めない。
