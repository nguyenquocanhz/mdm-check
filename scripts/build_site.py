#!/usr/bin/env python3
"""Sinh landing page tĩnh (tiếng Việt ở gốc, tiếng Anh ở /en/) vào thư mục docs/ cho GitHub Pages.

Chạy: python scripts/build_site.py
Không cần thư viện ngoài. Sửa nội dung ở biến PAGES, sửa giao diện ở docs/styles.css.
"""
import html
import io
import json
import os

SITE = "https://nguyenquocanhz.github.io/mdm-check/"
REPO = "https://github.com/nguyenquocanhz/mdm-check"
DOWNLOAD = REPO + "/releases/latest/download/MDMCheck.dmg"
VERSION = "0.1.1"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")

SHIELD = "M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"
ICONS = {
    "shield-check": [SHIELD, "m9 12 2 2 4-4"],
    "shield-alert": [SHIELD, "M12 8v4", "M12 16h.01"],
    "shield-x": [SHIELD, "m14.5 9.5-5 5", "m9.5 9.5 5 5"],
    "shield-question": [SHIELD, "M9.1 9a3 3 0 0 1 5.82 1c0 2-3 3-3 3", "M12 17h.01"],
    "download": ["M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4", "m7 10 5 5 5-5", "M12 15V3"],
    "arrow": ["M7 7h10v10", "M7 17 17 7"],
    "chevron": ["m6 9 6 6 6-6"],
    "x": ["M18 6 6 18", "m6 6 12 12"],
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    '<symbol id="i-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</symbol>'
    % (name, "".join('<path d="%s"/>' % d for d in paths))
    for name, paths in ICONS.items()
) + "</svg>"


def icon(name):
    return '<svg class="icon" aria-hidden="true"><use href="#i-%s"/></svg>' % name


VERDICT_ICON = {"clean": "shield-check", "enrolled": "shield-alert", "ade": "shield-x", "unknown": "shield-question"}

PAGES = {
    "vi": {
        "path": "",
        "title": "MDM Checker: kiểm tra MacBook cũ có dính MDM, ADE trước khi mua",
        "description": "App macOS miễn phí, mã nguồn mở. Hỏi thẳng Apple xem máy Mac cũ có thuộc công ty hay trường học nào không và trả lời: CLEAN, ENROLLED hay ADE RISK.",
        "nav": [("#cach-dung", "Cách dùng"), ("#cau-hoi", "Câu hỏi"), (REPO, "GitHub"), ("en/", "English")],
        "badge": "Miễn phí · Mã nguồn mở · Bản %s" % VERSION,
        "h1": "Kiểm tra MacBook cũ có dính MDM trước khi trả tiền",
        "lead": "MDM Checker hỏi thẳng Apple xem máy Mac có thuộc công ty hay trường học nào không, rồi trả lời bằng một chữ: sạch, đang bị quản lý, hay không nên mua.",
        "cta": "Tải cho macOS",
        "cta2": "Xem mã nguồn",
        "meta": "macOS 12 trở lên · chip Apple và Intel · 150 KB",
        "mock_caption": "Minh hoạ giao diện app với dữ liệu mẫu",
        "mock": {
            "code": "MDM: ADE RISK", "title": "Máy thuộc một tổ chức",
            "reason": "Apple đang gán số serial này cho một tổ chức. Xoá máy cài lại thì máy tự đăng ký lại MDM.",
            "advice_label": "Nên làm gì:", "advice": "Không nên mua. Chỉ tổ chức đó mới gỡ được máy.",
            "rows": [("Máy đang cài MDM?", "Có"), ("Đăng ký qua ADE/DEP?", "Có"), ("Apple gán số serial vào tổ chức?", "Có")],
        },
        "verdict_h2": "Bốn kết luận, mỗi kết luận một việc cần làm",
        "verdict_p": "Bạn không cần đọc kết quả lệnh. App đọc và nói thẳng nên làm gì.",
        "verdicts": [
            ("clean", "CLEAN", "Máy sạch", "Không có MDM, Apple xác nhận số serial không thuộc tổ chức nào."),
            ("enrolled", "ENROLLED", "Máy đang bị quản lý", "Máy đang cài hồ sơ quản lý từ xa. Người bán phải gỡ trước khi bạn trả tiền."),
            ("ade", "ADE RISK", "Máy thuộc một tổ chức", "Số serial thuộc một công ty hoặc trường học. Xoá máy cũng không hết. Đừng mua."),
            ("unknown", "CHƯA XÁC ĐỊNH", "Chưa đủ dữ liệu", "Thiếu mạng hoặc thiếu mật khẩu admin. App không bao giờ báo sạch khi chưa đủ dữ liệu."),
        ],
        "steps_id": "cach-dung",
        "steps_h2": "Dùng trong ba bước",
        "steps_p": "Mất khoảng một phút, ngay tại chỗ xem máy.",
        "steps": [
            ("Tải và mở app", "Chép file <code>MDMCheck.dmg</code> sang máy cần kiểm tra, mở ra và chạy app. macOS chặn thì vào System Settings, mục Privacy &amp; Security, bấm Open Anyway."),
            ("Bấm “Hỏi Apple về ADE”", "Nhập mật khẩu admin của máy. Máy phải đang có mạng."),
            ("Đọc kết luận", "Chép báo cáo để gửi người bán hoặc lưu làm bằng chứng."),
        ],
        "trust_h2": "Vì sao tin được",
        "trust_p": "App không có máy chủ riêng và không tra số serial qua bên thứ ba.",
        "trust_a": ("Cách hoạt động", [
            "Chạy đúng hai lệnh có sẵn của macOS: <code>profiles status</code> và <code>profiles show</code>.",
            "Câu trả lời về ADE đến từ máy chủ Apple.",
            'Mã nguồn mở, giấy phép MIT, build công khai trên <a href="%s/actions">GitHub Actions</a>.' % REPO,
        ]),
        "trust_b": ("Giới hạn", [
            "Chỉ dành cho Mac. iPhone và iPad phải kiểm tay trong Cài đặt.",
            "Cần mạng để hỏi Apple. Mất mạng thì kết luận là chưa xác định, không phải sạch.",
            "Chỉ phát hiện. App không gỡ và không bẻ khoá MDM.",
        ]),
        "faq_id": "cau-hoi",
        "faq_h2": "Câu hỏi thường gặp",
        "faq": [
            ("MDM và ADE khác nhau thế nào?", "MDM là hồ sơ quản lý đang cài trên máy, gỡ được. ADE (tên cũ là DEP) là việc Apple ghi số serial vào tài khoản của một tổ chức: máy sẽ tự cài lại MDM sau mỗi lần xoá, và chỉ tổ chức đó gỡ được."),
            ("App có gửi số serial của tôi đi đâu không?", "Không. App chỉ chạy lệnh profiles có sẵn của macOS; chính lệnh đó hỏi máy chủ Apple. App không có máy chủ riêng, không có tài khoản, không theo dõi."),
            ("Vì sao macOS chặn khi mở app?", "App chưa được Apple chứng nhận (notarize). Vào System Settings, mục Privacy & Security, kéo xuống và bấm Open Anyway."),
            ("Kiểm tra iPhone, iPad được không?", "Không. Apple không cho app trên iPhone đọc trạng thái này. Hãy yêu cầu người bán xoá máy và kích hoạt lại trước mặt bạn: máy dính ADE sẽ hiện màn Remote Management."),
            ("App có gỡ được MDM không?", "Không. App chỉ phát hiện, không gỡ và không bẻ khoá."),
        ],
        "footer": "MDM Checker · mã nguồn mở, giấy phép MIT",
        "footer_links": [(REPO, "GitHub"), (REPO + "/releases", "Bản phát hành"), ("en/", "English")],
    },
    "en": {
        "path": "en/",
        "title": "MDM Checker: check a used MacBook for MDM and ADE before you buy",
        "description": "Free, open-source macOS app. It asks Apple whether a used Mac belongs to a company or school and answers CLEAN, ENROLLED or ADE RISK.",
        "nav": [("#how", "How to use"), ("#faq", "FAQ"), (REPO, "GitHub"), ("../", "Tiếng Việt")],
        "badge": "Free · Open source · Version %s" % VERSION,
        "h1": "Check a used MacBook for MDM before you pay",
        "lead": "MDM Checker asks Apple whether a Mac belongs to a company or a school, then answers in one word: clean, managed, or do not buy.",
        "cta": "Download for macOS",
        "cta2": "View source",
        "meta": "macOS 12 or later · Apple silicon and Intel · 150 KB",
        "mock_caption": "Illustration of the app with sample data",
        "mock": {
            "code": "MDM: ADE RISK", "title": "This Mac belongs to an organization",
            "reason": "Apple has this serial number assigned to an organization. The Mac re-enrolls in MDM after every erase.",
            "advice_label": "What to do:", "advice": "Do not buy. Only that organization can release it.",
            "rows": [("MDM profile installed?", "Yes"), ("Enrolled via ADE/DEP?", "Yes"), ("Serial assigned by Apple?", "Yes")],
        },
        "verdict_h2": "Four verdicts, each with one thing to do",
        "verdict_p": "You do not need to read command output. The app reads it and tells you what to do.",
        "verdicts": [
            ("clean", "CLEAN", "Clean", "No MDM profile, and Apple confirms the serial number is not assigned to any organization."),
            ("enrolled", "ENROLLED", "Managed right now", "A remote-management profile is installed. The seller must remove it before you pay."),
            ("ade", "ADE RISK", "Belongs to an organization", "The serial number belongs to a company or school. Erasing does not help. Do not buy."),
            ("unknown", "UNDETERMINED", "Not enough data", "No network or no admin password. The app never reports clean on incomplete data."),
        ],
        "steps_id": "how",
        "steps_h2": "Three steps",
        "steps_p": "About a minute, right where you inspect the Mac.",
        "steps": [
            ("Download and open the app", "Copy <code>MDMCheck.dmg</code> to the Mac you are inspecting, open it and run the app. If macOS blocks it, go to System Settings, Privacy &amp; Security, and click Open Anyway."),
            ("Click “Hỏi Apple về ADE”", "That button asks Apple about ADE. Enter the Mac's admin password. The Mac must be online. The app interface is in Vietnamese for now."),
            ("Read the verdict", "Copy the report to send to the seller or keep as proof."),
        ],
        "trust_h2": "Why you can trust it",
        "trust_p": "The app has no server of its own and uses no third-party serial lookup.",
        "trust_a": ("How it works", [
            "Runs the two commands that ship with macOS: <code>profiles status</code> and <code>profiles show</code>.",
            "The ADE answer comes from Apple's own servers.",
            'Open source under the MIT license, built in public on <a href="%s/actions">GitHub Actions</a>.' % REPO,
        ]),
        "trust_b": ("Limits", [
            "Mac only. iPhone and iPad must be checked by hand in Settings.",
            "Needs internet to ask Apple. Offline, the verdict is undetermined, not clean.",
            "Detection only. It does not remove or bypass MDM.",
        ]),
        "faq_id": "faq",
        "faq_h2": "Frequently asked questions",
        "faq": [
            ("What is the difference between MDM and ADE?", "MDM is a management profile installed on the Mac; it can be removed. ADE (formerly DEP) means Apple has the serial number recorded under an organization's account: the Mac reinstalls MDM after every erase, and only that organization can release it."),
            ("Does the app send my serial number anywhere?", "No. It only runs the profiles command built into macOS; that command contacts Apple. The app has no server, no account and no tracking."),
            ("Why does macOS block the app?", "The app is not notarized by Apple. Open System Settings, Privacy & Security, scroll down and click Open Anyway."),
            ("Can it check an iPhone or iPad?", "No. Apple does not let iPhone apps read this state. Ask the seller to erase and re-activate the device in front of you: an ADE device shows a Remote Management screen."),
            ("Can it remove MDM?", "No. It only detects management. It does not remove or bypass it."),
        ],
        "footer": "MDM Checker · open source, MIT license",
        "footer_links": [(REPO, "GitHub"), (REPO + "/releases", "Releases"), ("../", "Tiếng Việt")],
    },
}


def render(lang, p):
    base = "../" if p["path"] else ""
    url = SITE + p["path"]
    e = html.escape
    software = {
        "@context": "https://schema.org", "@type": "SoftwareApplication", "name": "MDM Checker", "alternateName": "MDMCheck",
        "description": p["description"], "url": url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "macOS 12 or later",
        "softwareVersion": VERSION, "downloadUrl": DOWNLOAD, "license": "https://opensource.org/licenses/MIT", "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "codeRepository": REPO, "inLanguage": lang,
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    m = p["mock"]
    nav = "".join('<a href="%s">%s</a>' % (e(h), e(t)) for h, t in p["nav"])
    verdicts = "".join(
        '<article class="card tone-%s">%s<p class="code">%s</p><h3>%s</h3><p>%s</p></article>' % (k, icon(VERDICT_ICON[k]), e(code), e(t), e(d))
        for k, code, t, d in p["verdicts"])
    steps = "".join('<li><span class="num">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(t), d) for i, (t, d) in enumerate(p["steps"]))
    lists = "".join('<div><h3>%s</h3><ul>%s</ul></div>' % (e(t), "".join("<li>%s</li>" % li for li in items)) for t, items in (p["trust_a"], p["trust_b"]))
    faqs = "".join('<details%s><summary>%s%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", e(q), icon("chevron"), e(a)) for i, (q, a) in enumerate(p["faq"]))
    rows = "".join('<li>%s<span>%s</span><b>%s</b></li>' % (icon("x"), e(q), e(a)) for q, a in m["rows"])
    footer_links = "".join('<a href="%s">%s</a>' % (e(h), e(t)) for h, t in p["footer_links"])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["description"])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="vi" href="{SITE}">
<link rel="alternate" hreflang="en" href="{SITE}en/">
<link rel="alternate" hreflang="x-default" href="{SITE}en/">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#09090b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MDM Checker">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{"vi_VN" if lang == "vi" else "en_US"}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{base}styles.css">
<script type="application/ld+json">{json.dumps(software, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
</head>
<body>
{SPRITE}
<header class="site-header"><div class="wrap">
  <a class="brand" href="./">{icon("shield-check")}MDM Checker</a>
  <nav aria-label="{"Điều hướng" if lang == "vi" else "Main"}">{nav}</nav>
</div></header>
<main>
<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <p class="badge">{e(p["badge"])}</p>
    <h1>{e(p["h1"])}</h1>
    <p class="lead">{e(p["lead"])}</p>
    <div class="cta"><a class="btn btn-primary" href="{DOWNLOAD}">{icon("download")}{e(p["cta"])}</a><a class="btn" href="{REPO}">{e(p["cta2"])}{icon("arrow")}</a></div>
    <p class="meta">{e(p["meta"])}</p>
  </div>
  <figure class="mock">
    <div class="window" role="img" aria-label="{e(p["mock_caption"])}">
      <div class="titlebar"><i></i><i></i><i></i><span>MDM Checker</span></div>
      <div class="window-body">
        <div class="verdict tone-ade">{icon("shield-x")}<div><p class="code">{e(m["code"])}</p><p class="verdict-title">{e(m["title"])}</p><p>{e(m["reason"])}</p></div></div>
        <p class="advice"><b>{e(m["advice_label"])}</b> {e(m["advice"])}</p>
        <ul class="checks tone-ade">{rows}</ul>
      </div>
    </div>
    <figcaption>{e(p["mock_caption"])}</figcaption>
  </figure>
</div></section>
<section class="section"><div class="wrap">
  <h2>{e(p["verdict_h2"])}</h2><p class="section-lead">{e(p["verdict_p"])}</p>
  <div class="cards">{verdicts}</div>
</div></section>
<section class="section" id="{p["steps_id"]}"><div class="wrap">
  <h2>{e(p["steps_h2"])}</h2><p class="section-lead">{e(p["steps_p"])}</p>
  <ol class="steps">{steps}</ol>
</div></section>
<section class="section"><div class="wrap">
  <h2>{e(p["trust_h2"])}</h2><p class="section-lead">{e(p["trust_p"])}</p>
  <div class="split">{lists}</div>
</div></section>
<section class="section faq" id="{p["faq_id"]}"><div class="wrap">
  <h2>{e(p["faq_h2"])}</h2>
  {faqs}
</div></section>
</main>
<footer class="site-footer"><div class="wrap"><span>{e(p["footer"])}</span><nav aria-label="Footer">{footer_links}</nav></div></footer>
</body>
</html>
"""


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


for lang, page in PAGES.items():
    write(page["path"] + "index.html", render(lang, page))

write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join("  <url><loc>%s%s</loc></url>\n" % (SITE, p["path"]) for p in PAGES.values()) + "</urlset>\n")
write(".nojekyll", "")
print("built", ", ".join(p["path"] + "index.html" for p in PAGES.values()))
