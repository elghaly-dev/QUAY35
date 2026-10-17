#!/usr/bin/env python3
"""Build scripts/i18n_strings.json and patch build_i18n.py STRINGS block."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = Path("/tmp/en_strings.json")

# ar / ru / zh — professional site copy (HTML preserved where present in EN).
L: dict[str, dict[str, str]] = {}

def add(key: str, ar: str, ru: str, zh: str) -> None:
    L[key] = {"ar": ar, "ru": ru, "zh": zh}


# ── shared chrome ──────────────────────────────────────────────────────
add("skip_main", "تخطي إلى المحتوى الرئيسي", "Перейти к основному содержанию", "跳到主要内容")
add("nav_aria", "الموقع", "Сайт", "网站")
add("nav_products", "المنتجات", "Продукты", "产品")
add("nav_fees", "مراجعة الرسوم", "Разбор комиссий", "费用审查")
add("nav_hold", "مؤجّل", "Отложено", "暂不开发")
add("footer_chatting", "💬 Chatting", "💬 Chatting", "💬 Chatting")
add("lang_aria", "اللغة", "Язык", "语言")
add("lang_en", "English", "English", "English")
add("lang_ar", "العربية", "العربية", "العربية")
add("lang_ru", "Русский", "Русский", "Русский")
add("lang_zh", "中文", "中文", "中文")

add("meta_title", "QUAY — 35 ElGhaly", "QUAY — 35 ElGhaly", "QUAY — 35 ElGhaly")
add(
    "meta_description",
    "تقارير مكتبية لروبوتات سولana: ورقة أسبوعية للمعاملات الناجحة مقابل الفاشلة، بطاقات إثبات، تقييم للعملة للقراءة فقط، وتنبيهات مراقبة RPC.",
    "Отчёты для деска по ботам Solana: еженедельная сводка landed/failed, proof-карты, оценка mint с доступом на просмотр и RPC-watch.",
    "Solana 机器人桌面报告：每周上链/失败对比、证明卡片、只读 mint 评分与 RPC 监控提醒。",
)
add("og_title", "QUAY — 35 ElGhaly", "QUAY — 35 ElGhaly", "QUAY — 35 ElGhaly")
add(
    "og_description",
    "تقارير مكتبية لروبوتات سولana: ورقة أسبوعية، بطاقات إثبات، تقييم mint للقراءة فقط، وتنبيهات RPC.",
    "Отчёты для деска по ботам Solana: еженедельная сводка, proof-карты, mint с доступом на просмотр и RPC-watch.",
    "Solana 机器人桌面报告：周报、证明卡片、只读 mint 评分与 RPC 提醒。",
)
add(
    "og_image_alt",
    "QUAY — تقارير مكتبية لروبوتات سولana",
    "QUAY — отчёты для деска по ботам Solana",
    "QUAY — Solana 机器人桌面报告",
)

add("hero_kicker", "35 · QUAY · ElGhaly", "35 · QUAY · ElGhaly", "35 · QUAY · ElGhaly")
add(
    "hero_h1",
    "تقارير يستطيع المكتب بيعها. ليست رسمًا بيانيًا فارغًا آخر.",
    "Отчёты, которые деск может продавать. Не ещё один пустой график.",
    "桌面能卖出去的报告。不是又一张空图表。",
)
add(
    "hero_lede",
    "يعمل QUAY من بيانات عامة والنص الذي ترسله — توقيعات، mint، أو feed — ويرد بصفحة أو بطاقة أو تنبيه. تشتري ملفًا أو بطاقة أو مراقبة، لا token. لا نحتفظ بالمفاتيح أبدًا.",
    "QUAY работает с публичными данными и текстом, который вы присылаете — подписи, mint, feed — и возвращает страницу, карту или ping. Вы покупаете файл, карту или watch, не токен. Мы никогда не храним ключи.",
    "QUAY 使用公开数据与您提供的文本——签名、mint、feed——返回页面、卡片或提醒。您购买的是文件、卡片或监控，不是代币。我们从不保管密钥。",
)
add("cta_products", "عرض المنتجات الخمسة", "Смотреть пять продуктов", "查看五项产品")
add("cta_fees", "ابدأ بمراجعة الرسوم مقابل 199$", "Начать с разбора комиссий за $199", "从 $199 费用审查开始")
add("hero_img_alt", "QUAY — 35 ElGhaly", "QUAY — 35 ElGhaly", "QUAY — 35 ElGhaly")

add("trust1_title", "بيانات عامة فقط", "Только публичные данные", "只用公开数据")
add("trust1_body", "لا مفاتيح، لا عبارة استرداد، لا وصول للمحفظة. أبدًا.", "Никаких ключей, seed-фраз и доступа к кошельку. Никогда.", "不要密钥、助记词或钱包访问。绝不。")
add("trust2_title", "استرداد في أي وقت", "Возврат в любой момент", "随时退款")
add("trust2_body", "بدون نموذج، بدون سبب، بدون مهلة.", "Без формы, без причины, без срока.", "无需表单、理由或时限。")
add("trust2_link", "كيف", "Как", "如何")
add("trust3_title", "شركة حقيقية", "Настоящая компания", "真实公司")
add("trust3_body", "elghaly, LLC.", "elghaly, LLC.", "elghaly, LLC.")
add("trust3_link", "أين نحن", "Где мы", "我们在哪")

add("how_title", "كيف يعمل", "Как это работает", "如何运作")
add(
    "how_lead",
    "كل ما نقرأه موجود أصلًا على السلسلة أو في مستكشف الكتل.",
    "Всё, что мы читаем, уже публично в блокчейне или в explorer.",
    "我们读取的一切本就公开在链上或区块浏览器中。",
)
add("step1_title", "ترسل بيانات عامة", "Вы присылаете публичные данные", "您发送公开数据")
add(
    "step1_body",
    "توقيعات، عنوان mint، الـ feed للمراقبة، أو نص البطاقات. لا مفتاحًا ولا RPC يحتوي token.",
    "Подписи, mint, feed для watch или текст для карт. Никогда ключ или RPC с token.",
    "签名、mint 地址、要监控的 feed 或卡片文案。不要密钥或带 token 的 RPC。",
)
add("step2_title", "نقرأها", "Мы читаем", "我们读取")
add(
    "step2_body",
    "مقابل ما landed فعليًا على السلسلة. إن تعذّر القراءة من بيانات عامة، نقول UNKNOWN بدل التخمين.",
    "Сверяем с тем, что реально landed в chain. Если из публичных данных не прочитать — пишем UNKNOWN, не угадываем.",
    "对照实际上链结果。无法从公开数据读取时，我们写 UNKNOWN，不猜测。",
)
add("step3_title", "تحصل على ملف أو بطاقة أو تنبيه", "Вы получаете файл, карту или ping", "您收到文件、卡片或提醒")
add(
    "step3_body",
    "بالبريد. لا شيء من عندنا يلمس إعداداتك أو محفظتك أو معاملاتك.",
    "По email. Ничего наше не трогает ваш config, кошелёк или транзакции.",
    "通过邮件。我们的东西不会碰您的配置、钱包或交易。",
)

add("products_title", "المنتجات", "Продукты", "产品")
add(
    "products_lead",
    "ادفع عبر PayPal هنا، أو من المتجر، أو من محفظتك أدناه.",
    "Оплата PayPal здесь, через shop checkout или кошельком ниже.",
    "在此用 PayPal、商店结账或下方钱包支付。",
)
add("spec_send", "ترسل", "Вы присылаете", "您提供")
add("spec_get", "تحصل", "Вы получаете", "您获得")
add("spec_when", "متى", "Срок", "时间")
add("price_once", "مرة واحدة", "разово", "一次性")
add("price_month", " / شهر", " / мес.", " / 月")
add("price_onetime", "مرة واحدة", "разово", "一次性")
add("paypal_btn", "الدفع عبر PayPal", "Оплатить через PayPal", "PayPal 支付")
add("shop_alt", "أو من متجر الدفع", "или через shop checkout", "或使用商店结账")

# Continue in populate_i18n_part2 — merged at runtime
from populate_i18n_part2 import register_part2  # noqa: E402

register_part2(add)


def main() -> None:
    en: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))
    missing = [k for k in en if k not in L]
    if missing:
        raise SystemExit(f"Missing translations for {len(missing)} keys: {missing[:20]}…")

    strings: dict[str, dict[str, str]] = {}
    for key, en_text in en.items():
        strings[key] = {"en": en_text, **L[key]}

    strings["lang_en"] = {"en": "English", "ar": "English", "ru": "English", "zh": "English"}
    strings["lang_ar"] = {"en": "العربية", "ar": "العربية", "ru": "العربية", "zh": "العربية"}
    strings["lang_ru"] = {"en": "Русский", "ar": "Русский", "ru": "Русский", "zh": "Русский"}
    strings["lang_zh"] = {"en": "中文", "ar": "中文", "ru": "中文", "zh": "中文"}

    out_json = ROOT / "scripts" / "i18n_strings.json"
    out_json.write_text(json.dumps(strings, ensure_ascii=False, indent=2), encoding="utf-8")

    # Patch build_i18n.py STRINGS dict
    build_py = ROOT / "scripts" / "build_i18n.py"
    src = build_py.read_text(encoding="utf-8")
    # Render STRINGS as Python source
    lines = ["STRINGS: dict[str, dict[str, str]] = {"]
    for key in sorted(strings.keys()):
        lines.append(f'    "{key}": {{')
        for loc in ("en", "ar", "ru", "zh"):
            val = strings[key][loc].replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'        "{loc}": "{val}",')
        lines.append("    },")
    lines.append("}")
    new_block = "\n".join(lines)
    patched, n = re.subn(
        r"STRINGS: dict\[str, dict\[str, str\]\] = \{.*?\n\}\n\nMARKER_RE",
        new_block + "\n\nMARKER_RE",
        src,
        count=1,
        flags=re.DOTALL,
    )
    if n != 1:
        raise SystemExit("Failed to patch build_i18n.py STRINGS block")
    build_py.write_text(patched, encoding="utf-8")
    print(f"Wrote {len(strings)} keys to build_i18n.py and {out_json}")


if __name__ == "__main__":
    main()
