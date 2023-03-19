import streamlit as st
import pandas as pd

# Define a function to filter the dataframe based on user input
def filter_dataframe(df, choices):
    filtered_df = df[df['Tags (Semicolon Separated)'].str.contains(choices[0]) & df['Tags (Semicolon Separated)'].str.contains(choices[1])]

    return filtered_df

# Define the Streamlit app
def main():
    # Set the title and description of the app
    st.title("Excel File Filter IIA")
    st.write("This app allows you to filter an Excel file based on multiple the tags extracted from the excel file")

    # Create a file uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    # If a file is uploaded, read it into a Pandas dataframe
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        all_tags = [tag.strip() for tags in df['Tags (Semicolon Separated)'].str.split(';') for tag in tags]

        # Create a set of unique tags
        unique_tags = set(all_tags)

        print(list(unique_tags))
        # Display the dataframe
        st.write("Original Dataframe:")
        st.write(df)

        # Create a multiselect widget for the user to select multiple choices
        choices = st.multiselect("Select choices", unique_tags)

        # Create a button to filter the dataframe only if all choices are selected
        if len(choices) != 0:
            if st.button("Filter Dataframe"):
                filtered_df = filter_dataframe(df, choices)
                #Display the filtered dataframe with a border
                st.write("Filtered Dataframe:")
                st.write(filtered_df.style.set_table_styles([{'selector': 'th',
                                                                'props': [('border', '1px solid black')]}]))
        else:
            st.write("Please select at least one choice to filter the dataframe.")

# Run the app
if __name__ == '__main__':
    main()
