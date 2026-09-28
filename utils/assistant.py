# =============================================================================
# assistant.py  — AI assistant response engine (English + Hindi/Hinglish)
# =============================================================================
import re


def _is_hindi(text: str) -> bool:
    if re.search(r'[\u0900-\u097F]', text):
        return True
    pat = (r'\b(mera|meri|mujhe|kya|kyun|kaise|batao|samjhao|result|karo|'
           r'chahiye|hai|hain|aur|kam|zyada|neend|padhai|mobile|phone|'
           r'accha|bura|kuch|theek|thoda|bahut|abhi|pehle)\b')
    return bool(re.search(pat, text, re.IGNORECASE))


def _collect_factors(pred: str, d: dict) -> list:
    f   = []
    sm  = d.get("Daily_Usage_Hours", 0)
    sl  = d.get("Sleep_Duration_Hours", 0)
    st_ = d.get("Perceived_Stress_Score", 0)
    mhi = d.get("Mental_Health_Index", 0)
    gpa = d.get("Academic_Performance_GPA", 0)
    lnu = d.get("Late_Night_Usage_int", 0)
    soc = d.get("Social_Comparison_Frequency", "")
    plt_= d.get("Primary_Platform", "")

    if sm >= 8:
        f.append(f"Very high daily social-media usage ({sm} hrs) — strongest risk factor.")
    elif sm >= 5:
        f.append(f"Moderate-to-high daily social-media usage ({sm} hrs).")
    elif sm <= 2:
        f.append(f"Low social-media usage ({sm} hrs/day) — positive signal.")

    if sl < 6:
        f.append(f"Insufficient sleep ({sl} hrs/night) — recommended 7–9 hrs.")
    elif 7 <= sl <= 9:
        f.append(f"Healthy sleep duration ({sl} hrs/night) — positive factor.")
    elif sl > 9:
        f.append(f"Oversleeping ({sl} hrs) may indicate fatigue or disengagement.")

    if st_ >= 22:
        f.append(f"High perceived stress ({st_}) — strongly associated with Negative impact.")
    elif st_ <= 12:
        f.append(f"Low stress score ({st_}) — positive wellbeing indicator.")

    if mhi >= 70:
        f.append(f"Good mental health index ({mhi}) — positive factor.")
    elif mhi <= 50:
        f.append(f"Low mental health index ({mhi}) — significant risk factor.")

    if gpa >= 3.5:
        f.append(f"Strong GPA ({gpa}) — positive factor.")
    elif gpa <= 2.5:
        f.append(f"Lower GPA ({gpa}) correlates with higher-risk patterns.")

    if lnu == 1:
        f.append("Late-night social-media usage — disrupts sleep and recovery.")

    if soc in ("Frequently", "Always"):
        f.append(f"Frequent social comparison ('{soc}') is linked to higher stress.")

    if plt_ in ("TikTok", "Instagram"):
        f.append(f"{plt_} is a high-engagement platform — associated with higher passive usage.")

    return f


def _why_result(pred: str, d: dict) -> str:
    factors = _collect_factors(pred, d)
    lines   = [f"**Why your result is '{pred.capitalize()}':**\n",
               "The model evaluated these aspects of your profile:\n"]
    lines  += [f"• {f}" for f in factors]
    lines.append(
        "\n📌 *Model-based statistical estimation — not a diagnosis. "
        "The combination of factors drives the result, not any single one.*"
    )
    return "\n".join(lines)


def _improve_suggestions(pred: str, d: dict) -> str:
    sm  = d.get("Daily_Usage_Hours", 0)
    sl  = d.get("Sleep_Duration_Hours", 0)
    st_ = d.get("Perceived_Stress_Score", 0)
    lnu = d.get("Late_Night_Usage_int", 0)
    plt_= d.get("Primary_Platform", "")
    soc = d.get("Social_Comparison_Frequency", "")

    tips = []
    if sm >= 5:
        tips.append("📵 Set a daily screen-time limit — aim for under 2–3 hrs using your phone's built-in tools.")
    if sl < 7:
        tips.append(f"😴 Work toward 7–9 hrs of sleep. Your current {sl} hrs is below the recommended range. Consistent bedtime + no screens 30–60 min before bed helps.")
    if st_ >= 20:
        tips.append("🧘 Your stress score is elevated. Try 10–15 min of daily mindfulness, journaling, or light exercise.")
    if lnu == 1:
        tips.append("🌙 Avoid social media after 10 pm. Late-night usage delays melatonin release and disrupts sleep quality.")
    if soc in ("Frequently", "Always"):
        tips.append("🔕 Unfollow or mute accounts that trigger comparison. Curate your feed toward content that inspires rather than compares.")
    if plt_ in ("TikTok", "Instagram"):
        tips.append(f"📱 {plt_} is designed to maximise engagement. Use grayscale mode or set app timers to reduce unintentional scrolling.")
    tips.append("📚 Protect study time: phone in another room or Focus/DND mode during study sessions.")
    tips.append("🏃 Add even 20–30 min of daily walking — significantly improves mood and concentration.")
    tips.append("⏰ Track screen time for one week using your phone's report. Awareness is the first step.")
    return ("**Practical suggestions based on your profile:**\n\n"
            + "\n\n".join(tips)
            + "\n\n💡 *Start with just one change this week.*")


def _what_if_reduce(d: dict) -> str:
    sm = d.get("Daily_Usage_Hours", 0)
    return (
        "**Hypothetical scenario (model-based only):**\n\n"
        f"Your current daily usage is **{sm} hrs**. If you reduced it, the model "
        "would likely assign a more favourable score — lower usage is one of the "
        "strongest predictors of a Beneficial outcome.\n\n"
        "Combining that with better sleep and lower stress amplifies the effect.\n\n"
        "⚠️ *This is a what-if model scenario, not a guaranteed real-world outcome. "
        "Research broadly supports that reducing passive scrolling improves mood and academic focus.*"
    )


def _sleep_tips(d: dict) -> str:
    sl   = d.get("Sleep_Duration_Hours", 0)
    note = ""
    if sl and sl < 7:
        note = f"You reported **{sl} hrs/night** — below the recommended 7–9 hrs. This impairs memory, mood, and focus.\n\n"
    elif sl and sl >= 7:
        note = f"Your **{sl} hrs/night** is in a healthy range! Here are tips to protect it:\n\n"
    return note + (
        "**Sleep improvement tips:**\n\n"
        "• Same bedtime and wake time every day (including weekends)\n"
        "• No screens 30–60 min before bed — blue light suppresses melatonin\n"
        "• Cool, dark, quiet room\n"
        "• No caffeine after 4 pm\n"
        "• Replace late-night scrolling with light reading or a wind-down routine\n\n"
        "💤 *Even 30–60 extra minutes per night produces noticeable benefits within a week.*"
    )


def _study_tips(d: dict) -> str:
    sm = d.get("Daily_Usage_Hours", 0)
    extra = (f"\n📵 *Your current usage of {sm} hrs/day may compete with study time. "
             "Consider a usage limit on study days.*") if sm >= 4 else ""
    return (
        "**Study & focus tips:**\n\n"
        "• **Pomodoro**: 25 min focused study → 5 min break → repeat\n"
        "• Phone in another room or Focus/DND mode during study\n"
        "• Study at the same time and place daily — builds a habit cue\n"
        "• Identify your peak focus hours and protect them\n"
        "• Break large tasks into small timed steps to beat procrastination\n"
        "• Use active recall (self-testing) rather than passive re-reading\n"
        "• Adequate sleep consolidates memory during deep sleep"
        + extra
    )


def _mood_tips(d: dict) -> str:
    return (
        "**Mood & digital wellbeing tips:**\n\n"
        "• Notice which apps leave you drained vs. energised\n"
        "• Unfollow/mute accounts that trigger anxiety or comparison\n"
        "• Try a 24-hour social-media break once a week\n"
        "• Physical activity — even a short walk — is a fast natural mood-lifter\n"
        "• Invest in in-person connections\n"
        "• If you regularly feel low after usage, that pattern is worth paying attention to\n\n"
        "⚠️ *If anxiety, sadness, or low mood persist, please speak with a counsellor "
        "or qualified mental-health professional. This assistant cannot diagnose conditions.*"
    )


def _hindi_why(pred: str, d: dict) -> str:
    label = {"Beneficial": "Faydemand ✅", "Neutral": "Milaajula ⚖️",
             "Negative": "Nukasaandeh ⚠️"}.get(pred, pred)
    sm  = d.get("Daily_Usage_Hours", 0)
    sl  = d.get("Sleep_Duration_Hours", 0)
    st_ = d.get("Perceived_Stress_Score", 0)
    mhi = d.get("Mental_Health_Index", 0)
    lnu = d.get("Late_Night_Usage_int", 0)
    lines = [f"**Aapka result '{label}' kyun aaya:**\n",
             "Model ne aapki profile ke kai pehluon ko dekha:\n"]
    if sm >= 5:
        lines.append(f"• Roz {sm} ghante social media — yeh zyada hai")
    elif sm <= 2:
        lines.append(f"• Kam usage ({sm} ghante) — positive signal hai")
    if sl < 7:
        lines.append(f"• Neend sirf {sl} ghante — recommended 7–9 hain")
    else:
        lines.append(f"• {sl} ghante ki neend — positive hai")
    if st_ >= 20:
        lines.append(f"• Stress score {st_} — zyada hai, negative impact se juda")
    if mhi <= 50:
        lines.append(f"• Mental health index {mhi} — risk factor hai")
    if lnu == 1:
        lines.append("• Raat ko social media — neend pe bura asar dalta hai")
    lines.append("\n📌 *Yeh model ka statistical result hai, koi medical diagnosis nahi.*")
    return "\n".join(lines)


def _hindi_improve(d: dict) -> str:
    sm  = d.get("Daily_Usage_Hours", 0)
    sl  = d.get("Sleep_Duration_Hours", 0)
    st_ = d.get("Perceived_Stress_Score", 0)
    lnu = d.get("Late_Night_Usage_int", 0)
    tips = []
    if sm >= 4:
        tips.append(f"📵 Social media ko {sm} ghante se 2–3 ghante tak laane ki koshish karein.")
    if sl < 7:
        tips.append(f"😴 {sl} ghante ki neend kam hai — 7–9 ghante zaruri hain.")
    if st_ >= 20:
        tips.append("🧘 Stress zyada hai — roz 10–15 min walking ya deep breathing try karein.")
    if lnu == 1:
        tips.append("🌙 Raat 10 baje ke baad social media avoid karein.")
    tips.append("📚 Padhai ke waqt phone DND mode par rakhein.")
    tips.append("🏃 Roz 20–30 min ki activity mood aur focus ke liye faydemand hai.")
    return ("**Aapke liye sujhav:**\n\n" + "\n\n".join(tips)
            + "\n\n💡 *Pehle sirf ek chiz se shuru karein!*")


def _hindi_reduce(d: dict) -> str:
    sm = d.get("Daily_Usage_Hours", 0)
    return (
        f"**Agar aap social media kam karein (model scenario):**\n\n"
        f"Abhi aap roz **{sm} ghante** use karte hain. Kam karne par model "
        "zyada positive score dega.\n\n"
        "⚠️ *Yeh sirf model-based scenario hai — real life ki guarantee nahi. "
        "Lekin research kehti hai: kam passive scrolling = better mood + focus.*"
    )


def generate_bot_reply(user_text: str, pred: str,
                       input_dict: dict, predicted: bool) -> str:
    """Main dispatcher — routes any message to the right response function."""
    t     = user_text.lower().strip()
    hindi = _is_hindi(user_text)
    d     = input_dict

    # No prediction yet
    if not predicted:
        if hindi:
            return ("Pehle **🔮 Prediction** page par jaiye, details fill karein aur "
                    "result hasil karein. Phir main sab explain kar sakta hoon! 😊")
        return ("Please go to **🔮 Prediction**, fill in your details, and get your result first. "
                "I'll then give you personalised answers! 😊")

    # Medical/diagnosis guard
    if re.search(r'diagnos|medical|doctor|psycholog|condition|disease|therapy|treatment', t):
        return ("This assistant provides **educational and digital-wellbeing information only**. "
                "It cannot diagnose any condition. Please consult a qualified professional "
                "for persistent stress, anxiety, sleep problems, or low mood.")

    # Hindi branch
    if hindi:
        if re.search(r'kyun|reason|kyu|samjhao|explain|result|factors', t):
            return _hindi_why(pred, d)
        if re.search(r'improve|sudhar|better|kya karun|kaise|sujhav|tips|change', t):
            return _hindi_improve(d)
        if re.search(r'kam kar|reduce|ghata|less|agar|what if', t):
            return _hindi_reduce(d)
        if re.search(r'neend|sleep|so ', t):
            return _sleep_tips(d)
        if re.search(r'padhai|study|focus|concentrate', t):
            return _study_tips(d)
        if re.search(r'mood|tension|stress|anxiety|sad|depress', t):
            return _mood_tips(d)
        label_hi = {"Beneficial": "Faydemand ✅", "Neutral": "Milaajula ⚖️",
                    "Negative": "Nukasaandeh ⚠️"}.get(pred, pred)
        return (f"Aapka predicted impact **{label_hi}** hai.\n\n"
                "Pooch sakte hain: result kyun aaya? • kya sudhar karein? • neend/padhai tips\n"
                "Main taiyaar hoon! 😊")

    # English branch
    if re.search(r'why|reason|cause|factor|contribut|explain.*result|result.*explain|how.*get', t):
        return _why_result(pred, d)
    if re.search(r'improve|suggest|better|what (should|can|do)|how to|tips|advice|change|help|recommend', t):
        return _improve_suggestions(pred, d)
    if re.search(r'reduce|less(en)?|cut.*down|decrease|what if|if i (reduce|use less|stop|quit)', t):
        return _what_if_reduce(d)
    if re.search(r'sleep|rest|insomnia|tired|fatigue|nap', t):
        return _sleep_tips(d)
    if re.search(r'study|focus|productiv|concentrat|attention|academic|distract|exam|homework', t):
        return _study_tips(d)
    if re.search(r'mood|anx|stress|sad|depress|mental|emotion|feel|happy|unhappy|low', t):
        return _mood_tips(d)
    if re.search(r'exercise|physical|gym|sport|walk|activ|fitness', t):
        return ("**Physical activity & digital wellbeing:**\n\n"
                "• Even 20–30 min of brisk walking daily has measurable mood/focus benefits\n"
                "• Exercise raises dopamine naturally — reducing urge to seek stimulation from scrolling\n"
                "• Replace 1 scrolling session per day with a short walk\n"
                "• No gym needed — home workouts, cycling, or dancing all count\n\n"
                "🏃 *Consistency matters more than intensity.*")
    if re.search(r'my (result|predict|score|outcome|impact)', t):
        emoji = {"Beneficial": "🟢", "Neutral": "🟡", "Negative": "🔴"}.get(pred, "🔵")
        return (f"Your prediction is: {emoji} **{pred.upper()}**\n\n"
                "Ask me why you got it, or what you could improve!")
    if re.search(r'^(hi|hello|hey|namaste|hii)\b', t):
        emoji = {"Beneficial": "🟢", "Neutral": "🟡", "Negative": "🔴"}.get(pred, "🔵")
        return (f"Hello! 😊 Your prediction is {emoji} **{pred.upper()}**.\n\n"
                "You can ask:\n• Why did I get this result?\n• What should I improve?\n"
                "• What if I reduce usage?\n• Sleep / study / mood tips\n"
                "• Or ask in Hindi!")

    # Fallback
    emoji = {"Beneficial": "🟢", "Neutral": "🟡", "Negative": "🔴"}.get(pred, "🔵")
    return (f"I'm here to help with your {emoji} **{pred.upper()}** prediction.\n\n"
            "Ask me:\n"
            "• \"Why did I get this result?\"\n• \"What should I improve?\"\n"
            "• \"What if I reduce my social media usage?\"\n"
            "• Sleep, study, mood, or activity tips\n• Or ask in Hindi!\n\n"
            "⚠️ *Educational information only — not medical advice.*")
