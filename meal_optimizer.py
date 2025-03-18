import streamlit as st
from collections import defaultdict

# Inventory input
inventory = {
    'meat': st.sidebar.number_input('Meat', min_value=0, value=0),
    'vegetable': st.sidebar.number_input('Vegetable', min_value=0, value=0),
    'spice': st.sidebar.number_input('Spice', min_value=0, value=0),
    'rice': st.sidebar.number_input('Rice', min_value=0, value=0),
    'fruit': st.sidebar.number_input('Fruit', min_value=0, value=0),
    'deer': st.sidebar.number_input('Deer', min_value=0, value=0)
}

sets_available = st.sidebar.number_input('Sets Available', min_value=0, value=0)

# Ingredient set details
set_contents = {'vegetable':8, 'meat':2, 'spice':4, 'rice':8, 'fruit':2, 'deer':1}

# Dish recipes
dishes = {
    'cold_plate': {'vegetable':1, 'meat':1, 'spice':1},
    'grilled_plate': {'meat':1, 'spice':1, 'rice':1},
    'cherry_plate': {'vegetable':1, 'rice':1, 'fruit':1},
    'pro_plate': {'spice':1, 'fruit':1, 'deer':1}
}

# Rewards thresholds and scores
rewards = {
    'cold_plate': [(1, ('purple_book',3)), (5,('purple_book',20))],
    'grilled_plate': [(1, ('metal',25)), (5,('metal',50))],
    'cherry_plate': [(1, ('hourglass',4)), (5,('hourglass',8))],
    'pro_plate': [(1, ('gold_metal',25)), (5,('gold_metal',50))]
}

reward_scores = {'purple_book':1, 'metal':0.2, 'hourglass':2}

# Optimize best decision
best_score, best_plan = -1, {}

for dish, recipe in dishes.items():
    max_possible = min(inventory[ing] // amt for ing, amt in recipe.items())
    needed = defaultdict(int)
    for ing, amt in recipe.items():
        needed[ing] = amt * max_possible

    score = 0
    reward_got = defaultdict(int)

    for threshold, (reward, qty) in sorted(rewards[dish]):
        if max_possible >= threshold:
            reward_got = (reward, qty)
            score = qty

    if score > best_score:
        best_score = score
        best_plan = {'dish': dish, 'quantity': max_possible, 'reward': reward_got}

# Display results
st.write("### Optimal Decision")
st.write(f"Dish to prepare: **{best_plan['dish']}**")
st.write(f"Quantity: {best_plan['quantity']}")
st.write(f"Reward: {best_plan['reward'][1]} {best_plan['reward'][0]}")
