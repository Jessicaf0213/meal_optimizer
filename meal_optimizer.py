import streamlit as st
import itertools
from collections import defaultdict

# Streamlit UI - Parameter Input
st.title("Meal Optimization")
st.sidebar.header("Input Inventory Parameters")

# Inventory parameters input
inventory = {
    'meat': st.sidebar.number_input('Meat', min_value=0, value=0),
    'vegetable': st.sidebar.number_input('Vegetable', min_value=0, value=0),
    'spice': st.sidebar.number_input('Spice', min_value=0, value=0),
    'rice': st.sidebar.number_input('Rice', min_value=0, value=0),
    'fruit': st.sidebar.number_input('Fruit', min_value=0, value=0),
    'deer': st.sidebar.number_input('Deer', min_value=0, value=0),
}

sets_available = st.sidebar.number_input('Sets Available', min_value=0, value=0)

# Ingredient set details
set_contents = {'vegetable':8, 'meat':2, 'spice':4, 'rice':8, 'fruit':2, 'deer':1}

# Dish recipes
dishes = {
    'cold_plate': {'meat':1, 'vegetable':1, 'spice':1},
    'grilled_plate': {'meat':1, 'spice':1, 'rice':1},
    'cherry_plate': {'vegetable':1, 'rice':1, 'fruit':1},
    'pro_plate': {'spice':1, 'fruit':1, 'deer':1}
}

# Rewards thresholds and scores
rewards = {
    'cold_plate': [(1, ('purple_book',3)), (5,('purple_book',5)), (10,('purple_book',8)), (20,('purple_book',20)), (30,('orange_book',8)), (50,('red_book',5))],
    'grilled_plate': [(1, ('metal',25)), (5,('metal',50)), (10,('orange_metal',1)), (20,('orange_metal',2)), (30,('orange_metal',3)), (50,('orange_metal',6))],
    'cherry_plate': [(1, ('hourglass',4)), (5,('hourglass',8)), (10,('hourglass',12)), (20,('hourglass',20)), (30,('gold_brick',50)), (50,('gold_brick',100))],
    'pro_plate': [(1, ('gold_metal',25)), (5,('gold_metal',50)), (10,('gold_metal',80)), (20,('gold_metal',160)), (30,('red_drink',1)), (50,('red_drink',2))]
}

reward_scores = {'purple_book':1, 'orange_book':5, 'red_book':12, 'metal':0.2, 'orange_metal':12,
                 'hourglass':2, 'gold_brick':1, 'gold_metal':0.8, 'red_drink':150}

# Optimization calculation
best_score, best_plan = -1, {}

for opened_sets in range(sets_available+1):
    available = inventory.copy()
    for ing in set_contents:
        available[ing] += set_contents[ing]*opened_sets

    max_dish_counts = {dish: min(available[ing]//amt for ing, amt in recipe.items()) for dish, recipe in dishes.items()}

    for cp in range(max_dish_counts['cold_plate']+1):
        for gp in range(max_dish_counts['grilled_plate']+1):
            for chp in range(max_dish_counts['cherry_plate']+1):
                for pp in range(max_dish_counts['pro_plate']+1):

                    needed = defaultdict(int)
                    for dish, count in zip(['cold_plate','grilled_plate','cherry_plate','pro_plate'], [cp,gp,chp,pp]):
                        for ing, amt in dishes[dish].items():
                            needed[ing] += amt*count

                    if all(available[ing]>=needed[ing] for ing in needed):
                        score = 0
                        dish_made = {'cold_plate':cp, 'grilled_plate':gp, 'cherry_plate':chp, 'pro_plate':pp}
                        reward_got = defaultdict(int)

                        for dish, dish_count in dish_made.items():
                            for threshold, (reward, qty) in sorted(rewards[dish]):
                                if dish_count >= threshold:
                                    reward_got[reward] += qty

                        score += sum(reward_scores[reward]*qty for reward, qty in reward_got.items())

                        unused_points = sum((available[ing]-needed[ing])*0.5 for ing in set_contents)
                        score += unused_points

                        if score > best_score:
                            best_score = score
                            best_plan = {'opened_sets': opened_sets, 'dishes_made': dish_made.copy(), 'rewards':dict(reward_got), 'unused_points':unused_points}

# Display results
st.header("Optimal Results")
st.write("**Best Score:**", best_score)
st.write("**Sets opened:**", best_plan['opened_sets'])
st.write("**Dishes made:**")
for dish, qty in best_plan['dishes_made'].items():
    st.write(f"- {dish}: {qty}")

st.write("**Rewards:**")
for reward, qty in best_plan['rewards'].items():
    st.write(f"- {reward}: {qty}")

st.write("**Unused ingredient points:**", best_plan['unused_points'])
