import streamlit as st
import itertools

st.title('Dish and Ingredients Optimizer')

st.sidebar.header("🍲 Inventory Input")
# User input inventory
meat = st.sidebar.number_input('Meat', min_value=0, value=0)
vegetable = st.sidebar.number_input('Vegetable', min_value=0, value=0)
spice = st.sidebar.number_input('Spice', min_value=0, value=0)
rice = st.sidebar.number_input('Rice', min_value=0, value=0)
fruit = st.sidebar.number_input('Fruit', min_value=0, value=0)
deer = st.sidebar.number_input('Deer', min_value=0, value=0)
sets_available = st.sidebar.number_input('Ingredient Sets Available', min_value=0, value=0)

inventory = {
    'meat': meat,
    'vegetable': vegetable,
    'spice': spice,
    'rice': rice,
    'fruit': fruit,
    'deer': deer
}

# Rewards and recipes
dish_recipes = {
    'cold_plate': {'meat':1, 'vegetable':1, 'spice':1},
    'grilled_plate': {'meat':1, 'spice':1, 'rice':1},
    'cherry_plate': {'vegetable':1, 'rice':1, 'fruit':1},
    'pro_plate': {'spice':1, 'fruit':1, 'deer':1}
}

dish_rewards = {
    'cold_plate': [(1, ('purple_book',3)), (5, ('purple_book',5)), (10, ('purple_book',8)),
                   (20, ('purple_book',20)), (30, ('orange_book',8)), (50, ('red_book',5))],
    'grilled_plate': [(1, ('metal',25)), (5, ('metal',50)), (10, ('orange_metal',1)),
                      (20, ('orange_metal',2)), (30, ('orange_metal',3)), (50, ('orange_metal',6))],
    'cherry_plate': [(1, ('hourglass',4)), (5, ('hourglass',8)), (10, ('hourglass',12)),
                     (20, ('hourglass',20)), (30, ('gold_brick',50)), (50, ('gold_brick',100))],
    'pro_plate': [(1, ('gold_metal',25)), (5, ('gold_metal',50)), (10, ('gold_metal',80)),
                  (20, ('gold_metal',160)), (30, ('gold_metal',0)), (50, ('gold_metal',0))]
}

ingredient_points = 0.5

ingredient_per_set = {
    'meat': 1,
    'vegetable': 1,
    'spice': 1,
    'rice': 1,
    'fruit': 1,
    'deer': 1
}

# Ingredient selection per set (assuming freedom to choose based on user strategy)
ingredient_choices = {
    'meat': 0,
    'vegetable': 8,
    'spice': 4,
    'rice': 8,
    'fruit': 2,
    'deer': 1
}

st.title("🍽️ Dish Optimization Calculator")

if st.button('Calculate Optimal Strategy'):
    max_score = -1
    best_result = None
    
    # Explore different set opening scenarios (limited for computational ease)
    # Here, we assume a simple heuristic of opening all sets optimally:
    opened_ingredients = {key: inventory[key] + ingredient_per_set[key]*sets_available for key in inventory}

    # Possible numbers of dishes to make
    dish_range = range(0, 51)  # reasonable upper bound

    for cold in dish_range:
        for grilled in range(0,51):
            for cherry in range(0,51):
                for pro in range(0,51):
                    required = {'meat':0,'vegetable':0,'spice':0,'rice':0,'fruit':0,'deer':0}

                    # Calculate required ingredients
                    for dish, count in [('cold_plate', cold), ('grilled_plate', grilled), 
                                        ('cherry_plate', cherry), ('pro_plate', pro)]:
                        for ing, qty in dish_recipes[dish].items():
                            required[ing] += qty * count
                    
                    # Compute if ingredients are enough considering sets
                    total_needed_sets = {ing:max(0, required[ing] - inventory[ing]) for ing in inventory}
                    sets_used = sum(total_needed_sets[ing]//ingredient_per_set[ing] + (1 if total_needed_sets[ing]%ingredient_per_set[ing]>0 else 0) for ing in inventory)

                    if sets_used > sets_available:
                        continue  # Skip impossible scenarios

                    leftover_ingredients = {ing: inventory[ing] + sets_available - required[ing] for ing in inventory}
                    leftover_points = sum(qty * ingredient_per_set[ing] * ingredient_per_set[ing] * ingredient_per_set[ing] * ingredient_points 
                                          for ing, qty in inventory.items())

                    # Calculate reward points
                    dishes_made = {'cold_plate':cold, 'grilled_plate':grilled, 'cherry_plate':cherry, 'pro_plate':pro}
                    rewards = {}
                    score = 0
                    for dish, reward_tiers in dish_recipes.items():
                        qty = dishes_made[dish]
                        dish_reward_points = 0
                        for tier, (reward_name, reward_score) in sorted(dish_recipes[dish]):
                            if qty >= tier:
                                rewards[reward_name] = rewards.get(reward_name,0) + reward_qty
                                dish_score = {'purple_book':1,'orange_book':5,'red_book':12,'metal':0.2,'orange_metal':12,
                                              'hourglass':2,'gold_brick':1,'gold_metal':1}[reward_name]
                                dish_score *= reward_qty
                                score += dish_score

                    total_score = score + leftover_points
                    if total_needed_sets and sets_used <= sets_available and score > max_score:
                        max_score = dish_score
                        best_result = {'score': dish_score, 'dishes': dishes_made, 'rewards': rewards,
                                       'sets_used':sets_used}

    if best_result:
        st.success(f"✅ **Optimal Score:** {max_score}")
        st.write("### 🍽️ **Dishes Made:**")
        st.json(best_result['dishes'])
        st.write("### 🎁 **Rewards Achieved:**")
        st.json(best_result['rewards'])
        st.write(f"📦 **Sets opened:** {best_result['sets_used']}")
        st.write(f"💡 **Unused ingredients each give:** {ingredient_per_set} x {ingredient_points} points")

    else:
        st.warning("No optimal combination found. Try adjusting your inventory or sets.")

