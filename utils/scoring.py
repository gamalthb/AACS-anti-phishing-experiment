from utils.loader import load_emails

def compute_scores(responses: dict) -> dict:
    emails = load_emails()
    scores = {}

    for phase_key, ids in [("phase1", _phase1_ids()), ("phase2", _phase2_ids())]:
        correct = 0
        phishing_correct = 0
        phishing_total = 0
        legit_correct = 0
        legit_total = 0
        confidence_sum = 0
        count = 0
        cue_correct = 0
        cue_total = 0

        for eid in ids:
            if eid not in responses:
                continue
            email = emails[eid]
            resp = responses[eid]
            is_correct = resp["answer"] == email["correct_answer"]
            correct += int(is_correct)
            confidence_sum += resp["confidence"]
            count += 1
            if email["type"] == "phishing":
                phishing_total += 1
                phishing_correct += int(is_correct)
                # Cue accuracy: did they select at least 1 correct cue?
                if email.get("cue_options") and resp.get("cues_selected"):
                    correct_cue_ids = {
                        o["id"] for o in email["cue_options"] if o["correct"]
                    }
                    selected = set(resp.get("cues_selected", []))
                    hit = bool(selected & correct_cue_ids)
                    cue_correct += int(hit)
                    cue_total += 1
            else:
                legit_total += 1
                legit_correct += int(is_correct)

        scores[phase_key] = {
            "accuracy": round(correct / count, 2) if count else 0,
            "phishing_accuracy": round(phishing_correct / phishing_total, 2) if phishing_total else 0,
            "legit_accuracy": round(legit_correct / legit_total, 2) if legit_total else 0,
            "avg_confidence": round(confidence_sum / count, 2) if count else 0,
            "correct": correct,
            "total": count,
            "cue_accuracy": round(cue_correct / cue_total, 2) if cue_total else None,
        }

    return scores

def _phase1_ids():
    from config import PHASE1_IDS
    return PHASE1_IDS

def _phase2_ids():
    from config import PHASE2_IDS
    return PHASE2_IDS