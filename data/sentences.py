"""
Dutch sentence builder — scrambled words to reorder.
Each entry: scrambled (list), correct (list), english, cefr.
"""

SENTENCES = [
    {"scrambled": ["is", "mijn", "naam", "Jan"], "correct": ["Mijn","naam","is","Jan"], "english": "My name is Jan.", "cefr": "A1"},
    {"scrambled": ["koffie", "ik", "drink", "graag"], "correct": ["Ik","drink","graag","koffie"], "english": "I like to drink coffee.", "cefr": "A1"},
    {"scrambled": ["mooi", "het", "is", "weer"], "correct": ["Het","weer","is","mooi"], "english": "The weather is beautiful.", "cefr": "A1"},
    {"scrambled": ["vijf", "per", "werk", "dagen", "ik", "week"], "correct": ["Ik","werk","vijf","dagen","per","week"], "english": "I work five days per week.", "cefr": "A1"},
    {"scrambled": ["Amsterdam", "in", "woon", "ik"], "correct": ["Ik","woon","in","Amsterdam"], "english": "I live in Amsterdam.", "cefr": "A1"},
    {"scrambled": ["spreekt", "Nederlands", "zij", "goed"], "correct": ["Zij","spreekt","goed","Nederlands"], "english": "She speaks Dutch well.", "cefr": "A1"},
    {"scrambled": ["naar", "school", "kinderen", "de", "gaan"], "correct": ["De","kinderen","gaan","naar","school"], "english": "The children go to school.", "cefr": "A1"},
    {"scrambled": ["een", "boek", "lees", "ik"], "correct": ["Ik","lees","een","boek"], "english": "I am reading a book.", "cefr": "A1"},

    {"scrambled": ["morgen", "naar", "ik", "de", "ga", "dokter"], "correct": ["Ik","ga","morgen","naar","de","dokter"], "english": "Tomorrow I am going to the doctor.", "cefr": "A2"},
    {"scrambled": ["de", "Nederland", "in", "fietst", "iedereen"], "correct": ["Iedereen","fietst","in","Nederland"], "english": "Everyone cycles in the Netherlands.", "cefr": "A2"},
    {"scrambled": ["wil", "een", "ik", "biertje", "graag"], "correct": ["Ik","wil","graag","een","biertje"], "english": "I would like a beer.", "cefr": "A2"},
    {"scrambled": ["heeft", "zij", "broers", "twee"], "correct": ["Zij","heeft","twee","broers"], "english": "She has two brothers.", "cefr": "A2"},
    {"scrambled": ["mijn", "Amsterdam", "in", "vriend", "woont"], "correct": ["Mijn","vriend","woont","in","Amsterdam"], "english": "My friend lives in Amsterdam.", "cefr": "A2"},
    {"scrambled": ["kunt", "dat", "herhalen", "u"], "correct": ["Kunt","u","dat","herhalen"], "english": "Can you repeat that?", "cefr": "A2"},
    {"scrambled": ["drie", "vertrekt", "de", "om", "trein", "uur"], "correct": ["De","trein","vertrekt","om","drie","uur"], "english": "The train departs at three o'clock.", "cefr": "A2"},
    {"scrambled": ["elke", "ik", "ochtend", "koffie", "drink"], "correct": ["Ik","drink","elke","ochtend","koffie"], "english": "I drink coffee every morning.", "cefr": "A2"},

    {"scrambled": ["als", "ik", "bel", "je", "thuis", "kom"], "correct": ["Ik","bel","je","als","ik","thuis","kom"], "english": "I'll call you when I get home.", "cefr": "B1"},
    {"scrambled": ["wil", "omdat", "het", "ik", "lekker", "is", "eten"], "correct": ["Ik","wil","eten","omdat","het","lekker","is"], "english": "I want to eat because it is tasty.", "cefr": "B1"},
    {"scrambled": ["heeft", "mij", "dat", "hij", "gezegd"], "correct": ["Hij","heeft","mij","dat","gezegd"], "english": "He told me that.", "cefr": "B1"},
    {"scrambled": ["was", "het", "koud", "ik", "binnen", "bleef", "omdat"], "correct": ["Omdat","het","koud","was","bleef","ik","binnen"], "english": "Because it was cold, I stayed inside.", "cefr": "B1"},
    {"scrambled": ["als", "komt", "zij", "ik", "schrijf", "een", "tijd", "heb"], "correct": ["Als","ik","tijd","heb","schrijf","ik","een","brief"], "english": "When I have time, I will write a letter.", "cefr": "B1"},
    {"scrambled": ["hoewel", "hij", "ging", "moe", "naar", "was", "feest", "het"], "correct": ["Hoewel","hij","moe","was","ging","hij","naar","het","feest"], "english": "Although he was tired, he went to the party.", "cefr": "B1"},
]

CEFR_LEVELS = sorted(set(s["cefr"] for s in SENTENCES))
