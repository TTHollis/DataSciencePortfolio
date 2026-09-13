import locale
from datetime import datetime
from collections import defaultdict

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class CashRegister:
    def __init__(self, total_price=0.0, item_count=0):
        self.total_price = total_price
        self.item_count = item_count
        self.items = []
        self.cash_rendered = 0.0

    def add_item(self, name, price, quantity=1):
        for _ in range(quantity):
            self.total_price += price
            self.item_count += 1
            self.items.append((name, price))

    def get_total(self):
        return self.total_price

    def get_count(self):
        return self.item_count

    def remove_item(self, name, quantity=1):
        available_quantity = self.get_item_quantity(name)
        if quantity > available_quantity:
            return f"Cannot remove {quantity} of {name}. Only {available_quantity} available."
        if available_quantity == 0:
            return f'Item "{name}" not found in cart.'

        items_to_remove = [
            (i, item_name, price)
            for i, (item_name, price) in enumerate(self.items)
            if item_name.lower() == name.lower()
        ]

        total_removed_price = 0
        removed_count = 0

        for i, item_name, price in reversed(items_to_remove[:quantity]):
            del self.items[i]
            total_removed_price += price
            removed_count += 1

        self.total_price -= total_removed_price
        self.item_count -= removed_count

        return f"Removed {removed_count} of {name}"

    def get_item_quantity(self, name):
        return sum(1 for item_name, _ in self.items if item_name.lower() == name.lower())

    def print_receipt(self):
        lines = []
        lines.append('🧾 Receipt:')
        lines.append(f'Date: {datetime.now().strftime("%m-%d-%Y %H:%M")}')
        lines.append('-' * 40)

        grouped = defaultdict(lambda: [0, 0.0])
        for name, price in self.items:
            grouped[name.lower()][0] += 1
            grouped[name.lower()][1] += price

        sorted_items = sorted(grouped.items(), key=lambda item: item[1][1], reverse=True)

        for name_lower, (count, total) in sorted_items:
            display_name = next(name for name, _ in self.items if name.lower() == name_lower)
            lines.append(f'{count}x {display_name:<16} {locale.currency(total, grouping=True):>10}')

        lines.append('-' * 40)
        lines.append(f'Total items: {self.get_count()}')
        lines.append(f'Total amount: {locale.currency(self.get_total(), grouping=True)}')
        lines.append(f'Cash rendered: {locale.currency(self.cash_rendered, grouping=True)}')

        change = self.cash_rendered - self.total_price
        if change == 0:
            lines.append("No change due.")
        else:
            lines.append(f'Change given: {locale.currency(change, grouping=True)}')

        lines.append('-' * 40)
        lines.append('Thanks for using the Python Cash Register, bye for now!')

        return "\n".join(lines)