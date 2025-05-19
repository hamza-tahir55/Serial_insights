import streamlit as st
import json
import hashlib
import base64
import copy
from cryptography.fernet import Fernet
from phi.agent.python import PythonAgent
from phi.model.deepseek import DeepSeekChat
from phi.agent import Agent
import re
from IPython.display import display, Markdown
import time


# ----------------- UI Inputs -----------------

st.title("📊 DashAnalytix Agentic Analysis")

openai_api_key = st.text_input("🔑 Enter OpenAI API Key", type="password")
deepseek_api_key = st.text_input("🔑 Enter DeepSeek API Key", type="password")


graph_data_text = st.text_area("Enter Graph Data (JSON format)", height=300)
additional_data_text = st.text_area("Enter Additional Data (JSON format)", height=300)

if graph_data_text and additional_data_text:
    # Load the data
    import json
    graph_data = graph_data_text
    additional_data = additional_data_text





if st.button("Run Agent Analysis"):
    if not (graph_data and additional_data and deepseek_api_key):
        st.error("Please provide all inputs.")
    else:
        try:
            graph_data = graph_data_text
            additional_data = additional_data_text


            # Set API Keys
            import os
            os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
            os.environ["OPENAI_API_KEY"] = openai_api_key
            



            combined_data = {
                "description": "Combined financial and transactional data for insight generation.",
                "graph_data": graph_data,  # your first JSON block
                "additional_data": additional_data  # your second JSON block
            }



            # ----------------- Agent Setup -----------------

            # Configure the PythonAgent with Groq's Llama model and the local CSV file
            analysis_agent = PythonAgent(
                model=DeepSeekChat(),
                data = combined_data,
                # base_dir=tmp,  # Temporary directory for intermediate files
                # description=data_description,  # Provide a description of the data

            instructions = [f"""If the value
            of the **KPI** has increased, decreased, or remained the same, you must:

            1. Check the **relevant components** such as **customers** and **invoices** in the description to identify the factors responsible for the change in the KPI.
            2. For **financial measures** (like **Income**, **Other Income**, **Cost of Sales**, and **Expenses**):
            - **Analyze changes** in these KPIs and explain them with **transactional data** (such as **Invoice Total**, **new customers**, and **Invoice Count**) to determine the underlying cause.
            - For example, if **Income increased**, check if the increase can be attributed to **higher invoice totals**, **more invoices**, or **new customers** added during that period.
            - For **decreases**, check whether the decrease is due to **lower sales volume**, **reduced customer activity**, or **fewer invoices**.

            The analysis should involve checking the changes in each relevant component (customers, invoices, etc.) and explaining how they contributed to the overall change in the KPI.

            **Example**:

            Let’s say **Income** increased from **$50,000** in **January 2023** to **$60,000** in **February 2023**.

            - Check if the increase in **Income** is related to **higher invoices**:
            - Invoices for **February 2023** showed a **$10,000 increase** in **Invoice Total** compared to **January 2023**.
            - This indicates that the **increase in Income** was likely due to the **higher invoice totals** during February.

            - Check if the increase was caused by **new customers**:
            - There were **5 new customers** added in **February 2023**, contributing an additional **$5,000** to the total **Invoice Total**.

            In this case, the **increase in Income** was largely driven by **higher invoice totals** and **new customers** contributing to the overall sales.
            """
            ],

            markdown=True,  # Enable markdown formatting for responses
            pip_install=False,  # Install required dependencies automatically
            show_tool_calls=False,  # Display tool calls for better transparency
            )

            # Agent 2: Analysis Agent
            analysis_agent = PythonAgent(
                name="Analysis Agent",
                role="Performs data analysis and insight generation based on combined financial and transactional data",
                model=DeepSeekChat(),
                # data = combined_data,
                # base_dir=tmp,  # Temporary directory for intermediate files

            instructions = [
                f"""
                    You are a top analyst in finance and data analysis. You’ve received the `data` variable (from {combined_data}), which includes:
                    - **Financial data** (`graph_data`): Income, Cost of Sales (COS), Expenses, Other Income
                    - **Transactional data** (`additional_data`): Invoices, customer activity, sales
                    - Do not execute or suggest any code.
                    - Do not invoke any tools or external functions.

                    Your task: Generate insights by analyzing changes in financial KPIs and **explaining them using transactional data**. Identify key trends, peaks, and root causes with **numerical evidence**.
                    There is no need to code—just analyze and provide insights based on the data.

                    ---

                    **Workflow**:

                    1. **Financial Trends & Peaks**
                    - Track trends in KPIs over time.
                    - Identify peaks/troughs (state value + date).
                    - Explain each with supporting transactional factors.

                    2. **Peak Analysis by KPI**
                    For each KPI (Income, COS, Expenses):
                    - Identify peak/trough with exact values and time
                    - Explain using related transactional data:
                        - **Income**: Driven by invoice totals, count, or new customers
                        - **COS**: Linked to tp_invoices/cp_invoices, unit volume/price
                        - **Expenses**: Influenced by tp_values (e.g., Tech & Content), invoice volume/value

                    3. **Transactional Correlation**
                    - Match each KPI change with its tagged transactional indicators
                    - Examples:
                        - “Income peaked at $2,000 in May 2021 due to 100 new customers and invoice totals increase”
                        - “COS rose from Jan to Feb due to tp_invoices growing from $44,257 to $52,660”
                        - ”Do Mention Names of customers in final Insight as they are Hashed and FULL hashed values”

                    4. **Root Cause Analysis**
                    - Identify specific drivers: invoice count, customer activity, volume, pricing
                    - Only explain when data shows a clear cause

                    5. **Insight Output**
                    - State:
                        -For each KPI:
                        - KPI change value/%
                        - Peak period and value
                        - Transactional cause (with figures and customers)
                        - Dont leave customer names even if they are hashed, mention them
                    - Example:
                        “Income rose from $50K to $60K (Feb 2021), driven by a $10K increase in invoice totals and 50 new customers”

                    6. **Report**
                    - Summarize changes across all KPIs
                    - Explain financial trends with transactional data
                    - Deliver a clear, evidence-based insight narrative

                    ---

                    **Final Instructions**
                    - Don’t assume causes—only include *data-supported reasons*
                    - If no link found, say so
                    - Cover **every KPI**, no omissions
                    - Dont leave customner names even if they are hashed, mention them
                    - Dont use sterics unless its a heading
                    - Dont generate graphs as it slows down the ouput
                    - Dont give recommendations
                    - Dont code—just analyze and provide insights based on the data
                    - Dont Use double sterics
                    - I will output it using python Display library in markdown so make sure your response comes formatted for Display function



            """
            ],

                markdown=True,
                pip_install=False,
                show_tool_calls=False,
                structured_outputs=True
            )


            validation_agent = PythonAgent(
                name="Validation Agent",
                role="Validates the response of the Analysis Agent and ensures the generated insights are correct and consistent",
                model=DeepSeekChat(),
                # base_dir=tmp,  # Temporary directory for intermediate files
                # data = combined_data,
            instructions = [
                f"""You are a data validation expert. Validate insights from the Analysis Agent using the {combined_data} dataset (graph_data + additional data):

            1. Insight Consistency:
            - Ensure insights match data structure and trends.
            - If Income ↑, confirm it's due to increased invoices, new customers, or related transactions.
            - Root causes must be supported by data.

            2. Data Alignment:
            - KPI insights (Income, Expenses, Cost of Sales) must reflect actual data values.
            - KPI changes should be tied to transactional factors (Invoice Total, customer behavior).

            3. Completeness:
            - Flag insights without clear explanations.
            - All KPI changes must have data-backed causes.
            - Avoid vague statements; include peak values where mentioned.

            4. Data Integrity:
            - No contradictions between insights and data.
            - E.g., if Income ↑ due to new customers, validate that in the data.
            - Invoice Count/Total should support Income change if referenced.

            5. Period Comparison:
            - Ensure correct periods are compared.
            - Time-based comparisons must use correct filtering/aggregation.

            6. Issue Flagging:
            - Flag contradictory insights, missing explanations, or unexplained outliers.

            7. Validation Report:
            - Summarize validated insights, discrepancies, and data alignment.
            - E.g., “Income ↑ due to Invoice Total ↑”.

            8. Final Output:
            - Pass only validated, consistent insights to Data Loader Agent.

            Additional Checks:
            - Each KPI insight must be backed by its transactional data.
            - Confirm KPI ↔ transactional correlations are valid.
            - Ensure data structure matches insight logic.
            - Report gaps or unclear KPI drivers.
            - Dont Use Double Sterics **
            - I will output it using python Display library in markdown so make sure your response comes formatted for Display function
            """
            ],
                markdown=True,
                pip_install=False,
                show_tool_calls=False,
            )


            # Director Agent (Team Leader)
            team_leader = Agent(
                name="Director Agent",
                role="CSV Analysis Team Leader to delegate tasks to each agent for performing their tasks and providing final output to user",
                team=[analysis_agent, validation_agent],
                model=DeepSeekChat(),
                # base_dir=tmp,  # Temporary directory for intermediate files correlate

                instructions=[
                    f"""You are the lead person responsible for generating insights based on the given KPIs {graph_data} and {additional_data}.
                    You have three agents working under your direction:


                    1. **Analysis Agent**:
                        - Once the data is given, the **Analysis Agent** is tasked with analyzing the financial KPIs (such as **Income**, **Cost of Sales**, etc.) from the **graph_data** and explaining them with the transactional data (such as invoices and customer activity).
                        - The **Analysis Agent** will generate insights based on the changes in financial KPIs and provide explanations for **why** those changes occurred.
                        - Provide Analysis for each KPI and Explain them with their respective Transacional data to explain why it happened


                    2. **Validation Agent**:
                        - The **Validation Agent** is responsible for validating the insights generated by the **Analysis Agent**.
                        - They will ensure that the analysis is accurate, consistent, and aligns with the original data structure.
                        - They will check if the explanations are properly supported by the data and flag any inconsistencies or issues.

                    **Your responsibilities**:
                    - **Delegate tasks**: Assign the task of data loading, analysis, and validation to the respective agents.
                    - Ensure that **Data Loader Agent** receives the dataset and prepares it properly.
                    - Ensure that **Analysis Agent** receives the clean and processed data and generates **insights** about the changes in the KPIs and their causes.
                    - Ensure that **Validation Agent** checks the quality and accuracy of the insights generated by the **Analysis Agent**.
                    - Once all tasks are completed, collect the insights and ensure they are **accurate** and **clear**.
                    - Do mention Customers with their full Hashed Values.
                    - Provide the final response to the user based on the insights and validation results.
                    - Dont use double sterics
                    - I will output it using python Display library in markdown so make sure your response comes formatted for Display function


                    Your primary goal is to ensure that the generated insights are **correct**, **consistent**, and **data-backed**.
                    """
                ],
                markdown=True,
                show_tool_calls=False,
                structured_outputs=False,
            )



            # ----------------- Run Analysis -----------------

            start_time = time.time()

            with st.spinner('🚀 Running analysis... please wait ⏳'):
                result = team_leader.run("Analyze the provided financial dataset, focusing on key KPIs such as Income, Cost of Sales (COS), and Expense ratios. Provide insights into any anomalies in the data, such as negative values in 'Other Income,' large customer invoices, or irregular transaction patterns. Highlight key drivers of financial performance and operational efficiency based on the data provided. State the numbers too, dont generate graphs as it slows down the ouput also dont perform code, just give insights directly Also no need to validate insights using code " )


            end_time = time.time()
            elapsed_minutes = (end_time - start_time) / 60

            st.success(f"Agents took {elapsed_minutes:.2f} minutes")

            # Assuming 'result.content' holds the full insight text
            insight_text = str(result.content)

            # Split into sections using the 📊 marker (lookahead so the marker stays)
            sections = re.split(r"(?=📊)", insight_text.strip())

            # Display the main title for generated insights
            st.markdown("## 📊 Generated Insights")

            # Iterate and display each insight section with a subheading
            for i, section in enumerate(sections, 1):
                cleaned = section.strip()
                if cleaned:
                    st.markdown(f"### Insight {i}\n\n{cleaned}")


        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format.")
        except Exception as e:
            st.error(f"❌ Error running analysis: {str(e)}")
