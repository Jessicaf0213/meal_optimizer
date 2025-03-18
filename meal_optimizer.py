import streamlit as st

# Define optimization function (your logic)
def optimize(params):
    # Add your earlier optimization logic here
    return {
        'best_score': 123,
        'opened_sets': 5,
        'dishes_made': {'cold_plate':1, 'grilled_plate':2},
        'rewards': {'purple_book':3, 'metal':50},
        'unused_points': 12.5
    }

st.title("Dish Optimization Calculator")

with st.form("inventory_form"):
    meat = st.number_input("Meat", min_value=0, value=0)
    vegetable = st.number_input("Vegetable", min_value=0, value=0)
    spice = st.number_input("Spice", min_value=0, value=0)
    rice = st.number_input("Rice", min_value=0, value=0)
    fruit = st.number_input("Fruit", min_value=0, value=0)
    deer = st.number_input("Deer", min_value=0, value=0)
    cold_plate = st.number_input("Cold Plate", min_value=0, value=0)
    grilled_plate = st.number_input("Grilled Plate", min_value=0, value=0)
    cherry_plate = st.number_input("Cherry Plate", min_value=0, value=0)
    pro_plate = st.number_input("Pro Plate", min_value=0, value=0)
    sets_available = st.number_input("Ingredient Sets Available", min_value=0, value=0)

    submitted = st.form_submit_button("Optimize")

    if submitted:
        params = {
            'meat': meat,
            'vegetable': vegetable,
            'spice': spice,
            'rice': rice,
            'fruit': fruit,
            'deer': deer,
            'cold_plate': cold_plate,
            'grilled_plate': grilled_plate,
            'cherry_plate': cherry_plate,
            'pro_plate': pro_plate,
            'sets_available': sets_available
        }
        result = optimize(params)

        st.subheader("Best Optimization Result")
        st.write(f"**Best Score:** {result['best_score']}")
        st.write(f"**Sets Opened:** {result['opened_sets']}")
        st.write("**Dishes Made:**")
        st.json(result['dishes_made'])
        st.write("**Rewards:**")
        st.json(result['rewards'])
        st.write(f"**Unused Ingredient Points:** {result['unused_points']}")

