#!/usr/bin/env python3
"""Generate locale HTML from marked English templates. Run from repo root."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCALES = {
    "en": {"dir": "ltr", "lang": "en", "prefix": "", "root": ROOT},
    "ar": {"dir": "rtl", "lang": "ar", "prefix": "ar/", "root": ROOT / "ar"},
    "ru": {"dir": "ltr", "lang": "ru", "prefix": "ru/", "root": ROOT / "ru"},
    "zh": {"dir": "ltr", "lang": "zh-Hans", "prefix": "zh/", "root": ROOT / "zh"},
}

# Translations keyed by <!--i18n:key-->…<!--/i18n:key--> marker id.
STRINGS: dict[str, dict[str, str]] = {
    "ask_blurb": {
        "en": "Mail <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> with what you run. We answer with the smallest product that fits — or tell you plainly that none does.",
        "ar": "راسل <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> بما تشغّله. نرد بأصغر منتج يناسب — أو نقول بوضوح أن لا شيء يناسب.",
        "ru": "Напишите на <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>, что вы запускаете. Ответим минимальным продуктом — или честно скажем, что ни один не подходит.",
        "zh": "邮件 <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> 说明您在跑什么。我们会推荐最小合适产品，或明确说明都不合适。",
    },
    "ask_cta": {
        "en": "Ask first",
        "ar": "اسأل أولًا",
        "ru": "Сначала спросить",
        "zh": "先咨询",
    },
    "ask_title": {
        "en": "Not sure which one?",
        "ar": "غير متأكد أي واحد؟",
        "ru": "Не уверены, что выбрать?",
        "zh": "不确定选哪个？",
    },
    "copied": {
        "en": "Copied",
        "ar": "تم النسخ",
        "ru": "Скопировано",
        "zh": "已复制",
    },
    "copy_base": {
        "en": "Copy Base",
        "ar": "نسخ Base",
        "ru": "Копировать Base",
        "zh": "复制 Base",
    },
    "copy_btc": {
        "en": "Copy BTC",
        "ar": "نسخ BTC",
        "ru": "Копировать BTC",
        "zh": "复制 BTC",
    },
    "copy_eth": {
        "en": "Copy ETH",
        "ar": "نسخ ETH",
        "ru": "Копировать ETH",
        "zh": "复制 ETH",
    },
    "copy_sol": {
        "en": "Copy SOL",
        "ar": "نسخ SOL",
        "ru": "Копировать SOL",
        "zh": "复制 SOL",
    },
    "cta_fees": {
        "en": "Start with the $199 fee review",
        "ar": "ابدأ بمراجعة الرسوم مقابل 199$",
        "ru": "Начать с разбора комиссий за $199",
        "zh": "从 $199 费用审查开始",
    },
    "cta_products": {
        "en": "See the five products",
        "ar": "عرض المنتجات الخمسة",
        "ru": "Смотреть пять продуктов",
        "zh": "查看五项产品",
    },
    "fee_badge": {
        "en": "Start here",
        "ar": "ابدأ هنا",
        "ru": "Начните здесь",
        "zh": "从这里开始",
    },
    "fee_blurb": {
        "en": "Your priority-fee and tip settings, read against what your public transactions actually paid and landed at.",
        "ar": "إعدادات priority fee والإكرامية، مقروءة مقابل ما دفعته معاملاتك العامة فعليًا وما landed عنده.",
        "ru": "Ваши priority fee и tip сверяются с тем, что публичные транзакции реально платили и где landed.",
        "zh": "根据您公开交易的实际支付与上链情况，审阅优先费与小费设置。",
    },
    "fee_cta": {
        "en": "Details &amp; brief",
        "ar": "التفاصيل والـ brief",
        "ru": "Детали и brief",
        "zh": "详情与 brief",
    },
    "fee_get": {
        "en": "One written page: the percentile you land at, the one to target, where you overpay. Gaps say UNKNOWN.",
        "ar": "صفحة مكتوبة واحدة: الم percentile الذي landed عنده، الهدف، وأين تدفع زيادة. الفجوات تقول UNKNOWN.",
        "ru": "Одна страница: percentile landed, цель, где переплата. Пробелы — UNKNOWN.",
        "zh": "一页书面报告：实际上链分位、目标分位、多付之处；未知处标 UNKNOWN。",
    },
    "fee_send": {
        "en": "Up to 200 transaction signatures and your current settings. Nothing private.",
        "ar": "حتى 200 توقيع معاملة وإعداداتك الحالية. لا شيء خاص.",
        "ru": "До 200 подписей транзакций и текущие настройки. Ничего приватного.",
        "zh": "最多 200 条交易签名及当前设置。不含私密信息。",
    },
    "fee_title": {
        "en": "Fee review",
        "ar": "مراجعة الرسوم",
        "ru": "Разбор комиссий",
        "zh": "费用审查",
    },
    "fee_when": {
        "en": "Within 48 hours of a complete brief.",
        "ar": "خلال 48 ساعة من brief كامل.",
        "ru": "В течение 48 часов после полного brief.",
        "zh": "完整 brief 后 48 小时内。",
    },
    "fees_brief_btn": {
        "en": "Send brief — support@elghaly.dev",
        "ar": "أرسل brief — support@elghaly.dev",
        "ru": "Brief — support@elghaly.dev",
        "zh": "发送 brief — support@elghaly.dev",
    },
    "fees_cannot_intro": {
        "en": "Signatures show what was submitted and what landed on chain. They do not show everything about your operation. At minimum, we cannot see:",
        "ar": "التوقيعات تظهر ما أُرسل وما landed. لا تظهر كل شيء عن عملك. على الأقل لا نرى:",
        "ru": "Подписи показывают submit и landed, не всю операцию. Минимум не видим:",
        "zh": "签名显示提交与上链，不能反映运营全貌。至少看不到：",
    },
    "fees_cannot_li1": {
        "en": "whether a landed transaction achieved the trade outcome you wanted",
        "ar": "هل حققت المعاملة landed النتيجة التي wanted",
        "ru": "Достигла ли landed tx нужного trade outcome",
        "zh": "上链交易是否达到预期成交结果",
    },
    "fees_cannot_li1_b": {
        "en": "Your fills",
        "ar": "تنفيذاتك (fills)",
        "ru": "Ваши fills",
        "zh": "成交（fills）",
    },
    "fees_cannot_li2": {
        "en": "intent, sizing logic, or timing rules behind each send",
        "ar": "النية، حجم الصفقة، أو قواعد التوقيت behind كل send",
        "ru": "Intent, sizing, timing rules за каждым send",
        "zh": "每次发送背后的意图、 sizing 与 timing 规则",
    },
    "fees_cannot_li2_b": {
        "en": "Your strategy",
        "ar": "استراتيجيتك",
        "ru": "Вашу стратегию",
        "zh": "您的策略",
    },
    "fees_cannot_li3": {
        "en": "how long your node or provider took to propagate the transaction",
        "ar": "كم استغرق node أو المزود لنشر المعاملة",
        "ru": "Сколько node/провайдеру на propagate",
        "zh": "节点/提供商传播交易所用时间",
    },
    "fees_cannot_li3_b": {
        "en": "Your RPC latency",
        "ar": "زمن RPC",
        "ru": "RPC latency",
        "zh": "RPC 延迟",
    },
    "fees_cannot_li4": {
        "en": "if the failure is not recorded on chain (simulation rejections, dropped packets, client-side aborts)",
        "ar": "إن لم يُسجَّل الفشل on-chain (رفض simulation، packets، إلغاء client)",
        "ru": "Если failure не on-chain (simulation, drop, client abort)",
        "zh": "若失败未上链（模拟拒绝、丢包、客户端取消）",
    },
    "fees_cannot_li4_b": {
        "en": "Why a specific transaction failed",
        "ar": "لماذا فشلت معاملة محددة",
        "ru": "Почему упала конкретная tx",
        "zh": "某笔交易失败原因",
    },
    "fees_cannot_title": {
        "en": "What we cannot tell you from signatures alone",
        "ar": "ما لا نستطيع قوله من التوقيعات وحدها",
        "ru": "Чего не видно только по подписям",
        "zh": "仅凭签名无法告知的内容",
    },
    "fees_disclaimer": {
        "en": "This is a written recommendation based on public chain data. We do not touch your config, your wallet, or your transactions. Following the recommendation may not improve your landing rate or lower your cost, and we do not promise that it will. We make no claim about earnings, returns or savings.",
        "ar": "توصية مكتوبة من بيانات سلسلة عامة. لا نلمس config أو محفظتك أو معاملاتك. اتباع التوصية قد لا يحسّن landed أو يخفض التكلفة، ولا نعد بذلك. لا ادعاءات أرباح أو ادخار.",
        "ru": "Письменная рекомендация по публичным chain-данным. Config/кошелёк/tx не трогаем. Следование может не улучшить landed или cost — не обещаем. Без claims о доходе/экономии.",
        "zh": "基于公开链上数据的书面建议。不碰配置、钱包或交易。遵循建议未必改善上链或降本，我们不做承诺。不宣称收益或节省。",
    },
    "fees_get_intro": {
        "en": "One page, delivered within 48 hours of a complete brief:",
        "ar": "صفحة واحدة خلال 48 ساعة من brief كامل:",
        "ru": "Одна страница за 48 ч после полного brief:",
        "zh": "完整 brief 后 48 小时内一页报告：",
    },
    "fees_get_li1": {
        "en": "The percentile your current setting actually lands at",
        "ar": "الـ percentile الذي landed عنده إعدادك الحالي",
        "ru": "Percentile landed для текущих настроек",
        "zh": "当前设置实际上链分位",
    },
    "fees_get_li2": {
        "en": "The percentile to target, with the reasoning shown",
        "ar": "الـ percentile المستهدف مع المبرر",
        "ru": "Целевой percentile с обоснованием",
        "zh": "目标分位及理由",
    },
    "fees_get_li3": {
        "en": "When to raise, and the specific condition that should trigger it",
        "ar": "متى ترفع، والشرط الذي يجب أن يفعّل ذلك",
        "ru": "Когда повышать и условие триггера",
        "zh": "何时提高及触发条件",
    },
    "fees_get_li4": {
        "en": "Where you are overpaying, with the wasted amount per landed tx",
        "ar": "أين تدفع زيادة، مع الهدر لكل tx landed",
        "ru": "Где переплата и waste на landed tx",
        "zh": "多付之处及每笔上链浪费量",
    },
    "fees_get_li5": {
        "en": "What we could not determine from the signatures, named explicitly",
        "ar": "ما لم نستطع تحديده من التوقيعات، مسماة صراحة",
        "ru": "Что не вывели из подписей — явно по имени",
        "zh": "无法从签名确定的内容，明确列出",
    },
    "fees_get_note": {
        "en": "If an input cannot be read from a signature, the report says <strong>UNKNOWN</strong> — not a guess.",
        "ar": "إن تعذّر قراءة مدخل من التوقيع، يقول التقرير <strong>UNKNOWN</strong> — لا تخمين.",
        "ru": "Если из подписи не прочитать — в отчёте <strong>UNKNOWN</strong>, не догадка.",
        "zh": "签名无法读取的字段，报告写 <strong>UNKNOWN</strong>——不猜测。",
    },
    "fees_get_title": {
        "en": "What you get back",
        "ar": "ما تحصل عليه",
        "ru": "Что получите",
        "zh": "您将获得",
    },
    "fees_h1": {
        "en": "Priority-fee and tip configuration review",
        "ar": "مراجعة إعداد priority fee والإكرامية",
        "ru": "Разбор priority fee и tip",
        "zh": "优先费与小费配置审查",
    },
    "fees_kicker": {
        "en": "QUAY · Fee review",
        "ar": "QUAY · مراجعة الرسوم",
        "ru": "QUAY · Разбор комиссий",
        "zh": "QUAY · 费用审查",
    },
    "fees_lede1": {
        "en": "We read your public transaction signatures and compare your current priority-fee and tip settings against what those transactions actually paid and landed at.",
        "ar": "نقرأ توقيعات معاملاتك العامة ونقارن إعدادات priority fee والإكرامية بما دفعته تلك المعاملات فعليًا وما landed عنده.",
        "ru": "Читаем публичные подписи и сравниваем priority fee/tip с тем, что транзакции реально платили и где landed.",
        "zh": "读取您的公开交易签名，将当前优先费/小费设置与交易实际支付及上链情况对比。",
    },
    "fees_lede2": {
        "en": "You receive one written page within 48 hours of a complete brief. This is a recommendation only — we do not change your config, your wallet, or your transactions.",
        "ar": "صفحة مكتوبة واحدة خلال 48 ساعة من brief كامل. توصية فقط — لا نغيّر config أو محفظتك أو معاملاتك.",
        "ru": "Одна страница за 48 ч после полного brief. Только рекомендация — не трогаем config, кошелёк, транзакции.",
        "zh": "完整 brief 后 48 小时内交付一页书面报告。仅为建议——不改动配置、钱包或交易。",
    },
    "fees_meta_description": {
        "en": "48-hour priority-fee and tip configuration review from public transaction signatures. $199 once.",
        "ar": "مراجعة priority fee والإكرامية خلال 48 ساعة من توقيعات عامة. 199$ مرة واحدة.",
        "ru": "Разбор priority fee и tip за 48 ч по публичным подписям. $199 разово.",
        "zh": "48 小时内基于公开签名的优先费与小费配置审查。$199 一次性。",
    },
    "fees_meta_title": {
        "en": "Fee review — QUAY · 35 ElGhaly",
        "ar": "مراجعة الرسوم — QUAY · 35 ElGhaly",
        "ru": "Разбор комиссий — QUAY · 35 ElGhaly",
        "zh": "费用审查 — QUAY · 35 ElGhaly",
    },
    "fees_paypal_aria": {
        "en": "Pay with PayPal: Fee review, $199 once",
        "ar": "الدفع عبر PayPal: مراجعة الرسوم، 199$ مرة واحدة",
        "ru": "PayPal: Fee review, $199 разово",
        "zh": "PayPal：费用审查，$199 一次性",
    },
    "fees_price_note": {
        "en": "Once · English only · PayPal or invoice on reply",
        "ar": "مرة واحدة · English only · PayPal أو فاتورة في الرد",
        "ru": "Разово · English only · PayPal или invoice в ответе",
        "zh": "一次性 · 仅英文 · PayPal 或回复发票",
    },
    "fees_price_p": {
        "en": "Pay with PayPal here and send your brief with the PayPal transaction ID, or send the brief first and pay on the invoice we send when we confirm it. No form on this page collects anything.",
        "ar": "ادفع PayPal هنا وأرسل brief مع PayPal transaction ID، أو أرسل brief أولًا وادفع على الفاتورة عند التأكيد. لا نموذج على هذه الصفحة.",
        "ru": "PayPal здесь + brief с PayPal transaction ID, или brief сначала и invoice после подтверждения. Формы на странице нет.",
        "zh": "在此 PayPal 支付并邮件 brief 附 PayPal 交易号，或先发 brief 待确认后付发票。本页无表单。",
    },
    "fees_price_title": {
        "en": "Price and intake",
        "ar": "السعر والاستلام",
        "ru": "Цена и intake",
        "zh": "价格与提交",
    },
    "fees_refunds_lead": {
        "en": "If you want your money back, you get it.",
        "ar": "إن أردت أموالك، تحصل عليها.",
        "ru": "Хотите деньги назад — получите.",
        "zh": "要退款就能退。",
    },
    "fees_sample_banner": {
        "en": "Example layout — not a real client report",
        "ar": "مثال تخطيط — ليس تقرير عميل حقيقي",
        "ru": "Пример макета — не реальный отчёт",
        "zh": "版式示例——非真实客户报告",
    },
    "fees_sample_current": {
        "en": "Current setting — landed percentile",
        "ar": "الإعداد الحالي — landed percentile",
        "ru": "Текущие настройки — landed percentile",
        "zh": "当前设置 — 上链分位",
    },
    "fees_sample_overpay": {
        "en": "Overpaying",
        "ar": "دفع زائد",
        "ru": "Переплата",
        "zh": "多付",
    },
    "fees_sample_raise": {
        "en": "When to raise",
        "ar": "متى ترفع",
        "ru": "Когда повышать",
        "zh": "何时提高",
    },
    "fees_sample_scope": {
        "en": "Sample scope",
        "ar": "نطاق العينة",
        "ru": "Sample scope",
        "zh": "样例范围",
    },
    "fees_sample_settings": {
        "en": "Settings as submitted",
        "ar": "الإعدادات كما أُرسلت",
        "ru": "Settings as submitted",
        "zh": "提交的设置",
    },
    "fees_sample_settings_dd": {
        "en": "Priority: <span class=\"redacted\">[your value]</span> · Tip: <span class=\"redacted\">[your value]</span>",
        "ar": "Priority: <span class=\"redacted\">[your value]</span> · Tip: <span class=\"redacted\">[your value]</span>",
        "ru": "Priority: <span class=\"redacted\">[your value]</span> · Tip: <span class=\"redacted\">[your value]</span>",
        "zh": "Priority: <span class=\"redacted\">[your value]</span> · Tip: <span class=\"redacted\">[your value]</span>",
    },
    "fees_sample_target": {
        "en": "Recommended target percentile",
        "ar": "الـ percentile المستهدف الموصى به",
        "ru": "Рекомендуемый target percentile",
        "zh": "建议目标分位",
    },
    "fees_sample_title": {
        "en": "Fee review · one-page output (redacted shape)",
        "ar": "مراجعة الرسوم · مخرجات صفحة واحدة (شكل محذوف)",
        "ru": "Fee review · одна страница (redacted)",
        "zh": "费用审查 · 单页输出（脱敏样例）",
    },
    "fees_sample_unknown": {
        "en": "Could not determine (UNKNOWN)",
        "ar": "تعذّر التحديد (UNKNOWN)",
        "ru": "Could not determine (UNKNOWN)",
        "zh": "无法确定 (UNKNOWN)",
    },
    "fees_send_intro": {
        "en": "All of this is public data. Send nothing that is not already visible on chain or in a block explorer.",
        "ar": "كل هذا بيانات عامة. لا ترسل ما ليس ظاهرًا على السلسلة أو في explorer.",
        "ru": "Всё это публичные данные. Не присылайте то, чего нет в chain/explorer.",
        "zh": "均为公开数据。请勿发送链上或浏览器中不可见的内容。",
    },
    "fees_send_li1": {
        "en": "signatures only. Never a private key, never a seed phrase, never an RPC URL with a token in it.",
        "ar": "توقيعات فقط. لا مفتاح خاص، لا seed phrase، لا RPC يحتوي token.",
        "ru": "Только подписи. Никогда private key, seed или RPC с token.",
        "zh": "仅签名。不要私钥、助记词或带 token 的 RPC。",
    },
    "fees_send_li1_b": {
        "en": "Up to 200 transaction signatures",
        "ar": "حتى 200 توقيع معاملة",
        "ru": "До 200 подписей транзакций",
        "zh": "最多 200 条交易签名",
    },
    "fees_send_li2_b": {
        "en": "Your current priority-fee setting",
        "ar": "إعداد priority fee الحالي",
        "ru": "Текущий priority fee",
        "zh": "当前优先费设置",
    },
    "fees_send_li3_b": {
        "en": "Your current tip setting",
        "ar": "إعداد الإكرامية الحالي",
        "ru": "Текущий tip",
        "zh": "当前小费设置",
    },
    "fees_send_li4_b": {
        "en": "Which venue or aggregator you route through",
        "ar": "Venue أو aggregator الذي تمر عبره",
        "ru": "Venue или aggregator маршрута",
        "zh": "您使用的 venue 或 aggregator",
    },
    "fees_send_note": {
        "en": "We will not ask for, display, or accept an API key, an RPC URL containing a token, or a private key.",
        "ar": "لن نطلب أو نعرض أو نقبل API key أو RPC يحتوي token أو مفتاحًا خاصًا.",
        "ru": "Не запрашиваем, не показываем и не принимаем API key, RPC с token или private key.",
        "zh": "我们不会索取、展示或接受 API key、含 token 的 RPC 或私钥。",
    },
    "fees_send_title": {
        "en": "What you send",
        "ar": "ما ترسل",
        "ru": "Что прислать",
        "zh": "您需提供",
    },
    "fees_unknown_rule": {
        "en": "Anything that cannot be derived from the signatures you send is marked <strong>UNKNOWN</strong> in the report. We do not infer or fill gaps.",
        "ar": "ما لا يُستنتج من التوقيعات يُوسَم <strong>UNKNOWN</strong> في التقرير. لا نملأ الفجوات.",
        "ru": "Всё, что не выводится из подписей, — <strong>UNKNOWN</strong>. Пробелы не заполняем.",
        "zh": "无法从签名推导的内容在报告中标记 <strong>UNKNOWN</strong>。不填补空白。",
    },
    "fees_where_link": {
        "en": "Where we are",
        "ar": "أين نحن",
        "ru": "Где мы",
        "zh": "我们在哪",
    },
    "flex_blurb": {
        "en": "Desk proof cards in the 35 lockup, made from text you send. No made-up numbers from us.",
        "ar": "بطاقات إثبات للمكتب بتنسيق 35 من نص ترسله. لا أرقام مخترعة منا.",
        "ru": "Proof-карты в lockup 35 из вашего текста. Без выдуманных цифр.",
        "zh": "用您提供的文案制作 35 版式桌面证明卡。我们不编造数字。",
    },
    "flex_get": {
        "en": "Image cards by email.",
        "ar": "بطاقات صور بالبريد.",
        "ru": "Картинки-карты по email.",
        "zh": "邮件发送图片卡片。",
    },
    "flex_send": {
        "en": "The text for your cards.",
        "ar": "نص البطاقات.",
        "ru": "Текст для карт.",
        "zh": "卡片文案。",
    },
    "flex_title": {
        "en": "Flex card pack",
        "ar": "Flex card pack",
        "ru": "Flex card pack",
        "zh": "Flex card pack",
    },
    "flex_when": {
        "en": "Confirmed in reply to your order.",
        "ar": "يُؤكَّد في رد على طلبك.",
        "ru": "Подтверждаем в ответ на заказ.",
        "zh": "下单后邮件确认。",
    },
    "footer_about": {
        "en": "About",
        "ar": "About",
        "ru": "About",
        "zh": "About",
    },
    "footer_contact": {
        "en": "elghaly, LLC · Email first: <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>. Calls only by appointment.",
        "ar": "elghaly, LLC · البريد أولًا: <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>. المكالمات بموعد فقط.",
        "ru": "elghaly, LLC · Сначала email: <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>. Звонки по записи.",
        "zh": "elghaly, LLC · 优先邮件：<a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>。通话仅预约。",
    },
    "footer_contact_link": {
        "en": "Contact",
        "ar": "Contact",
        "ru": "Contact",
        "zh": "Contact",
    },
    "footer_delivery": {
        "en": "Delivery",
        "ar": "Delivery",
        "ru": "Delivery",
        "zh": "Delivery",
    },
    "footer_privacy": {
        "en": "Privacy",
        "ar": "Privacy",
        "ru": "Privacy",
        "zh": "Privacy",
    },
    "footer_refunds": {
        "en": "Refunds",
        "ar": "الاسترداد",
        "ru": "Возвраты",
        "zh": "退款",
    },
    "footer_terms": {
        "en": "Terms",
        "ar": "Terms",
        "ru": "Terms",
        "zh": "Terms",
    },
    "hero_h1": {
        "en": "Reports a desk can sell. Not another empty chart.",
        "ar": "تقارير يستطيع المكتب بيعها. ليست رسمًا بيانيًا فارغًا آخر.",
        "ru": "Отчёты, которые деск может продавать. Не ещё один пустой график.",
        "zh": "桌面能卖出去的报告。不是又一张空图表。",
    },
    "hero_img_alt": {
        "en": "QUAY — 35 ElGhaly",
        "ar": "QUAY — 35 ElGhaly",
        "ru": "QUAY — 35 ElGhaly",
        "zh": "QUAY — 35 ElGhaly",
    },
    "hero_kicker": {
        "en": "35 · QUAY · ElGhaly",
        "ar": "35 · QUAY · ElGhaly",
        "ru": "35 · QUAY · ElGhaly",
        "zh": "35 · QUAY · ElGhaly",
    },
    "hero_lede": {
        "en": "QUAY works from public data and the text you send — signatures, a mint, a feed — and sends back a page, a card or a ping. You buy a file, a card or a watch, not a token. We never hold keys.",
        "ar": "يعمل QUAY من بيانات عامة والنص الذي ترسله — توقيعات، mint، أو feed — ويرد بصفحة أو بطاقة أو تنبيه. تشتري ملفًا أو بطاقة أو مراقبة، لا token. لا نحتفظ بالمفاتيح أبدًا.",
        "ru": "QUAY работает с публичными данными и текстом, который вы присылаете — подписи, mint, feed — и возвращает страницу, карту или ping. Вы покупаете файл, карту или watch, не токен. Мы никогда не храним ключи.",
        "zh": "QUAY 使用公开数据与您提供的文本——签名、mint、feed——返回页面、卡片或提醒。您购买的是文件、卡片或监控，不是代币。我们从不保管密钥。",
    },
    "hold_closing": {
        "en": "These stay on hold until QUAY Land has three paying operators. Not because the risk changes — it does not — but because we will not learn custody on someone else's money.",
        "ar": "تبقى مؤجّلة حتى يكون لـ QUAY Land ثلاثة مشغّلين يدفعون. ليس لأن المخاطر تتغيّر — لا تتغيّر — بل لأننا لن نتعلّم الحفظ على مال الغير.",
        "ru": "On hold, пока у QUAY Land не будет трёх платящих операторов. Риск тот же — но custody на чужих деньгах не учимся.",
        "zh": "在 QUAY Land 有三名付费运营者之前一直搁置。风险不变——但我们不会在别人的钱上学习托管。",
    },
    "hold_copy_body": {
        "en": "Copying trades automatically needs either your keys or a wallet we control, and we will not hold either.",
        "ar": "نسخ الصفقات تلقائيًا يحتاج مفاتيحك أو محفظة نتحكم بها، ولن نحتفظ بأيّ منهما.",
        "ru": "Авто-копирование сделок требует ваших ключей или нашего кошелька — мы не держим ни то, ни другое.",
        "zh": "自动跟单需要您的密钥或我们控制的钱包——两者我们都不持有。",
    },
    "hold_copy_title": {
        "en": "Copy-trading",
        "ar": "Copy-trading",
        "ru": "Copy-trading",
        "zh": "Copy-trading",
    },
    "hold_escrow_body": {
        "en": "Holding someone else's funds between two strangers makes us a custodian in a dispute we have no way to adjudicate.",
        "ar": "ح holding أموال الغير بين غريبين يجعلنا أمينًا في نزاع لا نستطيع الفصل فيه.",
        "ru": "Держать чужие деньги между незнакомцами — мы custodian в споре без суда.",
        "zh": "在陌生人之间托管资金使我们成为无法裁决争议的保管人。",
    },
    "hold_escrow_title": {
        "en": "Telegram escrow",
        "ar": "Telegram escrow",
        "ru": "Telegram escrow",
        "zh": "Telegram escrow",
    },
    "hold_footer_products": {
        "en": "All products",
        "ar": "كل المنتجات",
        "ru": "Все продукты",
        "zh": "全部产品",
    },
    "hold_h1": {
        "en": "What QUAY will not build.",
        "ar": "ما لن يبنيه QUAY.",
        "ru": "Что QUAY не будет строить.",
        "zh": "QUAY 不会构建的内容。",
    },
    "hold_kicker": {
        "en": "QUAY · Hold",
        "ar": "QUAY · Hold",
        "ru": "QUAY · Hold",
        "zh": "QUAY · Hold",
    },
    "hold_lede": {
        "en": "These come up often. Here is why the answer is no, and what would have to change.",
        "ar": "تُطلب كثيرًا. إليك لماذا الجواب لا، وما الذي يجب أن يتغيّر.",
        "ru": "Спрашивают часто. Почему нет и что должно измениться.",
        "zh": "常被问起。说明为何拒绝，以及需要什么条件才会变。",
    },
    "hold_meta_description": {
        "en": "Three products QUAY refuses to build, and why.",
        "ar": "ثلاثة منتجات يرفض QUAY بناءها، ولماذا.",
        "ru": "Три продукта, которые QUAY отказывается делать, и почему.",
        "zh": "QUAY 拒绝做的三项产品及原因。",
    },
    "hold_meta_title": {
        "en": "What QUAY will not build — QUAY · 35 ElGhaly",
        "ar": "ما لن يبنيه QUAY — QUAY · 35 ElGhaly",
        "ru": "Что QUAY не будет строить — QUAY · 35 ElGhaly",
        "zh": "QUAY 不会做什么 — QUAY · 35 ElGhaly",
    },
    "hold_panic_body": {
        "en": "A button that sells for you is signing authority, and the day it fires wrongly the loss is ours to argue about and yours to carry.",
        "ar": "زر يبيع عنك هو صلاحية توقيع، ويوم يخطئ الخسارة لنا نجادل ولكنك تحملها.",
        "ru": "Кнопка «продать за вас» — signing authority; ошибся — спор наш, убыток ваш.",
        "zh": "代您卖出的按钮即签名权限；一旦误触，损失由您承担，争议归我们扯皮。",
    },
    "hold_panic_title": {
        "en": "Auto-panic sell",
        "ar": "Auto-panic sell",
        "ru": "Auto-panic sell",
        "zh": "Auto-panic sell",
    },
    "how_lead": {
        "en": "Everything we read is already public on chain or in a block explorer.",
        "ar": "كل ما نقرأه موجود أصلًا على السلسلة أو في مستكشف الكتل.",
        "ru": "Всё, что мы читаем, уже публично в блокчейне или в explorer.",
        "zh": "我们读取的一切本就公开在链上或区块浏览器中。",
    },
    "how_title": {
        "en": "How it works",
        "ar": "كيف يعمل",
        "ru": "Как это работает",
        "zh": "如何运作",
    },
    "land_blurb": {
        "en": "Weekly paper for one bot: landed vs failed, and where tips are wasted.",
        "ar": "ورقة أسبوعية لروبوت واحد: landed مقابل failed، وأين تُهدر الإكراميات.",
        "ru": "Еженедельный отчёт для одного бота: landed vs failed и где теряются tips.",
        "zh": "单个机器人周报：上链 vs 失败，以及小费浪费位置。",
    },
    "land_get": {
        "en": "A written report every week, by email.",
        "ar": "تقرير مكتوب كل أسبوع بالبريد.",
        "ru": "Письменный отчёт каждую неделю по email.",
        "zh": "每周邮件书面报告。",
    },
    "land_send": {
        "en": "Transaction hashes. You keep the wallet.",
        "ar": "Hashes المعاملات. المحفظة تبقى عندك.",
        "ru": "Хеши транзакций. Кошелёк остаётся у вас.",
        "zh": "交易哈希。钱包仍在您处。",
    },
    "land_title": {
        "en": "QUAY Land",
        "ar": "QUAY Land",
        "ru": "QUAY Land",
        "zh": "QUAY Land",
    },
    "land_when": {
        "en": "Confirmed in reply to your order.",
        "ar": "يُؤكَّد في رد على طلبك.",
        "ru": "Подтверждаем в ответ на заказ.",
        "zh": "下单后邮件确认。",
    },
    "lang_ar": {
        "en": "العربية",
        "ar": "العربية",
        "ru": "العربية",
        "zh": "العربية",
    },
    "lang_aria": {
        "en": "Language",
        "ar": "اللغة",
        "ru": "Язык",
        "zh": "语言",
    },
    "lang_en": {
        "en": "English",
        "ar": "English",
        "ru": "English",
        "zh": "English",
    },
    "lang_ru": {
        "en": "Русский",
        "ar": "Русский",
        "ru": "Русский",
        "zh": "Русский",
    },
    "lang_zh": {
        "en": "中文",
        "ar": "中文",
        "ru": "中文",
        "zh": "中文",
    },
    "lic_ai": {
        "en": "AI-assisted analysis of public pages",
        "ar": "تحليل بمساعدة AI لصفحات عامة",
        "ru": "AI-анализ публичных страниц",
        "zh": "AI 辅助分析公开页面",
    },
    "lic_ai_chain": {
        "en": "AI-assisted analysis of public on-chain data",
        "ar": "تحليل بمساعدة AI لبيانات عامة على السلسلة",
        "ru": "AI-анализ публичных on-chain данных",
        "zh": "AI 辅助分析公开链上数据",
    },
    "lic_cc": {
        "en": "© elghaly · CC BY 4.0",
        "ar": "© elghaly · CC BY 4.0",
        "ru": "© elghaly · CC BY 4.0",
        "zh": "© elghaly · CC BY 4.0",
    },
    "lic_mit": {
        "en": "Code: MIT",
        "ar": "Code: MIT",
        "ru": "Code: MIT",
        "zh": "Code: MIT",
    },
    "lic_oss": {
        "en": "Open source",
        "ar": "Open source",
        "ru": "Open source",
        "zh": "Open source",
    },
    "meta_description": {
        "en": "Desk reports for Solana bots: a weekly landed-vs-failed paper, proof cards, a read-only mint score and RPC watch pings.",
        "ar": "تقارير مكتبية لروبوتات سولana: ورقة أسبوعية للمعاملات الناجحة مقابل الفاشلة، بطاقات إثبات، تقييم للعملة للقراءة فقط، وتنبيهات مراقبة RPC.",
        "ru": "Отчёты для деска по ботам Solana: еженедельная сводка landed/failed, proof-карты, read-only оценка mint и RPC-watch.",
        "zh": "Solana 机器人桌面报告：每周上链/失败对比、证明卡片、只读 mint 评分与 RPC 监控提醒。",
    },
    "meta_title": {
        "en": "QUAY — 35 ElGhaly",
        "ar": "QUAY — 35 ElGhaly",
        "ru": "QUAY — 35 ElGhaly",
        "zh": "QUAY — 35 ElGhaly",
    },
    "nav_aria": {
        "en": "Site",
        "ar": "الموقع",
        "ru": "Сайт",
        "zh": "网站",
    },
    "nav_chatting": {
        "en": "💬 Chatting",
        "ar": "💬 Chatting",
        "ru": "💬 Chatting",
        "zh": "💬 Chatting",
    },
    "nav_fees": {
        "en": "Fee review",
        "ar": "مراجعة الرسوم",
        "ru": "Разбор комиссий",
        "zh": "费用审查",
    },
    "nav_hold": {
        "en": "Hold",
        "ar": "مؤجّل",
        "ru": "Отложено",
        "zh": "暂不开发",
    },
    "nav_products": {
        "en": "Products",
        "ar": "المنتجات",
        "ru": "Продукты",
        "zh": "产品",
    },
    "og_description": {
        "en": "Desk reports for Solana bots: a weekly landed-vs-failed paper, proof cards, a read-only mint score and RPC watch pings.",
        "ar": "تقارير مكتبية لروبوتات سولana: ورقة أسبوعية، بطاقات إثبات، تقييم mint للقراءة فقط، وتنبيهات RPC.",
        "ru": "Отчёты для деска по ботам Solana: еженедельная сводка, proof-карты, read-only mint и RPC-watch.",
        "zh": "Solana 机器人桌面报告：周报、证明卡片、只读 mint 评分与 RPC 提醒。",
    },
    "og_image_alt": {
        "en": "QUAY — desk reports for Solana bots",
        "ar": "QUAY — تقارير مكتبية لروبوتات سولana",
        "ru": "QUAY — отчёты для деска по ботам Solana",
        "zh": "QUAY — Solana 机器人桌面报告",
    },
    "og_title": {
        "en": "QUAY — 35 ElGhaly",
        "ar": "QUAY — 35 ElGhaly",
        "ru": "QUAY — 35 ElGhaly",
        "zh": "QUAY — 35 ElGhaly",
    },
    "paypal_btn": {
        "en": "Pay with PayPal",
        "ar": "الدفع عبر PayPal",
        "ru": "Оплатить через PayPal",
        "zh": "PayPal 支付",
    },
    "paypal_flex_aria": {
        "en": "Pay with PayPal: Flex card pack, $29 one-time",
        "ar": "الدفع عبر PayPal: Flex card pack، 29$ مرة واحدة",
        "ru": "Оплата PayPal: Flex card pack, $29 разово",
        "zh": "PayPal 支付：Flex card pack，$29 一次性",
    },
    "paypal_land_aria": {
        "en": "Pay with PayPal: QUAY Land, $149 / month",
        "ar": "الدفع عبر PayPal: QUAY Land، 149$ / شهر",
        "ru": "Оплата PayPal: QUAY Land, $149 / мес.",
        "zh": "PayPal 支付：QUAY Land，$149/月",
    },
    "paypal_score_aria": {
        "en": "Pay with PayPal: Score report, $49 one-time",
        "ar": "الدفع عبر PayPal: Score report، 49$ مرة واحدة",
        "ru": "Оплата PayPal: Score report, $49 разово",
        "zh": "PayPal 支付：Score report，$49 一次性",
    },
    "paypal_watch_aria": {
        "en": "Pay with PayPal: Node Watch, $79 / month",
        "ar": "الدفع عبر PayPal: Node Watch، 79$ / شهر",
        "ru": "Оплата PayPal: Node Watch, $79 / мес.",
        "zh": "PayPal 支付：Node Watch，$79/月",
    },
    "price_month": {
        "en": "/ month",
        "ar": " / شهر",
        "ru": " / мес.",
        "zh": " / 月",
    },
    "price_once": {
        "en": "once",
        "ar": "مرة واحدة",
        "ru": "разово",
        "zh": "一次性",
    },
    "price_onetime": {
        "en": "one-time",
        "ar": "مرة واحدة",
        "ru": "разово",
        "zh": "一次性",
    },
    "products_lead": {
        "en": "Pay with PayPal here, use the shop checkout, or pay from a wallet below.",
        "ar": "ادفع عبر PayPal هنا، أو من المتجر، أو من محفظتك أدناه.",
        "ru": "Оплата PayPal здесь, через shop checkout или кошельком ниже.",
        "zh": "在此用 PayPal、商店结账或下方钱包支付。",
    },
    "products_title": {
        "en": "Products",
        "ar": "المنتجات",
        "ru": "Продукты",
        "zh": "产品",
    },
    "recourse": {
        "en": "A PayPal payment, here or through the shop checkout, can be disputed through PayPal; a card payment through the shop, through your card issuer. A wallet transfer cannot. Same product, different recourse.",
        "ar": "دفع PayPal هنا أو عبر المتجر يمكن disputed عبر PayPal؛ الدفع بالبطاقة عبر المتجر — عبر البنك. تحويل المحفظة لا. نفس المنتج، recourse مختلف.",
        "ru": "PayPal здесь или в shop можно оспорить в PayPal; карта в shop — через банк. Кошелёк — нет. Тот же продукт, разный recourse.",
        "zh": "此处或商店的 PayPal 可通过 PayPal 争议；商店卡支付通过发卡行。钱包转账不可。同一产品，救济途径不同。",
    },
    "refunds_lead": {
        "en": "If you want your money back, you get it.",
        "ar": "إن أردت أموالك، تحصل عليها.",
        "ru": "Хотите деньги назад — получите.",
        "zh": "要退款就能退。",
    },
    "refunds_p1": {
        "en": "No form, no reason, no time limit, no exceptions. Mail <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> and say you want a refund.",
        "ar": "بدون نموذج، بدون سبب، بدون مهلة، بدون استثناء. راسل <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> وقل إنك تريد استردادًا.",
        "ru": "Без формы, причины, срока и исключений. Напишите на <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> о возврате.",
        "zh": "无需表单、理由、时限或例外。邮件 <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> 说明要退款。",
    },
    "refunds_p2": {
        "en": "This covers everything QUAY sells — the fee review, Land reports, proof cards, Node Watch. Before we start, after we deliver, either way.",
        "ar": "يشمل كل ما يبيعه QUAY — مراجعة الرسوم، Land، البطاقات، Node Watch. قبل البدء أو بعد التسليم.",
        "ru": "На всё QUAY — fee review, Land, карты, Node Watch. До старта или после дelivery.",
        "zh": "涵盖 QUAY 全部产品——费用审查、Land、卡片、Node Watch。开始前或交付后均可。",
    },
    "refunds_p3": {
        "en": "We would rather return money than keep money someone does not want us to have.",
        "ar": "نفضّل إرجاع المال على الإبقاء على مال لا يريد صاحبه أن نحتفظ به.",
        "ru": "Лучше вернуть деньги, чем держать то, что клиент не хочет нам оставлять.",
        "zh": "我们宁愿退钱，也不留您不想让我们持有的款项。",
    },
    "refunds_paypal_body": {
        "en": "back to the same card or PayPal account, 5–10 business days. A PayPal payment can also be disputed through PayPal.",
        "ar": "إلى نفس البطاقة أو حساب PayPal، 5–10 أيام عمل. يمكن أيضًا disputed عبر PayPal.",
        "ru": "На ту же карту или PayPal, 5–10 раб. дней. Можно оспорить в PayPal.",
        "zh": "退回原卡或 PayPal，5–10 个工作日。也可通过 PayPal 争议。",
    },
    "refunds_paypal_label": {
        "en": "Paid with PayPal here, or through the shop checkout",
        "ar": "Paid with PayPal here, or through the shop checkout",
        "ru": "Оплата PayPal здесь или через shop checkout",
        "zh": "此处 PayPal 或商店结账",
    },
    "refunds_title": {
        "en": "Refunds",
        "ar": "الاسترداد",
        "ru": "Возвраты",
        "zh": "退款",
    },
    "refunds_wallet_body": {
        "en": "back to the address it came from, same asset, same network, within 3 business days, minus the network fee. Send from an address you control; we cannot refund an exchange deposit address.",
        "ar": "إلى العنوان المرسل منه، نفس الأصل والشبكة، خلال 3 أيام عمل ناقص رسوم الشبكة. أرسل من عنوان تتحكم به؛ لا نسترد عنوان إيداع exchange.",
        "ru": "На адрес отправителя, тот же asset и сеть, за 3 раб. дня минус fee. Только адрес под вашим контролем; deposit биржи — нет.",
        "zh": "退回来源地址，同资产同网络，3 个工作日内（扣网络费）。请用您控制的地址；无法退至交易所充值地址。",
    },
    "refunds_wallet_label": {
        "en": "Wallet",
        "ar": "المحفظة",
        "ru": "Кошелёк",
        "zh": "钱包",
    },
    "refunds_where_aria": {
        "en": "Refunds and where we are",
        "ar": "الاسترداد وأين نحن",
        "ru": "Возвраты и где мы",
        "zh": "退款与我们在哪",
    },
    "score_blurb": {
        "en": "A read-only note on one mint. Not a sell bot, not advice.",
        "ar": "ملاحظة للقراءة فقط على mint واحد. ليس bot بيع ولا نصيحة.",
        "ru": "Read-only заметка по одному mint. Не sell-бот и не совет.",
        "zh": "单个 mint 只读说明。非卖出机器人，非投资建议。",
    },
    "score_get": {
        "en": "A written note by email.",
        "ar": "ملاحظة مكتوبة بالبريد.",
        "ru": "Письменная заметка по email.",
        "zh": "邮件书面说明。",
    },
    "score_send": {
        "en": "The mint address.",
        "ar": "عنوان الـ mint.",
        "ru": "Адрес mint.",
        "zh": "mint 地址。",
    },
    "score_title": {
        "en": "Score report",
        "ar": "Score report",
        "ru": "Score report",
        "zh": "Score report",
    },
    "score_when": {
        "en": "Confirmed in reply to your order.",
        "ar": "يُؤكَّد في رد على طلبك.",
        "ru": "Подтверждаем в ответ на заказ.",
        "zh": "下单后邮件确认。",
    },
    "shop_alt": {
        "en": "or use the shop checkout",
        "ar": "أو من متجر الدفع",
        "ru": "или через shop checkout",
        "zh": "或使用商店结账",
    },
    "skip_main": {
        "en": "Skip to main content",
        "ar": "تخطي إلى المحتوى الرئيسي",
        "ru": "Перейти к основному содержанию",
        "zh": "跳到主要内容",
    },
    "spec_get": {
        "en": "You get",
        "ar": "تحصل",
        "ru": "Вы получаете",
        "zh": "您获得",
    },
    "spec_send": {
        "en": "You send",
        "ar": "ترسل",
        "ru": "Вы присылаете",
        "zh": "您提供",
    },
    "spec_when": {
        "en": "When",
        "ar": "متى",
        "ru": "Срок",
        "zh": "时间",
    },
    "step1_body": {
        "en": "Signatures, a mint address, the feed to watch, or the text for your cards. Never a key or an RPC URL with a token in it.",
        "ar": "توقيعات، عنوان mint، الـ feed للمراقبة، أو نص البطاقات. لا مفتاحًا ولا RPC يحتوي token.",
        "ru": "Подписи, mint, feed для watch или текст для карт. Никогда ключ или RPC с token.",
        "zh": "签名、mint 地址、要监控的 feed 或卡片文案。不要密钥或带 token 的 RPC。",
    },
    "step1_title": {
        "en": "You send public data",
        "ar": "ترسل بيانات عامة",
        "ru": "Вы присылаете публичные данные",
        "zh": "您发送公开数据",
    },
    "step2_body": {
        "en": "Against what actually landed on chain. If something cannot be read from public data, we say UNKNOWN instead of guessing.",
        "ar": "مقابل ما landed فعليًا على السلسلة. إن تعذّر القراءة من بيانات عامة، نقول UNKNOWN بدل التخمين.",
        "ru": "Сверяем с тем, что реально landed в chain. Если из публичных данных не прочитать — пишем UNKNOWN, не угадываем.",
        "zh": "对照实际上链结果。无法从公开数据读取时，我们写 UNKNOWN，不猜测。",
    },
    "step2_title": {
        "en": "We read it",
        "ar": "نقرأها",
        "ru": "Мы читаем",
        "zh": "我们读取",
    },
    "step3_body": {
        "en": "By email or Telegram. Nothing of ours touches your config, your wallet or your transactions.",
        "ar": "بالبريد أو Telegram. لا شيء من عندنا يلمس إعداداتك أو محفظتك أو معاملاتك.",
        "ru": "По email или Telegram. Ничего наше не трогает ваш config, кошелёк или транзакции.",
        "zh": "通过邮件或 Telegram。我们的东西不会碰您的配置、钱包或交易。",
    },
    "step3_title": {
        "en": "You get a file, a card or a ping",
        "ar": "تحصل على ملف أو بطاقة أو تنبيه",
        "ru": "Вы получаете файл, карту или ping",
        "zh": "您收到文件、卡片或提醒",
    },
    "thanks_brief_fees_link": {
        "en": "its page",
        "ar": "صفحتها",
        "ru": "её странице",
        "zh": "该页",
    },
    "thanks_brief_p1": {
        "en": "The product you paid for, your PayPal transaction ID, and what the product page asks you to send — for the fee review, the signatures and settings listed on",
        "ar": "المنتج الذي دفعت له، PayPal transaction ID، وما تطلبه صفحة المنتج — لمراجعة الرسوم، التوقيعات والإعدادات المذكورة في",
        "ru": "Продукт, PayPal transaction ID и то, что просит страница продукта — для fee review подписи и настройки на",
        "zh": "所购产品、PayPal 交易号，以及产品页要求的内容——费用审查的签名与设置见",
    },
    "thanks_brief_p2_prefix": {
        "en": "Refunds follow",
        "ar": "الاسترداد وفق",
        "ru": "Возврат по",
        "zh": "退款遵循",
    },
    "thanks_brief_p2_suffix": {
        "en": ". A PayPal payment can also be disputed through PayPal.",
        "ar": ". يمكن disputed عبر PayPal أيضًا.",
        "ru": ". PayPal можно оспорить.",
        "zh": "。也可通过 PayPal 争议。",
    },
    "thanks_brief_title": {
        "en": "What to put in the brief",
        "ar": "ماذا تضع في الـ brief",
        "ru": "Что указать в brief",
        "zh": "brief 应包含什么",
    },
    "thanks_h1": {
        "en": "PayPal has your payment",
        "ar": "PayPal استلم دفعتك",
        "ru": "PayPal получил оплату",
        "zh": "PayPal 已收到您的付款",
    },
    "thanks_kicker": {
        "en": "QUAY · Payment",
        "ar": "QUAY · الدفع",
        "ru": "QUAY · Оплата",
        "zh": "QUAY · 付款",
    },
    "thanks_lede": {
        "en": "Send your brief to <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> with your PayPal transaction ID. We start once the payment shows in PayPal.",
        "ar": "أرسل brief إلى <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> مع PayPal transaction ID. نبدأ عندما تظهر الدفعة في PayPal.",
        "ru": "Brief на <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> с PayPal transaction ID. Стартуем, когда платёж виден в PayPal.",
        "zh": "请将 brief 发至 <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a> 并附上 PayPal 交易号。PayPal 显示付款后我们开始。",
    },
    "thanks_meta_description": {
        "en": "PayPal has your payment. Send your brief to support@elghaly.dev with your PayPal transaction ID.",
        "ar": "PayPal استلم دفعتك. أرسل brief إلى support@elghaly.dev مع PayPal transaction ID.",
        "ru": "PayPal получил оплату. Brief на support@elghaly.dev с PayPal transaction ID.",
        "zh": "PayPal 已收到付款。请将 brief 发至 support@elghaly.dev 并附上 PayPal 交易号。",
    },
    "thanks_meta_title": {
        "en": "Thank you — QUAY · 35 ElGhaly",
        "ar": "شكرًا — QUAY · 35 ElGhaly",
        "ru": "Спасибо — QUAY · 35 ElGhaly",
        "zh": "谢谢 — QUAY · 35 ElGhaly",
    },
    "thanks_refund_link": {
        "en": "our refund policy",
        "ar": "سياسة الاسترداد",
        "ru": "политике возвратов",
        "zh": "退款政策",
    },
    "trust1_body": {
        "en": "No keys, no seed phrase, no wallet access. Ever.",
        "ar": "لا مفاتيح، لا عبارة استرداد، لا وصول للمحفظة. أبدًا.",
        "ru": "Никаких ключей, seed-фраз и доступа к кошельку. Никогда.",
        "zh": "不要密钥、助记词或钱包访问。绝不。",
    },
    "trust1_title": {
        "en": "Public data in",
        "ar": "بيانات عامة فقط",
        "ru": "Только публичные данные",
        "zh": "只用公开数据",
    },
    "trust2_body": {
        "en": "No form, no reason, no time limit.",
        "ar": "بدون نموذج، بدون سبب، بدون مهلة.",
        "ru": "Без формы, без причины, без срока.",
        "zh": "无需表单、理由或时限。",
    },
    "trust2_link": {
        "en": "How",
        "ar": "كيف",
        "ru": "Как",
        "zh": "如何",
    },
    "trust2_title": {
        "en": "Refund any time",
        "ar": "استرداد في أي وقت",
        "ru": "Возврат в любой момент",
        "zh": "随时退款",
    },
    "trust3_body": {
        "en": "elghaly, LLC.",
        "ar": "elghaly, LLC.",
        "ru": "elghaly, LLC.",
        "zh": "elghaly, LLC.",
    },
    "trust3_link": {
        "en": "Where we are",
        "ar": "أين نحن",
        "ru": "Где мы",
        "zh": "我们在哪",
    },
    "trust3_title": {
        "en": "A real company",
        "ar": "شركة حقيقية",
        "ru": "Настоящая компания",
        "zh": "真实公司",
    },
    "wallet_irreversible": {
        "en": "A wallet transfer cannot be reversed. There is no chargeback. Read what you are buying before you send.",
        "ar": "تحويل المحفظة لا يُعكَس. لا chargeback. اقرأ ما تشتري قبل الإرسال.",
        "ru": "Перевод кошельком необратим. Chargeback нет. Прочитайте, что покупаете, до отправки.",
        "zh": "钱包转账不可撤销。无 chargeback。发送前请确认购买内容。",
    },
    "wallet_kicker": {
        "en": "Wallet send",
        "ar": "الدفع من المحفظة",
        "ru": "Оплата кошельком",
        "zh": "钱包支付",
    },
    "wallet_network": {
        "en": "ETH and Base use the same address format. Sending on the wrong network loses the funds and cannot be recovered.",
        "ar": "ETH و Base يستخدمان نفس شكل العنوان. الشبكة الخاطئة تفقد الأموال ولا تُسترد.",
        "ru": "ETH и Base — один формат адреса. Неверная сеть = потеря средств без возврата.",
        "zh": "ETH 与 Base 地址格式相同。发错网络会永久丢失资金。",
    },
    "wallet_p1": {
        "en": "Same prices as the shop. Send the product amount, then mail the hash to <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>.",
        "ar": "نفس أسعار المتجر. أرسل مبلغ المنتج، ثم راسل الـ hash إلى <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>.",
        "ru": "Те же цены, что в shop. Отправьте сумму продукта, затем hash на <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>.",
        "zh": "与商店同价。发送产品金额，再将 hash 邮件至 <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>。",
    },
    "wallet_title": {
        "en": "Pay from your wallet",
        "ar": "ادفع من محفظتك",
        "ru": "Платите кошельком",
        "zh": "用钱包支付",
    },
    "watch_blurb": {
        "en": "A Telegram ping when an RPC or gRPC feed goes quiet.",
        "ar": "تنبيه Telegram عندما يصمت feed من RPC أو gRPC.",
        "ru": "Ping в Telegram, когда RPC/gRPC feed замолкает.",
        "zh": "RPC 或 gRPC feed 静默时 Telegram 提醒。",
    },
    "watch_get": {
        "en": "Alerts in Telegram.",
        "ar": "تنبيهات في Telegram.",
        "ru": "Алерты в Telegram.",
        "zh": "Telegram 提醒。",
    },
    "watch_send": {
        "en": "Which feed to watch.",
        "ar": "أي feed نراقبه.",
        "ru": "Какой feed смотреть.",
        "zh": "要监控的 feed。",
    },
    "watch_title": {
        "en": "Node Watch",
        "ar": "Node Watch",
        "ru": "Node Watch",
        "zh": "Node Watch",
    },
    "watch_when": {
        "en": "Once you have sent us the feed.",
        "ar": "بعد أن ترسل لنا الـ feed.",
        "ru": "После того как пришлёте feed.",
        "zh": "您发来 feed 之后。",
    },
    "where_contact": {
        "en": "Email first: <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>. Calls only by appointment.",
        "ar": "البريد أولًا: <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>. المكالمات بموعد فقط.",
        "ru": "Сначала email: <a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>. Звонки только по записи.",
        "zh": "优先邮件：<a href=\"mailto:support@elghaly.dev\">support@elghaly.dev</a>。通话仅预约。",
    },
    "where_li1": {
        "en": "The four wallet addresses below each link to a public explorer. Open them and read the history before you send anything — that is a check you can run without us.",
        "ar": "عناوين المحفظة الأربعة أدناه تربط بمستكشف عام. افتحها واقرأ السجل قبل الإرسال — تحقق بدوننا.",
        "ru": "Четыре адреса кошелька ниже ведут в explorer. Откройте историю до отправки — проверка без нас.",
        "zh": "下方四个钱包地址链到公开浏览器。发送前请自行查看历史——无需通过我们。",
    },
    "where_li2": {
        "en": "Refunds are unconditional. Ask and the money goes back. That is the cheapest way to find out whether we keep our word.",
        "ar": "الاسترداد غير مشروط. اطلب فيُرجع المال. أرخص طريقة لمعرفة إن كنا نفي بوعودنا.",
        "ru": "Возврат без условий. Попросили — вернули. Дешёвая проверка, держим ли слово.",
        "zh": "退款无条件。开口即退。这是验证我们是否守诺的最便宜方式。",
    },
    "where_li3_link": {
        "en": "$199 buys a written fee review",
        "ar": "199$ تشتري مراجعة رسوم مكتوبة",
        "ru": "$199 — письменный fee review",
        "zh": "$199 购买书面费用审查",
    },
    "where_li3_tail": {
        "en": "with nothing of yours at risk — no keys, no wallet, no access to anything. Cheaper still: the $29 Flex card pack.",
        "ar": " بلا مخاطرة على مفاتيح أو محفظة أو وصول. أرخص: حزمة Flex card بـ 29$.",
        "ru": " без ключей, кошелька и доступа. Дешевле — Flex card pack за $29.",
        "zh": " 无密钥、钱包或访问风险。更便宜：$29 Flex 卡片包。",
    },
    "where_p1": {
        "en": "QUAY is a remote desk. Support is by email, and the handover call is scheduled to your timezone, not ours. There is no counter to walk into, so hold us to the things you can actually test instead:",
        "ar": "QUAY مكتب عن بُعد. الدعم بالبريد، والمكالمة حسب منطقتك الزمنية. لا مكتب تزوره — لذا اختبر ما يمكنك التحقق منه:",
        "ru": "QUAY — удалённый desk. Поддержка email, созвон по вашему TZ. Нет офиса — проверяйте то, что можете сами:",
        "zh": "QUAY 是远程 desk。邮件支持，交接通话按您的时区。没有门店——请验证您自己能核实的事：",
    },
    "where_p2": {
        "en": "We are a small remote operation, not a large supplier with a legal department behind it. If that matters for your purchase, ask before you pay and we will tell you plainly what we can and cannot commit to.",
        "ar": "عملية صغيرة عن بُعد، وليست موردًا كبيرًا بقسم قانوني. إن كان ذلك مهمًا لشرائك، اسأل قبل الدفع وسنقول بوضوح ما نستطيع وما لا نستطيع.",
        "ru": "Маленькая удалённая команда, не крупный поставщик с legal. Если важно для покупки — спросите до оплаты, скажем честно, что можем и не можем.",
        "zh": "我们是小型远程团队，不是有法务部门的大供应商。若对采购重要，请先问清我们能与不能承诺什么。",
    },
    "where_title": {
        "en": "Where we are",
        "ar": "أين نحن",
        "ru": "Где мы",
        "zh": "我们在哪",
    },
    "wide_img_alt": {
        "en": "35 QUAY ElGhaly",
        "ar": "35 QUAY ElGhaly",
        "ru": "35 QUAY ElGhaly",
        "zh": "35 QUAY ElGhaly",
    },
}

MARKER_RE = re.compile(
    r"<!--i18n:([a-z0-9_]+)-->(.*?)<!--/i18n:\1-->",
    re.DOTALL,
)


def lang_href(locale: str, page: str) -> str:
    """page like '' (home), 'quay/fees.html', 'index.html' for home."""
    pref = LOCALES[locale]["prefix"]
    if page in ("", "index.html"):
        return f"/{pref}" if pref else "/"
    return f"/{pref}{page}"


def asset_prefix_for(locale: str, dest_rel: str) -> str:
    """Relative prefix from generated HTML file to repo-root assets."""
    meta = LOCALES[locale]
    depth = 0
    if meta["prefix"]:
        depth += 1
    if dest_rel != "index.html":
        depth += dest_rel.count("/")
    return "../" * depth if depth else ""


def apply_locale(html: str, locale: str, page: str, dest_rel: str) -> str:
    meta = LOCALES[locale]

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key == "html_lang":
            return f"<!--i18n:html_lang-->{meta['lang']}<!--/i18n:html_lang-->"
        if key == "html_dir":
            return f"<!--i18n:html_dir-->{meta['dir']}<!--/i18n:html_dir-->"
        if key == "asset_prefix":
            ap = asset_prefix_for(locale, dest_rel)
            return f"<!--i18n:asset_prefix-->{ap}<!--/i18n:asset_prefix-->"
        if key == "home_href":
            return f"<!--i18n:home_href-->{lang_href(locale, '')}<!--/i18n:home_href-->"
        if key.startswith("href_"):
            target = key[5:].replace("_", "/")
            if target == "fees":
                target = "quay/fees.html"
            elif target == "hold":
                target = "quay/hold.html"
            elif target == "thanks":
                target = "quay/thanks.html"
            elif target == "products":
                h = lang_href(locale, "")
                return f"<!--i18n:{key}-->{h}#products<!--/i18n:{key}-->"
            href = lang_href(locale, target)
            return f"<!--i18n:{key}-->{href}<!--/i18n:{key}-->"
        if key.startswith("lang_link_"):
            loc = key.replace("lang_link_", "")
            href = lang_href(loc, page)
            return f"<!--i18n:{key}-->{href}<!--/i18n:{key}-->"
        if key.startswith("lang_current_"):
            loc = key.replace("lang_current_", "")
            cur = ' aria-current="page"' if loc == locale else ""
            return f"<!--i18n:{key}-->{cur}<!--/i18n:{key}-->"
        if key == "canonical_url":
            path = lang_href(locale, page if page else "index.html")
            return f"<!--i18n:canonical_url-->https://quay-35.elghaly.dev{path}<!--/i18n:canonical_url-->"
        if key.startswith("hreflang_"):
            loc = key.replace("hreflang_", "")
            path = lang_href(loc, page if page else "index.html")
            return f"<!--i18n:{key}-->https://quay-35.elghaly.dev{path}<!--/i18n:{key}-->"
        if key in STRINGS:
            text = STRINGS[key].get(locale, STRINGS[key]["en"])
            return f"<!--i18n:{key}-->{text}<!--/i18n:{key}-->"
        return match.group(0)

    out = MARKER_RE.sub(repl, html)
    # Strip markers, keep inner content
    out = MARKER_RE.sub(lambda m: m.group(2), out)
    return out


def build_template(src: Path, dest_rel: str) -> None:
    html = src.read_text(encoding="utf-8")
    page = dest_rel.replace("index.html", "").lstrip("/")
    for loc, meta in LOCALES.items():
        out_root = meta["root"]
        dest = out_root / dest_rel if dest_rel != "index.html" else out_root / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        body = apply_locale(html, loc, page if page else "index.html", dest_rel)
        dest.write_text(body, encoding="utf-8")
        if loc == "en" and dest_rel == "index.html":
            (ROOT / "index.html").write_text(body, encoding="utf-8")


def main() -> None:
    templates = [
        (ROOT / "_templates" / "index.html", "index.html"),
        (ROOT / "_templates" / "fees.html", "quay/fees.html"),
        (ROOT / "_templates" / "hold.html", "quay/hold.html"),
        (ROOT / "_templates" / "thanks.html", "quay/thanks.html"),
    ]
    for src, rel in templates:
        if not src.is_file():
            raise SystemExit(f"Missing template: {src}")
        build_template(src, rel)
    print("Built locales:", ", ".join(LOCALES))


if __name__ == "__main__":
    main()
