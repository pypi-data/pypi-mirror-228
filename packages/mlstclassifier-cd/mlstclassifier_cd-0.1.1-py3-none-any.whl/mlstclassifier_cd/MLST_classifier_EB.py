#!/usr/bin/env python3

import pandas as pd
import sys
import joblib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Number of argument must be 3")
        print("Usage: MLSTclassifier_cd input_path output_path")
        sys.exit(1)

    # Extract the command-line arguments
    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]

    # Read the input CSV file
    try:
        df = pd.read_csv(input_csv_file)
    except FileNotFoundError:
        print("Error: Input CSV file not found.")
        sys.exit(1)

    # Load the pre-trained model
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_directory, "finalized_KNN_model.sav")
        model = joblib.load(model_path)
    except FileNotFoundError:
        print("Error: Model file not found.")
        sys.exit(1)

    # Extract features (X) from the DataFrame and make predictions
    X = df[['adk', 'atpA', 'dxr', 'glyA', 'recA', 'sodA', 'tpi']]   # Extract columns corresponding to the 7 genes as features 'X'
    df['predicted_clade'] = model.predict(X)   # Make predictions using the pre-trained model and add them as a new column 'predicted_clade' in the DataFrame 'df'
    
    output_dir = os.path.dirname(output_csv_file)
    with open(os.path.join(output_dir, "stat.txt"), "w") as f:
        f.write("Total number of sample: {}\n".format(df.shape[0]))
        f.write("Counts of predicted classes:\n")
        f.write(str(df['predicted_clade'].value_counts()))

    # Create a pie chart with the value counts
    fig = make_subplots(1, 1, specs=[[{"type": "pie"}]])
    fig.add_trace(
        go.Pie(
            labels=df['predicted_clade'].value_counts().index,
            values=df['predicted_clade'].value_counts().values,
            textinfo="label+percent",
            showlegend=False,
        ),
        row=1, col=1
    )

    fig.update_layout(title_text="Predicted Clade Distribution")

    # Save the pie chart as an HTML file
    fig.write_html(os.path.join(output_dir, "pie_chart.html"))
    
    # Write the DataFrame with the added column of predictions to the output CSV file
    try:
        with open(output_csv_file, 'w') as f:   # Open the output CSV file
            df.to_csv(f, index=False)   # Write the DataFrame 'df' to the CSV file 'f', excluding the index column
    except PermissionError:
        print("Error: Unable to write to output CSV file.")
        sys.exit(1)

if __name__ == "__main__":
    main()   # Call the main function if the script is run as the main program (not imported as a module)


