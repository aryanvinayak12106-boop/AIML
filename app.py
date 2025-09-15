import streamlit as st
import requests
import json

st.set_page_config(page_title="Dish → Ingredients → Shopping List", page_icon="🍽️", layout="wide")

# --- Title
st.title("🔍 Dish → Ingredients → Shopping List")
st.write("Type a dish name, fetch ingredients (via TheMealDB), and turn them into a clean shopping list.")

# --- Sidebar for scaling servings
st.sidebar.header("Settings")
servings = st.sidebar.number_input("Servings (scale measures)", min_value=1, value=1, step=1)
default_servings = st.sidebar.number_input("Recipe's default servings (if known)", min_value=1, value=1, step=1)

scale_factor = servings / default_servings
st.sidebar.write(f"Scale factor: **{scale_factor:.2f}x**")

# --- Dish Input
dish_name = st.text_input("Dish name", placeholder="e.g. Chicken Biryani")

if st.button("🔍 Get Ingredients"):
    if dish_name.strip() == "":
        st.warning("Please enter a dish name.")
    else:
        # Call TheMealDB API
        response = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={dish_name}")
        data = response.json()

        if not data or not data["meals"]:
            st.error("No results from TheMealDB. Try a different name or spelling.")
        else:
            meal = data["meals"][0]
            st.subheader(f"🍛 Ingredients for {meal['strMeal']}")

            ingredients = []
            for i in range(1, 21):
                ing = meal.get(f"strIngredient{i}")
                meas = meal.get(f"strMeasure{i}")
                if ing and ing.strip():
                    ingredients.append(f"{meas} {ing}".strip())

            # Scale the ingredients
            scaled_ingredients = [f"{item} × {scale_factor:.2f}" for item in ingredients]

            # Show ingredients
            st.write("### 📝 Shopping List")
            for item in scaled_ingredients:
                st.write(f"- {item}")

            # Export option
            if st.button("📥 Export Shopping List"):
                filename = f"{meal['strMeal']}_shopping_list.txt"
                with open(filename, "w") as f:
                    f.write("\n".join(scaled_ingredients))
                with open(filename, "rb") as f:
                    st.download_button("Download File", f, file_name=filename)

# Optional manual item adding
st.write("---")
st.subheader("🖊️ Add Custom Items (Optional)")
manual_item = st.text_input("Custom Item")
if st.button("Add to List"):
    st.write(f"Added: {manual_item}")
