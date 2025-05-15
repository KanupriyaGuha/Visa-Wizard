import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime, timedelta
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set page config
st.set_page_config(page_title="Visa Wizard", page_icon="🧳")

# Page title and description
st.title("🧳 Visa Wizard – F1 Visa & OPT Timeline Planner")
st.markdown("Plan your OPT/STEM/H-1B milestones interactively 🚀")

# Sidebar for Input Organization
st.sidebar.title("Visa Information")
first_name = st.sidebar.text_input("First Name")
last_name = st.sidebar.text_input("Last Name")
graduation_date = st.sidebar.date_input("Expected Graduation Date")
visa_type = st.sidebar.selectbox("Visa Type", ["F1", "OPT", "STEM OPT", "H-1B"])
country = st.sidebar.selectbox("Country of Origin", ["USA", "India", "China", "Canada"])

# Additional Inputs
program = st.sidebar.selectbox("What is your academic program?", ["Bachelor's", "Master's", "Ph.D."])
is_stem = st.sidebar.checkbox("Are you in a STEM field?")

# Display the chosen inputs
st.sidebar.write(f"You selected: {program}")
st.sidebar.write(f"STEM field: {'Yes' if is_stem else 'No'}")

# User decision for OPT/STEM OPT planning
has_applied_opt = st.sidebar.checkbox("Have you already applied for OPT?")
if has_applied_opt:
    st.sidebar.write("You have applied for OPT, let's move on to STEM OPT planning!")

# Create layout for centered "Generate Timeline" Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button(
        "Generate Timeline 🎉", 
        help="Click to generate your personalized visa timeline",
        use_container_width=True
    )

# Function to generate PDF
def generate_pdf(name, timeline):
    pdf_filename = f"Visa_Timeline_{name.replace(' ', '_')}.pdf"  # Ensure filename is valid
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"Visa Timeline for {name}")
    y_position = 730
    for milestone in timeline:
        c.drawString(100, y_position, f"{milestone['label']}: {milestone['start'].strftime('%B %d, %Y')}")
        y_position -= 20
    c.save()
    return pdf_filename

# Function to create Altair-based interactive timeline
def create_altair_timeline(timeline):
    # Convert timeline to a DataFrame
    df = pd.DataFrame(timeline)

    # Explicitly define the types for milestones and dates
    df['label'] = df['label'].astype(str)
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])

    # Create the Altair chart (interactive timeline)
    chart = alt.Chart(df).mark_bar().encode(
        x='start:T',        # 'start' as temporal
        x2='end:T',         # 'end' as temporal
        y='label:N',        # 'label' as nominal (string)
        color='label:N', 
        tooltip=['label', 'start:T', 'end:T']
    ).properties(
        title="Visa Application Timeline"
    ).configure_axis(
        labelAngle=45
    )

    # Show the chart
    st.altair_chart(chart, use_container_width=True)

# Function to collect reminders from the user
def get_reminders(timeline):
    reminders = []
    for milestone in timeline:
        reminder_date = st.date_input(f"Set a reminder for {milestone['label']}:", value=milestone['start'])
        reminders.append({"label": milestone['label'], "reminder_date": reminder_date})
    return reminders

# Function to send in-app reminders
def send_in_app_reminder(reminders):
    for reminder in reminders:
        reminder_date = reminder['reminder_date']
        if reminder_date == datetime.today().date():
            st.success(f"Reminder: {reminder['label']} is coming up today, {reminder_date.strftime('%B %d, %Y')}!")
        elif reminder_date > datetime.today().date():
            st.info(f"Upcoming Reminder: {reminder['label']} on {reminder_date.strftime('%B %d, %Y')}")
        else:
            st.warning(f"Reminder: {reminder['label']} was due on {reminder_date.strftime('%B %d, %Y')}")

# Generate Timeline
if generate:
    with st.spinner('Generating your timeline...'):
        time.sleep(2)  # Simulate some processing time
    
    if not first_name or not last_name or not graduation_date:
        st.error("Please fill out all fields.")
    else:
        full_name = f"{first_name} {last_name}"
        st.success(f"Here's your personalized timeline, {full_name}!")
        
        timeline = []
        if has_applied_opt:
            if is_stem:
                stem_opt_start_date = graduation_date + timedelta(days=270)
                stem_opt_end_date = stem_opt_start_date + timedelta(days=365)
                
                timeline = [
                    {"label": "STEM OPT Application Opens", "start": stem_opt_start_date, "end": stem_opt_start_date},
                    {"label": "STEM OPT Start Date", "start": stem_opt_start_date, "end": stem_opt_start_date},
                    {"label": "STEM OPT End Date", "start": stem_opt_end_date, "end": stem_opt_end_date},
                ]
                st.markdown("### 📅 Your STEM OPT Timeline")
                for milestone in timeline:
                    st.markdown(f"- **{milestone['label']}**: `{milestone['start'].strftime('%B %d, %Y')}`")
            else:
                st.error("To apply for STEM OPT, you must be in a STEM field. Please check your program.")
        else:
            timeline = [
                {"label": "OPT Application Window Opens", "start": graduation_date - timedelta(days=90), "end": graduation_date - timedelta(days=90)},
                {"label": "Last Day to Apply for OPT", "start": graduation_date + timedelta(days=60), "end": graduation_date + timedelta(days=60)},
            ]
        
        # Show the Altair Timeline
        create_altair_timeline(timeline)
        
        # Get reminders from the user
        reminders = get_reminders(timeline)

        st.markdown("### 📅 Your Reminders")
        for reminder in reminders:
            st.markdown(f"- **{reminder['label']}**: `{reminder['reminder_date'].strftime('%B %d, %Y')}`")
        
        # Send in-app reminders for upcoming or past milestones
        send_in_app_reminder(reminders)
        
        # Generate and download the PDF
        with st.spinner('Generating your PDF...'):
            pdf_filename = generate_pdf(full_name, timeline)
        st.success('PDF Generated!')
        st.download_button("Download PDF", pdf_filename, file_name=pdf_filename)

# Enhanced "Need Help?" Section
st.markdown("### 📚 Need Help?")
with st.expander("Click to Expand Help Section"):
    st.markdown(
        """
        **What is OPT?**  
        OPT (Optional Practical Training) allows international students on an F-1 visa to work in the U.S. for up to 12 months after graduation.

        **What is STEM OPT?**  
        STEM OPT is an extension of the OPT program for students in STEM fields, allowing up to 24 additional months of work.

        **How do I apply for OPT?**  
        You can apply for OPT up to 90 days before your graduation date. Make sure to check the exact dates and requirements for your country and visa type.

        **What is H-1B?**  
        The H-1B visa is for foreign workers in specialty occupations. It’s typically applied for after your OPT period ends, allowing you to stay and work in the U.S. longer.

        **For more information, check these resources**:  
        - [USCIS Website for OPT](https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training)
        - [Visa Bulletin for Current Information](https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html)
        
        **Watch the video tutorial** on how to apply for OPT:  
        [How to Apply for OPT - YouTube](https://www.youtube.com/watch?v=OPT-video-link)
        """
    )
