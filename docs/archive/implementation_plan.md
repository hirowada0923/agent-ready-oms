# Python版 受注管理システム (OMS) 実装計画

Next.js + Prisma 7 から、より枯れていて安定した **Python (FastAPI + SQLAlchemy + SQLite)** のスタックへ移行します。

## 構成案
- **Framework**: FastAPI (現代的で高速、型安全なWebフレームワーク)
- **ORM**: SQLAlchemy (Pythonにおけるデファクトスタンダード)
- **Database**: SQLite (軽量・単一ファイル)
- **Frontend**: Jinja2 Templates + Tailwind CSS (プレミアムなUIデザインを維持)

## 3層アーキテクチャ設計
1. **Presentation Layer**: FastAPI Endpoints + Jinja2 (HTML/Tailwind)
2. **Business Logic Layer**: `services/` (受注バリデーション、在庫計算、トランザクション管理)
3. **Data Access Layer**: `models/` (SQLAlchemy Models), `database.py`

## 改訂後のディレクトリ構成
```bash
.
├── app/
│   ├── main.py          # エントリポイント
│   ├── database.py      # DB接続設定
│   ├── models/          # DAL: SQLAlchemyデータモデル
│   ├── services/        # BLL: ビジネスロジック (在庫チェック等)
│   ├── templates/       # PL: Jinja2テンプレート
│   └── static/          # 静的ファイル (CSS/JS)
├── requirements.txt
└── .env
```

## 予定される主要機能 (再実装)
- **受注管理**: 顧客・商品選択、在庫チェックを伴う受注登録。
- **マスタ管理**: 商品（単価・在庫）、顧客のCRUD。**既存在庫の調整機能**を追加。
- **ダッシュボード**: 統計情報の視覚化。

## Agent-ready 構成 (安全な追加開発)
AIエージェントが自律的に、かつ安全にシステムを改修・運用するための基盤を導入しました。

### 1. Agent Skill (論理的ガードレール)
- **oms-dev-governance**: `.agents/skills/` 配下に配置された開発規約。ビジネスロジックやデータベースの直接・無断な書き換えを禁止し、必ず「提案→承認→実行」のプロセスを踏むよう指示します。

### 2. MCP サーバー (物理的ガードレール)
- **Development MCP**: `mcp/` ディレクトリに配置された Python ベースのツール。ファイルの整合性チェックや影響分析を行い、開発時の安全性を高めます。

## 検証プラン
### 自動テスト
- `pytest` を使用したサービス層のユニットテスト。
### 手動検証
- ブラウザを使用したUI操作。
- **Agent検証**: エージェントに擬似的な修正を指示し、規約（Skill）や検証（MCP）が機能することを確認。
### 3. UI/UX デザイン基準の永続化
- **デザインシステムの明文化**: `oms-dev-governance` スキルに、今回決定した「Soft Modern / Glassmorphism」の基準（配色、フォント、レイアウト等）を統合します。これにより、誰が開発しても一貫したプレミアムなデザインが維持されます。
### 4. AIエージェント向け引き継ぎドキュメントの永続化
- **Handover Document**: チャット履歴にのみ存在する設計判断や技術的負債、今後の展望を `docs/HANDOVER_FOR_AGENTS.md` に集約し、新しいエージェントが即座にコンテキストを同期できるようにします。
- **Artifacts Sync**: `task.md` や `implementation_plan.md` などのシステム生成ドキュメントを `docs/` 配下にコピーし、リポジトリ自体が開発の歴史を保持するようにします。
