def show_dataframe_with_priority(df, *data_lists):
    count_dict = count_priority(*data_lists)

    df = df.copy()  # Ensure we don't modify the original DataFrame
    df["Priority"] = ""  # Default priority label

    for index, value in count_dict.items():
        df.at[index, "Priority"] = "✅" * value  # Repeats '✅ Prior' based on value

        # Function to highlight priority rows

    def highlight_rows(row):
        if row.name in count_dict:
            return ['background-color: #fffa9b; color: black; font-weight: bold;'] * len(row)  # Gold for main priority

        return [''] * len(row)

    # Apply styling and display DataFrame
    st.write("### Data with Priority Labels")
    st.dataframe(df.style.apply(highlight_rows, axis=1), use_container_width=True)
