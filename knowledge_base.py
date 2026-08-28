"""
Non-diagnostic health information knowledge base.
Every entry gives general, educational guidance ONLY — no diagnosis,
no medication dosing, no definitive medical claims. Every entry ends
by pointing the user toward professional care.

Structured as (topic, keywords, response) so it can be swapped for a
real medical-content API/dataset later without touching the retrieval
or UI layers.
"""

KB = [
    {
        "topic": "Fever",
        "keywords": "fever high temperature hot body temperature chills",
        "answer": (
            "A fever is your body's natural response to infection or illness. "
            "General self-care while you arrange to see a doctor: rest, drink "
            "plenty of fluids, and dress lightly. A fever that is very high, "
            "lasts more than 2-3 days, or comes with severe symptoms (stiff "
            "neck, difficulty breathing, confusion) needs urgent medical "
            "attention — please visit a nearby health center."
        ),
        "urgent_flags": ["difficulty breathing", "stiff neck", "confusion", "seizure"],
    },
    {
        "topic": "Cough and Cold",
        "keywords": "cough cold sore throat runny nose congestion sneezing",
        "answer": (
            "Coughs and colds are usually caused by common viral infections and "
            "often ease within one to two weeks. Rest, warm fluids, and steam "
            "inhalation can help with comfort. If the cough lasts more than "
            "3 weeks, brings up blood, or comes with chest pain or breathlessness, "
            "please get checked by a doctor promptly."
        ),
        "urgent_flags": ["blood", "chest pain", "breathless"],
    },
    {
        "topic": "Diarrhea",
        "keywords": "diarrhea loose motion stomach upset dehydration vomiting",
        "answer": (
            "Diarrhea is often caused by infection or food/water contamination. "
            "The most important general step is staying hydrated — oral "
            "rehydration solution (ORS) or clean fluids with small sips "
            "frequently. If there is blood in stool, high fever, signs of "
            "dehydration (very little urine, dizziness), or it lasts more than "
            "2 days, please see a doctor immediately — this can be serious, "
            "especially in children and the elderly."
        ),
        "urgent_flags": ["blood", "dehydration", "child", "infant"],
    },
    {
        "topic": "Headache",
        "keywords": "headache head pain migraine pressure",
        "answer": (
            "Headaches are commonly caused by stress, dehydration, poor sleep, "
            "or eye strain. Resting in a quiet, dark space and staying "
            "hydrated often helps. A sudden, severe headache unlike any before, "
            "or one with vision changes, weakness, or confusion, needs "
            "emergency care right away."
        ),
        "urgent_flags": ["sudden", "severe", "vision", "weakness", "confusion"],
    },
    {
        "topic": "Skin Rash",
        "keywords": "skin rash itching allergy redness swelling",
        "answer": (
            "Skin rashes can result from allergies, infections, or irritants. "
            "Keeping the area clean and avoiding known irritants is a general "
            "first step. A rash that spreads quickly, blisters, or comes with "
            "fever or breathing trouble should be seen by a doctor without delay."
        ),
        "urgent_flags": ["spreading", "breathing", "swelling of face"],
    },
    {
        "topic": "Body Pain / Weakness",
        "keywords": "body pain weakness fatigue tiredness joint pain muscle pain",
        "answer": (
            "General body aches can come from overexertion, poor sleep, "
            "infection, or nutritional gaps. Rest, hydration, and balanced "
            "meals often help. Persistent weakness, pain that doesn't improve, "
            "or pain with swelling or fever should be evaluated by a doctor."
        ),
        "urgent_flags": ["chest", "one-sided weakness", "sudden"],
    },
    {
        "topic": "Pregnancy Care",
        "keywords": "pregnancy pregnant maternal care prenatal",
        "answer": (
            "Regular prenatal check-ups are important throughout pregnancy for "
            "both maternal and child health. General care includes balanced "
            "nutrition, adequate rest, and attending scheduled check-ups. Any "
            "bleeding, severe pain, or reduced baby movement needs immediate "
            "medical attention — please go to the nearest health center."
        ),
        "urgent_flags": ["bleeding", "severe pain", "reduced movement"],
    },
    {
        "topic": "Child Health",
        "keywords": "child baby infant vaccination growth immunization",
        "answer": (
            "Regular immunization and growth check-ups are key parts of "
            "child healthcare. Keep a record of vaccination dates and "
            "milestones. If a child has high fever, refuses to eat/drink, "
            "is unusually drowsy, or has breathing difficulty, seek medical "
            "help immediately."
        ),
        "urgent_flags": ["breathing", "drowsy", "not eating"],
    },
    {
        "topic": "Mental Wellbeing",
        "keywords": "stress anxiety worry sad mental health sleep problems",
        "answer": (
            "Feelings of stress or low mood are common and support is "
            "available. General steps that can help: regular sleep, talking "
            "to someone you trust, and light physical activity. If feelings "
            "are overwhelming, persistent, or affecting daily life, speaking "
            "with a health professional or counselor is strongly recommended."
        ),
        "urgent_flags": ["hopeless", "self harm", "suicide"],
    },
    {
        "topic": "Minor Cuts and Wounds",
        "keywords": "cut wound injury bleeding bruise burn",
        "answer": (
            "For minor cuts: clean the wound with clean water, apply gentle "
            "pressure to stop bleeding, and cover with a clean cloth or "
            "bandage. Deep wounds, wounds that won't stop bleeding, animal "
            "bites, or signs of infection (increasing redness, pus, fever) "
            "need prompt medical attention."
        ),
        "urgent_flags": ["deep", "won't stop bleeding", "animal bite", "infection"],
    },
]

EMERGENCY_CONTACTS = {
    "National Ambulance": "108",
    "National Emergency Number": "112",
    "Women's Helpline": "181",
    "Child Helpline": "1098",
}

DISCLAIMER = (
    "⚕️ This assistant provides general health information only. "
    "It does not diagnose conditions or prescribe treatment. "
    "For any medical concern, please consult a qualified doctor."
)
