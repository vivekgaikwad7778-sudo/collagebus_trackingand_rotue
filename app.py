import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="TKIET Bus Management System",
    page_icon="🚌",
    layout="wide"
)

# Custom Styling / Title
st.title("🚌 TKIET Warananagar - Bus Tracking & Management System")

# ---------------------------------------------------------
# Sidebar: City & College Selection
# ---------------------------------------------------------
st.sidebar.header("🏫 Institution Details")
selected_city = st.sidebar.selectbox("Select City / Region", ["Kolhapur", "Sangli", "Karad", "Ichalkaranji"])
selected_college = st.sidebar.selectbox("Select College", ["TKIET Warananagar", "TKCP Warananagar"])

st.sidebar.markdown("---")

# Navigation Menu
menu = st.sidebar.radio(
    "Navigation Menu", 
    ["Dashboard Overview", "Bus Routes & Interactive Map", "Driver & Fleet Info", "Student Bus Registration"]
)

# ---------------------------------------------------------
# Sample Data Customized for TKIET
# ---------------------------------------------------------
COLLEGE_LAT = 16.8559
COLLEGE_LON = 74.1966

routes_data = pd.DataFrame([
    {
        "Route ID": "R1", 
        "Route Name": "Kolhapur (CBS) to TKIET", 
        "Bus No": "MH-09-CV-1001", 
        "Driver": "Rajesh Patil", 
        "Phone": "+91 9822012345",
        "Capacity": 50, 
        "Registered Students": 42,
        "Fee_Semester": 12000
    },
    {
        "Route ID": "R2", 
        "Route Name": "Sangli - Ashta to TKIET", 
        "Bus No": "MH-09-CV-2002", 
        "Driver": "Suresh Kamble", 
        "Phone": "+91 9822056789",
        "Capacity": 50, 
        "Registered Students": 48,
        "Fee_Semester": 14000
    },
    {
        "Route ID": "R3", 
        "Route Name": "Ichalkaranji to TKIET", 
        "Bus No": "MH-09-CV-3003", 
        "Driver": "Anand Shinde", 
        "Phone": "+91 9822099999",
        "Capacity": 45, 
        "Registered Students": 30,
        "Fee_Semester": 11000
    }
])

stops_data = pd.DataFrame([
    # Route R1 - Kolhapur
    {"Route": "R1", "Stop Name": "CBS Kolhapur", "Lat": 16.7050, "Lon": 74.2433, "Time": "07:15 AM"},
    {"Route": "R1", "Stop Name": "Tarabai Park", "Lat": 16.7150, "Lon": 74.2380, "Time": "07:25 AM"},
    {"Route": "R1", "Stop Name": "Shiroli Naka", "Lat": 16.7500, "Lon": 74.2600, "Time": "07:40 AM"},
    {"Route": "R1", "Stop Name": "Wathar Naka", "Lat": 16.8200, "Lon": 74.2300, "Time": "08:00 AM"},
    {"Route": "R1", "Stop Name": "TKIET Campus", "Lat": COLLEGE_LAT, "Lon": COLLEGE_LON, "Time": "08:20 AM"},
    
    # Route R2 - Sangli
    {"Route": "R2", "Stop Name": "Sangli Stand", "Lat": 16.8570, "Lon": 74.5810, "Time": "07:00 AM"},
    {"Route": "R2", "Stop Name": "Ashta Naka", "Lat": 16.9500, "Lon": 74.4000, "Time": "07:30 AM"},
    {"Route": "R2", "Stop Name": "Kodoli", "Lat": 16.8800, "Lon": 74.2000, "Time": "08:10 AM"},
    {"Route": "R2", "Stop Name": "TKIET Campus", "Lat": COLLEGE_LAT, "Lon": COLLEGE_LON, "Time": "08:25 AM"},

    # Route R3 - Ichalkaranji
    {"Route": "R3", "Stop Name": "Ichalkaranji Stand", "Lat": 16.6961, "Lon": 74.4582, "Time": "07:10 AM"},
    {"Route": "R3", "Stop Name": "Hatkanangale", "Lat": 16.7455, "Lon": 74.4447, "Time": "07:35 AM"},
    {"Route": "R3", "Stop Name": "TKIET Campus", "Lat": COLLEGE_LAT, "Lon": COLLEGE_LON, "Time": "08:20 AM"}
])

# ---------------------------------------------------------
# 1. Dashboard Overview
# ---------------------------------------------------------
if menu == "Dashboard Overview":
    st.subheader(f"📊 Dashboard - {selected_college} ({selected_city})")
    
    col1, col2, col3, col4 = st.columns(4)
    total_buses = len(routes_data)
    total_capacity = routes_data["Capacity"].sum()
    total_students = routes_data["Registered Students"].sum()
    available_seats = total_capacity - total_students
    
    col1.metric("Active Bus Routes", total_buses)
    col2.metric("Total Seat Capacity", total_capacity)
    col3.metric("Registered Students", total_students)
    col4.metric("Available Seats", available_seats, delta_color="normal")
    
    st.markdown("---")
    st.write("### Fleet & Seat Capacity Details")
    st.dataframe(routes_data[["Route ID", "Route Name", "Bus No", "Driver", "Capacity", "Registered Students"]], use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# 2. Bus Routes & Interactive Map
# ---------------------------------------------------------
elif menu == "Bus Routes & Interactive Map":
    st.subheader(f"📍 Interactive Route Map - {selected_college}")
    
    selected_route = st.selectbox("Select Route to View", routes_data["Route Name"])
    route_row = routes_data[routes_data["Route Name"] == selected_route].iloc[0]
    filtered_stops = stops_data[stops_data["Route"] == route_row["Route ID"]]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write(f"### Route Details ({route_row['Route ID']})")
        st.write(f"**Bus Number:** {route_row['Bus No']}")
        st.write(f"**Driver Name:** {route_row['Driver']}")
        st.write(f"**Phone:** {route_row['Phone']}")
        st.write(f"**Capacity:** {route_row['Registered Students']} / {route_row['Capacity']} Seats Filled")
        
        st.write("---")
        st.write("### Stop Timings")
        st.dataframe(filtered_stops[["Stop Name", "Time"]], hide_index=True, use_container_width=True)
        
    with col2:
        start_lat = filtered_stops.iloc[0]["Lat"]
        start_lon = filtered_stops.iloc[0]["Lon"]
        
        m = folium.Map(location=[start_lat, start_lon], zoom_start=11)
        route_points = list(zip(filtered_stops["Lat"], filtered_stops["Lon"]))
        folium.PolyLine(route_points, color="blue", weight=4, opacity=0.7).add_to(m)
        
        for idx, stop in filtered_stops.iterrows():
            is_college = "TKIET" in stop["Stop Name"]
            icon_color = "red" if is_college else "blue"
            icon_type = "university" if is_college else "bus"
            
            folium.Marker(
                [stop["Lat"], stop["Lon"]],
                popup=f"<b>{stop['Stop Name']}</b><br>Arrival: {stop['Time']}",
                tooltip=stop['Stop Name'],
                icon=folium.Icon(color=icon_color, icon=icon_type, prefix="fa")
            ).add_to(m)
            
        st_folium(m, width=700, height=450)

# ---------------------------------------------------------
# 3. Driver & Fleet Info
# ---------------------------------------------------------
elif menu == "Driver & Fleet Info":
    st.subheader("👨‍✈️ Registered Drivers & Fleet Details")
    st.table(routes_data[["Bus No", "Driver", "Phone", "Route Name", "Capacity"]])

# ---------------------------------------------------------
# 4. Student Bus Registration (Improved)
# ---------------------------------------------------------
elif menu == "Student Bus Registration":
    st.subheader(f"📝 Bus Pass Registration Form ({selected_college})")
    
    # Route selection outside the form to enable dynamic dependent stop selection
    selected_route_name = st.selectbox("Select Bus Route*", routes_data["Route Name"].tolist())
    route_info = routes_data[routes_data["Route Name"] == selected_route_name].iloc[0]
    
    # Filter valid pickup stops based on chosen route
    available_stops = stops_data[
        (stops_data["Route"] == route_info["Route ID"]) & 
        (~stops_data["Stop Name"].str.contains("TKIET"))
    ]["Stop Name"].tolist()

    st.markdown("---")

    with st.form("tkiet_registration_form", clear_on_submit=False):
        st.markdown("#### 1. Personal & Academic Details")
        c1, c2 = st.columns(2)
        
        with c1:
            student_id = st.text_input("PRN / Roll Number*", placeholder="e.g., 2109001")
            student_name = st.text_input("Full Student Name*", placeholder="First Middle Last")
            email = st.text_input("Email Address*", placeholder="student@tkiet.ac.in")
            
        with c2:
            department = st.selectbox("Department", [
                "Computer Science & Engg", 
                "Mechanical Engg", 
                "Civil Engg", 
                "Electrical Engg", 
                "Chemical Engg",
                "Electronics & Telecommunication"
            ])
            year = st.selectbox("Year of Study", ["First Year (FE)", "Second Year (SE)", "Third Year (TE)", "Final Year (BE)"])
            phone = st.text_input("Contact Mobile Number*", placeholder="10-digit mobile number")

        st.markdown("#### 2. Route & Fee Details")
        c3, c4 = st.columns(2)
        
        with c3:
            pickup_stop = st.selectbox("Select Preferred Pickup Stop*", available_stops)
            pass_duration = st.selectbox("Pass Duration", ["1 Semester (6 Months)", "Full Academic Year (12 Months)"])

        with c4:
            base_fee = route_info["Fee_Semester"]
            calculated_fee = base_fee if "1 Semester" in pass_duration else base_fee * 1.85
            st.metric("Estimated Transport Fee", f"₹ {calculated_fee:,.0f}")
            payment_status = st.selectbox("Preferred Payment Method", ["Online UPI / Net Banking", "Cash at Counter", "Demand Draft (DD)"])

        submitted = st.form_submit_button("Submit & Generate Application Pass")

    if submitted:
        # Field Validations
        if not student_id or not student_name or not phone or not email:
            st.error("⚠️ Please fill in all required fields marked with (*).")
        elif len(phone) < 10 or not phone.isdigit():
            st.error("⚠️ Please enter a valid 10-digit mobile number.")
        else:
            st.success("🎉 Bus Registration Request Submitted Successfully!")
            
            # Bus Pass Preview Card
            st.markdown("---")
            st.subheader("💳 Digital Bus Pass Receipt")
            
            pass_card = st.container(border=True)
            with pass_card:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"### **{selected_college}**")
                    st.markdown(f"**Pass Holder:** {student_name} | **PRN:** {student_id}")
                    st.markdown(f"**Dept:** {department} ({year})")
                    st.markdown(f"**Route:** {selected_route_name}")
                    st.markdown(f"**Pickup Stop:** {pickup_stop}")
                    st.markdown(f"**Pass Validity:** {pass_duration}")
                with col_b:
                    st.metric("Amount Paid/Due", f"₹{calculated_fee:,.0f}")
                    st.caption(f"Status: Pending ({payment_status})")

            st.info("📌 **Next Steps:** Please bring your PRN receipt to the TKIET Transport Cell to collect your physical ID badge.")