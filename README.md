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
本プロジェクトをAIエージェントが開発・メンテナンスする際は、必ず以下のドキュメントを確認してください。
- [AIエージェント向け引き継ぎガイド](docs/HANDOVER_FOR_AGENTS.md)
- [開発規約 (oms-dev-governance)](.agents/skills/oms-dev-governance/SKILL.md)

### 外部ツールでの MCP 設定 (Claude Desktop / Cursor 等)
プロジェクト固有のツール（在庫検証・建築分析等）を外部 AI から利用するには、MCP 設定に以下を追加します：

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
