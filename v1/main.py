import json
import streamlit as st
import pandas as pd
from tasks import sector_analyze, sector_filter, technology_finder, project_complexity_finder, service_category_finder, \
    email_priority_finder, location_priority_finder, analyze_motive, company_type_finder, urgency_pricing_finder
import agents
from crewai import Crew


def category_selection():
    st.title("Select a Category")

    options = [
        "E-commerce & Retail",
        "Healthcare & Fitness",
        "Technology & Software",
        "Education & Training",
        "Other"
    ]

    selected_options = st.multiselect("Choose one or more categories:", options)

    # Country selector added here
    country_options = ["USA", "Canada", "UK", "Germany", "India", "Australia"]
    selected_country = st.multiselect("Select your country:", country_options)

    if st.button("Next") and selected_options:
        st.session_state.page = "upload"
        st.session_state.selected_sectors = selected_options  # Store selected sectors
        st.session_state.selected_country = selected_country  # Store selected country
        st.rerun()


def motive_checker(query):
    task = analyze_motive(query)  # Pass selected sectors
    tech_crew = Crew(agents=[agents.motive_agent], tasks=[task])
    model_result = tech_crew.kickoff()

    if model_result:
        return model_result.raw
    return None


def sector_queries(query, selected_sectors):
    print(f"Processing query: {query} with sectors: {selected_sectors}")

    task = sector_analyze(query, selected_sectors)  # Pass selected sectors
    tech_crew = Crew(agents=[agents.sector_agent], tasks=[task])
    model_result = tech_crew.kickoff()

    if model_result:
        st.session_state.sector_list.append(model_result.raw)
        print(f"Sector analysis result: {model_result.raw}")
        return model_result.raw
    return None


def response_checker(query, selected_sector):
    task = sector_filter(query, selected_sector)
    tech_crew = Crew(agents=[agents.sector_filter_agent], tasks=[task])

    model_result = tech_crew.kickoff()

    if model_result:
        return model_result.raw
    return None


def tech_finder(query, category):
    task = technology_finder(query, category)
    tech_crew = Crew(agents=[agents.technology_finder_agent], tasks=[task])

    model_result = tech_crew.kickoff()

    if model_result:
        print(f"Tech: {model_result.raw}")
        return model_result.raw
    return None


def complex_finder(query, resource, technology):
    task = project_complexity_finder(query, resource, technology)
    tech_crew = Crew(agents=[agents.project_complexity_agent], tasks=[task])
    model_result = tech_crew.kickoff()

    if model_result:
        print(f"Complexity: {model_result.raw}")
        return model_result.raw
    return None


def cate_finder(query):
    task = service_category_finder(query)
    tech_crew = Crew(agents=[agents.service_category_finder_agent], tasks=[task])
    tech_crew.tasks = [task]
    model_result = tech_crew.kickoff()

    if model_result:
        print(f"Category: {model_result.raw}")
        return model_result.raw
    return None


def email_sort(email):
    task = email_priority_finder(email)
    tech_crew = Crew(agents=[agents.email_priority_agent], tasks=[task])
    model_result = tech_crew.kickoff()

    if model_result:
        print(f"Email : {model_result.raw}")
        return model_result.raw
    return None


def location_sort(country, location):
    task = location_priority_finder(country, location)
    tech_crew = Crew(agents=[agents.country_priority_agent], tasks=[task])
    model_result = tech_crew.kickoff()

    if model_result:
        print(f"Location: {model_result.raw}")
        return model_result.raw
    return None


def urgency_finder(query):
    task = urgency_pricing_finder(query)
    tech_crew = Crew(agents=[agents.urgency_pricing_agent], tasks=[task])
    tech_crew.tasks = [task]
    model_result = tech_crew.kickoff()

    if model_result:
        print(f"Urgency: {model_result.raw}")
        return model_result.raw
    return None


def company_size_finder(query):
    task = company_type_finder(query)
    tech_crew = Crew(agents=[agents.provider_type_agent], tasks=[task])
    model_result = tech_crew.kickoff()

    if model_result:
        print(f"Company Type: {model_result.raw}")
        return model_result.raw
    return None


def upload_excel():
    st.title("Upload Excel File")
    st.write(f"**Selected Categories:** {', '.join(st.session_state.selected_sectors)}")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    email_priority_list = []
    country_priority_list = []
    sector_priority_list = []
    urgency_priority_list = []
    motive_priority_list = []

    message_colum = 'message'
    email_colum = 'email'
    country_colum = 'country'

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file).head(10)
            # df = pd.read_excel(uploaded_file)
            data_dict = {}
            # df["Status"] = "Qualified"

            for index, row in df.iterrows():
                query = row[message_colum] if message_colum in row else ''
                priority_index = 0
                if query:
                    motive_of_query = motive_checker(query)

                    if 'False' in motive_of_query:
                        # motive_priority_list.append(index)
                        add_df_data(df, 'Status', index, 'UnQualified')
                        continue
                    else:
                        add_df_data(df, 'Status', index, 'Qualified')

                    sector_result = sector_queries(query, st.session_state.selected_sectors)

                    if sector_result:
                        sector = response_checker(sector_result, st.session_state.selected_sectors)

                        if 'False' in sector:
                            sector_priority_list.append(index)
                        else:
                            priority_index += 1

                        category = cate_finder(query)
                        add_df_data(df, 'Industry', index, category)

                        technology = tech_finder(query, category)
                        add_df_data(df, 'Technology', index, technology)

                        complexity = complex_finder(query, category, technology)

                        email = row[email_colum] if email_colum in row else ''
                        country = row[country_colum] if country_colum in row else ''

                        country_priority = location_sort(country, st.session_state.selected_country)

                        if 'Prior' in country_priority:
                            priority_index += 1
                            country_priority_list.append(index)

                        email_priority = email_sort(email)
                        if 'Prior' in email_priority:
                            priority_index += 1
                            email_priority_list.append(index)

                        urgency = urgency_finder(query)
                        if 'High' in urgency:
                            priority_index += 1
                            urgency_priority_list.append(index)

                        company_size = company_size_finder(query)
                        add_df_data(df, 'Company Type', index, company_size)

                        if priority_index == 4:
                            add_df_data(df, 'Priority', index, 'High')
                        elif priority_index == 3:
                            add_df_data(df, 'Priority', index, 'Medium')
                        else:
                            add_df_data(df, 'Priority', index, 'Low')

                        current_data = {
                            'query': query,
                            'Motive': motive_of_query,
                            'sector_analysis': sector_result,
                            'sector': sector,
                            'Query': query,
                            'Category': category,
                            'Tech': technology,
                            'Complexity': complexity,
                            'Company_size': company_size,
                            'Urgency': urgency
                        }

                        data_dict[index] = current_data

                        st.write(current_data)

            # # st.write(data_dict)
            st.dataframe(df, use_container_width=True)

            with open('data_dict.json', 'w') as file:
                json.dump(data_dict, file, indent=4)

            # st.write(data_dict)
            st.success("✅ Results saved to 'data_llam.json'")

        except Exception as e:
            st.error(f"⚠️ Error reading the file: {str(e)}")


def add_df_data(dataframe, column_name, index, value):
    if column_name not in dataframe.columns:
        dataframe[column_name] = None  # Initialize with None if the column does not exist

    dataframe.at[index, column_name] = value  # Set the value at the given index

    return dataframe


def count_priority(*data_lists):
    data_dict = {}
    for data_list in data_lists:
        for data in data_list:
            if data in data_dict:
                data_dict[data] += 1
            else:
                data_dict[data] = 1
    return data_dict

## we only used if we need some extra UI color in table
# def show_dataframe_with_priority(df, *data_lists):
#     count_dict = count_priority(*data_lists)
#
#     df = df.copy()  # Ensure we don't modify the original DataFrame
#     df["Priority"] = ""  # Default priority label
#
#     for index, value in count_dict.items():
#         df.at[index, "Priority"] = "✅" * value  # Repeats '✅ Prior' based on value
#
#         # Function to highlight priority rows
#
#     def highlight_rows(row):
#         if row.name in count_dict:
#             return ['background-color: #fffa9b; color: black; font-weight: bold;'] * len(row)  # Gold for main priority
#
#         return [''] * len(row)
#
#     # Apply styling and display DataFrame
#     st.write("### Data with Priority Labels")
#     st.dataframe(df.style.apply(highlight_rows, axis=1), use_container_width=True)
