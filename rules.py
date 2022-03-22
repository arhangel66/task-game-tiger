from enum import Enum

animals_rules = {
    "Lion": ["Tiger", "Wolf", "Deer"],
    "Tiger": ["Wolf", "Deer"],
    "Wolf": ["Deer"],
    "Deer": [],
}

rock_paper_scissors_rules = {
    "Rock": ["Scissors"],
    "Paper": ["Rock"],
    "Scissors": ["Paper"],
}

