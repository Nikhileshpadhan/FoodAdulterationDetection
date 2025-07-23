import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(
    page_title="Food Adulteration webapp",
    page_icon="🧪",
    layout="wide"
)

# --- Model and Encoder Loading ---
@st.cache_resource
def load_assets():
    """Loads all required models and encoders."""
    try:
        adulteration_model = joblib.load('adulteration_model.joblib')
        risk_model = joblib.load('risk_level_model.joblib')
        adulteration_encoder = joblib.load('adulteration_label_encoder.joblib')
        risk_encoder = joblib.load('risk_level_label_encoder.joblib')
        model_features = joblib.load('model_features.joblib')
        return adulteration_model, risk_model, adulteration_encoder, risk_encoder, model_features
    except Exception as e:
        return e, None, None, None, None

# --- Visualization Function ---
def create_risk_gauge(risk_level):
    """Creates a donut chart gauge to visualize the health risk level."""
    risk_map = {
        'Safe': {'value': 1, 'color': '#2ca02c'},  # Green
        'Low Risk': {'value': 2, 'color': '#ff7f0e'}, # Orange
        'Moderate': {'value': 3, 'color': '#d62728'}, # Red
        'Toxic': {'value': 4, 'color': '#8c564b'}   # Brown-Red
    }
    
    # Data for the gauge background
    labels = list(risk_map.keys())
    values = [1] * len(labels) # Equal segments
    colors = [risk_map[label]['color'] for label in labels]
    
    # Get current risk info
    current_risk_info = risk_map.get(risk_level, {'value': 0, 'color': 'grey'})
    
    # Create the plot with a smaller figure size
    fig, ax = plt.subplots(figsize=(3, 3), facecolor='#0e1117') # <-- SIZE REDUCED HERE
    
    # Create the donut chart
    ax.pie(values, colors=colors, startangle=90, counterclock=False,
           wedgeprops=dict(width=0.4, edgecolor='#0e1117'))
           
    # Create a circle for the center to make it a donut
    centre_circle = plt.Circle((0,0), 0.60, fc='#0e1117')
    fig.gca().add_artist(centre_circle)
    
    # Add the risk level text in the middle
    ax.text(0, 0, risk_level, ha='center', va='center', fontsize=22, color=current_risk_info['color'], weight='bold')
    
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    
    return fig

# --- Initialize Session State ---
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Load assets and handle potential errors
assets = load_assets()
if isinstance(assets[0], Exception):
    st.error("🚨 An error occurred while loading the model files.")
    st.error("Please ensure all `.joblib` files are in the correct folder and that you have the necessary libraries (like scikit-learn) installed.")
    st.subheader("Error Details:")
    st.exception(assets[0])
else:
    adulteration_model, risk_model, adulteration_encoder, risk_encoder, model_features = assets

    # --- Main App Interface ---
    st.title("🧪 Welcome to the Food Adulteration Dashboard!")
    st.markdown("This tool uses a machine learning model to help you identify potentially adulterated food samples. Fill out the details below to get an instant analysis.")
    st.markdown("---")

    # --- Create two columns for the input form ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sample Origin & Appearance")
        food_item = st.selectbox("Food Item", ['Milk', 'Rice', 'Wheat', 'Turmeric', 'Chilli Powder', 'Tomato'])
        source_type = st.selectbox("Source Type", ['Farmer', 'Local Market', 'Vendor', 'Self-grown'])
        storage_type = st.selectbox("Storage Type", ['Open', 'Sack', 'Covered', 'Container', 'Loose'])
        color = st.selectbox("Color", ['Normal', 'Faded', 'Too Bright', 'Yellowish', 'Mixed Shades'])
        smell = st.selectbox("Smell", ['Normal', 'Rotten', 'Chemical', 'Strong', 'No Smell'])
        appearance = st.selectbox("Appearance", ['Uniform', 'Clumpy', 'Dusty', 'Layered'])
        
    with col2:
        st.subheader("Physical & Chemical Tests")
        texture = st.selectbox("Texture", ['Smooth', 'Powdery', 'Sticky', 'Gritty', 'Wet', 'Dry'])
        foreign_particles = st.selectbox("Foreign Particles", ['None', 'Stones', 'Seeds', 'Insects', 'Husks'])
        taste = st.selectbox("Taste", ['Bitter', 'Sweet', 'Bland', 'Sharp', 'Not Tested'])
        float_settle_test = st.selectbox("Float or Settle Test", ['Floats', 'Sinks', 'Mixed', 'Foam Appears'])
        dissolves_in_water = st.selectbox("Dissolves in Water", ['Fully Dissolves', 'Leaves Residue', 'Forms Layer'])
        foam_after_mixing = st.selectbox("Foam After Mixing", ['No Foam', 'Slight Foam', 'Excessive Foam'])
        burn_test = st.selectbox("Burn Test Result", ['Melts', 'Plastic Smell', 'Burns Cleanly', 'Leaves Black Residue'])

    # --- Prediction Button ---
    if st.button("Analyze Sample", type="primary", use_container_width=True):
        input_data = {
            'Food_Item': [food_item], 'Source_Type': [source_type], 'Storage_Type': [storage_type],
            'Color': [color], 'Smell': [smell], 'Texture': [texture], 'Foreign_Particles': [foreign_particles],
            'Appearance': [appearance], 'Float_or_Settle_Test': [float_settle_test],
            'Dissolves_in_Water': [dissolves_in_water], 'Foam_After_Mixing': [foam_after_mixing],
            'Burn_Test_Result': [burn_test], 'Taste': [taste]
        }
        input_df = pd.DataFrame(input_data)
        input_encoded = pd.get_dummies(input_df)
        final_input = input_encoded.reindex(columns=model_features, fill_value=0)

        adulteration_pred_encoded = adulteration_model.predict(final_input)
        risk_pred_encoded = risk_model.predict(final_input)

        adulteration_prediction = adulteration_encoder.inverse_transform(adulteration_pred_encoded)[0]
        risk_prediction = risk_encoder.inverse_transform(risk_pred_encoded)[0]
        
        # Store the latest prediction at the top of the history
        st.session_state.prediction_history.insert(0, {
            "Food Item": food_item,
            "Adulteration Status": adulteration_prediction,
            "Predicted Health Risk": risk_prediction,
            "Color": color,
            "Smell": smell,
            "Texture": texture
        })

    # --- Analysis Results Section ---
    st.markdown("---")
    st.header("Analysis Results")
    
    if not st.session_state.prediction_history:
        st.info("Results will be displayed here after you analyze a sample.")
    else:
        # Display the most recent prediction
        latest_prediction = st.session_state.prediction_history[0]
        res_col1, res_col2 = st.columns((1, 1))

        with res_col1:
            st.metric("Adulteration Status", latest_prediction["Adulteration Status"])
            if latest_prediction["Adulteration Status"] == 'Yes':
                st.warning("The model predicts this sample is likely **adulterated**.")
            else:
                st.success("The model predicts this sample is likely **not adulterated**.")
        
        with res_col2:
            st.pyplot(create_risk_gauge(latest_prediction["Predicted Health Risk"]), use_container_width=True)

    # --- Prediction History Dashboard ---
    st.markdown("---")
    st.header("Prediction History")
    if not st.session_state.prediction_history:
        st.write("No samples analyzed yet in this session.")
    else:
        history_df = pd.DataFrame(st.session_state.prediction_history)
        st.dataframe(history_df, use_container_width=True)
