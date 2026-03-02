import os
import sys
from mcp.server.fastmcp import FastMCP
from app.database import SessionLocal, engine, Base
from app.services.services import OrderService, MasterService
from app.models.models import Customer, Product
from seed import seed_data

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

@mcp.tool()
def seed_mock_order(status: str = "未対応", items_count: int = 1, customer_id: int = None) -> str:
    """
    指定したステータスのテスト用注文データを、必要な関連データ（顧客、商品）を含めてDBに自動生成します。
    エージェントが自律的に特定のステータス（例：「準備中」や「キャンセル」）でのAPIやUIの挙動をテストする際に利用します。
    
    Args:
        status: 生成する注文のステータス（未対応, 準備中, 出荷済, 完了, キャンセル など）
        items_count: 注文に含める商品の種類数
        customer_id: 既存の顧客IDを指定する場合（None の場合はテスト用顧客を自動生成します）
        
    Returns:
        str: 生成された注文のサマリー（注文番号、合計金額、最終ステータス）
    """
    db = SessionLocal()
    try:
        # 1. 顧客の特定またはモック作成
        if not customer_id:
            mock_customer = MasterService.create_customer(
                db, 
                name=f"Mock Customer ({status})", 
                address="Test Address", 
                contact="090-0000-0000", 
                name_kana="モック カスタマー"
            )
            customer_id = mock_customer.id

        # 2. テスト用商品のモック作成（必要な数だけ）
        items_data = []
        for i in range(items_count):
            mock_product = MasterService.create_product(
                db, 
                name=f"Mock Product {i+1} for {status}", 
                price=1000 * (i + 1), 
                stock=999 # 在庫不足エラーを避けるために多めに設定
            )
            items_data.append({"product_id": mock_product.id, "quantity": 1})

        # 3. 注文の作成
        new_order = OrderService.create_order(db, customer_id, items_data)
        
        # 4. 指定されたステータスへの上書き (デフォルト以外のステータスが指定された場合)
        if status != "未対応":
            new_order = OrderService.update_status(db, new_order.id, status)
            
        summary = (
            f"✅ モック注文データの生成に成功しました:\n"
            f"- 注文番号: {new_order.order_number}\n"
            f"- ステータス: {new_order.status}\n"
            f"- 合計金額: {new_order.total_amount} 円\n"
            f"- 顧客ID: {new_order.customer_id}\n"
            f"- 作成されたモック商品数: {items_count}"
        )
        return summary
        
    except Exception as e:
        return f"❌ テストデータの生成に失敗しました: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def reset_test_environment() -> str:
    """
    テスト環境のデータベースを完全に初期状態（シードデータのみが存在する状態）にリセットします。
    エージェントがテスト用データを大量に生成したあとや、データベースが汚染された場合に呼び出してクリーンアップを行います。
    
    警告: この操作は現在のデータベース内のすべてのレコード（モックテストで作成した注文や新機能で追加したデータなど）を完全に削除し、初期状態にロールバックします。
    
    Returns:
        str: リセット処理の結果メッセージ
    """
    try:
        # テーブルの全削除と再作成
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        # シードデータの再投入
        seed_data()
        
        return "✅ データベースを初期状態（シード状態）にリセットしました。すべてのモックデータは削除されました。"
    except Exception as e:
        return f"❌ テスト環境のリセットに失敗しました: {str(e)}"

if __name__ == "__main__":
    mcp.run()
