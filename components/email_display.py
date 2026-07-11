import streamlit as st
import re as re

_CARD_CSS = """
<style>
/* ── Reset & base ───────────────────────────── */
.em-wrap * { box-sizing: border-box; font-family: Arial, sans-serif; }

/* ── Outer card ─────────────────────────────── */
.em-wrap {
    background: #fff;
    border: 1px solid #dadce0;
    border-radius: 8px;
    overflow: hidden;
    margin: 0 0 12px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,.08);
}

/* ── Top bar ─────────────────────────────────── */
.em-topbar {
    background: #1a73e8;
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 600;
}

/* ── Subject strip ───────────────────────────── */
.em-subject {
    padding: 10px 14px 6px;
    font-size: 15px;
    font-weight: 700;
    color: #202124;
    border-bottom: 1px solid #f1f3f4;
    word-break: break-word;
}

/* ── Sender row ──────────────────────────────── */
.em-sender {
    display: flex;
    align-items: flex-start;
    padding: 10px 14px;
    gap: 10px;
    border-bottom: 1px solid #f1f3f4;
}
.em-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
}
.em-sender-info { flex: 1; min-width: 0; }
.em-sender-name {
    font-size: 14px;
    font-weight: 600;
    color: #202124;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.em-sender-addr {
    font-size: 11px;
    color: #5f6368;
    word-break: break-all;
    margin-top: 1px;
}
.em-time {
    font-size: 11px;
    color: #5f6368;
    white-space: nowrap;
    margin-top: 2px;
    flex-shrink: 0;
}

/* ── Warning banners ─────────────────────────── */
.em-banner-warn {
    background: #fef9e7;
    border-top: 1px solid #f9ca24;
    border-bottom: 1px solid #f9ca24;
    padding: 10px 14px;
}
.em-banner-safe {
    background: #f0fdf4;
    border-top: 1px solid #86efac;
    border-bottom: 1px solid #86efac;
    padding: 10px 14px;
}
.em-banner-scaffold-warn {
    background: #fff9f9;
    border-top: 2px solid #dc2626;
    border-bottom: 1px solid #dc2626;
    padding: 10px 14px;
}
.em-banner-scaffold-safe {
    background: #f0fdf4;
    border-top: 2px solid #16a34a;
    border-bottom: 1px solid #86efac;
    padding: 10px 14px;
}

.em-banner-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.badge-high {
    background: #dc2626;
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    text-transform: none;
    letter-spacing: 0;
}
.badge-low {
    background: #16a34a;
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    text-transform: none;
    letter-spacing: 0;
}
.em-signal {
    font-size: 12px;
    color: #374151;
    line-height: 1.5;
    padding: 3px 0;
    border-bottom: 1px solid rgba(0,0,0,.05);
    display: flex;
    gap: 6px;
}
.em-signal:last-of-type { border-bottom: none; }
.em-signal-num {
    font-weight: 700;
    color: #1a73e8;
    flex-shrink: 0;
}
.em-signal-num-safe { color: #16a34a; }

/* ── Body ────────────────────────────────────── */
.em-body {
    padding: 14px;
    font-size: 14px;
    color: #202124;
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── CTA button ──────────────────────────────── */
.em-cta {
    padding: 0 14px 14px;
}
.em-cta-btn {
    display: inline-block;
    background: #1a73e8;
    color: #fff !important;
    text-decoration: none !important;
    padding: 10px 18px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 700;
    cursor: default;
    word-break: break-all;
}
.em-cta-url {
    display: block;
    font-size: 10px;
    color: #9ca3af;
    margin-top: 4px;
    word-break: break-all;
}
</style>
"""

_AVATAR_COLORS = [
    "#1a73e8","#d93025","#188038","#f29900",
    "#9334e6","#00796b","#c2185b","#0288d1",
]

def _avatar_color(name: str) -> str:
    return _AVATAR_COLORS[ord(name[0].upper()) % len(_AVATAR_COLORS)]

def _short(text: str, max_chars: int = 80) -> str:
    """Extract first sentence or truncate."""
    for sep in [". ", " — ", " \u2014 "]:
        if sep in text:
            part = text.split(sep)[0]
            return part if len(part) <= max_chars else part[:max_chars] + "…"
    return text[:max_chars] + "…" if len(text) > max_chars else text

def _banner_html(email: dict, mode: str) -> str:
    if mode not in ("a", "b"):
        return ""

    is_phishing = email["type"] == "phishing"

    if mode == "a":
        # Extract the text first. If it's null in JSON, this becomes None.
        warning_text = email.get("generic_warning")
        
        # If it's None or an empty string, don't draw the banner at all
        if not warning_text:
            return ""

        if is_phishing:
            return f"""
            <div class="em-banner-warn">
              <div class="em-banner-title">
                <span>⚠️ Peringatan Keamanan</span>
                <span class="badge-high">Mencurigakan</span>
              </div>
              <div style="font-size:12px;color:#374151;">
                {warning_text}
              </div>
            </div>"""
        else:
            return f"""
            <div class="em-banner-safe">
              <div class="em-banner-title">
                <span>✅ Tidak Ada Sinyal Mencurigakan</span>
                <span class="badge-low">Aman</span>
              </div>
              <div style="font-size:12px;color:#374151;">
                {warning_text}
              </div>
            </div>"""

    if mode == "b":
        scaffold = email.get("scaffold")
        if not scaffold:
            return ""

        risk = scaffold["risk_level"]
        is_high = risk == "TINGGI"
        badge_class = "badge-high" if is_high else "badge-low"
        badge_emoji = "🔴" if is_high else "🟢"
        box_class = "em-banner-scaffold-warn" if is_phishing else "em-banner-scaffold-safe"
        num_class = "" if is_phishing else " em-signal-num-safe"
        title_color = "#dc2626" if is_phishing else "#16a34a"

        signals_html = ""
        for i, sig in enumerate(scaffold["signals"], 1):
            # short = _short(sig["text"])
            signals_html += (
                f'<div class="em-signal">'
                f'<span class="em-signal-num{num_class}">{"①②③"[i-1]}</span>'
                f'<span><strong>{sig["layer"]}:</strong> {sig["text"]}</span>'
                f'</div>'
            )

        return f"""
        <div class="{box_class}">
          <div class="em-banner-title">
            <span style="color:{title_color};">Peringatan</span>
            <span class="{badge_class}">Risiko: {badge_emoji} {risk}</span>
          </div>
          {signals_html}
        </div>"""

    return ""

def _render_body(body: str) -> str:
    body_html = body.replace("\n", "<br>")
    # Style inline URLs as non-functional links
    body_html = re.sub(
        r'(https?://[^\s<]+)',
        r'<a href="#" onclick="return false;" style="color:#1a73e8;text-decoration:underline;">\1</a>',
        body_html
    )
    return body_html

def render_email_card(email: dict, mode: str, current_num: int):
    total = 16
    d = email["display"]
    sender_initial = d["from_name"][0].upper()
    avatar_color = _avatar_color(d["from_name"])
    banner = _banner_html(email, mode)

    body_html = _render_body(d["body"])

    cta_html = ""
    if d.get("link_text"):
        cta_html = f"""
        <div class="em-cta">
          <a href="#" onclick="return false;" class="em-cta-btn">
            {d['link_text']}
          </a>
          <span class="em-cta-url">{d.get('link_url','#')}</span>
        </div>"""

    html = f"""
    {_CARD_CSS}
    <div class="em-wrap">

      <div class="em-topbar">
        <span>📧 WebMail — Kotak Masuk</span>
        <span>{current_num} / {total}</span>
      </div>

      <div class="em-subject">{d['subject']}</div>

      <div class="em-sender">
        <div class="em-avatar" style="background:{avatar_color};">{sender_initial}</div>
        <div class="em-sender-info">
          <div class="em-sender-name">{d['from_name']}</div>
          <div class="em-sender-addr">{d['from_address']}</div>
        </div>
        <div class="em-time">Hari ini</div>
      </div>

      {banner}

      <div class="em-body">{body_html}</div>

      {cta_html}

    </div>
    """
    st.html(html)