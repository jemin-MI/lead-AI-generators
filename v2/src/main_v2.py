import json
import os

import streamlit as st
import pandas as pd
import time
from datetime import datetime
from crew import SalesLead
from crewai import Crew
import multiprocessing as mp

import threading

sl = SalesLead()


def category_selection():
    st.title("Lead Gen v2")

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
    tasks = [sl.analyze_motive()]  # Pass selected sectors
    agents = [sl.motive_agent()]
    input_data = {"query": query}
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)
    # crew_(agents, tasks, input_data)
    return response.raw if response else None


def sector_queries(query, selected_sectors):
    print(f"Processing query: {query} with sectors: {selected_sectors}")
    tasks = [sl.sector_analyze()]  # Pass selected sectors
    agents = [sl.sector_agent()]
    input_data = {'query': query, 'selected_sectors': selected_sectors}
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)
    # crew_(agents, tasks, input_data)
    # crew(agents, tasks, input_data)
    return response.raw if response else None


def response_checker(query, selected_sector):
    tasks = [sl.sector_filter()]  # Pass selected sectors
    agents = [sl.sector_filter_agent()]
    input_data = {'query': query, 'selected_sectors': selected_sector}
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    return response.raw if response else None


def tech_finder(query, category):
    tasks = [sl.technology_finder()]  # Pass selected sectors
    agents = [sl.technology_finder_agent()]
    input_data = {'query': query, 'category': category}
    # crew(agents, tasks, input_data)
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    return response.raw if response else None


def complex_finder(query, resource, technology):
    tasks = [sl.project_complexity_finder()]  # Pass selected sectors
    agents = [sl.project_complexity_agent()]
    input_data = {'query': query, 'resource': resource, 'technology': technology}
    # crew(agents, tasks, input_data)
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    return response.raw if response else None


def cate_finder(query):
    tasks = [sl.service_category_finder()]  # Pass selected sectors
    agents = [sl.service_category_finder_agent()]
    input_data = {'query': query}
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    # crew(agents, tasks, input_data)
    return response.raw if response else None


def email_sort(email):
    tasks = [sl.email_priority_finder()]  # Pass selected sectors
    agents = [sl.email_priority_agent()]
    input_data = {'email': email}
    # crew(agents, tasks, input_data)
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    return response.raw if response else None


def location_sort(country, locations):
    tasks = [sl.location_priority_finder()]  # Pass selected sectors
    agents = [sl.country_priority_agent()]
    input_data = {'country': country, 'country_list': locations}
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    # crew(agents, tasks, input_data)
    return response.raw if response else None


def urgency_finder(query):
    tasks = [sl.urgency_pricing_finder()]  # Pass selected sectors
    agents = [sl.urgency_pricing_agent()]
    input_data = {'query': query}
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    # crew(agents, tasks, input_data)
    return response.raw if response else None


def company_size_finder(query):
    tasks = [sl.company_type_finder()]  # Pass selected sectors
    agents = [sl.provider_type_agent()]
    input_data = {'query': query}
    response = Crew(agents=agents, tasks=tasks).kickoff(inputs=input_data)

    # crew(agents, tasks, input_data)
    return response.raw if response else None


final_results = []
email_priority_list = []
country_priority_list = []
sector_priority_list = []
urgency_priority_list = []
motive_priority_list = []
message_colum = 'message'
email_colum = 'email'
country_colum = 'country'
manager = mp.Manager()
results_list = manager.list()  # Shared list for multiprocessing

def upload_excel():
    st.title("Upload Excel File")
    st.write(f"**Selected Categories:** {', '.join(st.session_state.selected_sectors)}")
    st.write(f"**Selected Country:** {', '.join(st.session_state.selected_country)}")

    selected_sector = st.session_state.selected_sectors
    selected_country = st.session_state.selected_country

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    if uploaded_file is not None:
        try:
            start_time = time.time()
            df = pd.read_excel(uploaded_file)
            raw_per_batch = 10
            processes = []

            for batch_number, start in enumerate(range(0, len(df), raw_per_batch)):
                batch_df = df.iloc[start:start + raw_per_batch].copy()  # Copy to avoid conflicts
                p = mp.Process(target=process_rows, args=(batch_df, selected_sector, selected_country, batch_number))
                processes.append(p)
                p.start()

            # Wait for all processes to complete
            for p in processes:
                p.join()


            end_time = time.time()
            execution_time = end_time - start_time
            # data_dict['Total Exceution Time'] = execution_time
            print("execution time", execution_time)
            st.write("Time taken to run", "%.2f" % execution_time)
            final_df = pd.concat(list(results_list), ignore_index=True)
            final_results.append(final_df)  # Store it globally
            # final_df.to_csv("final_result.csv", index=False)
            st.write("---Final DF data ---")
            # st.dataframe(final_df)
            highlight_qualified(final_df)

            st.success("✅ Results saved'")


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


def highlight_qualified(df):
    def row_style(row):
        return ["background-color: #ebebeb"] * len(row) if row["Status"] == "Qualified" else [""] * len(row)

    styled_df = df.style.apply(row_style, axis=1)
    st.dataframe(styled_df)
    st.write("data frame created with color")


def process_rows(df, selected_sector, selected_country, batch=None):
    data_dict = {}
    count = 0

    for index, row in df.iterrows():

        query = row[message_colum] if message_colum in row else ''
        priority_index = 0
        if query:
            query_start_time = time.time()
            motive_of_query = motive_checker(query)

            if 'False' in motive_of_query:
                # motive_priority_list.append(index)
                add_df_data(df, 'Status', index, 'UnQualified')
                continue
            else:
                add_df_data(df, 'Status', index, 'Qualified')

            sector_result = sector_queries(query, selected_sector)

            if sector_result:
                sector = response_checker(sector_result, selected_sector)

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
                country_priority = location_sort(country, selected_country)

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
                query_end_time = time.time()

                time_taken_query = query_end_time - query_start_time

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
                    'Urgency': urgency,
                    'Query Execution time': time_taken_query
                }

                data_dict[index] = current_data
                # st.write(current_data)

        count += 1
        print(f"completed row ::::: {count}")

    results_list.append(df)  # Append processed batch to shared list
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    dir_path = "data_dict/batch"
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f'v2_{str(current_datetime)}__{batch}.json')
    with open(file_path, 'w') as file:
        json.dump(data_dict, file, indent=4)
