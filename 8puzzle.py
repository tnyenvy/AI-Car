import streamlit as st
from simpleai.search import astar, SearchProblem
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image

# Goal and initial states
GOAL = '''1-2-3
4-5-6
7-8-e'''

INITIAL = '''4-1-2
7-e-3
8-5-6'''

# Helper functions
def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])

def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]

def find_location(rows, element_to_find):
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic

# Precompute goal positions for each piece
goal_positions = {}
rows_goal = string_to_list(GOAL)
for number in '12345678e':
    goal_positions[number] = find_location(rows_goal, number)

class EigthPuzzleProblem(SearchProblem):
    def actions(self, state):
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')
        actions = []
        if row_e > 0:
            actions.append(rows[row_e - 1][col_e])
        if row_e < 2:
            actions.append(rows[row_e + 1][col_e])
        if col_e > 0:
            actions.append(rows[row_e][col_e - 1])
        if col_e < 2:
            actions.append(rows[row_e][col_e + 1])
        return actions

    def result(self, state, action):
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')
        row_n, col_n = find_location(rows, action)
        rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]
        return list_to_string(rows)

    def is_goal(self, state):
        return state == GOAL

    def cost(self, state1, action, state2):
        return 1

    def heuristic(self, state):
        rows = string_to_list(state)
        distance = 0
        for number in '12345678e':
            row_n, col_n = find_location(rows, number)
            row_n_goal, col_n_goal = goal_positions[number]
            distance += abs(row_n - row_n_goal) + abs(col_n - col_n_goal)
        return distance

# Function to display the puzzle as an image
def display_puzzle(state):
    rows = string_to_list(state)
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.axis('off')
    
    # Create a table for the puzzle
    cell_text = [[f"{item}" for item in row] for row in rows]
    table = ax.table(cellText=cell_text, cellLoc='center', loc='center', colWidths=[0.1] * 3)
    
    # Style the table
    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_fontsize(12)
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#d3d3d3')
        else:
            cell.set_fontsize(14)
            cell.set_facecolor('#ffffff')
    
    # Save the table to an image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    return img

# Streamlit app
st.title("8 Puzzle Solver")

# Input for the initial state
st.write("Enter the initial state of the puzzle:")
input_state = st.text_area("Initial state (use - for empty space)", INITIAL)

# Solve button
if st.button("Solve"):
    try:
        problem = EigthPuzzleProblem(input_state)
        result = astar(problem)

        if not result:
            st.error("No solution found!")
        else:
            st.write("Solution Path:")
            for action, state in result.path():
                st.write(f"Move piece '{action}'")
                img = display_puzzle(state)
                st.image(img, caption=f"State after moving '{action}'")
                st.text(state)
    except Exception as e:
        st.error(f"Error: {e}")

st.write("Algorithm: A* Search")
st.write("Heuristic used: Manhattan Distance")
