# -*- coding: utf-8 -*-
"""
Premium English Mastery Telegram Bot
100 Advanced Questions - Production Ready
"""

import logging
import os
import sys
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ==================== CONFIGURATION ====================

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN not found!")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== DATA STORAGE ====================

user_sessions = {}
user_preferences = {}
stats = {
    "total_users": 0,
    "total_questions": 0,
    "total_correct": 0,
    "start_time": datetime.now().isoformat()
}

# ==================== 100 QUESTIONS ====================

questions = [
    # Section 1: Reading Passage Completion (1-15)
    {
        "question": "Read the passage: 'The ancient manuscript, which ______ in a monastery for centuries, was finally discovered in 2019.'",
        "options": ["A) had been hidden", "B) was hidden", "C) has been hidden", "D) is hidden"],
        "answer": "A",
        "explanation": "Past Perfect Passive 'had been hidden' - action completed before discovery."
    },
    {
        "question": "Passage completion: 'By the time the rescue team arrived, the survivors ______ for over 48 hours.'",
        "options": ["A) waited", "B) have been waiting", "C) had been waiting", "D) were waiting"],
        "answer": "C",
        "explanation": "Past Perfect Continuous emphasizes duration before another past action."
    },
    {
        "question": "Passage completion: 'Currently, the new bridge ______, and it's expected to open next spring.'",
        "options": ["A) is constructing", "B) is being constructed", "C) has constructed", "D) was constructed"],
        "answer": "B",
        "explanation": "Present Continuous Passive - ongoing action at present."
    },
    {
        "question": "Passage completion: 'By 2030, scientists predict that renewable energy ______ fossil fuels as the primary power source.'",
        "options": ["A) will replace", "B) will have replaced", "C) replaces", "D) is replacing"],
        "answer": "B",
        "explanation": "Future Perfect - action completed by specific future time."
    },
    {
        "question": "Passage completion: 'After the CEO ______ the company for 20 years, he announced his retirement.'",
        "options": ["A) led", "B) was leading", "C) had been leading", "D) has led"],
        "answer": "C",
        "explanation": "Past Perfect Continuous - duration before announcement."
    },
    {
        "question": "Passage completion: 'Climate change, which ______ a global crisis for decades, requires immediate action.'",
        "options": ["A) was", "B) had been", "C) has been", "D) is"],
        "answer": "C",
        "explanation": "Present Perfect - connects past to present."
    },
    {
        "question": "Passage completion: 'By the time you read this, the spacecraft ______ on Mars for three days.'",
        "options": ["A) will land", "B) will have landed", "C) will have been landing", "D) lands"],
        "answer": "C",
        "explanation": "Future Perfect Continuous - duration up to future point."
    },
    {
        "question": "Passage completion: 'The artifacts, which ______ in the tomb since 3000 BCE, provided invaluable insights.'",
        "options": ["A) were buried", "B) had been buried", "C) have been buried", "D) are buried"],
        "answer": "B",
        "explanation": "Past Perfect Passive - state before discovery."
    },
    {
        "question": "Passage completion: 'As we speak, negotiations ______ between the two countries to resolve the conflict.'",
        "options": ["A) hold", "B) are held", "C) are being held", "D) have held"],
        "answer": "C",
        "explanation": "Present Continuous Passive - ongoing at moment of speaking."
    },
    {
        "question": "Passage completion: 'The professor, along with her research team, ______ on this project since 2015.'",
        "options": ["A) work", "B) has been working", "C) have been working", "D) worked"],
        "answer": "B",
        "explanation": "Present Perfect Continuous - duration from past to present."
    },
    {
        "question": "Passage completion: 'Before the internet revolutionized communication, information ______ primarily through print media.'",
        "options": ["A) was disseminated", "B) is disseminated", "C) has been disseminated", "D) disseminates"],
        "answer": "A",
        "explanation": "Past Simple Passive - completed past state."
    },
    {
        "question": "Passage completion: 'The suspect ______ to have fled the country before the warrant was issued.'",
        "options": ["A) believes", "B) is believed", "C) believed", "D) has believed"],
        "answer": "B",
        "explanation": "Impersonal passive with reporting verb."
    },
    {
        "question": "Passage completion: 'By next December, I ______ as a software engineer for a decade.'",
        "options": ["A) will work", "B) will have been working", "C) work", "D) am working"],
        "answer": "B",
        "explanation": "Future Perfect Continuous - duration up to future point."
    },
    {
        "question": "Passage completion: 'The documentary, which ______ by millions worldwide, won multiple awards.'",
        "options": ["A) has been viewed", "B) had been viewed", "C) was viewed", "D) is viewed"],
        "answer": "A",
        "explanation": "Present Perfect Passive - past action with present relevance."
    },
    {
        "question": "Passage completion: 'During the summit, it ______ that the trade agreement would be signed by year-end.'",
        "options": ["A) announced", "B) was announced", "C) has announced", "D) is announcing"],
        "answer": "B",
        "explanation": "Past Simple Passive - reported past event."
    },
    
    # Section 2: Modal Auxiliaries (16-25)
    {
        "question": "Conversation:\nA: 'Someone's at the door. Who ______ it be at this hour?'\nB: 'I'm not sure. It ______ be the delivery person.'",
        "options": ["A) can / might", "B) must / should", "C) will / can", "D) shall / would"],
        "answer": "A",
        "explanation": "'Can' for possibility in questions; 'might' for possibility in statements."
    },
    {
        "question": "Conversation:\nA: 'I'm exhausted. I ______ have stayed up so late.'\nB: 'You're right. You ______ have gone to bed earlier.'",
        "options": ["A) shouldn't / should", "B) mustn't / must", "C) couldn't / could", "D) wouldn't / would"],
        "answer": "A",
        "explanation": "'Shouldn't have' expresses regret; 'should have' gives advice."
    },
    {
        "question": "Conversation:\nA: 'Look at that car! It ______ have cost a fortune.'\nB: 'Definitely. Only a millionaire ______ afford that.'",
        "options": ["A) can / must", "B) must / could", "C) might / should", "D) would / may"],
        "answer": "B",
        "explanation": "'Must have' for deduction; 'could' for possibility."
    },
    {
        "question": "Conversation:\nA: 'You ______ have told me you were coming! I would have prepared dinner.'\nB: 'I'm sorry. I ______ have let you know.'",
        "options": ["A) should / should", "B) must / must", "C) could / could", "D) might / might"],
        "answer": "A",
        "explanation": "'Should have' expresses criticism/regret about past action."
    },
    {
        "question": "Conversation:\nA: 'The museum ______ be closed today. It's a national holiday.'\nB: 'Actually, I think it ______ be open. I saw people inside.'",
        "options": ["A) must / might", "B) can / should", "C) might / must", "D) should / can"],
        "answer": "C",
        "explanation": "'Might' for possibility; 'must' for strong deduction."
    },
    {
        "question": "Conversation:\nA: 'You ______ have seen the look on his face when I told him!'\nB: 'I wish I ______ have been there.'",
        "options": ["A) should / should", "B) must / could", "C) could / would", "D) might / might"],
        "answer": "B",
        "explanation": "'Must have' for deduction; 'could have' for unrealized possibility."
    },
    {
        "question": "Conversation:\nA: 'I'm not feeling well. I ______ have eaten that seafood.'\nB: 'You're right. You ______ avoid street food in the future.'",
        "options": ["A) shouldn't / should", "B) mustn't / must", "C) couldn't / could", "D) wouldn't / would"],
        "answer": "A",
        "explanation": "'Shouldn't have' for regret; 'should' for future advice."
    },
    {
        "question": "Conversation:\nA: 'You ______ borrow my car if you need it.'\nB: 'Really? You ______ be so generous!'",
        "options": ["A) can / must", "B) may / might", "C) will / would", "D) could / should"],
        "answer": "A",
        "explanation": "'Can' for permission; 'must' for appreciation."
    },
    {
        "question": "Conversation:\nA: 'The instructions say we ______ not open the package until Christmas.'\nB: 'We ______ better follow the rules then.'",
        "options": ["A) must / had", "B) should / would", "C) can / might", "D) may / could"],
        "answer": "A",
        "explanation": "'Must not' for prohibition; 'had better' for strong advice."
    },
    {
        "question": "Conversation:\nA: 'You ______ be tired after that long flight.'\nB: 'I am. I ______ really use some sleep.'",
        "options": ["A) can / could", "B) must / could", "C) might / should", "D) would / may"],
        "answer": "B",
        "explanation": "'Must' for deduction; 'could' for polite expression."
    },
    
    # Section 3: Conditionals (26-40)
    {
        "question": "Zero Conditional (General Truth): 'If you ______ water to 100°C, it ______.'",
        "options": ["A) heat / boils", "B) will heat / boils", "C) heat / will boil", "D) heated / boiled"],
        "answer": "A",
        "explanation": "Zero Conditional: If + Present Simple, Present Simple."
    },
    {
        "question": "First Conditional (Real Future): 'If she ______ the exam, she ______ medical school next year.'",
        "options": ["A) passes / will enter", "B) will pass / enters", "C) passed / would enter", "D) had passed / would have entered"],
        "answer": "A",
        "explanation": "First Conditional: If + Present Simple, will + infinitive."
    },
    {
        "question": "Second Conditional (Unreal Present): 'If I ______ you, I ______ that job offer immediately.'",
        "options": ["A) am / will accept", "B) were / would accept", "C) had been / would have accepted", "D) was / accept"],
        "answer": "B",
        "explanation": "Second Conditional: If + Past Simple, would + infinitive."
    },
    {
        "question": "Third Conditional (Unreal Past): 'If they ______ the warning, the accident ______.'",
        "options": ["A) heeded / wouldn't happen", "B) had heeded / wouldn't have happened", "C) heeded / wouldn't have happened", "D) had heeded / didn't happen"],
        "answer": "B",
        "explanation": "Third Conditional: If + Past Perfect, would have + past participle."
    },
    {
        "question": "Mixed Conditional: 'If she ______ harder in college, she ______ a better job now.'",
        "options": ["A) studied / would have", "B) had studied / would have", "C) had studied / would be", "D) studied / would be"],
        "answer": "C",
        "explanation": "Mixed Conditional: Past condition affects present result."
    },
    {
        "question": "Mixed Conditional: 'If I ______ more confident, I ______ for that promotion last year.'",
        "options": ["A) am / would apply", "B) were / would have applied", "C) had been / would apply", "D) was / would apply"],
        "answer": "B",
        "explanation": "Mixed Conditional: Present state would have changed past outcome."
    },
    {
        "question": "Inverted Conditional: '______ earlier, the disaster could have been prevented.'",
        "options": ["A) Had they evacuated", "B) If they evacuated", "C) Were they to evacuate", "D) They evacuated"],
        "answer": "A",
        "explanation": "Inverted Third Conditional: 'Had + subject + past participle'."
    },
    {
        "question": "Inverted Conditional: '______ to win the lottery, what would you do?'",
        "options": ["A) Had you", "B) Were you", "C) If you", "D) Should you"],
        "answer": "B",
        "explanation": "Inverted Second Conditional: 'Were + subject + to + infinitive'."
    },
    {
        "question": "Conditional with 'unless': 'The project will succeed ______ everyone contributes fully.'",
        "options": ["A) unless", "B) if", "C) provided that", "D) only if"],
        "answer": "A",
        "explanation": "'Unless' means 'if not'."
    },
    {
        "question": "Conditional with 'provided that': 'You can borrow the car ______ you return it by 10 PM.'",
        "options": ["A) unless", "B) even if", "C) provided that", "D) as long as"],
        "answer": "C",
        "explanation": "'Provided that' introduces a necessary condition."
    },
    {
        "question": "Conditional with 'but for': '______ your support, I would have given up long ago.'",
        "options": ["A) Without", "B) But for", "C) Except for", "D) Aside from"],
        "answer": "B",
        "explanation": "'But for' means 'if it were not for'."
    },
    {
        "question": "Conditional with 'even if': 'I wouldn't marry him ______ he were the last man on Earth.'",
        "options": ["A) even if", "B) only if", "C) unless", "D) provided that"],
        "answer": "A",
        "explanation": "'Even if' introduces condition that doesn't change outcome."
    },
    {
        "question": "Conditional with 'supposing': '______ you inherited a million dollars, how would you spend it?'",
        "options": ["A) Unless", "B) Supposing", "C) Provided", "D) Even if"],
        "answer": "B",
        "explanation": "'Supposing' introduces a hypothetical scenario."
    },
    {
        "question": "Conditional with 'were it not for': '______ his quick thinking, the company would have collapsed.'",
        "options": ["A) Were it not for", "B) If it wasn't for", "C) Had it not been for", "D) But for"],
        "answer": "C",
        "explanation": "'Had it not been for' is third conditional for past events."
    },
    {
        "question": "Conditional with 'as long as': 'You'll succeed ______ you never give up.'",
        "options": ["A) unless", "B) as long as", "C) even if", "D) whereas"],
        "answer": "B",
        "explanation": "'As long as' introduces necessary condition for result."
    },
    
    # Section 4: Reported Speech (41-50)
    {
        "question": "Reported Speech: Direct: 'I will finish the project by Friday,' she said.\nReported: She said that she ______ the project by Friday.",
        "options": ["A) will finish", "B) would finish", "C) finishes", "D) finished"],
        "answer": "B",
        "explanation": "'Will' changes to 'would' in reported speech."
    },
    {
        "question": "Reported Speech: Direct: 'Where did you buy that jacket?' he asked.\nReported: He asked me where I ______ that jacket.",
        "options": ["A) bought", "B) had bought", "C) buy", "D) have bought"],
        "answer": "B",
        "explanation": "Past Simple changes to Past Perfect in reported questions."
    },
    {
        "question": "Reported Speech: Direct: 'Don't touch the artifacts,' the curator said.\nReported: The curator warned us ______ the artifacts.",
        "options": ["A) not to touch", "B) to not touch", "C) don't touch", "D) didn't touch"],
        "answer": "A",
        "explanation": "Negative commands use 'not to + infinitive'."
    },
    {
        "question": "Reported Speech: Direct: 'Could you help me with this?' she asked.\nReported: She asked me ______ help her with that.",
        "options": ["A) that I could", "B) if I could", "C) could I", "D) I could"],
        "answer": "B",
        "explanation": "Polite requests become 'asked if + subject + could'."
    },
    {
        "question": "Reported Speech: Direct: 'I'll see you tomorrow,' he said.\nReported: He said he would see me ______.",
        "options": ["A) tomorrow", "B) the next day", "C) on tomorrow", "D) the following tomorrow"],
        "answer": "B",
        "explanation": "Time expressions shift: tomorrow → the next day."
    },
    {
        "question": "Reported Speech: Direct: 'I'm staying here,' she said.\nReported: She said she was staying ______.",
        "options": ["A) there", "B) here", "C) at here", "D) in there"],
        "answer": "A",
        "explanation": "Place references shift: here → there."
    },
    {
        "question": "Reported Speech: Direct: 'You must finish this tonight,' he said.\nReported: He said I ______ finish that that night.",
        "options": ["A) must", "B) had to", "C) must have", "D) would"],
        "answer": "B",
        "explanation": "'Must' often changes to 'had to' for obligation."
    },
    {
        "question": "Reported Speech: Direct: 'Please arrive on time,' the manager said.\nReported: The manager asked us ______ on time.",
        "options": ["A) arrive", "B) to arrive", "C) arriving", "D) that we arrive"],
        "answer": "B",
        "explanation": "Imperatives use 'ask/tell + object + to + infinitive'."
    },
    {
        "question": "Reported Speech: Direct: 'The Earth orbits the Sun,' the teacher said.\nReported: The teacher said that the Earth ______ the Sun.",
        "options": ["A) orbited", "B) orbits", "C) had orbited", "D) was orbiting"],
        "answer": "B",
        "explanation": "Universal truths don't change tense."
    },
    {
        "question": "Reported Speech: Direct: 'I was waiting when you called,' he explained.\nReported: He explained that he ______ when I ______.",
        "options": ["A) waited / called", "B) was waiting / had called", "C) had been waiting / called", "D) had been waiting / had called"],
        "answer": "D",
        "explanation": "Past Continuous → Past Perfect Continuous; Past Simple → Past Perfect."
    },
    
    # Section 5: Advanced Vocabulary (51-65)
    {
        "question": "Vocabulary: The CEO's ______ speech inspired the entire company to work toward ambitious goals.",
        "options": ["A) lackluster", "B) mundane", "C) rousing", "D) tedious"],
        "answer": "C",
        "explanation": "'Rousing' means exciting, stirring, and inspiring."
    },
    {
        "question": "Vocabulary: Despite their ______ differences, the two leaders reached a historic agreement.",
        "options": ["A) trivial", "B) profound", "C) superficial", "D) negligible"],
        "answer": "B",
        "explanation": "'Profound' means deep, significant, and far-reaching."
    },
    {
        "question": "Vocabulary: The investigation was ______ by the sudden disappearance of key evidence.",
        "options": ["A) facilitated", "B) expedited", "C) hampered", "D) accelerated"],
        "answer": "C",
        "explanation": "'Hampered' means hindered, obstructed, or made difficult."
    },
    {
        "question": "Vocabulary: Her argument was so ______ that even her opponents had to admit she was right.",
        "options": ["A) tenuous", "B) flimsy", "C) compelling", "D) weak"],
        "answer": "C",
        "explanation": "'Compelling' means convincing, persuasive, and irrefutable."
    },
    {
        "question": "Vocabulary: The company's ______ growth has attracted investors from around the world.",
        "options": ["A) stagnant", "B) meteoric", "C) gradual", "D) modest"],
        "answer": "B",
        "explanation": "'Meteoric' means rapid, spectacular, and swift."
    },
    {
        "question": "Vocabulary: He's known for his ______ personality, always seeing the positive side of everything.",
        "options": ["A) cynical", "B) pessimistic", "C) sanguine", "D) morose"],
        "answer": "C",
        "explanation": "'Sanguine' means optimistic, cheerful, and positive."
    },
    {
        "question": "Vocabulary: The diplomat's ______ response avoided committing to either side of the conflict.",
        "options": ["A) candid", "B) forthright", "C) equivocal", "D) explicit"],
        "answer": "C",
        "explanation": "'Equivocal' means ambiguous, unclear, and deliberately vague."
    },
    {
        "question": "Vocabulary: The project's failure was ______; warning signs had appeared months earlier.",
        "options": ["A) unforeseeable", "B) inevitable", "C) fortuitous", "D) serendipitous"],
        "answer": "B",
        "explanation": "'Inevitable' means unavoidable and certain to happen."
    },
    {
        "question": "Vocabulary: Her ______ knowledge of ancient languages made her invaluable to the research team.",
        "options": ["A) superficial", "B) rudimentary", "C) encyclopedic", "D) limited"],
        "answer": "C",
        "explanation": "'Encyclopedic' means comprehensive, vast, and all-encompassing."
    },
    {
        "question": "Vocabulary: The artist's work was ______ by critics who dismissed it as meaningless.",
        "options": ["A) lauded", "B) celebrated", "C) vilified", "D) acclaimed"],
        "answer": "C",
        "explanation": "'Vilified' means harshly criticized or denounced."
    },
    {
        "question": "Vocabulary: After years of economic decline, the country is finally showing signs of ______.",
        "options": ["A) stagnation", "B) recession", "C) rejuvenation", "D) deterioration"],
        "answer": "C",
        "explanation": "'Rejuvenation' means restoration and revival after decline."
    },
    {
        "question": "Vocabulary: The lawyer presented a ______ case that left no doubt about his client's innocence.",
        "options": ["A) weak", "B) tenuous", "C) ironclad", "D) dubious"],
        "answer": "C",
        "explanation": "'Ironclad' means unbreakable, solid, and incontrovertible."
    },
    {
        "question": "Vocabulary: Her ______ remarks during the meeting offended several colleagues.",
        "options": ["A) tactful", "B) diplomatic", "C) brusque", "D) considerate"],
        "answer": "C",
        "explanation": "'Brusque' means abrupt, blunt, and rude."
    },
    {
        "question": "Vocabulary: The company's ______ into new markets proved to be highly profitable.",
        "options": ["A) retreat", "B) withdrawal", "C) foray", "D) hesitation"],
        "answer": "C",
        "explanation": "'Foray' means an initial attempt or venture into new area."
    },
    {
        "question": "Vocabulary: The government's ______ approach to reform frustrated those who wanted immediate change.",
        "options": ["A) radical", "B) drastic", "C) incremental", "D) revolutionary"],
        "answer": "C",
        "explanation": "'Incremental' means gradual, step-by-step, and slow."
    },
    
    # Section 6: Reading Comprehension (66-80)
    {
        "question": "Reading: 'Despite the company's efforts to diversify, its fortunes remained inextricably linked to the volatile oil market.'\nWhat does 'inextricably linked' mean?",
        "options": ["A) Completely separated", "B) Unavoidably connected", "C) Temporarily associated", "D) Superficially related"],
        "answer": "B",
        "explanation": "'Inextricably linked' means impossible to separate or disconnect."
    },
    {
        "question": "Reading: 'The protagonist is a quintessential antihero: brilliant but morally ambiguous, driven by self-interest yet capable of unexpected altruism.'\nThe protagonist is:",
        "options": ["A) A perfect hero", "B) A complex character with contradictions", "C) A purely villainous figure", "D) A simple character"],
        "answer": "B",
        "explanation": "The description shows contradictions, making the character complex."
    },
    {
        "question": "Reading: 'The policy has been met with a groundswell of opposition.'\nWhat does 'groundswell' suggest?",
        "options": ["A) Minor opposition", "B) Rapidly growing movement", "C) Organized by management", "D) Temporary opposition"],
        "answer": "B",
        "explanation": "'Groundswell' refers to a rapidly growing grassroots movement."
    },
    {
        "question": "Reading: 'While initial results were promising, subsequent trials failed to replicate the findings.'\nWhat does this imply?",
        "options": ["A) Definitely correct", "B) Findings may be unreliable", "C) Never published", "D) Immediately accepted"],
        "answer": "B",
        "explanation": "Inability to replicate results casts doubt on validity."
    },
    {
        "question": "Reading: 'The CEO's resignation precipitated a cascade of executive departures.'\nWhat does 'precipitating' mean?",
        "options": ["A) Preventing", "B) Delaying", "C) Causing suddenly", "D) Ignoring"],
        "answer": "C",
        "explanation": "'Precipitating' means causing something to happen suddenly."
    },
    {
        "question": "Reading: 'Implementation has been stymied by bureaucratic inertia.'\nWhat happened to implementation?",
        "options": ["A) Progressed quickly", "B) Fully implemented", "C) Obstructed", "D) Celebrated"],
        "answer": "C",
        "explanation": "'Stymied' means prevented, obstructed, or blocked."
    },
    {
        "question": "Reading: 'She held the audience spellbound for over two hours.'\nWhat does 'spellbound' mean?",
        "options": ["A) Bored", "B) Confused", "C) Captivated", "D) Angry"],
        "answer": "C",
        "explanation": "'Spellbound' means completely captivated and fascinated."
    },
    {
        "question": "Reading: 'The economy is predicated on tourism.'\nWhat does 'predicated on' mean?",
        "options": ["A) Independent of", "B) Based on", "C) Unrelated to", "D) Harmful to"],
        "answer": "B",
        "explanation": "'Predicated on' means based on, founded upon, or dependent on."
    },
    {
        "question": "Reading: 'His argument was replete with logical fallacies.'\nWhat does 'replete with' mean?",
        "options": ["A) Lacked", "B) Filled with", "C) Few", "D) Ignored"],
        "answer": "B",
        "explanation": "'Replete with' means full of, abundantly supplied with."
    },
    {
        "question": "Reading: 'The discovery was serendipitous.'\nWhat does 'serendipitous' mean?",
        "options": ["A) Planned", "B) Expected", "C) Accidental but fortunate", "D) Disappointing"],
        "answer": "C",
        "explanation": "'Serendipitous' means occurring by chance in a happy way."
    },
    {
        "question": "Reading: 'Despite sanguine projections, profits plummeted.'\nWhat does 'sanguine' mean?",
        "options": ["A) Pessimistic", "B) Realistic", "C) Overly optimistic", "D) Accurate"],
        "answer": "C",
        "explanation": "'Sanguine' means optimistic, especially when unwarranted."
    },
    {
        "question": "Reading: 'The decision was a fait accompli.'\nWhat does 'fait accompli' mean?",
        "options": ["A) Ongoing discussion", "B) Already completed fact", "C) Future possibility", "D) Rejected idea"],
        "answer": "B",
        "explanation": "'Fait accompli' is French for 'accomplished fact'."
    },
    {
        "question": "Reading: 'Her research was characterized by meticulous attention to detail.'\nWhat does 'meticulous' mean?",
        "options": ["A) Careless", "B) Extremely careful", "C) Quick", "D) Superficial"],
        "answer": "B",
        "explanation": "'Meticulous' means showing great attention to detail."
    },
    {
        "question": "Reading: 'The rebranding was largely cosmetic.'\nWhat does 'cosmetic' mean?",
        "options": ["A) Fundamental", "B) Superficial", "C) Innovative", "D) Successful"],
        "answer": "B",
        "explanation": "'Cosmetic' changes are superficial, affecting appearance only."
    },
    {
        "question": "Reading: 'His taciturn nature was mistaken for hostility.'\nWhat does 'taciturn' mean?",
        "options": ["A) Talkative", "B) Reserved and silent", "C) Friendly", "D) Aggressive"],
        "answer": "B",
        "explanation": "'Taciturn' means reserved, uncommunicative, and inclined to silence."
    },
    
    # Section 7: Complex Reading (81-90)
    {
        "question": "Complex Reading: 'The juxtaposition of opulence and squalor illustrates the widening chasm between socioeconomic strata.'\nWhat does 'juxtaposition' mean?",
        "options": ["A) Separation", "B) Blending", "C) Side-by-side placement", "D) Confusion"],
        "answer": "C",
        "explanation": "'Juxtaposition' means placing two things side by side for contrast."
    },
    {
        "question": "Complex Reading: 'Her magnum opus cemented her legacy as a preeminent literary voice.'\nWhat is a 'magnum opus'?",
        "options": ["A) Minor work", "B) Masterpiece", "C) Unfinished project", "D) Failed attempt"],
        "answer": "B",
        "explanation": "'Magnum opus' refers to an artist's greatest work."
    },
    {
        "question": "Complex Reading: 'The negotiations reached an impasse.'\nWhat does 'impasse' mean?",
        "options": ["A) Breakthrough", "B) Deadlock", "C) Compromise", "D) Agreement"],
        "answer": "B",
        "explanation": "'Impasse' means a situation where no progress is possible."
    },
    {
        "question": "Complex Reading: 'Despite espoused commitment, documents revealed disregard for regulations.'\nWhat does 'espoused' suggest?",
        "options": ["A) Genuine", "B) Secret", "C) Claimed but possibly insincere", "D) Recent"],
        "answer": "C",
        "explanation": "'Espoused' means claimed or professed, possibly insincere."
    },
    {
        "question": "Complex Reading: 'The work eschewed hagiography in favor of nuanced analysis.'\nWhat does 'eschewing hagiography' mean?",
        "options": ["A) Avoiding uncritical praise", "B) Embracing criticism", "C) Writing biography", "D) Focusing on flaws"],
        "answer": "A",
        "explanation": "'Eschewing' means avoiding; 'hagiography' is idealized biography."
    },
    {
        "question": "Complex Reading: 'The software was fraught with bugs.'\nWhat does 'fraught with' mean?",
        "options": ["A) Lacking", "B) Filled with problems", "C) Improved by", "D) Enhanced by"],
        "answer": "B",
        "explanation": "'Fraught with' means filled with (usually something negative)."
    },
    {
        "question": "Complex Reading: 'His mercurial temperament made him difficult to work with.'\nWhat does 'mercurial' describe?",
        "options": ["A) Stable", "B) Predictable", "C) Volatile", "D) Calm"],
        "answer": "C",
        "explanation": "'Mercurial' means subject to sudden, unpredictable mood changes."
    },
    {
        "question": "Complex Reading: 'The company's fiduciary duty to shareholders conflicted with ethical sourcing.'\nWhat is 'fiduciary duty'?",
        "options": ["A) Ethical responsibility", "B) Legal obligation", "C) Financial trust responsibility", "D) Social commitment"],
        "answer": "C",
        "explanation": "'Fiduciary duty' is a legal obligation to act in financial interest."
    },
    {
        "question": "Complex Reading: 'The film's denouement provides cathartic release.'\nWhat does 'denouement' refer to?",
        "options": ["A) Beginning", "B) Climax", "C) Resolution", "D) Conflict"],
        "answer": "C",
        "explanation": "'Denouement' is the final resolution of a story."
    },
    {
        "question": "Complex Reading: 'His argument was predicated on a specious assumption.'\nWhat does 'specious' mean?",
        "options": ["A) Valid", "B) Superficially plausible but false", "C) Well-reasoned", "D) Proven"],
        "answer": "B",
        "explanation": "'Specious' means superficially plausible but actually false."
    },
    
    # Section 8: All Tenses (91-100)
    {
        "question": "Tense: 'By the time she arrives, the speaker ______ for over an hour.'",
        "options": ["A) will speak", "B) will have spoken", "C) will have been speaking", "D) speaks"],
        "answer": "C",
        "explanation": "Future Perfect Continuous emphasizes duration up to future point."
    },
    {
        "question": "Tense: 'I ______ to contact you several times last week.'",
        "options": ["A) try", "B) have tried", "C) tried", "D) had tried"],
        "answer": "C",
        "explanation": "Past Simple for completed actions at a specific time."
    },
    {
        "question": "Tense: 'For the past decade, the company ______ its market share steadily.'",
        "options": ["A) increased", "B) has been increasing", "C) had increased", "D) was increasing"],
        "answer": "B",
        "explanation": "Present Perfect Continuous emphasizes ongoing action up to now."
    },
    {
        "question": "Tense: 'When I arrived, I realized I ______ my ticket at home.'",
        "options": ["A) left", "B) have left", "C) had left", "D) was leaving"],
        "answer": "C",
        "explanation": "Past Perfect for action completed before another past action."
    },
    {
        "question": "Tense: 'Next week at this time, we ______ on a beach.'",
        "options": ["A) will relax", "B) will be relaxing", "C) relax", "D) are relaxing"],
        "answer": "B",
        "explanation": "Future Continuous for action in progress at specific future time."
    },
    {
        "question": "Tense: 'She ______ as a nurse for fifteen years before she decided to pursue medicine.'",
        "options": ["A) worked", "B) has worked", "C) had been working", "D) was working"],
        "answer": "C",
        "explanation": "Past Perfect Continuous emphasizes duration before another past action."
    },
    {
        "question": "Tense: 'This is the third time you ______ that excuse this week.'",
        "options": ["A) use", "B) used", "C) have used", "D) are using"],
        "answer": "C",
        "explanation": "'This is the + ordinal number + time' requires present perfect."
    },
    {
        "question": "Tense: 'By 2030, autonomous vehicles ______ conventional cars.'",
        "options": ["A) will replace", "B) will have replaced", "C) replace", "D) are replacing"],
        "answer": "B",
        "explanation": "Future Perfect for actions completed by a specific future time."
    },
    {
        "question": "Tense: 'I ______ to call you when you walked through the door.'",
        "options": ["A) was about", "B) am about", "C) have been about", "D) had about"],
        "answer": "A",
        "explanation": "'Was about to' expresses an action that was going to happen but was interrupted."
    },
    {
        "question": "Tense: 'It's high time we ______ action on climate change.'",
        "options": ["A) take", "B) took", "C) have taken", "D) are taking"],
        "answer": "B",
        "explanation": "'It's (high) time' is followed by past simple."
    }
]

TOTAL_QUESTIONS = len(questions)
logger.info(f"📚 Loaded {TOTAL_QUESTIONS} questions")

# ==================== HELPER FUNCTIONS ====================

def get_category(index):
    if index < 15: return "📖 Reading Completion"
    elif index < 25: return "💬 Modal Conversations"
    elif index < 40: return "🔄 Conditionals"
    elif index < 50: return "🗣️ Reported Speech"
    elif index < 65: return "📚 Advanced Vocabulary"
    elif index < 90: return "📖 Reading Comprehension"
    else: return "⏰ Tense Mastery"

def get_progress_bar(current, total, width=10):
    filled = int((current / total) * width)
    return "█" * filled + "░" * (width - filled)

def get_level(percentage):
    if percentage >= 95: return ("🏆 GRAND MASTER", "🌟 LEGENDARY!")
    elif percentage >= 85: return ("🥇 ADVANCED EXPERT", "🎉 EXCELLENT!")
    elif percentage >= 75: return ("🥈 PROFICIENT", "📚 VERY GOOD!")
    elif percentage >= 65: return ("🥉 COMPETENT", "💪 GOOD EFFORT!")
    elif percentage >= 50: return ("📘 INTERMEDIATE", "📖 KEEP PRACTICING!")
    else: return ("🌱 DEVELOPING", "🌟 Review and try again!")

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    user_sessions[user_id] = {"index": 0, "score": 0}
    if user_id not in user_preferences:
        user_preferences[user_id] = {"show_explanations": True}
    
    stats["total_users"] = len(user_sessions)
    
    settings_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")]
    ])
    
    await update.message.reply_text(
        f"<b>🏆 PREMIUM ENGLISH MASTERY</b>\n\n"
        f"<b>📚 {TOTAL_QUESTIONS} Questions</b>\n"
        f"✓ Reading | ✓ Modals | ✓ Conditionals\n"
        f"✓ Reported | ✓ Vocabulary | ✓ Comprehension | ✓ Tenses\n\n"
        f"<b>⚙️ Settings:</b>\n"
        f"• Explanations: {'✅ ON' if user_preferences[user_id]['show_explanations'] else '❌ OFF'}\n\n"
        f"<b>🎯 Let's begin!</b>",
        reply_markup=settings_button,
        parse_mode="HTML"
    )
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    
    if not session or session["index"] >= TOTAL_QUESTIONS:
        score = session.get("score", 0) if session else 0
        percentage = (score / TOTAL_QUESTIONS) * 100
        level, feedback = get_level(percentage)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"<b>🏆 QUIZ COMPLETE!</b>\n\n"
                 f"📊 <b>Score:</b> {score}/{TOTAL_QUESTIONS}\n"
                 f"📈 <b>Percentage:</b> {percentage:.1f}%\n"
                 f"⭐ <b>Level:</b> {level}\n\n"
                 f"{feedback}\n\n"
                 f"<i>Type /start to try again!</i>",
            parse_mode="HTML"
        )
        return
    
    idx = session["index"]
    q = questions[idx]
    
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt[0])] for opt in q["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    progress = get_progress_bar(idx, TOTAL_QUESTIONS)
    percent = (idx / TOTAL_QUESTIONS) * 100
    category = get_category(idx)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"<b>{category}</b>\n"
             f"<b>📝 Q{idx + 1}/{TOTAL_QUESTIONS}</b>\n"
             f"<code>[{progress}]</code> <i>{percent:.0f}%</i>\n\n"
             f"{q['question']}",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    # Settings menu
    if query.data == "open_settings":
        await show_settings(update, context)
        return
    elif query.data == "toggle_explanations":
        await toggle_explanations(update, context)
        return
    elif query.data == "back_to_quiz":
        await back_to_quiz(update, context)
        return
    
    # Handle answers
    session = user_sessions.get(user_id)
    if not session:
        return
    
    idx = session["index"]
    if idx >= TOTAL_QUESTIONS:
        return
    
    user_choice = query.data
    q = questions[idx]
    
    # Disable buttons
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except:
        pass
    
    # Check answer
    stats["total_questions"] += 1
    if user_choice == q["answer"]:
        session["score"] += 1
        stats["total_correct"] += 1
        result_text = "✅ <b>CORRECT!</b> 🎯\n\n"
    else:
        correct_text = next(opt for opt in q["options"] if opt.startswith(q["answer"]))
        result_text = f"❌ <b>INCORRECT</b>\n\n<b>✓ Correct Answer:</b> {correct_text}\n\n"
    
    # Show explanation
    show_exp = user_preferences.get(user_id, {}).get("show_explanations", True)
    
    if show_exp:
        text = result_text + f"<b>📖 Explanation:</b>\n{q['explanation']}\n\n<i>⚡ Next in 1s...</i>"
    else:
        text = result_text + f"<i>⚡ Next question in 1s...</i>"
    
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode="HTML"
    )
    
    # Next question
    session["index"] += 1
    asyncio.create_task(send_question(update, context))
    
    # Delete explanation after 1 second
    if show_exp:
        async def delete_later():
            await asyncio.sleep(1)
            try:
                await msg.delete()
            except:
                pass
        asyncio.create_task(delete_later())

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    show_exp = user_preferences.get(user_id, {}).get("show_explanations", True)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{'✅' if show_exp else '❌'} Show Explanations", callback_data="toggle_explanations")],
        [InlineKeyboardButton("🔙 Back to Quiz", callback_data="back_to_quiz")]
    ])
    
    await query.edit_message_text(
        text=f"<b>⚙️ Settings</b>\n\n"
             f"<b>Explanations:</b> {'ON' if show_exp else 'OFF'}\n\n"
             f"<b>Tips:</b>\n"
             f"• OFF = faster quiz\n"
             f"• ON = detailed learning\n\n"
             f"<i>Choose below:</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await query.answer()

async def toggle_explanations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    current = user_preferences.get(user_id, {}).get("show_explanations", True)
    user_preferences[user_id] = {"show_explanations": not current}
    
    await query.answer(f"Explanations {'ON' if not current else 'OFF'}!")
    await show_settings(update, context)

async def back_to_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    session = user_sessions.get(user_id)
    if session and session["index"] < TOTAL_QUESTIONS:
        idx = session["index"]
        q = questions[idx]
        
        keyboard = [[InlineKeyboardButton(opt, callback_data=opt[0])] for opt in q["options"]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        progress = get_progress_bar(idx, TOTAL_QUESTIONS)
        percent = (idx / TOTAL_QUESTIONS) * 100
        category = get_category(idx)
        
        await query.edit_message_text(
            text=f"<b>{category}</b>\n"
                 f"<b>📝 Q{idx + 1}/{TOTAL_QUESTIONS}</b>\n"
                 f"<code>[{progress}]</code> <i>{percent:.0f}%</i>\n\n"
                 f"{q['question']}",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    await query.answer()

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    accuracy = (stats["total_correct"] / stats["total_questions"] * 100) if stats["total_questions"] > 0 else 0
    await update.message.reply_text(
        f"<b>📊 GLOBAL STATS</b>\n\n"
        f"👥 Users: {stats['total_users']}\n"
        f"📝 Questions: {stats['total_questions']:,}\n"
        f"✅ Correct: {stats['total_correct']:,}\n"
        f"📈 Accuracy: {accuracy:.1f}%",
        parse_mode="HTML"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

# ==================== MAIN ====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_error_handler(error_handler)
    
    logger.info("🚀 Bot starting with polling mode...")
    app.run_polling()

if __name__ == "__main__":
    main()
