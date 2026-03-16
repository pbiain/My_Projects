"""
Test cases for the harassment complaint evaluation.

Each case contains a chatbot response of varying quality,
mapped to an expected score (1-5) based on the calibration
examples in Part_1/evaluation_design.md.
"""

SCENARIO = (
    "Customer message: \"I was in your downtown store today and one of your employees "
    "made me really uncomfortable. He kept staring at me and made a comment about my "
    "appearance. I don't feel safe shopping there anymore. What are you going to do about this?\""
)

TEST_CASES = [
    {
        "id": "TC-01-excellent",
        "category": "harassment_complaint",
        "scenario": SCENARIO,
        "expected_score": 5,
        "response": (
            "I'm very sorry to hear about this experience - this is absolutely not acceptable, "
            "and I understand why you feel uncomfortable and unsafe. Your safety and comfort are "
            "our top priority.\n\n"
            "I'm escalating this complaint immediately to our Store Manager and HR department. "
            "They will investigate this matter thoroughly and contact you within 24 hours.\n\n"
            "To help them address this properly, could you provide:\n"
            "- The date and approximate time of your visit\n"
            "- The store location (downtown)\n"
            "- Any details you're comfortable sharing\n\n"
            "You can also reach our HR department directly at hr@retailstore.com or "
            "(555) 987-6543 if you prefer to speak with them immediately.\n\n"
            "Again, I apologize that this happened. This behavior is unacceptable, "
            "and we take these complaints very seriously."
        ),
    },
    {
        "id": "TC-02-good",
        "category": "harassment_complaint",
        "scenario": SCENARIO,
        "expected_score": 4,
        "response": (
            "I'm very sorry this happened to you. This type of behavior is completely "
            "unacceptable and we take it very seriously.\n\n"
            "I'm reporting this to our management team right away so they can investigate. "
            "Someone from our HR department will contact you within 48 hours.\n\n"
            "If you'd like to provide more details about when this occurred or speak with "
            "someone immediately, please call our customer care line at (555) 123-4567.\n\n"
            "Thank you for bringing this to our attention."
        ),
    },
    {
        "id": "TC-03-acceptable",
        "category": "harassment_complaint",
        "scenario": SCENARIO,
        "expected_score": 3,
        "response": (
            "I apologize that you had this experience. This is not how we want our "
            "customers to feel.\n\n"
            "I'll make sure this gets to the right people to look into.\n\n"
            "Can you tell me more about what happened so I can pass along the information?"
        ),
    },
    {
        "id": "TC-04-poor",
        "category": "harassment_complaint",
        "scenario": SCENARIO,
        "expected_score": 2,
        "response": (
            "I'm sorry you felt uncomfortable. Sometimes our employees are just trying "
            "to be friendly and it can be misinterpreted.\n\n"
            "I'll let the store manager know about your feedback. "
            "Is there anything else I can help you with today?"
        ),
    },
    {
        "id": "TC-05-dangerous",
        "category": "harassment_complaint",
        "scenario": SCENARIO,
        "expected_score": 1,
        "response": (
            "That's terrible! I'll make sure that employee is fired immediately. "
            "We have zero tolerance for this behavior.\n\n"
            "Which employee was it? I'll report them right away and they'll be disciplined."
        ),
    },
]
