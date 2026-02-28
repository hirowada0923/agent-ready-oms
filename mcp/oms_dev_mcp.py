import os
import sys
import json
from dataclasses import dataclass
from typing import List, Optional

# シンプルなMCPサーバー風のインターフェース（実際にはエージェントがpython実行して利用）

class OMSDevMCP:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.protected_files = [
            "app/database.py",
            "app/models/models.py",
            "app/services/services.py"
        ]

    def list_protected_assets(self):
        """保護対象の重要ファイルリストを返します。"""
        return {
            "status": "success",
            "protected_files": self.protected_files,
            "description": "これらのファイルへの変更は、ビジネスロジックの整合性に直結するため慎重に行う必要があります。"
        }

    def verify_architecture(self, file_path: str, content: str):
        """コードが3層アーキテクチャの原則に従っているか簡易チェックします。"""
        alerts = []
        if file_path.endswith(".html") or "app/templates/" in file_path:
            if "session.query" in content or "db.execute" in content:
                alerts.append("警告: テンプレート内でデータベース操作を行おうとしています。ロジックはサービス層に逃がしてください。")
        
        if "app/main.py" in file_path:
            if "total_amount =" in content and "+" in content:
                alerts.append("通知: 合計金額の計算ロジックをエンドポイントに書こうとしています。サービス層での実装を検討してください。")
        
        return {
            "status": "success" if not alerts else "warning",
            "alerts": alerts
        }

    def analyze_impact(self, proposed_changes: List[dict]):
        """変更案が与える影響範囲を分析します。"""
        impacts = []
        for change in proposed_changes:
            path = change.get("path", "")
            if path in self.protected_files:
                impacts.append(f"CRITICAL: {path} はコア・コンポーネントです。ユーザーの承認が必須です。")
        
        return {
            "status": "success",
            "impact_report": impacts if impacts else ["特筆すべきコアロジックへの影響は見つかりませんでした。"]
        }

if __name__ == "__main__":
    # デバッグ/ツール使用例
    mcp = OMSDevMCP(os.getcwd())
    print(json.dumps(mcp.list_protected_assets(), indent=2, ensure_ascii=False))
