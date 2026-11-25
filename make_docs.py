from pathlib import Path

docs = {
    "returns.md": "Desert Mart returns policy. Customers can return most items within 30 days of purchase with a receipt. Electronics must be returned within 14 days and must be unopened. Food and perishable items cannot be returned unless they are damaged or expired.",
    "refunds.md": "Desert Mart refunds policy. Refunds go back to the original payment method. Card refunds take 5 to 7 working days. Cash purchases are refunded in cash at the store. Customers without a receipt get store credit only.",
    "delivery.md": "Desert Mart delivery policy. Standard delivery in Dubai takes 1 to 2 days and is free on orders above AED 100. Orders below AED 100 pay a delivery fee of AED 15. Express delivery within 2 hours costs AED 25 and is available from 8 AM to 10 PM.",
    "loyalty.md": "Desert Mart loyalty program. Members earn 1 point for every AED 10 spent. 100 points can be used as AED 5 off the next purchase. Points expire after 12 months if the account is not used.",
    "damaged_items.md": "Desert Mart damaged items policy. If an item arrives damaged, the customer must report it within 48 hours with a photo. Desert Mart will send a free replacement or give a full refund. The customer does not need to return the damaged item.",
    "store_hours.md": "Desert Mart store hours. Stores are open from 8 AM to 11 PM, Saturday to Thursday. On Friday, stores open at 2 PM and close at 11 PM. During Ramadan, store hours change and are shared on the website.",
}

folder = Path("data/docs")
folder.mkdir(parents=True, exist_ok=True)
for name, text in docs.items():
    (folder / name).write_text(text)
print(f"Created {len(docs)} docs in {folder}")