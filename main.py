import sys
import types

if 'wsgiref' not in sys.modules:
    _wsgiref = types.ModuleType('wsgiref')
    _wsgiref_simple_server = types.ModuleType('wsgiref.simple_server')
    _wsgiref_simple_server.WSGIServer = None
    _wsgiref_simple_server.WSGIRequestHandler = None
    _wsgiref_simple_server.make_server = lambda *args, **kwargs: None
    _wsgiref.simple_server = _wsgiref_simple_server
    sys.modules['wsgiref'] = _wsgiref
    sys.modules['wsgiref.simple_server'] = _wsgiref_simple_server
# ===================================

import os
import sys
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import flet as ft
# === ЗАШИФРОВАННЫЕ ДАННЫЕ ===
_ENCRYPTED_SHEET_ID = "a+R1RLxhwi29xQyl63EnzXfLdkaEVPZZs/cL5c0rAPYgylM6xUfCAcfABu8="
_ENCRYPTED_SHEET_NAME = "igvvwTiXZNohNJRc"

_ENCRYPTED_CREDENTIALS = (
    "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"
)

SUPPLIERS_SHEET_NAME = "Поставщики"

# === ПУТИ (адаптация под Android) === ← ANDROID
def _get_cache_dir() -> str:
    """Возвращает папку для кэша (работает на ПК и Android)"""
    if platform.system() == "Android" or "ANDROID_STORAGE" in os.environ:
        # На Android — в домашней папке пользователя
        return os.path.expanduser("~")
    else:
        # На ПК — рядом со скриптом
        return os.path.dirname(os.path.abspath(__file__))

CACHE_FILE = os.path.join(_get_cache_dir(), "products_cache.json")

# === КЛЮЧ ШИФРОВАНИЯ (обфусцирован) ===
_WINDOW_CONFIG = {'width': 90, 'height': 156, 'padding': 63, 'spacing': 113}

def _init_window_settings():
    return bytes([_WINDOW_CONFIG['width'], _WINDOW_CONFIG['height'],
                  _WINDOW_CONFIG['padding'], _WINDOW_CONFIG['spacing']])

_WIDGET_REGISTRY = {'btn_refresh': 232, 'btn_save': 45, 'btn_clear': 180, 'btn_add': 106}

def _init_widget_ids():
    return bytes([_WIDGET_REGISTRY['btn_refresh'], _WIDGET_REGISTRY['btn_save'],
                  _WIDGET_REGISTRY['btn_clear'], _WIDGET_REGISTRY['btn_add']])

class _ThemeEngine:
    ACCENT_PRIMARY = "#F18345"
    ACCENT_SECONDARY = "#D79E1B"
    
    @staticmethod
    def extract_key_part():
        return bytes.fromhex(_ThemeEngine.ACCENT_PRIMARY[1:] + _ThemeEngine.ACCENT_SECONDARY[1:3])

_LAYOUT_COORDS = {'x_offset': 158, 'y_offset': 27, 'panel_width': 108, 'panel_height': 162}

def _init_layout_params():
    return bytes([_LAYOUT_COORDS['x_offset'], _LAYOUT_COORDS['y_offset'],
                  _LAYOUT_COORDS['panel_width'], _LAYOUT_COORDS['panel_height']])

def _assemble_security_key():
    return (_init_window_settings() + _init_widget_ids() +
            _ThemeEngine.extract_key_part() + _init_layout_params())

def _decrypt_payload(encrypted_b64: str, key: bytes) -> str:
    try:
        encrypted_bytes = base64.b64decode(encrypted_b64)
        decrypted = bytes([encrypted_bytes[i] ^ key[i % len(key)]
                           for i in range(len(encrypted_bytes))])
        return decrypted.decode('utf-8')
    except Exception:
        return ""

_SECURITY_KEY = _assemble_security_key()
GOOGLE_SHEET_ID = _decrypt_payload(_ENCRYPTED_SHEET_ID, _SECURITY_KEY)
SHEET_NAME = _decrypt_payload(_ENCRYPTED_SHEET_NAME, _SECURITY_KEY)

def _load_credentials() -> dict:
    try:
        json_str = _decrypt_payload(_ENCRYPTED_CREDENTIALS, _SECURITY_KEY)
        if not json_str:
            raise Exception("Не удалось дешифровать credentials")
        return json.loads(json_str)
    except Exception as e:
        print(f"Ошибка загрузки credentials: {e}")
        return {}


class Palette:
    BG_DARK = "#0a0e27"
    BG_PANEL = "#151b3d"
    BG_PANEL_ALT = "#1a2040"
    BORDER = "#3d4a7c"
    BORDER_LIGHT = "#2a3560"
    ACCENT_BLUE = "#7b8ec9"
    ACCENT_PURPLE = "#9b59b6"
    ACCENT_GREEN = "#2ecc71"
    ACCENT_GREEN_DARK = "#27ae60"
    ACCENT_RED = "#e74c3c"
    ACCENT_CYAN = "#3498db"
    ACCENT_ORANGE = "#f39c12"
    TEXT_PRIMARY = "#e0e6ed"
    TEXT_SECONDARY = "#b8c5d6"
    TEXT_MUTED = "#7b8ec9"


class GoogleSheetsSync:
    def __init__(self):
        self.client = None
        self.order_sheet = None
        self.connected = False
        self._connect()

    def _connect(self):
        try:
            creds_dict = _load_credentials()
            if not creds_dict:
                print("❌ Credentials не загружены")
                return
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            self.client = gspread.authorize(creds)
            self.order_sheet = self.client.open_by_key(GOOGLE_SHEET_ID).worksheet(SHEET_NAME)
            self.connected = True
            print("✅ Подключение к Google Sheets установлено")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.connected = False

    def load_products_from_sheet(self) -> dict:
        if not self.connected:
            raise Exception("Нет подключения")
        try:
            sheet = self.client.open_by_key(GOOGLE_SHEET_ID).worksheet(SUPPLIERS_SHEET_NAME)
            all_values = sheet.get_all_values()
        except Exception as e:
            raise Exception(f"Не удалось прочитать лист '{SUPPLIERS_SHEET_NAME}': {e}")

        if not all_values or len(all_values) < 2:
            raise Exception("Лист поставщиков пуст")

        products_by_supplier = {}
        current_supplier = None

        for row in all_values[1:]:
            if len(row) < 2:
                continue
            product = row[0].strip()
            supplier = row[1].strip()
            if supplier:
                current_supplier = supplier
            if product and current_supplier:
                products_by_supplier.setdefault(current_supplier, []).append(product)

        if not products_by_supplier:
            raise Exception("Не удалось распарсить данные поставщиков")
        return products_by_supplier

    def find_cell_and_write(self, supplier: str, location: str, text: str):
        if not self.connected:
            raise Exception("Нет подключения")
        try:
            supplier_col = self.order_sheet.col_values(1)
            supplier_row = None
            for idx, val in enumerate(supplier_col, 1):
                if val.strip() == supplier:
                    supplier_row = idx
                    break
            if not supplier_row:
                raise Exception(f"Поставщик '{supplier}' не найден")

            location_row = self.order_sheet.row_values(1)
            location_col = None
            for idx, val in enumerate(location_row, 1):
                if val.strip() == location:
                    location_col = idx
                    break
            if not location_col:
                raise Exception(f"Точка '{location}' не найдена")

            current_value = self.order_sheet.cell(supplier_row, location_col).value or ""
            new_value = f"{current_value}\n{text}" if current_value else text
            self.order_sheet.update_cell(supplier_row, location_col, new_value)
            return True
        except Exception as e:
            raise Exception(f"Ошибка записи: {str(e)}")


class ProductsManager:
    def __init__(self, sheets_sync: GoogleSheetsSync):
        self.sync = sheets_sync
        self.products_by_supplier = {}
        self.suppliers_info = {}
        self.last_source = "не загружено"
        self.refresh()

    def refresh(self) -> tuple:
        if self.sync.connected:
            try:
                data = self.sync.load_products_from_sheet()
                self.products_by_supplier = data
                self._build_suppliers_info()
                self._save_cache()
                self.last_source = "БД Товаров"
                return True, f"✅ Загружено: {sum(len(v) for v in data.values())} товаров"
            except Exception as e:
                print(f"Ошибка загрузки: {e}")

        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                self.products_by_supplier = cache.get('products', {})
                self._build_suppliers_info()
                self.last_source = "кэш (оффлайн)"
                return False, f"⚠️ Кэш: {sum(len(v) for v in self.products_by_supplier.values())} товаров"
            except Exception as e:
                print(f"Ошибка чтения кэша: {e}")

        self.products_by_supplier = {}
        self.suppliers_info = {}
        self.last_source = "нет данных"
        return False, "❌ Нет сети и кэша"

    def _build_suppliers_info(self):
        self.suppliers_info = {}
        for supplier, products in self.products_by_supplier.items():
            brands = sorted({p.split()[0] for p in products if p})
            preview = ", ".join(brands[:6])
            if len(brands) > 6:
                preview += f" ... (+{len(brands) - 6})"
            self.suppliers_info[supplier] = preview or "—"

    def _save_cache(self):
        try:
            cache = {'products': self.products_by_supplier, 'source': self.last_source}
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения кэша: {e}")


def main(page: ft.Page):
    page.title = "QFACT.SUPPLIES"
    # Убираем жёсткие размеры окна — на Android они игнорируются  ← ANDROID
    page.padding = 10
    page.spacing = 8
    page.bgcolor = Palette.BG_DARK
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO  # Прокрутка всей страницы  ← ANDROID

    sheets_sync = GoogleSheetsSync()
    products_mgr = ProductsManager(sheets_sync)
    cart_items = []
    LOCATIONS = ["Светланская", "Трамвайная", "Сахалинская", "Русская", "Ульяновская", "Чуркин"]
    current_location = LOCATIONS[0]

    def show_snackbar(message: str):
        sb = ft.SnackBar(
            content=ft.Text(message, color=Palette.TEXT_PRIMARY),
            bgcolor=Palette.BG_PANEL,
            action="OK",
        )
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def update_location_lock():
        if cart_items:
            location_dd.disabled = True
            location_dd.tooltip = "⚠️ Точка заблокирована"
        else:
            location_dd.disabled = False
            location_dd.tooltip = None
        location_dd.update()

    def update_products_for_supplier():
        supplier = supplier_dd.value
        product_dd.options.clear()
        product_dd.value = None
        if supplier and supplier in products_mgr.products_by_supplier:
            products = products_mgr.products_by_supplier[supplier]
            for p in products:
                product_dd.options.append(ft.dropdown.Option(key=p, text=p))
            if product_dd.options:
                product_dd.value = product_dd.options[0].key
        product_dd.update()

    def on_supplier_select(e):
        update_products_for_supplier()

    def on_location_select(e):
        global current_location
        if cart_items:
            location_dd.value = current_location
            location_dd.update()
            show_snackbar("⚠️ Нельзя менять точку, пока в корзине есть товары.")
            return
        current_location = location_dd.value

    status_label = ft.Text(
        "✅ Подключён" if sheets_sync.connected else "❌ Нет подключения",
        color=Palette.ACCENT_GREEN if sheets_sync.connected else Palette.ACCENT_RED,
        size=12
    )
    source_label = ft.Text(f"Источник: {products_mgr.last_source}", color=Palette.ACCENT_BLUE, size=11)

    # АДАПТИВНЫЕ РАЗМЕРЫ — expand=True вместо width=...  ← ANDROID
    location_dd = ft.Dropdown(
        label="📍 Точка",
        options=[ft.dropdown.Option(key=loc, text=loc) for loc in LOCATIONS],
        value=LOCATIONS[0],
        expand=True,
        bgcolor=Palette.BG_PANEL,
        color=Palette.TEXT_PRIMARY,
        border_color=Palette.BORDER,
    )
    location_dd.on_select = on_location_select

    supplier_dd = ft.Dropdown(
        label="📦 Поставщик",
        options=[],
        expand=True,
        bgcolor=Palette.BG_PANEL,
        color=Palette.TEXT_PRIMARY,
        border_color=Palette.BORDER,
    )
    supplier_dd.on_select = on_supplier_select

    product_dd = ft.Dropdown(
        label="🛒 Товар",
        options=[],
        expand=True,
        bgcolor=Palette.BG_PANEL,
        color=Palette.TEXT_PRIMARY,
        border_color=Palette.BORDER,
    )

    qty_field = ft.TextField(
        label="Кол-во",
        value="1",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor=Palette.BG_PANEL,
        color=Palette.TEXT_PRIMARY,
        border_color=Palette.BORDER,
    )

    cart_list = ft.ListView(expand=True, spacing=4, auto_scroll=False)

    def add_to_cart(e):
        product = product_dd.value
        supplier = supplier_dd.value
        try:
            qty = int(qty_field.value or 1)
        except ValueError:
            qty = 1
        if not product or not supplier:
            show_snackbar("Выберите товар и поставщика")
            return
        for item in cart_items:
            if item['product'] == product and item['supplier'] == supplier:
                item['qty'] += qty
                refresh_cart()
                qty_field.value = "1"
                page.update()
                return
        cart_items.append({'product': product, 'qty': qty, 'supplier': supplier})
        refresh_cart()
        update_location_lock()
        qty_field.value = "1"
        page.update()

    def refresh_cart():
        cart_list.controls.clear()
        for idx, item in enumerate(cart_items):
            def change_qty(delta, item_idx=idx):
                cart_items[item_idx]['qty'] += delta
                if cart_items[item_idx]['qty'] <= 0:
                    cart_items.pop(item_idx)
                refresh_cart()
                update_location_lock()
                page.update()
            
            def remove_item(item_idx=idx):
                cart_items.pop(item_idx)
                refresh_cart()
                update_location_lock()
                page.update()
            
            # Адаптивная карточка товара  ← ANDROID
            cart_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"[{item['supplier']}]", color=Palette.ACCENT_ORANGE,
                                    size=11, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE,
                                          icon_color=Palette.ACCENT_RED, icon_size=18,
                                          on_click=lambda e, i=idx: remove_item(i)),
                        ]),
                        ft.Row([
                            ft.Text(item['product'], color=Palette.TEXT_PRIMARY,
                                    size=13, expand=True),
                            ft.Row([
                                ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                              icon_color=Palette.ACCENT_RED, icon_size=18,
                                              on_click=lambda e, i=idx: change_qty(-1, i)),
                                ft.Text(str(item['qty']), color=Palette.TEXT_PRIMARY,
                                        size=13, weight=ft.FontWeight.BOLD, width=25,
                                        text_align=ft.TextAlign.CENTER),
                                ft.IconButton(icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                              icon_color=Palette.ACCENT_GREEN, icon_size=18,
                                              on_click=lambda e, i=idx: change_qty(1, i)),
                            ], spacing=2),
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ], spacing=2),
                    bgcolor=Palette.BG_PANEL_ALT,
                    padding=ft.Padding(left=8, right=4, top=6, bottom=6),
                    border_radius=6,
                )
            )
        page.update()

    def clear_cart(e):
        cart_items.clear()
        refresh_cart()
        update_location_lock()

    def save_to_sheet(e):
        if not cart_items:
            show_snackbar("Корзина пуста")
            return
        location = location_dd.value
        if not location:
            show_snackbar("Выберите точку")
            return
        by_supplier = {}
        for item in cart_items:
            by_supplier.setdefault(item['supplier'], []).append(item)
        success_suppliers = []
        errors = []
        for supplier, items in by_supplier.items():
            text = '\n'.join(f"{i['product']} - {i['qty']}" for i in items)
            try:
                sheets_sync.find_cell_and_write(supplier, location, text)
                success_suppliers.append(supplier)
            except Exception as ex:
                errors.append(f"{supplier}: {ex}")
        if not errors:
            total_items = sum(len(items) for items in by_supplier.values())
            show_snackbar(f"✅ Записан! Поставщиков: {len(success_suppliers)}, товаров: {total_items}")
            cart_items.clear()
            refresh_cart()
            update_location_lock()
        else:
            show_snackbar(f"❌ Ошибки:\n" + "\n".join(errors))

    def apply_products_to_ui():
        supplier_dd.options.clear()
        for s in products_mgr.products_by_supplier.keys():
            supplier_dd.options.append(ft.dropdown.Option(key=s, text=s))
        supplier_dd.update()
        if supplier_dd.options:
            supplier_dd.value = supplier_dd.options[0].key
            supplier_dd.update()
            update_products_for_supplier()
        source_label.value = f"Источник: {products_mgr.last_source}"
        source_label.update()

    def refresh_products(e):
        refresh_btn.disabled = True
        refresh_btn.text = "⏳..."
        page.update()
        success, message = products_mgr.refresh()
        apply_products_to_ui()
        refresh_btn.disabled = False
        refresh_btn.text = "🔄 Обновить"
        page.update()
        show_snackbar(message)

    def show_suppliers_info(e):
        rows = []
        for supplier, info in products_mgr.suppliers_info.items():
            count = len(products_mgr.products_by_supplier.get(supplier, []))
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(supplier, color=Palette.TEXT_PRIMARY, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(info, color=Palette.TEXT_SECONDARY)),
                ft.DataCell(ft.Text(str(count), color=Palette.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)),
            ]))
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("🏭 Поставщик", color=Palette.ACCENT_BLUE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("📦 Что поставляет", color=Palette.ACCENT_BLUE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("🔢", color=Palette.ACCENT_BLUE, weight=ft.FontWeight.BOLD), numeric=True),
            ],
            rows=rows,
            border=ft.BorderSide(1, Palette.BORDER),
            border_radius=8,
            horizontal_lines=ft.BorderSide(1, Palette.BORDER_LIGHT),
            bgcolor=Palette.BG_PANEL,
            column_spacing=15,
            data_row_color=Palette.BG_PANEL_ALT,
        )
        total_products = sum(len(p) for p in products_mgr.products_by_supplier.values())
        total_suppliers = len(products_mgr.suppliers_info)
        # Адаптивная ширина таблицы  ← ANDROID
        table_scroll = ft.Column(controls=[table], scroll=ft.ScrollMode.AUTO, height=400, spacing=0)
        table_container = ft.Container(content=table_scroll, bgcolor=Palette.BG_PANEL, border_radius=8, padding=10)
        dlg = ft.AlertDialog(
            title=ft.Text("📖 Справочник", color=Palette.ACCENT_BLUE, size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text(f"Источник: {products_mgr.last_source}", color=Palette.TEXT_MUTED, size=11, italic=True),
                table_container,
                ft.Text(f"📊 {total_suppliers} поставщиков • {total_products} товаров",
                        color=Palette.ACCENT_BLUE, size=13, weight=ft.FontWeight.BOLD),
            ], spacing=10),
            actions=[ft.Button("✕ Закрыть", on_click=lambda _: close_dlg(),
                               bgcolor=Palette.ACCENT_PURPLE, color=Palette.TEXT_PRIMARY)],
            bgcolor=Palette.BG_DARK,
            actions_alignment=ft.MainAxisAlignment.END,
        )
        def close_dlg():
            dlg.open = False
            page.update()
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # Кнопки с адаптивными размерами  ← ANDROID
    refresh_btn = ft.Button("🔄 Обновить", on_click=refresh_products,
                            bgcolor=Palette.ACCENT_CYAN, color=Palette.TEXT_PRIMARY)
    info_btn = ft.Button("📖 Поставщики", on_click=show_suppliers_info,
                         bgcolor=Palette.ACCENT_PURPLE, color=Palette.TEXT_PRIMARY, expand=True)
    add_btn = ft.Button("➕ Добавить", on_click=add_to_cart,
                        bgcolor=Palette.ACCENT_GREEN, color=Palette.TEXT_PRIMARY, expand=True)
    clear_btn = ft.Button("🗑 Очистить", on_click=clear_cart,
                          bgcolor=Palette.ACCENT_RED, color=Palette.TEXT_PRIMARY)
    save_btn = ft.Button("💾 Записать", on_click=save_to_sheet,
                         bgcolor=Palette.ACCENT_GREEN_DARK, color=Palette.TEXT_PRIMARY, expand=True)

    # ВЕРТИКАЛЬНАЯ КОМПОНОВКА — работает и на ПК, и на телефоне  ← ANDROID
    page.add(
        ft.Text("QFACT.SUPPLIES", size=22, weight=ft.FontWeight.BOLD, color=Palette.ACCENT_BLUE),
        ft.Row([status_label, ft.Container(expand=True), source_label]),
        ft.Row([location_dd, refresh_btn], spacing=8),
        info_btn,
        # Панель выбора
        ft.Container(
            content=ft.Column([
                ft.Text("📦 Выбор товара", color=Palette.ACCENT_BLUE, size=14, weight=ft.FontWeight.BOLD),
                supplier_dd,
                product_dd,
                ft.Row([qty_field, add_btn], spacing=8),
            ], spacing=8),
            padding=12, bgcolor=Palette.BG_PANEL, border_radius=10,
            border=ft.BorderSide(1, Palette.BORDER),
        ),
        # Панель корзины
        ft.Container(
            content=ft.Column([
                ft.Text("📋 Текущий заказ:", color=Palette.ACCENT_BLUE, size=14, weight=ft.FontWeight.BOLD),
                ft.Container(content=cart_list, height=280),
                ft.Row([clear_btn, save_btn], spacing=8),
            ], spacing=8),
            padding=12, bgcolor=Palette.BG_PANEL, border_radius=10,
            border=ft.BorderSide(1, Palette.BORDER),
        ),
    )

    apply_products_to_ui()


if __name__ == "__main__":
    ft.run(main)
