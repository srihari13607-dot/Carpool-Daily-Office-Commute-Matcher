
import streamlit as st
import pandas as pd

from matcher.models import (
    UserRole, User, Location, CommuteSchedule,
    CommutePreferences, Vehicle, FuelType
)
from matcher.engine import CommuteMatchingEngine
from matcher.sample_data import (
    get_sample_commuters, HOME_HUBS, WORK_HUBS
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Carpool Connect",
    page_icon="🚗",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM DARK THEME
# --------------------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #0b1220;
    color: #ffffff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #121d30;
}

[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}

/* Main content spacing */
.block-container {
    padding-top: 1.7rem;
}

/* Headings */
h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 700;
}

/* Normal text */
p, label, li {
    color: #e2e8f0 !important;
}

/* Captions */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #cbd5e1 !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #17243a;
    border: 1px solid #293b56;
    padding: 16px;
    border-radius: 14px;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

/* Buttons */
div.stButton > button {
    background: #00d6a0;
    color: #071b19 !important;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
}

/* Button hover */
div.stButton > button:hover {
    background: #00b98a;
    color: #ffffff !important;
}

/* Input labels */
[data-testid="stWidgetLabel"] {
    color: #f1f5f9 !important;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stTimeInput input {
    color: #ffffff !important;
    background: #17243a !important;
}

/* Info messages */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #293b56;
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #293b56;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD MATCHING ENGINE
# --------------------------------------------------

@st.cache_resource
def load_engine():
    return CommuteMatchingEngine()


@st.cache_data
def load_people():
    return get_sample_commuters()


engine = load_engine()

if "people" not in st.session_state:
    st.session_state.people = load_people()

people = st.session_state.people


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------


# SIDEBAR NAVIGATION

def navigate_to(page_name):
    st.session_state["page"] = page_name

if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

st.sidebar.markdown("# 🚗 CARPOOL")
st.sidebar.caption("DAILY OFFICE COMMUTE MATCHER")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Find a Ride",
        "Register Commuter",
        "Commuters",
        "Alternating Rides",
        "About"
    ],
    key="page"
)

st.sidebar.divider()
st.sidebar.caption("Smart mobility • Shared journeys")

st.sidebar.caption("Smart mobility • Shared journeys")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("Your commute, connected.")

    st.caption(
        "Find nearby colleagues, coordinate schedules "
        "and share the journey."
    )

    drivers = sum(
        u.role in (
            UserRole.DRIVER,
            UserRole.HYBRID_ALTERNATING
        )
        for u in people
    )

    riders = sum(
        u.role in (
            UserRole.RIDER,
            UserRole.HYBRID_ALTERNATING
        )
        for u in people
    )

    a, b, c, d = st.columns(4)

    a.metric("Active commuters", len(people))
    b.metric("Drivers", drivers)
    c.metric("Riders", riders)

    d.metric(
        "Partner companies",
        len(set(u.company for u in people))
    )

    st.subheader("Quick actions")

    x, y = st.columns(2)

    with x:

        st.info(
            "**Find a ride**\n\n"
            "Match commuters by home area, office "
            "destination and departure time."
        )

        
        if st.button(
            "Find commute partners",
            use_container_width=True,
            on_click=navigate_to,
            args=("Find a Ride",)
        ):
            pass

    with y:

        st.info(
            "**Register a commuter**\n\n"
            "Add a driver or rider profile to the local session."
        )

        
        if st.button(
            "Add commuter",
             use_container_width=True,
             on_click=navigate_to,
             args=("Register Commuter",)
        ):
            pass


    st.subheader("How matching works")

    st.write(
        "The demo matching engine scores shared office areas, "
        "nearby home locations, departure-time compatibility "
        "and common commute days."
    )


# --------------------------------------------------
# FIND A RIDE
# --------------------------------------------------

elif page == "Find a Ride":

    st.title("Find your commute match")

    st.caption(
        "Choose a sample commuter profile or register your own."
    )

    options = {
        f"{u.name} · {u.company} · {u.role.value}": u
        for u in people
    }

    if not options:
        st.warning("No commuter profiles are available.")
    else:

        selected = st.selectbox(
            "Your profile",
            list(options)
        )

        target = options[selected]

        minimum = st.slider(
            "Minimum match score",
            0, 100, 40, 5
        )

        st.write(
            f"**Home:** {target.home_location.name}  ·  "
            f"**Office:** {target.work_location.name}  ·  "
            f"**Departure:** {target.schedule.morning_departure}"
        )

        if st.button(
            "🔎 Find matching commuters",
            use_container_width=True
        ):

            if target.role in (
                UserRole.DRIVER,
                UserRole.HYBRID_ALTERNATING
            ):
                matches = engine.find_matches_for_driver(
                    target, people, minimum
                )
            else:
                matches = engine.find_matches_for_rider(
                    target, people, minimum
                )

            st.session_state.matches = matches

        if "matches" in st.session_state:

            matches = st.session_state.matches

            st.subheader(
                f"{len(matches)} compatible match(es)"
            )

            if not matches:
                st.warning(
                    "No matches at this score. "
                    "Try lowering the minimum score."
                )

            for m in matches:

                with st.container(border=True):

                    left, right = st.columns([3, 1])

                    left.markdown(
                        f"### {m.commuter.name}"
                    )

                    left.write(
                        f"{m.commuter.company} · "
                        f"{m.commuter.role.value.title()}"
                    )

                    left.write(
                        f"{m.commuter.home_location.name} "
                        f"→ {m.commuter.work_location.name}"
                    )

                    left.caption(
                        " • ".join(m.reasons)
                    )

                    right.metric(
                        "Match score",
                        f"{m.score:.0f}/100"
                    )


# --------------------------------------------------
# REGISTER COMMUTER
# --------------------------------------------------

elif page == "Register Commuter":

    st.title("Create commuter profile")

    with st.form("register"):

        name = st.text_input("Full name")

        email = st.text_input("Email")

        company = st.text_input("Company")

        role_label = st.selectbox(
            "Commute role",
            ["Rider", "Driver", "Hybrid / alternating"]
        )

        c1, c2 = st.columns(2)

        with c1:

            home_name = st.selectbox(
                "Home area",
                list(HOME_HUBS)
            )

            home = HOME_HUBS[home_name]

        with c2:

            work_name = st.selectbox(
                "Office area",
                list(WORK_HUBS)
            )

            work = WORK_HUBS[work_name]

        departure = st.time_input(
            "Morning departure"
        )

        seats = st.number_input(
            "Available passenger seats",
            1, 8, 3
        )

        vehicle_name = st.text_input(
            "Vehicle model (drivers)",
            "Car"
        )

        submitted = st.form_submit_button(
            "Save commuter profile"
        )

    if submitted:

        if not name.strip() or not company.strip():

            st.error(
                "Please enter your name and company."
            )

        else:

            role = {
                "Rider": UserRole.RIDER,
                "Driver": UserRole.DRIVER,
                "Hybrid / alternating":
                    UserRole.HYBRID_ALTERNATING
            }[role_label]

            vehicle = (
                Vehicle(
                    vehicle_name,
                    int(seats),
                    FuelType.PETROL
                )
                if role != UserRole.RIDER
                else None
            )

            person = User(
                id=f"local_{len(st.session_state.people)+1}",
                name=name.strip(),
                email=email.strip() or "not-provided@example.com",
                company=company.strip(),
                role=role,
                gender="Not specified",
                home_location=home,
                work_location=work,
                schedule=CommuteSchedule(
                    morning_departure=departure.strftime("%H:%M")
                ),
                preferences=CommutePreferences(),
                vehicle=vehicle
            )

            st.session_state.people.append(person)

            st.success(
                "Profile added for this running session."
            )

            st.rerun()


# --------------------------------------------------
# COMMUTER DIRECTORY
# --------------------------------------------------

elif page == "Commuters":

    st.title("Commuter directory")

    rows = [
        {
            "Name": u.name,
            "Company": u.company,
            "Role": u.role.value.title(),
            "Home": u.home_location.name,
            "Office": u.work_location.name,
            "Departure": u.schedule.morning_departure
        }
        for u in people
    ]

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# ALTERNATING RIDES
# --------------------------------------------------

elif page == "Alternating Rides":

    st.title("Alternating driver pairs")

    pairs = engine.find_alternating_pairs(people)

    st.metric(
        "Potential pairs",
        len(pairs)
    )

    if pairs:

        st.dataframe(
            pd.DataFrame(pairs),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No potential alternating pairs "
            "in the current sample."
        )


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

else:

    st.title("About Carpool Connect")

    st.write(
        "A demonstration application for matching office "
        "commuters based on approximate home-area proximity, "
        "office-area proximity, departure times and shared weekdays."
    )

    st.warning(
        "This bundled version uses sample data and an "
        "illustrative matching score. It is not connected "
        "to a live database or GPS routing service."
    )
