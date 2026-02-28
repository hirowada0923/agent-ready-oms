# Handover Document for AI Agents

このドキュメントは、本プロジェクトを継続して開発・メンテナンスするAIエージェント（GitHub Copilot, Cursor, Antigravity etc.）のためのガイドラインです。

## 1. プロジェクトの背景と意思決定
- **技術スタックの転換**: 当初は Next.js + Prisma でしたが、安定性とシンプルさを重視し **Python (FastAPI + SQLAlchemy + SQLite)** に移行しました。
- **デザインコンセプト**: "Soft Modern / Glassmorphism"（テーマ名: Luminous Clarity）。透明感、奥行き、丸みを帯びたUIを特徴としています。
- **Agent-Ready 化**: AIエージェントが安全に開発できるよう、`mcp/` による検証ツールと `.agents/skills/oms-dev-governance` による開発規約を導入済みです。

## 2. 開発上の重要ルール
- **規約の遵守**: 変更を加える前に必ず `.agents/skills/oms-dev-governance/SKILL.md` を読み、アーキテクチャ（3層構造）を維持してください。
- **UI/UX**: 新しい画面や要素を追加する際は、`frontend-design` スキルを活用しつつ、既存の `base.html` に定義されたデザインシステムに従ってください。
- **日本語インターフェース**: ユーザーの要望により、ラベルやメッセージは原則として日本語で統一されています。

## 3. 現在の状態と次のステップ
- **実装済み**: 受注管理（ステータス遷移、在庫引き当て）、商品・顧客マスタ、ダッシュボード。
- **積み残し/改善案**:
    - 認証機能の実装（現在は未ログインで全操作可能）。
    - 受注データのCSVエクスポート機能。
    - 在庫変動履歴（ログ）の閲覧機能。

## 4. コンテキストの同期
より詳細な開発履歴（個別のタスク進捗や検証結果）を知りたい場合は、以下のアーカイブを参照してください。
- `docs/archive/task.md`: タスク完了履歴
- `docs/archive/implementation_plan.md`: 過去の設計・計画
- `docs/archive/walkthrough.md`: 動作検証の記録
