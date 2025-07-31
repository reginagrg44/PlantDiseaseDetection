# Integration Instructions for View History Feature

## Files Created:
1. `history_database.py` - Database operations for prediction history
2. `history_view.py` - Streamlit UI components for viewing history

## Integration Steps:

### Step 1: Add Import Statements
Add these imports at the top of your main file (after your existing imports):

```python
from history_view import view_history_page, save_prediction_to_history
```

### Step 2: Add "View History" to Navigation Menu
Find this line in your `app()` function:
```python
page = st.sidebar.selectbox("Select a page", ["Home", "Disease Prediction", "Disease Cure", "Crop Recommendation", "About", "Logout"])
```

Replace it with:
```python
page = st.sidebar.selectbox("Select a page", ["Home", "Disease Prediction", "Disease Cure", "Crop Recommendation", "View History", "About", "Logout"])
```

### Step 3: Add History Page Handler
In your `app()` function, after the "Crop Recommendation" section and before the "About" section, add:

```python
    # --- View History Page ---
    elif page == "View History":
        view_history_page()
```

### Step 4: Modify Disease Prediction Section to Save History
Replace your entire "Disease Prediction" section with this enhanced version:

```python
    # --- Disease Prediction Page ---
    elif page == "Disease Prediction":
        st.header(" Upload Leaf Image")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

        if uploaded_file:
            image = Image.open(uploaded_file)

            if st.button("Show Image"):
                st.image(image, caption="Uploaded Image", use_column_width=True)

            image_array = preprocess_image(image)

            leaf_check = predict_leaf_or_not(image_array)
            if leaf_check == "leaf":
                disease, confidence = predict_disease(image_array)
                st.success(f"✅ Predicted Disease: **{disease}**")
                st.info(f"📊 Confidence Score: **{confidence:.2f}%**")
                
                # Save to history
                current_username = st.session_state.get('username', 'unknown')
                cure_info = disease_cures.get(disease, "No cure information available")
                save_prediction_to_history(
                    username=current_username,
                    image_name=uploaded_file.name,
                    prediction_type="Disease Detection",
                    predicted_disease=disease,
                    confidence_score=confidence,
                    is_leaf=True,
                    cure_info=cure_info
                )
                st.success("🔄 Prediction saved to history!")
                
            else:
                st.error("❌ This image is not recognized as a leaf. Please try again.")
                
                # Save non-leaf detection to history too
                current_username = st.session_state.get('username', 'unknown')
                save_prediction_to_history(
                    username=current_username,
                    image_name=uploaded_file.name,
                    prediction_type="Leaf Detection",
                    predicted_disease=None,
                    confidence_score=None,
                    is_leaf=False,
                    cure_info=None
                )
```

### Step 5: Modify Disease Cure Section to Save History (Optional)
If you want to track when users look up cures, replace your "Disease Cure" section with:

```python
    # --- Disease Cure Page ---
    elif page == "Disease Cure":
        st.header(" Get Cure for Plant Disease")
        st.markdown("Enter the disease name **exactly** as predicted (e.g., `Tomato___Early_blight`)")

        input_disease = st.text_input("Enter Disease Name")

        if st.button("Get Cure"):
            cure = disease_cures.get(input_disease.strip())
            if cure:
                st.success(f"Cure for **{input_disease}**:")
                st.write(cure)
                
                # Save cure lookup to history
                current_username = st.session_state.get('username', 'unknown')
                save_prediction_to_history(
                    username=current_username,
                    image_name="Manual Lookup",
                    prediction_type="Cure Lookup",
                    predicted_disease=input_disease.strip(),
                    confidence_score=None,
                    is_leaf=None,
                    cure_info=cure
                )
                
            else:
                st.warning("❗ Cure not found. Please check the spelling or try a different disease name.")
```

## Complete Files Summary:

### Files you need to have:
1. **Your original main file** (with the modifications above)
2. **history_database.py** (database operations)
3. **history_view.py** (UI components)

### Database Files Created Automatically:
- `prediction_history.db` - SQLite database file (created automatically)
- `users.db` - Your existing user database

## Features Included:

### 📋 My History Tab:
- View all predictions with date/time stamps
- Filter by number of records (10, 25, 50, 100, All)
- Delete individual records
- Clear all history with confirmation
- Refresh history

### 📈 Statistics Tab:
- Total predictions count
- Leaf vs non-leaf image counts  
- Average confidence score
- Visual charts showing distribution
- Recent activity timeline

### 🔍 Search Tab:
- Search by disease name or image filename
- Real-time search results
- Filtered view of matching records

### Database Features:
- Automatic table creation
- User-specific history tracking
- Timestamped records
- Safe deletion operations
- Search capabilities
- Statistics generation

## How to Test:
1. Copy the two new files (`history_database.py` and `history_view.py`) to your project folder
2. Add the import statement to your main file
3. Make the modifications shown above
4. Run your application
5. Log in and make some predictions
6. Check the "View History" page to see your saved predictions

The history will automatically start saving once you make these changes!