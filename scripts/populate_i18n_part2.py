# Part 2 translations for populate_i18n.py
from __future__ import annotations

from typing import Callable


def register_part2(add: Callable[[str, str, str, str], None]) -> None:
    # Fee review product (home)
    add("fee_badge", "ابدأ هنا", "Начните здесь", "从这里开始")
    add("fee_title", "مراجعة الرسوم", "Разбор комиссий", "费用审查")
    add(
        "fee_blurb",
        "إعدادات priority fee والإكرامية، مقروءة مقابل ما دفعته معاملاتك العامة فعليًا وما landed عنده.",
        "Ваши priority fee и tip сверяются с тем, что публичные транзакции реально платили и где landed.",
        "根据您公开交易的实际支付与上链情况，审阅优先费与小费设置。",
    )
    add(
        "fee_send",
        "حتى 200 توقيع معاملة وإعداداتك الحالية. لا شيء خاص.",
        "До 200 подписей транзакций и текущие настройки. Ничего приватного.",
        "最多 200 条交易签名及当前设置。不含私密信息。",
    )
    add(
        "fee_get",
        "صفحة مكتوبة واحدة: الم percentile الذي landed عنده، الهدف، وأين تدفع زيادة. الفجوات تقول UNKNOWN.",
        "Одна страница: percentile landed, цель, где переплата. Пробелы — UNKNOWN.",
        "一页书面报告：实际上链分位、目标分位、多付之处；未知处标 UNKNOWN。",
    )
    add("fee_when", "خلال 48 ساعة من brief كامل.", "В течение 48 часов после полного brief.", "完整 brief 后 48 小时内。")
    add("fee_cta", "التفاصيل والـ brief", "Детали и brief", "详情与 brief")

    add("land_title", "QUAY Land", "QUAY Land", "QUAY Land")
    add(
        "land_blurb",
        "ورقة أسبوعية لروبوت واحد: landed مقابل failed، وأين تُهدر الإكراميات.",
        "Еженедельный отчёт для одного бота: landed vs failed и где теряются tips.",
        "单个机器人周报：上链 vs 失败，以及小费浪费位置。",
    )
    add("land_send", "Hashes المعاملات. المحفظة تبقى عندك.", "Хеши транзакций. Кошелёк остаётся у вас.", "交易哈希。钱包仍在您处。")
    add("land_get", "تقرير مكتوب كل أسبوع بالبريد.", "Письменный отчёт каждую неделю по email.", "每周邮件书面报告。")
    add("land_when", "يُؤكَّد في رد على طلبك.", "Подтверждаем в ответ на заказ.", "下单后邮件确认。")

    add("watch_title", "Node Watch", "Node Watch", "Node Watch")
    add(
        "watch_blurb",
        "تنبيه بالبريد عندما يصمت feed من RPC أو gRPC.",
        "Ping по email, когда RPC/gRPC feed замолкает.",
        "RPC 或 gRPC feed 静默时邮件提醒。",
    )
    add("watch_send", "أي feed نراقبه.", "Какой feed смотреть.", "要监控的 feed。")
    add("watch_get", "تنبيهات بالبريد.", "Алерты по email.", "邮件提醒。")
    add("watch_when", "بعد أن ترسل لنا الـ feed.", "После того как пришлёте feed.", "您发来 feed 之后。")

    add("score_title", "Score report", "Score report", "Score report")
    add(
        "score_blurb",
        "ملاحظة للقراءة فقط على mint واحد. ليس bot بيع ولا نصيحة.",
        "Заметка с доступом на просмотр по одному mint. Не sell-бот и не совет.",
        "单个 mint 只读说明。非卖出机器人，非投资建议。",
    )
    add("score_send", "عنوان الـ mint.", "Адрес mint.", "mint 地址。")
    add("score_get", "ملاحظة مكتوبة بالبريد.", "Письменная заметка по email.", "邮件书面说明。")
    add("score_when", "يُؤكَّد في رد على طلبك.", "Подтверждаем в ответ на заказ.", "下单后邮件确认。")

    add("flex_title", "Flex card pack", "Flex card pack", "Flex card pack")
    add(
        "flex_blurb",
        "بطاقات إثبات للمكتب بتنسيق 35 من نص ترسله. لا أرقام مخترعة منا.",
        "Proof-карты в lockup 35 из вашего текста. Без выдуманных цифр.",
        "用您提供的文案制作 35 版式桌面证明卡。我们不编造数字。",
    )
    add("flex_send", "نص البطاقات.", "Текст для карт.", "卡片文案。")
    add("flex_get", "بطاقات صور بالبريد.", "Картинки-карты по email.", "邮件发送图片卡片。")
    add("flex_when", "يُؤكَّد في رد على طلبك.", "Подтверждаем в ответ на заказ.", "下单后邮件确认。")

    add("ask_title", "غير متأكد أي واحد؟", "Не уверены, что выбрать?", "不确定选哪个？")
    add(
        "ask_blurb",
        'راسل <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> بما تشغّله. نرد بأصغر منتج يناسب — أو نقول بوضوح أن لا شيء يناسب.',
        'Напишите на <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>, что вы запускаете. Ответим минимальным продуктом — или честно скажем, что ни один не подходит.',
        '邮件 <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> 说明您在跑什么。我们会推荐最小合适产品，或明确说明都不合适。',
    )
    add("ask_cta", "اسأل أولًا", "Сначала спросить", "先咨询")

    add(
        "paypal_land_aria",
        "الدفع عبر PayPal: QUAY Land، 149$ / شهر",
        "Оплата PayPal: QUAY Land, $149 / мес.",
        "PayPal 支付：QUAY Land，$149/月",
    )
    add(
        "paypal_watch_aria",
        "الدفع عبر PayPal: Node Watch، 79$ / شهر",
        "Оплата PayPal: Node Watch, $79 / мес.",
        "PayPal 支付：Node Watch，$79/月",
    )
    add(
        "paypal_score_aria",
        "الدفع عبر PayPal: Score report، 49$ مرة واحدة",
        "Оплата PayPal: Score report, $49 разово",
        "PayPal 支付：Score report，$49 一次性",
    )
    add(
        "paypal_flex_aria",
        "الدفع عبر PayPal: Flex card pack، 29$ مرة واحدة",
        "Оплата PayPal: Flex card pack, $29 разово",
        "PayPal 支付：Flex card pack，$29 一次性",
    )

    add("wide_img_alt", "35 QUAY ElGhaly", "35 QUAY ElGhaly", "35 QUAY ElGhaly")
    add(
        "recourse",
        "دفع PayPal هنا أو عبر المتجر يمكن disputed عبر PayPal؛ الدفع بالبطاقة عبر المتجر — عبر البنك. تحويل المحفظة لا. نفس المنتج، recourse مختلف.",
        "PayPal здесь или в shop можно оспорить в PayPal; карта в shop — через банк. Кошелёк — нет. Тот же продукт, разный recourse.",
        "此处或商店的 PayPal 可通过 PayPal 争议；商店卡支付通过发卡行。钱包转账不可。同一产品，救济途径不同。",
    )

    add("refunds_where_aria", "الاسترداد وأين نحن", "Возвраты и где мы", "退款与我们在哪")
    add("refunds_title", "الاسترداد", "Возвраты", "退款")
    add("refunds_lead", "إن أردت أموالك، تحصل عليها.", "Хотите деньги назад — получите.", "要退款就能退。")
    add(
        "refunds_p1",
        'بدون نموذج، بدون سبب، بدون مهلة، بدون استثناء. راسل <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> وقل إنك تريد استردادًا.',
        'Без формы, причины, срока и исключений. Напишите на <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> о возврате.',
        '无需表单、理由、时限或例外。邮件 <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> 说明要退款。',
    )
    add(
        "refunds_p2",
        "يشمل كل ما يبيعه QUAY — مراجعة الرسوم، Land، البطاقات، Node Watch. قبل البدء أو بعد التسليم.",
        "На всё QUAY — fee review, Land, карты, Node Watch. До старта или после дelivery.",
        "涵盖 QUAY 全部产品——费用审查、Land、卡片、Node Watch。开始前或交付后均可。",
    )
    add("refunds_paypal_label", "Paid with PayPal here, or through the shop checkout", "Оплата PayPal здесь или через shop checkout", "此处 PayPal 或商店结账")
    add(
        "refunds_paypal_body",
        "إلى نفس البطاقة أو حساب PayPal، 5–10 أيام عمل. يمكن أيضًا disputed عبر PayPal.",
        "На ту же карту или PayPal, 5–10 раб. дней. Можно оспорить в PayPal.",
        "退回原卡或 PayPal，5–10 个工作日。也可通过 PayPal 争议。",
    )
    add("refunds_wallet_label", "المحفظة", "Кошелёк", "钱包")
    add(
        "refunds_wallet_body",
        "إلى العنوان المرسل منه، نفس الأصل والشبكة، خلال 3 أيام عمل ناقص رسوم الشبكة. أرسل من عنوان تتحكم به؛ لا نسترد عنوان إيداع exchange.",
        "На адрес отправителя, тот же asset и сеть, за 3 раб. дня минус fee. Только адрес под вашим контролем; deposit биржи — нет.",
        "退回来源地址，同资产同网络，3 个工作日内（扣网络费）。请用您控制的地址；无法退至交易所充值地址。",
    )
    add(
        "refunds_p3",
        "نفضّل إرجاع المال على الإبقاء على مال لا يريد صاحبه أن نحتفظ به.",
        "Лучше вернуть деньги, чем держать то, что клиент не хочет нам оставлять.",
        "我们宁愿退钱，也不留您不想让我们持有的款项。",
    )

    add("where_title", "أين نحن", "Где мы", "我们在哪")
    add(
        "where_contact",
        'البريد أولًا: <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>. المكالمات بموعد فقط.',
        'Сначала email: <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>. Звонки только по записи.',
        '优先邮件：<a href="mailto:support@elghaly.dev">support@elghaly.dev</a>。通话仅预约。',
    )
    add(
        "where_p1",
        "QUAY مكتب عن بُعد. الدعم بالبريد، والمكالمة حسب منطقتك الزمنية. لا مكتب تزوره — لذا اختبر ما يمكنك التحقق منه:",
        "QUAY — удалённый desk. Поддержка email, созвон по вашему TZ. Нет офиса — проверяйте то, что можете сами:",
        "QUAY 是远程 desk。邮件支持，交接通话按您的时区。没有门店——请验证您自己能核实的事：",
    )
    add(
        "where_li1",
        "عناوين المحفظة الأربعة أدناه تربط بمستكشف عام. افتحها واقرأ السجل قبل الإرسال — تحقق بدوننا.",
        "Четыре адреса кошелька ниже ведут в explorer. Откройте историю до отправки — проверка без нас.",
        "下方四个钱包地址链到公开浏览器。发送前请自行查看历史——无需通过我们。",
    )
    add(
        "where_li2",
        "الاسترداد غير مشروط. اطلب فيُرجع المال. أرخص طريقة لمعرفة إن كنا نفي بوعودنا.",
        "Возврат без условий. Попросили — вернули. Дешёвая проверка, держим ли слово.",
        "退款无条件。开口即退。这是验证我们是否守诺的最便宜方式。",
    )
    add("where_li3_link", "199$ تشتري مراجعة رسوم مكتوبة", "$199 — письменный fee review", "$199 购买书面费用审查")
    add(
        "where_li3_tail",
        " بلا مخاطرة على مفاتيح أو محفظة أو وصول. أرخص: حزمة Flex card بـ 29$.",
        " без ключей, кошелька и доступа. Дешевле — Flex card pack за $29.",
        " 无密钥、钱包或访问风险。更便宜：$29 Flex 卡片包。",
    )
    add(
        "where_p2",
        "عملية صغيرة عن بُعد، وليست موردًا كبيرًا بقسم قانوني. إن كان ذلك مهمًا لشرائك، اسأل قبل الدفع وسنقول بوضوح ما نستطيع وما لا نستطيع.",
        "Маленькая удалённая команда, не крупный поставщик с legal. Если важно для покупки — спросите до оплаты, скажем честно, что можем и не можем.",
        "我们是小型远程团队，不是有法务部门的大供应商。若对采购重要，请先问清我们能与不能承诺什么。",
    )

    add("wallet_kicker", "الدفع من المحفظة", "Оплата кошельком", "钱包支付")
    add("wallet_title", "ادفع من محفظتك", "Платите кошельком", "用钱包支付")
    add(
        "wallet_p1",
        'نفس أسعار المتجر. أرسل مبلغ المنتج، ثم راسل الـ hash إلى <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>.',
        'Те же цены, что в shop. Отправьте сумму продукта, затем hash на <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>.',
        '与商店同价。发送产品金额，再将 hash 邮件至 <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>。',
    )
    add(
        "wallet_irreversible",
        "تحويل المحفظة لا يُعكَس. لا chargeback. اقرأ ما تشتري قبل الإرسال.",
        "Перевод кошельком необратим. Chargeback нет. Прочитайте, что покупаете, до отправки.",
        "钱包转账不可撤销。无 chargeback。发送前请确认购买内容。",
    )
    add(
        "wallet_network",
        "ETH و Base يستخدمان نفس شكل العنوان. الشبكة الخاطئة تفقد الأموال ولا تُسترد.",
        "ETH и Base — один формат адреса. Неверная сеть = потеря средств без возврата.",
        "ETH 与 Base 地址格式相同。发错网络会永久丢失资金。",
    )
    add("copy_sol", "نسخ SOL", "Копировать SOL", "复制 SOL")
    add("copy_eth", "نسخ ETH", "Копировать ETH", "复制 ETH")
    add("copy_btc", "نسخ BTC", "Копировать BTC", "复制 BTC")
    add("copy_base", "نسخ Base", "Копировать Base", "复制 Base")
    add("copied", "تم النسخ", "Скопировано", "已复制")

    add(
        "footer_contact",
        'elghaly, LLC · البريد أولًا: <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>. المكالمات بموعد فقط.',
        'elghaly, LLC · Сначала email: <a href="mailto:support@elghaly.dev">support@elghaly.dev</a>. Звонки по записи.',
        'elghaly, LLC · 优先邮件：<a href="mailto:support@elghaly.dev">support@elghaly.dev</a>。通话仅预约。',
    )
    add("footer_about", "About", "About", "About")
    add("footer_contact_link", "Contact", "Contact", "Contact")
    add("footer_refunds", "الاسترداد", "Возвраты", "退款")
    add("footer_delivery", "Delivery", "Delivery", "Delivery")
    add("footer_terms", "Terms", "Terms", "Terms")
    add("footer_privacy", "Privacy", "Privacy", "Privacy")
    add("lic_cc", "© elghaly · CC BY 4.0", "© elghaly · CC BY 4.0", "© elghaly · CC BY 4.0")
    add("lic_mit", "Code: MIT", "Code: MIT", "Code: MIT")
    add("lic_oss", "Open source", "Open source", "Open source")
    add(
        "lic_ai",
        "تحليل بمساعدة AI لصفحات عامة",
        "AI-анализ публичных страниц",
        "AI 辅助分析公开页面",
    )
    add(
        "lic_ai_chain",
        "تحليل بمساعدة AI لبيانات عامة على السلسلة",
        "AI-анализ публичных on-chain данных",
        "AI 辅助分析公开链上数据",
    )

    # fees.html
    add("fees_meta_title", "مراجعة الرسوم — QUAY · 35 ElGhaly", "Разбор комиссий — QUAY · 35 ElGhaly", "费用审查 — QUAY · 35 ElGhaly")
    add(
        "fees_meta_description",
        "مراجعة priority fee والإكرامية خلال 48 ساعة من توقيعات عامة. 199$ مرة واحدة.",
        "Разбор priority fee и tip за 48 ч по публичным подписям. $199 разово.",
        "48 小时内基于公开签名的优先费与小费配置审查。$199 一次性。",
    )
    add("fees_kicker", "QUAY · مراجعة الرسوم", "QUAY · Разбор комиссий", "QUAY · 费用审查")
    add("fees_h1", "مراجعة إعداد priority fee والإكرامية", "Разбор priority fee и tip", "优先费与小费配置审查")
    add(
        "fees_lede1",
        "نقرأ توقيعات معاملاتك العامة ونقارن إعدادات priority fee والإكرامية بما دفعته تلك المعاملات فعليًا وما landed عنده.",
        "Читаем публичные подписи и сравниваем priority fee/tip с тем, что транзакции реально платили и где landed.",
        "读取您的公开交易签名，将当前优先费/小费设置与交易实际支付及上链情况对比。",
    )
    add(
        "fees_lede2",
        "صفحة مكتوبة واحدة خلال 48 ساعة من brief كامل. توصية فقط — لا نغيّر config أو محفظتك أو معاملاتك.",
        "Одна страница за 48 ч после полного brief. Только рекомендация — не трогаем config, кошелёк, транзакции.",
        "完整 brief 后 48 小时内交付一页书面报告。仅为建议——不改动配置、钱包或交易。",
    )
    add("fees_send_title", "ما ترسل", "Что прислать", "您需提供")
    add(
        "fees_send_intro",
        "كل هذا بيانات عامة. لا ترسل ما ليس ظاهرًا على السلسلة أو في explorer.",
        "Всё это публичные данные. Не присылайте то, чего нет в chain/explorer.",
        "均为公开数据。请勿发送链上或浏览器中不可见的内容。",
    )
    add("fees_send_li1_b", "حتى 200 توقيع معاملة", "До 200 подписей транзакций", "最多 200 条交易签名")
    add(
        "fees_send_li1",
        "توقيعات فقط. لا مفتاح خاص، لا seed phrase، لا RPC يحتوي token.",
        "Только подписи. Никогда private key, seed или RPC с token.",
        "仅签名。不要私钥、助记词或带 token 的 RPC。",
    )
    add("fees_send_li2_b", "إعداد priority fee الحالي", "Текущий priority fee", "当前优先费设置")
    add("fees_send_li3_b", "إعداد الإكرامية الحالي", "Текущий tip", "当前小费设置")
    add("fees_send_li4_b", "Venue أو aggregator الذي تمر عبره", "Venue или aggregator маршрута", "您使用的 venue 或 aggregator")
    add(
        "fees_send_note",
        "لن نطلب أو نعرض أو نقبل API key أو RPC يحتوي token أو مفتاحًا خاصًا.",
        "Не запрашиваем, не показываем и не принимаем API key, RPC с token или private key.",
        "我们不会索取、展示或接受 API key、含 token 的 RPC 或私钥。",
    )
    add("fees_get_title", "ما تحصل عليه", "Что получите", "您将获得")
    add("fees_get_intro", "صفحة واحدة خلال 48 ساعة من brief كامل:", "Одна страница за 48 ч после полного brief:", "完整 brief 后 48 小时内一页报告：")
    add("fees_get_li1", "الـ percentile الذي landed عنده إعدادك الحالي", "Percentile landed для текущих настроек", "当前设置实际上链分位")
    add("fees_get_li2", "الـ percentile المستهدف مع المبرر", "Целевой percentile с обоснованием", "目标分位及理由")
    add("fees_get_li3", "متى ترفع، والشرط الذي يجب أن يفعّل ذلك", "Когда повышать и условие триггера", "何时提高及触发条件")
    add("fees_get_li4", "أين تدفع زيادة، مع الهدر لكل tx landed", "Где переплата и waste на landed tx", "多付之处及每笔上链浪费量")
    add("fees_get_li5", "ما لم نستطع تحديده من التوقيعات، مسماة صراحة", "Что не вывели из подписей — явно по имени", "无法从签名确定的内容，明确列出")
    add(
        "fees_get_note",
        "إن تعذّر قراءة مدخل من التوقيع، يقول التقرير <strong>UNKNOWN</strong> — لا تخمين.",
        "Если из подписи не прочитать — в отчёте <strong>UNKNOWN</strong>, не догадка.",
        "签名无法读取的字段，报告写 <strong>UNKNOWN</strong>——不猜测。",
    )
    add(
        "fees_cannot_title",
        "ما لا نستطيع قوله من التوقيعات وحدها",
        "Чего не видно только по подписям",
        "仅凭签名无法告知的内容",
    )
    add(
        "fees_cannot_intro",
        "التوقيعات تظهر ما أُرسل وما landed. لا تظهر كل شيء عن عملك. على الأقل لا نرى:",
        "Подписи показывают submit и landed, не всю операцию. Минимум не видим:",
        "签名显示提交与上链，不能反映运营全貌。至少看不到：",
    )
    add("fees_cannot_li1_b", "تنفيذاتك (fills)", "Ваши fills", "成交（fills）")
    add("fees_cannot_li1", "هل حققت المعاملة landed النتيجة التي wanted", "Достигла ли landed tx нужного trade outcome", "上链交易是否达到预期成交结果")
    add("fees_cannot_li2_b", "استراتيجيتك", "Вашу стратегию", "您的策略")
    add("fees_cannot_li2", "النية، حجم الصفقة، أو قواعد التوقيت behind كل send", "Intent, sizing, timing rules за каждым send", "每次发送背后的意图、 sizing 与 timing 规则")
    add("fees_cannot_li3_b", "زمن RPC", "RPC latency", "RPC 延迟")
    add("fees_cannot_li3", "كم استغرق node أو المزود لنشر المعاملة", "Сколько node/провайдеру на propagate", "节点/提供商传播交易所用时间")
    add("fees_cannot_li4_b", "لماذا فشلت معاملة محددة", "Почему упала конкретная tx", "某笔交易失败原因")
    add(
        "fees_cannot_li4",
        "إن لم يُسجَّل الفشل on-chain (رفض simulation، packets، إلغاء client)",
        "Если failure не on-chain (simulation, drop, client abort)",
        "若失败未上链（模拟拒绝、丢包、客户端取消）",
    )
    add(
        "fees_unknown_rule",
        "ما لا يُستنتج من التوقيعات يُوسَم <strong>UNKNOWN</strong> في التقرير. لا نملأ الفجوات.",
        "Всё, что не выводится из подписей, — <strong>UNKNOWN</strong>. Пробелы не заполняем.",
        "无法从签名推导的内容在报告中标记 <strong>UNKNOWN</strong>。不填补空白。",
    )
    add("fees_sample_banner", "مثال تخطيط — ليس تقرير عميل حقيقي", "Пример макета — не реальный отчёт", "版式示例——非真实客户报告")
    add("fees_sample_title", "مراجعة الرسوم · مخرجات صفحة واحدة (شكل محذوف)", "Fee review · одна страница (redacted)", "费用审查 · 单页输出（脱敏样例）")
    add("fees_sample_scope", "نطاق العينة", "Sample scope", "样例范围")
    add("fees_sample_settings", "الإعدادات كما أُرسلت", "Settings as submitted", "提交的设置")
    add(
        "fees_sample_settings_dd",
        'Priority: <span class="redacted">[your value]</span> · Tip: <span class="redacted">[your value]</span>',
        'Priority: <span class="redacted">[your value]</span> · Tip: <span class="redacted">[your value]</span>',
        'Priority: <span class="redacted">[your value]</span> · Tip: <span class="redacted">[your value]</span>',
    )
    add("fees_sample_current", "الإعداد الحالي — landed percentile", "Текущие настройки — landed percentile", "当前设置 — 上链分位")
    add("fees_sample_target", "الـ percentile المستهدف الموصى به", "Рекомендуемый target percentile", "建议目标分位")
    add("fees_sample_raise", "متى ترفع", "Когда повышать", "何时提高")
    add("fees_sample_overpay", "دفع زائد", "Переплата", "多付")
    add("fees_sample_unknown", "تعذّر التحديد (UNKNOWN)", "Could not determine (UNKNOWN)", "无法确定 (UNKNOWN)")
    add("fees_price_title", "السعر والاستلام", "Цена и intake", "价格与提交")
    add("fees_price_note", "مرة واحدة · بالإنجليزية · PayPal أو فاتورة في الرد", "Разово · на английском · PayPal или invoice в ответе", "一次性 · 仅英文 · PayPal 或回复发票")
    add(
        "fees_price_p",
        "ادفع PayPal هنا وأرسل brief مع PayPal transaction ID، أو أرسل brief أولًا وادفع على الفاتورة عند التأكيد. لا نموذج على هذه الصفحة.",
        "PayPal здесь + brief с PayPal transaction ID, или brief сначала и invoice после подтверждения. Формы на странице нет.",
        "在此 PayPal 支付并邮件 brief 附 PayPal 交易号，或先发 brief 待确认后付发票。本页无表单。",
    )
    add(
        "fees_paypal_aria",
        "الدفع عبر PayPal: مراجعة الرسوم، 199$ مرة واحدة",
        "PayPal: Fee review, $199 разово",
        "PayPal：费用审查，$199 一次性",
    )
    add("fees_brief_btn", "أرسل brief — support@elghaly.dev", "Brief — support@elghaly.dev", "发送 brief — support@elghaly.dev")
    add(
        "fees_disclaimer",
        "توصية مكتوبة من بيانات سلسلة عامة. لا نلمس config أو محفظتك أو معاملاتك. اتباع التوصية قد لا يحسّن landed أو يخفض التكلفة، ولا نعد بذلك. لا ادعاءات أرباح أو ادخار.",
        "Письменная рекомендация по публичным chain-данным. Config/кошелёк/tx не трогаем. Следование может не улучшить landed или cost — не обещаем. Без claims о доходе/экономии.",
        "基于公开链上数据的书面建议。不碰配置、钱包或交易。遵循建议未必改善上链或降本，我们不做承诺。不宣称收益或节省。",
    )
    add("fees_refunds_lead", "إن أردت أموالك، تحصل عليها.", "Хотите деньги назад — получите.", "要退款就能退。")
    add("fees_where_link", "أين نحن", "Где мы", "我们在哪")

    # hold.html
    add(
        "hold_meta_title",
        "ما لن يبنيه QUAY — QUAY · 35 ElGhaly",
        "Что QUAY не будет строить — QUAY · 35 ElGhaly",
        "QUAY 不会做什么 — QUAY · 35 ElGhaly",
    )
    add(
        "hold_meta_description",
        "ثلاثة منتجات يرفض QUAY بناءها، ولماذا.",
        "Три продукта, которые QUAY отказывается делать, и почему.",
        "QUAY 拒绝做的三项产品及原因。",
    )
    add("hold_kicker", "QUAY · Hold", "QUAY · Hold", "QUAY · Hold")
    add("hold_h1", "ما لن يبنيه QUAY.", "Что QUAY не будет строить.", "QUAY 不会构建的内容。")
    add(
        "hold_lede",
        "تُطلب كثيرًا. إليك لماذا الجواب لا، وما الذي يجب أن يتغيّر.",
        "Спрашивают часто. Почему нет и что должно измениться.",
        "常被问起。说明为何拒绝，以及需要什么条件才会变。",
    )
    add("hold_copy_title", "Copy-mirroring", "Copy-mirroring", "Copy-mirroring")
    add(
        "hold_copy_body",
        "نسخ الصفقات تلقائيًا يحتاج مفاتيحك أو محفظة نتحكم بها، ولن نحتفظ بأيّ منهما.",
        "Авто-копирование сделок требует ваших ключей или нашего кошелька — мы не держим ни то, ни другое.",
        "自动跟单需要您的密钥或我们控制的钱包——两者我们都不持有。",
    )
    add("hold_panic_title", "Auto-panic sell", "Auto-panic sell", "Auto-panic sell")
    add(
        "hold_panic_body",
        "زر يبيع عنك هو صلاحية توقيع، ويوم يخطئ الخسارة لنا نجادل ولكنك تحملها.",
        "Кнопка «продать за вас» — signing authority; ошибся — спор наш, убыток ваш.",
        "代您卖出的按钮即签名权限；一旦误触，损失由您承担，争议归我们扯皮。",
    )
    add("hold_escrow_title", "Chat escrow", "Chat escrow", "Chat escrow")
    add(
        "hold_escrow_body",
        "ح holding أموال الغير بين غريبين يجعلنا أمينًا في نزاع لا نستطيع الفصل فيه.",
        "Держать чужие деньги между незнакомцами — мы custodian в споре без суда.",
        "在陌生人之间托管资金使我们成为无法裁决争议的保管人。",
    )
    add(
        "hold_closing",
        "تبقى مؤجّلة حتى يكون لـ QUAY Land ثلاثة مشغّلين يدفعون. ليس لأن المخاطر تتغيّر — لا تتغيّر — بل لأننا لن نتعلّم الحفظ على مال الغير.",
        "On hold, пока у QUAY Land не будет трёх платящих операторов. Риск тот же — но custody на чужих деньгах не учимся.",
        "在 QUAY Land 有三名付费运营者之前一直搁置。风险不变——但我们不会在别人的钱上学习托管。",
    )
    add("hold_footer_products", "كل المنتجات", "Все продукты", "全部产品")

    # thanks.html
    add("thanks_meta_title", "شكرًا — QUAY · 35 ElGhaly", "Спасибо — QUAY · 35 ElGhaly", "谢谢 — QUAY · 35 ElGhaly")
    add(
        "thanks_meta_description",
        "PayPal استلم دفعتك. أرسل brief إلى support@elghaly.dev مع PayPal transaction ID.",
        "PayPal получил оплату. Brief на support@elghaly.dev с PayPal transaction ID.",
        "PayPal 已收到付款。请将 brief 发至 support@elghaly.dev 并附上 PayPal 交易号。",
    )
    add("thanks_kicker", "QUAY · الدفع", "QUAY · Оплата", "QUAY · 付款")
    add("thanks_h1", "PayPal استلم دفعتك", "PayPal получил оплату", "PayPal 已收到您的付款")
    add(
        "thanks_lede",
        'أرسل brief إلى <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> مع PayPal transaction ID. نبدأ عندما تظهر الدفعة في PayPal.',
        'Brief на <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> с PayPal transaction ID. Стартуем, когда платёж виден в PayPal.',
        '请将 brief 发至 <a href="mailto:support@elghaly.dev">support@elghaly.dev</a> 并附上 PayPal 交易号。PayPal 显示付款后我们开始。',
    )
    add("thanks_brief_title", "ماذا تضع في الـ brief", "Что указать в brief", "brief 应包含什么")
    add(
        "thanks_brief_p1",
        "المنتج الذي دفعت له، PayPal transaction ID، وما تطلبه صفحة المنتج — لمراجعة الرسوم، التوقيعات والإعدادات المذكورة في",
        "Продукт, PayPal transaction ID и то, что просит страница продукта — для fee review подписи и настройки на",
        "所购产品、PayPal 交易号，以及产品页要求的内容——费用审查的签名与设置见",
    )
    add("thanks_brief_p2_prefix", "الاسترداد وفق", "Возврат по", "退款遵循")
    add(
        "thanks_brief_p2_suffix",
        ". يمكن disputed عبر PayPal أيضًا.",
        ". PayPal можно оспорить.",
        "。也可通过 PayPal 争议。",
    )
    add("thanks_brief_fees_link", "صفحتها", "её странице", "该页")
    add("thanks_refund_link", "سياسة الاسترداد", "политике возвратов", "退款政策")
