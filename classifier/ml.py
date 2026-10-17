import re
from pathlib import Path

import joblib
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from .data import SEED

MODEL_PATH = Path(settings.BASE_DIR) / "priority_model.joblib"
LABELS = ["High", "Medium", "Low"]

# Signals designed to inspect both subject and body text
URGENT_PATTERNS = re.compile(
    r"\b(urgent|asap|immediately|right away|deadline|due today|due tonight|critical|emergency|"
    r"action required|final reminder|overdue|server down|production outage|security breach|"
    r"account suspended|payment failed|unauthorized|fatal|outage|blocker)\b",
    re.I,
)

WORK_ACTION_PATTERNS = re.compile(
    r"\b(review|feedback|schedule|agenda|meeting|pull request|submission|status update|"
    r"draft|proposal|task|assigned|next week|by friday|discussion|attached|portal)\b",
    re.I,
)

SPAM_PROMO_PATTERNS = re.compile(
    r"\b(unsubscribe|% off|sale|coupon|free gift|newsletter|promotion|discount|weekly digest|"
    r"special offer|limited time|horoscope|click here to claim|buy now|view in browser|webinar)\b",
    re.I,
)


def _text(subject, body):
    """Combine subject and body giving strong weight to the email body content."""
    sub = (subject or "").strip()
    bod = (body or "").strip()
    if sub and bod:
        return f"{sub} {bod} {bod}".strip()
    return f"{sub} {bod}".strip()


def train(extra=None):
    """Train on seed data plus user-corrected emails: extra = [(text, label), ...]."""
    rows = list(SEED) + list(extra or [])
    X, y = zip(*rows)
    model = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model


def _load():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train()


def predict(subject="", body=""):
    """Predict priority label and confidence based on thorough analysis of subject and body."""
    text = _text(subject, body)
    model = _load()

    # Get ML model base probabilities
    probs = dict(zip(model.classes_, model.predict_proba([text])[0]))

    # Analyze body and full text for high-priority urgent signals
    if URGENT_PATTERNS.search(text):
        probs["High"] = probs.get("High", 0.0) + 0.30

    # Analyze for routine work/action items if not strongly urgent
    elif WORK_ACTION_PATTERNS.search(text):
        probs["Medium"] = probs.get("Medium", 0.0) + 0.15

    # Analyze body and full text for promotional/newsletter signals
    if SPAM_PROMO_PATTERNS.search(text):
        probs["Low"] = probs.get("Low", 0.0) + 0.30

    # Re-normalize probabilities
    total = sum(probs.values())
    label = max(probs, key=probs.get)
    confidence = round(probs[label] / total, 3)

    return label, confidence

