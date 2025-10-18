import pandas as pd
import numpy as np
import sys

def shuffle_quiz_dataframe(df):
    """
    Shuffles the questions (rows) and the answers within each question of a DataFrame.
    """
    # Shuffle the order of the questions (rows)
    shuffled_df = df.sample(frac=1).reset_index(drop=True)

    answer_cols = ['Answer 1', 'Answer 2', 'Answer 3', 'Answer 4']

    for index, row in shuffled_df.iterrows():
        # Get the answers and the correct answer index (1-based)
        answers = row[answer_cols].dropna().values
        correct_index_1_based = row['Correct']

        if pd.isna(correct_index_1_based):
            continue

        correct_index_0_based = int(correct_index_1_based) - 1

        if correct_index_0_based < 0 or correct_index_0_based >= len(answers):
            continue

        correct_answer_text = answers[correct_index_0_based]

        # Shuffle the answers
        np.random.shuffle(answers)

        # Find the new 0-based index of the correct answer
        new_correct_index_0_based = np.where(answers == correct_answer_text)[0][0]

        # Convert back to 1-based index
        new_correct_index_1_based = new_correct_index_0_based + 1

        # Clear existing answers before placing shuffled ones
        for col in answer_cols:
            shuffled_df.loc[index, col] = np.nan

        # Update the row with shuffled answers and new correct index
        for i in range(len(answers)):
            shuffled_df.loc[index, f'Answer {i+1}'] = answers[i]

        shuffled_df.loc[index, 'Correct'] = new_correct_index_1_based

    # The 'Correct' column might be float after modification, so cast it to int
    shuffled_df['Correct'] = shuffled_df['Correct'].astype('Int64')

    return shuffled_df

if __name__ == "__main__":
    # Check for command-line arguments, otherwise use defaults
    if len(sys.argv) == 3:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        # Default files for this specific task
        input_filename = "New_Shuffled_Kahoot_Quiz.xlsx"
        output_filename = "Next_Week_Shuffled_Quiz.xlsx"

    try:
        # 1. Read the quiz from an Excel file
        initial_df = pd.read_excel(input_filename)

        # 2. Shuffle the DataFrame
        final_shuffled_df = shuffle_quiz_dataframe(initial_df)

        # 3. Save the final DataFrame to an Excel file
        final_shuffled_df.to_excel(output_filename, index=False)

        print(f"Successfully re-shuffled the quiz from '{input_filename}' and saved it to '{output_filename}'")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
