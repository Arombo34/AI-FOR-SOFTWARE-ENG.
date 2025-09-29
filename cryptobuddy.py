
import random
import textwrap

# ---------- 1) Personality ----------
BOT_NAME = "CryptoBuddy"
BOT_TONE = "friendly"  # used for some reply variations

# ---------- 2) Predefined crypto dataset ----------
crypto_db = {
    "Bitcoin": {
        "symbol": "BTC",
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3.0,
        "notes": "Largest market cap; energy-intensive proof-of-work."
    },
    "Ethereum": {
        "symbol": "ETH",
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6.0,
        "notes": "Smart contracts leader; moving to greener consensus (historical)."
    },
    "Cardano": {
        "symbol": "ADA",
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8.0,
        "notes": "Paper-driven design; proof-of-stake, energy-efficient."
    },
    "Solana": {
        "symbol": "SOL",
        "price_trend": "falling",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 7.0,
        "notes": "Fast network, but has had outages in the past."
    },
    "Polkadot": {
        "symbol": "DOT",
        "price_trend": "stable",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 7.5,
        "notes": "Interoperability focused; proof-of-stake."
    }
}

# ---------- 3) Helper rule functions ----------
def best_by_sustainability(db):
    # return coin with highest sustainability score
    return max(db.items(), key=lambda item: item[1]["sustainability_score"])

def best_by_profitability(db):
    """
    Profitability scoring rules:
    - price_trend: rising > stable > falling
    - market_cap: high > medium > low
    Combine weights for a simple rule-based score.
    """
    trend_score = {"rising": 3, "stable": 2, "falling": 1}
    cap_score = {"high": 3, "medium": 2, "low": 1}
    def score(item):
        data = item[1]
        return (trend_score.get(data["price_trend"], 1) * 0.6 +
                cap_score.get(data["market_cap"], 1) * 0.4)
    best = max(db.items(), key=score)
    return best

def filter_trending_up(db):
    return [name for name, d in db.items() if d["price_trend"] == "rising"]

# ---------- 4) Basic NLP-ish parsing (keyword matching) ----------
def classify_query(query):
    q = query.lower()
    if any(k in q for k in ["sustain", "eco", "green", "environment", "energy"]):
        return "sustainability"
    if any(k in q for k in ["trend", "trending", "up", "growing", "rise", "rising"]):
        return "trending"
    if any(k in q for k in ["buy", "invest", "long-term", "hold", "should i buy"]):
        return "advice_buy"
    if any(k in q for k in ["compare", "which is better", "vs", "versus"]):
        return "compare"
    if any(k in q for k in ["help", "hello", "hi", "hey"]):
        return "greeting"
    if any(k in q for k in ["bye", "exit", "quit", "thanks", "thank"]):
        return "goodbye"
    # default
    return "unknown"

# ---------- 5) Response generator ----------
def generate_response(user_query):
    intent = classify_query(user_query)
    if intent == "greeting":
        return random.choice([
            f"Hey! I'm {BOT_NAME}. How can I help you find green & growing crypto today?",
            "Hello! Ask me about trending coins, sustainability, or long-term picks."
        ])
    if intent == "sustainability":
        name, data = best_by_sustainability(crypto_db)
        return (f"Top sustainability pick: {name} ({data['symbol']}).\n"
                f"Sustainability score: {data['sustainability_score']}/10.\n"
                f"Why: {data['energy_use']} energy use — {data['notes']}")
    if intent == "trending":
        trending = filter_trending_up(crypto_db)
        if trending:
            return f"Coins trending up right now: {', '.join(trending)}. Consider market cap and risk before acting."
        else:
            return "I don't see any coins with a 'rising' trend in my sample dataset."
    if intent == "advice_buy":
        # Combine rules: prefer rising + high market cap; otherwise suggest sustainable rising coin
        best_profit_name, best_profit_data = best_by_profitability(crypto_db)
        # If best by profitability also has good sustainability, highlight both.
        if best_profit_data["price_trend"] == "rising" and best_profit_data["market_cap"] == "high":
            return (f"For long-term growth, I recommend checking out {best_profit_name} ({best_profit_data['symbol']}). "
                    f"It's trending {best_profit_data['price_trend']} with {best_profit_data['market_cap']} market cap. "
                    "Remember: this is NOT financial advice — do your own research.")
        # Otherwise pick the top sustainable rising coin if available
        sustainable_name, sustainable_data = best_by_sustainability(crypto_db)
        if sustainable_data["price_trend"] == "rising":
            return (f"{sustainable_name} ({sustainable_data['symbol']}) looks like a strong long-term pick for a "
                    "balance of growth + sustainability. But crypto is risky — DYOR.")
        # Fallback
        return (f"My top pick by simple profitability rules is {best_profit_name} ({best_profit_data['symbol']}). "
                "Use proper risk management and consider diversification.")
    if intent == "compare":
        # crude compare: look for known coin names in query
        names_found = [name for name in crypto_db.keys() if name.lower() in user_query.lower()]
        if len(names_found) >= 2:
            a, b = names_found[:2]
            ad = crypto_db[a]; bd = crypto_db[b]
            cmp_lines = [
                f"{a} ({ad['symbol']}): trend={ad['price_trend']}, market_cap={ad['market_cap']}, sustainability={ad['sustainability_score']}/10",
                f"{b} ({bd['symbol']}): trend={bd['price_trend']}, market_cap={bd['market_cap']}, sustainability={bd['sustainability_score']}/10"
            ]
            return "\n".join(cmp_lines)
        else:
            return "Tell me two coin names to compare (e.g., 'Compare Bitcoin and Cardano')."
    if intent == "goodbye":
        return random.choice(["Goodbye! Trade safe and remember to do your own research. 👋",
                              "See you! Keep learning and manage your risk."])
    # unknown
    return ("I didn't quite catch that. Try asking: 'Which crypto is trending up?', "
            "'What's the most sustainable coin?', or 'Which should I buy for long-term growth?'")

# ---------- 6) Simple CLI / Notebook interaction ----------
def chat_loop():
    print("="*60)
    print(f"Welcome to {BOT_NAME} — Your First AI-Powered Financial Sidekick!")
    print("Type questions like: 'Which crypto is trending up?' or 'Which is the most sustainable coin?'")
    print("Type 'exit' or 'quit' to end.")
    print("="*60)
    while True:
        user = input("\nYou: ").strip()
        if not user:
            print("CryptoBuddy: Say something (or 'quit' to exit).")
            continue
        resp = generate_response(user)
        print("\nCryptoBuddy:", textwrap.fill(resp, width=80))
        if classify_query(user) == "goodbye":
            break

# ---------- 7) If executed as script ----------
if __name__ == "__main__":
    # For direct runs in terminal or Colab cell: start chat loop
    chat_loop()
