# Agent-Ready Order Management System (OMS)

Python (FastAPI) ベースの、AIエージェントとの協調開発に最適化された受注管理システムです。

## 🌟 特徴
- **Modern UI**: グラスモーフィズム（Soft Modern）を採用したプレミアムなデザイン。
- **Agent-Ready**: 開発規約（Skill）と物理的な制約（MCP）により、AIエージェントによる安全な自動改修が可能。
- **Robustness**: FastAPI + SQLAlchemy による型安全で安定したバックエンド。

## 🛠 セットアップ
1. **Python 環境の構築**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **データの初期化**:
   ```bash
   python seed.py
   ```
3. **サーバー起動**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🤖 AIエージェントによる開発

本プロジェクトは、AIエージェントが安全かつ自律的に開発・メンテナンスを行えるよう設計されています（Agent-Ready）。エージェントは以下のドキュメント、**Agent Skills**（振る舞いとルールの定義）、および **MCP**（検証・制御ツール）を利用してタスクを遂行します。

- 📚 [AIエージェント向け引き継ぎガイド](docs/HANDOVER_FOR_AGENTS.md)

### 🧠 Agent Skills (エージェントの自律パラメーター)
エージェントに対して、プロジェクト特有のドメイン知識や業界標準のルールを強制するスキル群です。`.agents/skills/` に定義されています。

1. **[`oms-dev-governance`](.agents/skills/oms-dev-governance/SKILL.md) (OMS開発ガバナンス)**
   受注管理システム特有のビジネスロジックやデータベースの整合性を保護するための厳格な開発規約。アーキテクチャの基本方針を定めます。
2. **[`git-workflow`](.agents/skills/git-workflow/SKILL.md) (標準Gitワークフロー)**
   Git/GitHubを用いた業界標準モデル（ブランチ戦略、Conventional Commits、Pull Requestの必須化）を強制し、`main`への直接Pushを技術的・ルール的に防止します。
3. **[`frontend-design`](.agents/skills/frontend-design/SKILL.md) (UI/UXデザイン)**
   グラスモーフィズムやモダンなタイポグラフィなど、洗練された高品質なフロントエンドUIを実装するためのデザインシステム規約です。

### 🛠 MCP (Model Context Protocol)
システムへの物理的なアクセスや、安全性の事前検証、テスト自動化を行うためのツール群です。`mcp/oms_dev_mcp.py` によってホストされます。

#### 提供されているツール (Tools)
- **`list_protected_assets`**: データベースの整合性に直結する保護対象ファイルのリストを提供します。
- **`verify_architecture`**: エージェントが提案するコードが、3層アーキテクチャの原則に違反していないか（例：テンプレート内にクエリを直書きしていないか）を静的解析します。
- **`analyze_impact`**: 変更予定のファイルがコア・コンポーネントに与える影響範囲を分析し、危険な変更を事前に警告します。
- **`seed_mock_order`**: 指定したステータス（準備中、キャンセルなど）のテスト用注文データ（関連する顧客・商品含む）を動的に生成します。
- **`reset_test_environment`**: 試行錯誤により汚染されたテスト環境のデータベースを、一瞬で安全な初期データ状態にリセット（クリーンアップ）します。

#### 外部ツールでの MCP 設定 (Claude Desktop / Cursor 等)
これらの独自ツールを外部 AI から利用するには、MCP 設定ファイルに以下を追加してください：

```json
"mcpServers": {
  "oms-dev": {
    "command": "[プロジェクトの絶対パス]/venv/bin/python",
    "args": ["[プロジェクトの絶対パス]/mcp/oms_dev_mcp.py"]
  }
}
```

## 📁 主要構成
- `app/`: アプリケーションコード（モデル、サービス、テンプレート）
- `.agents/`: AIエージェント用のメタデータとスキル定義
- `mcp/`: 開発支援・安全検証用MCPサーバー
- `docs/`: 設計文書・アーカイブ
