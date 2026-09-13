"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Đề tài: Trợ lý Quản lý Thư viện & Tài liệu (VinUni).
"""

import json
from typing import Any, Dict

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "library_query",
        "description": "Tra cứu vị trí kệ, tình trạng mượn/trả, hạn trả và số lượt gia hạn còn lại của tài liệu Thư viện VinUni theo mã sách.",
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "Mã sách cần tra cứu (ví dụ: 'BK2026001')"
                }
            },
            "required": ["book_id"]
        }
    },
    {
        "name": "renew_loan",
        "description": "Gia hạn thời gian mượn tài liệu Thư viện VinUni cho độc giả. Dùng khi sách đang được mượn và còn lượt gia hạn.",
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "Mã sách cần gia hạn (ví dụ: 'BK2026001')"
                },
                "reader_id": {
                    "type": "string",
                    "description": "Mã độc giả yêu cầu gia hạn (ví dụ: 'RD2026001')"
                },
                "extra_days": {
                    "type": "integer",
                    "description": "Số ngày muốn gia hạn thêm (ví dụ: 7)"
                }
            },
            "required": ["book_id", "reader_id", "extra_days"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "BK2026001": {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell, Peter Norvig",
        "shelf_location": "Kệ A3 - Tầng 2 - Mã kệ AI-204",
        "status": "BORROWED",
        "borrower_id": "RD2026001",
        "borrower_name": "Nguyễn Văn An",
        "due_date": "20/09/2026",
        "renewals_left": 1
    },
    "BK2026002": {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "shelf_location": "Kệ B1 - Tầng 1 - Mã kệ PY-118",
        "status": "AVAILABLE",
        "borrower_id": None,
        "borrower_name": None,
        "due_date": None,
        "renewals_left": 2
    }
}


def execute_library_query(book_id: str) -> str:
    """Thực thi tra cứu vị trí sách và tình trạng mượn/trả"""
    book = MOCK_DATABASE.get(book_id.strip().upper())
    if book:
        return json.dumps({
            "status": "SUCCESS",
            "book_id": book_id.strip().upper(),
            "data": book
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy tài liệu có mã '{book_id}' trong catalog Thư viện VinUni."
    }, ensure_ascii=False)


def execute_renew_loan(book_id: str, reader_id: str, extra_days: Any = 7) -> str:
    """Thực thi gia hạn tài liệu đang được mượn"""
    code = book_id.strip().upper()
    reader = reader_id.strip().upper()
    try:
        days = int(extra_days)
    except (TypeError, ValueError):
        days = 7

    book = MOCK_DATABASE.get(code)
    if not book:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy tài liệu có mã '{book_id}' nên không thể gia hạn."
        }, ensure_ascii=False)

    if book.get("status") != "BORROWED":
        return json.dumps({
            "status": "FAILED",
            "message": f"Sách '{book.get('title')}' đang {book.get('status')}, không cần gia hạn."
        }, ensure_ascii=False)

    if book.get("borrower_id") != reader:
        return json.dumps({
            "status": "FAILED",
            "message": f"Mã độc giả '{reader_id}' không khớp người đang mượn sách '{code}'."
        }, ensure_ascii=False)

    if int(book.get("renewals_left") or 0) <= 0:
        return json.dumps({
            "status": "FAILED",
            "message": f"Sách '{code}' đã hết lượt gia hạn."
        }, ensure_ascii=False)

    remaining = int(book["renewals_left"]) - 1
    return json.dumps({
        "status": "SUCCESS",
        "renewal_id": f"RN-{code}-99",
        "book_id": code,
        "reader_id": reader,
        "extra_days": days,
        "new_due_date": "27/09/2026",
        "renewals_left": remaining,
        "message": (
            f"Gia hạn thành công sách {code} cho độc giả {reader} thêm {days} ngày. "
            f"Hạn trả mới: 27/09/2026."
        )
    }, ensure_ascii=False)


TOOL_ROUTER = {
    "library_query": execute_library_query,
    "renew_loan": execute_renew_loan
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
