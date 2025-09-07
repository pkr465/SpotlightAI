PROMPTS = {
    "script_gen": (
        "You are a senior promo copywriter. Given the show title '{title}', "
        "logline '{logline}', target audience '{audience}', and highlight descriptions: "
        "{highlights}.\n"
        "Write a 15-30 second promo script with 2 strong taglines. "
        "Optimize for engagement and SEO using {brand} brand voice. "
        "Return JSON with keys: script, taglines, keywords."
    ),
    "personalize": (
        "Rewrite the promo script for audience segment '{segment}' and locale '{locale}'. "
        "Keep brand voice '{brand}'. Return JSON with keys: script, taglines."
    ),
    "ab_hypotheses": (
        "Given promo script and metadata: {metadata}. "
        "Generate 3 concise A/B test hypotheses with success metrics (CTR, CVR). "
        "Return JSON list."
    ),
}
