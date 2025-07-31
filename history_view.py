import streamlit as st
import pandas as pd
from history_database import HistoryDatabase, format_history_record

# Initialize history database
history_db = HistoryDatabase()

def view_history_page():
    """View History page for the Streamlit app"""
    st.header("📊 Prediction History")
    
    # Get current username from session state
    current_username = st.session_state.get('username', '')
    
    if not current_username:
        st.error("❌ Please log in to view your history.")
        return
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 My History", "📈 Statistics", "🔍 Search"])
    
    with tab1:
        st.subheader(f"Prediction History for {current_username}")
        
        # Options for viewing history
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            limit_records = st.selectbox(
                "Records to show:", 
                ["All", "10", "25", "50", "100"],
                index=1
            )
        
        with col2:
            if st.button("🔄 Refresh History"):
                st.rerun()
        
        with col3:
            if st.button("🗑️ Clear All History"):
                if st.session_state.get('confirm_delete', False):
                    history_db.delete_user_history(current_username)
                    st.success("✅ History cleared successfully!")
                    st.session_state.confirm_delete = False
                    st.rerun()
                else:
                    st.session_state.confirm_delete = True
                    st.warning("⚠️ Click again to confirm deletion")
        
        # Get user history
        limit = None if limit_records == "All" else int(limit_records)
        history_records = history_db.get_user_history(current_username, limit)
        
        if history_records:
            # Convert to DataFrame for better display
            df_data = []
            for record in history_records:
                formatted_record = format_history_record(record)
                df_data.append({
                    'Date & Time': formatted_record['timestamp'],
                    'Image Name': formatted_record['image_name'],
                    'Type': formatted_record['prediction_type'],
                    'Disease': formatted_record['predicted_disease'] or 'N/A',
                    'Confidence': f"{formatted_record['confidence_score']:.2f}%" if formatted_record['confidence_score'] else 'N/A',
                    'Is Leaf': '✅ Yes' if formatted_record['is_leaf'] else '❌ No',
                    'ID': formatted_record['id']
                })
            
            df = pd.DataFrame(df_data)
            
            # Display the dataframe
            st.dataframe(
                df.drop('ID', axis=1),  # Hide ID column from display
                use_container_width=True,
                hide_index=True
            )
            
            # Option to delete individual records
            st.subheader("🗑️ Delete Individual Records")
            record_to_delete = st.selectbox(
                "Select record to delete:",
                options=[f"ID {row['ID']}: {row['Image Name']} - {row['Date & Time']}" for row in df_data],
                format_func=lambda x: x,
                index=None,
                placeholder="Choose a record to delete..."
            )
            
            if record_to_delete and st.button("Delete Selected Record"):
                record_id = int(record_to_delete.split(':')[0].replace('ID ', ''))
                history_db.delete_record_by_id(record_id)
                st.success("✅ Record deleted successfully!")
                st.rerun()
        
        else:
            st.info("📝 No prediction history found. Start making predictions to see your history here!")
    
    with tab2:
        st.subheader("📈 Your Prediction Statistics")
        
        # Get statistics
        stats = history_db.get_history_stats(current_username)
        
        if stats and stats[0] > 0:
            total_predictions, leaf_predictions, non_leaf_predictions, avg_confidence = stats
            
            # Display stats in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Predictions", total_predictions)
            
            with col2:
                st.metric("Leaf Images", leaf_predictions or 0)
            
            with col3:
                st.metric("Non-Leaf Images", non_leaf_predictions or 0)
            
            with col4:
                avg_conf = avg_confidence if avg_confidence else 0
                st.metric("Avg Confidence", f"{avg_conf:.2f}%")
            
            # Create charts
            if leaf_predictions or non_leaf_predictions:
                # Pie chart for leaf vs non-leaf
                chart_data = pd.DataFrame({
                    'Type': ['Leaf Images', 'Non-Leaf Images'],
                    'Count': [leaf_predictions or 0, non_leaf_predictions or 0]
                })
                
                st.subheader("📊 Image Type Distribution")
                st.bar_chart(chart_data.set_index('Type'))
            
            # Recent activity
            st.subheader("🕐 Recent Activity (Last 7 predictions)")
            recent_records = history_db.get_user_history(current_username, 7)
            
            if recent_records:
                activity_data = []
                for record in recent_records:
                    formatted_record = format_history_record(record)
                    activity_data.append({
                        'Date': formatted_record['timestamp'].split(' ')[0],
                        'Time': formatted_record['timestamp'].split(' ')[1],
                        'Disease': formatted_record['predicted_disease'] or 'Non-leaf',
                        'Confidence': f"{formatted_record['confidence_score']:.1f}%" if formatted_record['confidence_score'] else 'N/A'
                    })
                
                activity_df = pd.DataFrame(activity_data)
                st.dataframe(activity_df, use_container_width=True, hide_index=True)
        
        else:
            st.info("📊 No statistics available yet. Make some predictions to see your stats!")
    
    with tab3:
        st.subheader("🔍 Search Your History")
        
        search_term = st.text_input(
            "Search by disease name or image name:",
            placeholder="e.g., Tomato, Apple_scab, my_plant.jpg"
        )
        
        if search_term:
            search_results = history_db.search_history(current_username, search_term)
            
            if search_results:
                st.success(f"Found {len(search_results)} matching records:")
                
                search_data = []
                for record in search_results:
                    formatted_record = format_history_record(record)
                    search_data.append({
                        'Date & Time': formatted_record['timestamp'],
                        'Image Name': formatted_record['image_name'],
                        'Disease': formatted_record['predicted_disease'] or 'N/A',
                        'Confidence': f"{formatted_record['confidence_score']:.2f}%" if formatted_record['confidence_score'] else 'N/A',
                        'Is Leaf': '✅ Yes' if formatted_record['is_leaf'] else '❌ No'
                    })
                
                search_df = pd.DataFrame(search_data)
                st.dataframe(search_df, use_container_width=True, hide_index=True)
            
            else:
                st.info("🔍 No matching records found. Try a different search term.")

def save_prediction_to_history(username, image_name, prediction_type, predicted_disease=None, 
                              confidence_score=None, is_leaf=None, cure_info=None):
    """Helper function to save prediction to history database"""
    try:
        history_db.add_prediction_record(
            username=username,
            image_name=image_name,
            prediction_type=prediction_type,
            predicted_disease=predicted_disease,
            confidence_score=confidence_score,
            is_leaf=is_leaf,
            cure_info=cure_info
        )
        return True
    except Exception as e:
        st.error(f"Error saving to history: {str(e)}")
        return False