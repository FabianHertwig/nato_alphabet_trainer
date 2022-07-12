import streamlit as st
from collections import Counter
import numpy as np
import pandas as pd
from numpy.random import choice

alphabet = {
    "A": ["Alfa", "Alpha"],
    "B": ["Bravo"],
    "C": ["Charlie"],
    "D": ["Delta"],
    "E": ["Echo"],
    "F": ["Foxtrot"],
    "G": ["Golf"],
    "H": ["Hotel"],
    "I": ["India"],
    "J": ["Juliett", "Juliet"],
    "K": ["Kilo"],
    "L": ["Lima"],
    "M": ["Mike"],
    "N": ["November"],
    "O": ["Oscar", "Oskar"],
    "P": ["Papa"],
    "Q": ["Quebec"],
    "R": ["Romeo"],
    "S": ["Sierra", "Siera"],
    "T": ["Tango"],
    "U": ["Uniform"],
    "V": ["Victor", "Viktor"],
    "W": ["Whiskey"],
    "X": ["XRay", "X-Ray"],
    "Y": ["Yankee"],
    "Z": ["Zulu"],
}

celebrate_emoticons = ["👏", "🥳", "🫡", "🙌", "🎉", "👍", "💪", "💃", "✅", "🚀"]

def pick_test_letter(alphabet, correct_answers, last_tested_letter):

    def set_zero_probability_for_last_tested(correct_answers, last_tested_letter, letter_pick_probabilities):
        index_of_last_tested_letter = list(correct_answers.keys()).index(last_tested_letter)
        letter_pick_probabilities[index_of_last_tested_letter] = 0.0
        return letter_pick_probabilities

    def get_inverse_distribution(correct_answers):
        correct_answers_numbers = np.array(list(correct_answers.values()))
        letter_pick_probabilities = 1.0 / correct_answers_numbers
        return letter_pick_probabilities

    def make_sum_to_one(letter_pick_probabilities):
        return letter_pick_probabilities / letter_pick_probabilities.sum()

    letter_pick_probabilities = get_inverse_distribution(correct_answers)

    if last_tested_letter is not None:
        letter_pick_probabilities = set_zero_probability_for_last_tested(correct_answers, last_tested_letter, letter_pick_probabilities)

    letter_pick_probabilities = make_sum_to_one(letter_pick_probabilities)
    letter_to_test = choice(list(alphabet.keys()), p=letter_pick_probabilities)
    return letter_to_test


if "hint" not in st.session_state:
    st.session_state.hint = ""

if "last_tested_letter" not in st.session_state:
    st.session_state.last_tested_letter = None

if "correct_answers" not in st.session_state:
    counter = Counter({key: 1 for key in alphabet.keys()})
    st.session_state.correct_answers = counter





def check_input(solutions, letter_to_test, show_balloons):
    text_input = st.session_state.input
    lower_solutions = [str.lower(solution) for solution in solutions]
    if str.lower(text_input) in lower_solutions:
        if show_balloons:
            st.balloons()
        st.session_state.hint = choice(celebrate_emoticons)
        st.session_state.correct_answers += Counter(letter_to_test)
    else:
        st.session_state.hint = f"The correct answer was: {solutions[0]}"

    st.session_state.input = ""
    st.session_state.last_tested_letter = letter_to_test

with st.sidebar:
    st.header("Settings")
    show_balloons=st.checkbox("🎈", True)

    st.header("Info")
    st.markdown("[ICAO / NATO Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet)")
    st.markdown("[Source code on Github](https://github.com/FabianHertwig/nato_alphabet_trainer)")
    st.write("Made by [@fabianhertwig](https://twitter.com/fabianhertwig)")


st.title("ICAO / NATO Alphabet Trainer")
st.subheader("Write the spelling of the following letter")

letter_to_test = pick_test_letter(alphabet, st.session_state.correct_answers, st.session_state.last_tested_letter)
solutions = alphabet[letter_to_test]

st.title(letter_to_test)
input = st.text_input("", key="input", on_change=check_input, args=[solutions, letter_to_test, show_balloons])
st.text(st.session_state.hint)

df = pd.DataFrame.from_dict(st.session_state.correct_answers, orient="index")
df = df.rename(columns= {0: "Correct Answers"})
df["Correct Answers"] = df["Correct Answers"] - 1

st.write("Correct Answers")
st.bar_chart(df)
