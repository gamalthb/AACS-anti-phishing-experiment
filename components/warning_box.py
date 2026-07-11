import streamlit as st

_CSS = """
<style>
.generic-warn {
    background: #fff3cd;
    border-left: 4px solid #f0ad4e;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    font-family: Arial, sans-serif;
}
.safe-box {
    background: #e6f4ea;
    border-left: 4px solid #188038;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    font-family: Arial, sans-serif;
}
.scaffold-box {
    background: #e8f0fe;
    border-left: 4px solid #1a73e8;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    font-family: Arial, sans-serif;
}
.scaffold-signal {
    background: white;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 6px 0;
    font-size: 13px;
    border: 1px solid #c5d8fb;
    line-height: 1.5;
}
.scaffold-layer {
    font-weight: bold;
    color: #1a73e8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.risk-badge-high {
    display: inline-block;
    background: #d93025;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 13px;
    margin-top: 8px;
}
.risk-badge-low {
    display: inline-block;
    background: #188038;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 13px;
    margin-top: 8px;
}
</style>
"""

def render_warning(email: dict, mode: str):
    if mode == "pilot":
        return

    # Phase 2 emails have null warnings by design — render nothing
    if email.get("generic_warning") is None and email.get("scaffold") is None:
        return

    is_phishing = email["type"] == "phishing"

    if mode == "a":
        text = email.get("generic_warning") or ""  # ← 'or ""' handles None
        if not text:                                # ← skip if still empty
            return
        box_class = "generic-warn" if is_phishing else "safe-box"
        html = _CSS + f'<div class="{box_class}">{text}</div>'
        st.markdown(html, unsafe_allow_html=True)

    elif mode == "b":
        scaffold = email.get("scaffold")
        if not scaffold:
            return

        risk = scaffold["risk_level"]
        emoji = scaffold["risk_emoji"]
        badge_class = "risk-badge-high" if risk == "TINGGI" else "risk-badge-low"
        box_class = "scaffold-box" if is_phishing else "safe-box"

        signals_html = ""
        for i, sig in enumerate(scaffold["signals"], 1):
            signals_html += (
                f'<div class="scaffold-signal">'
                f'<div class="scaffold-layer">({i}) {sig["layer"]}</div>'
                f'<div>{sig["text"]}</div>'
                f'</div>'
            )

        html = (
            _CSS
            + f'<div class="{box_class}">'
            + f'<strong>Analisis & Peringatan AI</strong>'
            + signals_html
            + f'<span class="{badge_class}">{emoji} Tingkat Risiko: {risk}</span>'
            + f'</div>'
        )
        st.markdown(html, unsafe_allow_html=True)