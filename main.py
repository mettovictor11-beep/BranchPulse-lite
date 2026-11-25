
import streamlit as st
import pandas as pd

from datetime import date

from performance import PerformanceRecord
from database import (
    create_table,
    add_record,
    get_all_records,
    update_record,
    delete_record
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="BranchPulse Lite",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# 2. DATABASE INITIALIZATION
# ==========================================

create_table()


# ==========================================
# 3. APPLICATION HEADER
# ==========================================

st.title("📊 BranchPulse Lite")

st.subheader("Branch Performance & Target Analysis")

st.write(
    "Monitor branch performance, compare actual results against targets, "
    "and make better business decisions."
)

st.divider()


# 
# 4. ADD PERFORMANCE RECORD
# 

st.header("Add Performance Record")

with st.form("performance_form"):

    branch_name = st.text_input("Branch Name")

    report_date = st.date_input(
        "Report Date",
        value=date.today()
    )

    performance_type = st.selectbox(
        "Performance Type",
        ["Revenue", "Disbursement", "Sales"]
    )

    target = st.number_input(
        "Target Amount",
        min_value=0.0,
        step=1000.0
    )

    actual = st.number_input(
        "Actual Amount",
        min_value=0.0,
        step=1000.0
    )

    notes = st.text_area("Notes (optional)")

    submitted = st.form_submit_button("Save Record")

    if submitted:

        record = PerformanceRecord(
            branch_name=branch_name,
            report_date=str(report_date),
            performance_type=performance_type,
            target=target,
            actual=actual,
            notes=notes
        )

        if record.is_valid():

            add_record(record)

            st.success("Performance record saved successfully!")

        else:

            st.error(
                "Please enter a branch name and a target greater than zero."
            )


st.divider()


# ==========================================
# 5. FETCH PERFORMANCE RECORDS
# ==========================================

records = get_all_records()

if records:

    df = pd.DataFrame(
        records,
        columns=[
            "ID",
            "Branch",
            "Report Date",
            "Performance Type",
            "Target",
            "Actual",
            "Notes"
        ]
    )

    # ======================================
    # 6. CALCULATE PERFORMANCE METRICS
    # ======================================

    df["Variance"] = df["Actual"] - df["Target"]

    df["Achievement (%)"] = (
        df["Actual"] / df["Target"] * 100
    ).round(2)

    df["Status"] = df["Achievement (%)"].apply(
        lambda percentage: "On Target"
        if percentage >= 100
        else "Below Target"
    )

    # ======================================
    # 7. BRANCH FILTER AND SEARCH
    # ======================================

    st.header("Performance Records")

    col1, col2 = st.columns(2)

    with col1:

        branch_names = sorted(df["Branch"].unique())

        selected_branch = st.selectbox(
            "Filter by Branch",
            ["All Branches"] + branch_names
        )

    with col2:

        search_term = st.text_input(
            "Search Branch",
            placeholder="Enter branch name..."
        )

    filtered_df = df.copy()

    if selected_branch != "All Branches":

        filtered_df = filtered_df[
            filtered_df["Branch"] == selected_branch
        ]

    if search_term:

        filtered_df = filtered_df[
            filtered_df["Branch"].str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    # ======================================
    # 8. PERFORMANCE OVERVIEW
    # ======================================

    st.divider()

    st.header("Performance Overview")

    total_target = filtered_df["Target"].sum()

    total_actual = filtered_df["Actual"].sum()

    total_variance = total_actual - total_target

    achievement = (
        (total_actual / total_target) * 100
        if total_target > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Target",
        f"KSh {total_target:,.0f}"
    )

    col2.metric(
        "Total Actual",
        f"KSh {total_actual:,.0f}"
    )

    col3.metric(
        "Total Variance",
        f"KSh {total_variance:,.0f}"
    )

    col4.metric(
        "Achievement",
        f"{achievement:.2f}%"
    )

    # ======================================
    # 9. PERFORMANCE RECORDS TABLE
    # ======================================

    st.divider()

    st.subheader("Performance Records")

    if not filtered_df.empty:

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No matching performance records found.")

    
    # ======================================
    # 10. EDIT PERFORMANCE RECORD
    # ======================================

    st.divider()

    st.header("Edit Performance Record")

    if not filtered_df.empty:

        record_ids = filtered_df["ID"].tolist()

        selected_record_id = st.selectbox(
            "Select Record to Edit",
            record_ids,
            format_func=lambda record_id: (
                f"ID {record_id} - "
                f"{filtered_df[filtered_df['ID'] == record_id]['Branch'].iloc[0]}"
            )
        )

        selected_record = filtered_df[
            filtered_df["ID"] == selected_record_id
        ].iloc[0]

        with st.form("edit_record_form"):

            edit_branch = st.text_input(
                "Branch Name",
                value=selected_record["Branch"]
            )

            edit_date = st.date_input(
                "Report Date",
                value=date.fromisoformat(
                    str(selected_record["Report Date"])
                )
            )

            edit_type = st.selectbox(
                "Performance Type",
                ["Revenue", "Disbursement", "Sales"],
                index=["Revenue", "Disbursement", "Sales"].index(
                    selected_record["Performance Type"]
                )
            )

            edit_target = st.number_input(
                "Target Amount",
                min_value=0.0,
                value=float(selected_record["Target"]),
                step=1000.0
            )

            edit_actual = st.number_input(
                "Actual Amount",
                min_value=0.0,
                value=float(selected_record["Actual"]),
                step=1000.0
            )

            edit_notes = st.text_area(
                "Notes",
                value=str(selected_record["Notes"] or "")
            )

            update_submitted = st.form_submit_button(
                "Update Record"
            )

            if update_submitted:

                updated_record = PerformanceRecord(
                    branch_name=edit_branch,
                    report_date=str(edit_date),
                    performance_type=edit_type,
                    target=edit_target,
                    actual=edit_actual,
                    notes=edit_notes
                )

                if updated_record.is_valid():

                    update_record(
                        selected_record_id,
                        updated_record
                    )

                    st.success("Record updated successfully!")

                    st.rerun()

                else:

                    st.error(
                        "Please enter a branch name and "
                        "a target greater than zero."
                    )

    else:

        st.info("No records available to edit.")


   
    # ======================================
    # 11. DELETE PERFORMANCE RECORD
    # ======================================

    st.divider()

    st.header("Delete Performance Record")

    if not filtered_df.empty:

        delete_record_id = st.selectbox(
            "Select Record to Delete",
            filtered_df["ID"].tolist(),
            format_func=lambda record_id: (
                f"ID {record_id} - "
                f"{filtered_df[filtered_df['ID'] == record_id]['Branch'].iloc[0]}"
            ),
            key="delete_record_selector"
        )

        confirm_delete = st.checkbox(
            "I understand that this record will be permanently deleted."
        )

        if st.button("Delete Selected Record", type="primary"):

            if confirm_delete:

                delete_record(delete_record_id)

                st.success("Record deleted successfully!")

                st.rerun()

            else:

                st.warning(
                    "Please confirm that you want to delete this record."
                )

    else:

        st.info("No records available to delete.")
 

    # ======================================
    # 12. BRANCH PERFORMANCE CHART
    # ======================================

    st.divider()

    st.header("Branch Performance Comparison")

    if not filtered_df.empty:

        branch_summary = filtered_df.groupby("Branch")[
            ["Target", "Actual"]
        ].sum()

        st.bar_chart(branch_summary)

    else:

        st.info("No records available for the chart.")

    # ======================================
    # 13. CSV REPORT EXPORT
    # ======================================

    st.divider()

    st.header("Export Performance Report")

    if not filtered_df.empty:

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download CSV Report",
            data=csv_data,
            file_name="branchpulse_performance_report.csv",
            mime="text/csv"
        )

    else:

        st.info("No records available for export.")

else:

    st.info(
        "No performance records found yet. "
        "Add your first branch performance record above."
    )


# ==========================================
# 14. APPLICATION FOOTER
# ==========================================

st.divider()

st.caption("BranchPulse Lite | Performance made simple")
