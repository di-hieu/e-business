"""Order management tools: stock check, create, lookup."""
from __future__ import annotations

import json
import time
import uuid

from langchain_core.tools import tool
from tinydb import Query, TinyDB

from app.core import analytics
from app.tenancy import TenantContext


def _orders(tenant: TenantContext) -> TinyDB:
    return TinyDB(tenant.orders_db)


def _products(tenant: TenantContext) -> TinyDB:
    return TinyDB(tenant.products_db)


# Stock per region. In production this would be a real WMS call - we mock it
# deterministically off the SKU so the demo behaves consistently.
_REGIONS = {"HN": "Hà Nội", "HCM": "TP. Hồ Chí Minh", "DN": "Đà Nẵng"}


def _stock(sku: str, region: str) -> int:
    h = abs(hash(sku.upper() + region.upper())) % 30
    return h  # 0..29


def make_order_tools(tenant: TenantContext):
    @tool
    def check_stock(sku: str, region: str) -> str:
        """Kiểm tra tồn kho sản phẩm theo khu vực giao hàng.

        `region`: mã khu vực (HN / HCM / DN). Trả về số lượng có sẵn và ETA.
        """
        region = region.upper()
        if region not in _REGIONS:
            return f"Khu vực không hỗ trợ. Chỉ nhận: {list(_REGIONS)}."
        P = Query()
        with _products(tenant) as db:
            prod = db.get(P.sku == sku.upper())
        if not prod:
            return f"Không tìm thấy sản phẩm {sku}."
        qty = _stock(sku, region)
        return json.dumps(
            {
                "sku": sku.upper(),
                "region": _REGIONS[region],
                "available_qty": qty,
                "eta_days": 2 if qty > 0 else None,
                "in_stock": qty > 0,
                "unit_price": prod.get("price"),
            },
            ensure_ascii=False,
        )

    @tool
    def create_order(
        sku: str,
        qty: int,
        customer_name: str,
        phone: str,
        address: str,
        region: str,
    ) -> str:
        """Tạo đơn hàng mới. AI phải hỏi đủ thông tin trước khi gọi tool.

        Bắt buộc: sku, qty, customer_name, phone, address, region.
        Trả về order_id và tổng tiền nếu thành công.
        """
        region = region.upper()
        if region not in _REGIONS:
            return f"Khu vực không hỗ trợ. Chỉ nhận: {list(_REGIONS)}."
        P = Query()
        with _products(tenant) as db:
            prod = db.get(P.sku == sku.upper())
        if not prod:
            return f"Không tìm thấy sản phẩm {sku}."
        if _stock(sku, region) < qty:
            return "Tồn kho không đủ cho khu vực này, đề nghị giảm số lượng hoặc đổi khu vực."

        order_id = "ORD-" + uuid.uuid4().hex[:8].upper()
        total = int(prod.get("price", 0)) * int(qty)
        record = {
            "order_id": order_id,
            "sku": sku.upper(),
            "product_name": prod.get("name"),
            "qty": qty,
            "unit_price": prod.get("price"),
            "total": total,
            "customer": {"name": customer_name, "phone": phone},
            "shipping": {"address": address, "region": _REGIONS[region]},
            "status": "confirmed",
            "created_at": time.time(),
        }
        with _orders(tenant) as db:
            db.insert(record)
        analytics.track(tenant, "order_created", {"order_id": order_id, "total": total})
        return json.dumps(
            {"order_id": order_id, "total": total, "status": "confirmed"}, ensure_ascii=False
        )

    @tool
    def lookup_order(order_id: str) -> str:
        """Tra cứu trạng thái đơn hàng theo order_id."""
        O = Query()
        with _orders(tenant) as db:
            row = db.get(O.order_id == order_id.upper())
        if not row:
            return f"Không tìm thấy đơn {order_id}."
        return json.dumps(row, ensure_ascii=False)

    return [check_stock, create_order, lookup_order]
