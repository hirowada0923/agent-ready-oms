import os
import sys
from mcp.server.fastmcp import FastMCP

# 正式な MCP サーバー (FastMCP を使用)
# 実行方法: mcp run mcp/oms_dev_mcp.py
# または直接 python mcp/oms_dev_mcp.py

mcp = FastMCP("OMS-Dev-Governance")

# 重要ファイルの定義
PROTECTED_FILES = [
    "app/database.py",
    "app/models/models.py",
    "app/services/services.py"
]

@mcp.tool()
def list_protected_assets() -> str:
    """保護対象の重要ファイルリストと、その重要性についての説明を返します。"""
    files = "\n".join([f"- {f}" for f in PROTECTED_FILES])
    return f"【保護対象ファイル】\n{files}\n\n説明: これらのファイルへの変更は、ビジネスロジックの整合性に直結するため慎重に行う必要があります。"

@mcp.tool()
def verify_architecture(file_path: str, content: str) -> str:
    """
    コードが3層アーキテクチャの原則に従っているかチェックします。
    
    Args:
        file_path: チェック対象のファイルパス
        content: ファイルの内容
    """
    alerts = []
    if file_path.endswith(".html") or "app/templates/" in file_path:
        if "session.query" in content or "db.execute" in content:
            alerts.append("⚠️ 警告: テンプレート内でデータベース操作を行おうとしています。ロジックはサービス層 (app/services/) に実装してください。")
    
    if "app/main.py" in file_path:
        if "total_amount =" in content and "+" in content:
            alerts.append("ℹ️ 通知: 合計金額の計算ロジックをエンドポイントに書こうとしています。サービス層での実装を推奨します。")
    
    if not alerts:
        return "✅ アーキテクチャの原則に従っています。問題は見つかりませんでした。"
    
    return "\n".join(alerts)

@mcp.tool()
def analyze_impact(proposed_paths: list[str]) -> str:
    """
    変更案がシステムに与える影響範囲を分析します。
    
    Args:
        proposed_paths: 変更予定のファイルパス（リスト）
    """
    impacts = []
    for path in proposed_paths:
        if path in PROTECTED_FILES:
            impacts.append(f"🔴 CRITICAL: {path} はコア・コンポーネントです。このファイルへの変更は、データベースの整合性やビジネスロジックに重大な影響を与える可能性があるため、ユーザーの明示的な承認が必須です。")
    
    if not impacts:
        return "🟢 特筆すべきコアロジックへの影響は見つかりませんでした。通常の改修プロセスを進めてください。"
    
    return "\n".join(impacts)

if __name__ == "__main__":
    mcp.run()
