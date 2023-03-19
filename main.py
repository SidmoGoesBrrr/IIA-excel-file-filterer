import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter


# Define a function to filter the dataframe based on user input
def filter_dataframe(df, choices):
    print(len(choices))
    # filtered_df = df[df['Tags (Semicolon Separated)'].str.contains(choices[0]) & df['Tags (Semicolon Separated)'].str.contains(choices[1])]
    filter_string = ' & '.join([f"df['Tags (Semicolon Separated)'].str.contains('{tag}')" for tag in choices])
    filtered_df = df[eval(filter_string)]
    return filtered_df


# Define the Streamlit app

# Set the title and description of the app
st.title("Excel File Filter IIA")
st.write("This app allows you to filter an Excel file based on multiple the tags extracted from the excel file")

# Create a file uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

# If a file is uploaded, read it into a Pandas dataframe
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, index_col=False)
    all_tags = [tag.strip() for tags in df['Tags (Semicolon Separated)'].str.split(';') for tag in tags]

    # Create a set of unique tags
    unique_tags = set(all_tags)

    # Display a word cloud of the tags

    # Generate the word cloud
    word_could_dict = Counter(unique_tags)
    wordcloud = WordCloud(width=800, height=500, background_color='white', min_font_size=10).generate_from_frequencies(
        word_could_dict)

    wordcloud.to_file("wordcloud.png")

    st.write("Word Cloud of Tags")
    st.image("wordcloud.png")
    # Create a multiselect widget for the user to select multiple choices
    choices = st.multiselect("Select choices", unique_tags)

    # Create a button to filter the dataframe only if all choices are selected
    if len(choices) != 0:
        if st.button("Filter Table"):
            filtered_df = filter_dataframe(df, choices)
            # Display the filtered dataframe with a border
            st.write("Filtered Table:")
            # print all columns of filtered_df
            # print the filtered dataframe

            # create a new dataframe, only displaying the startup bane, registration date, tags and description
            new_df = filtered_df[
                ['\nStart up Name', 'IIA Registration Date', 'Stage', 'Tags (Semicolon Separated)', 'Description']]
            #remove the timestamp

            new_df = new_df.reset_index(drop=True)

            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            st.table(new_df)
            # display the new dataframe

    else:
        st.write("Please select at least one choice to filter the dataframe.")

# Run the app
