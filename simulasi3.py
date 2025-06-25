import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

# Configuration
st.set_page_config(
    page_title="Simulasi Proyek Digital - Dinamis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class OperationalCosts:
    personnel_cost: float
    infrastructure_cost: float
    marketing_cost: float
    maintenance_cost: float
    licensing_cost: float
    legal_compliance_cost: float
    office_utilities_cost: float
    rd_cost: float

@dataclass
class ProjectData:
    name: str
    initial_investment: float
    annual_revenue_year1: float
    annual_growth_rate: float
    operational_cost_rate: float
    development_months: int
    market_risk_factor: float
    competition_impact: float
    operational_costs: OperationalCosts

# Default operational costs for each project (in Rupiah per year)
DEFAULT_OPERATIONAL_COSTS = {
    "super_apps_bali": OperationalCosts(
        personnel_cost=800_000_000,
        infrastructure_cost=300_000_000,
        marketing_cost=500_000_000,
        maintenance_cost=150_000_000,
        licensing_cost=100_000_000,
        legal_compliance_cost=80_000_000,
        office_utilities_cost=120_000_000,
        rd_cost=200_000_000
    ),
    "construction_mgmt": OperationalCosts(
        personnel_cost=600_000_000,
        infrastructure_cost=200_000_000,
        marketing_cost=300_000_000,
        maintenance_cost=120_000_000,
        licensing_cost=180_000_000,
        legal_compliance_cost=100_000_000,
        office_utilities_cost=100_000_000,
        rd_cost=250_000_000
    ),
    "data_center": OperationalCosts(
        personnel_cost=1_200_000_000,
        infrastructure_cost=800_000_000,
        marketing_cost=400_000_000,
        maintenance_cost=300_000_000,
        licensing_cost=250_000_000,
        legal_compliance_cost=150_000_000,
        office_utilities_cost=150_000_000,
        rd_cost=400_000_000
    ),
    "big_data": OperationalCosts(
        personnel_cost=1_800_000_000,
        infrastructure_cost=1_200_000_000,
        marketing_cost=600_000_000,
        maintenance_cost=400_000_000,
        licensing_cost=300_000_000,
        legal_compliance_cost=200_000_000,
        office_utilities_cost=200_000_000,
        rd_cost=800_000_000
    ),
    "cyber_security": OperationalCosts(
        personnel_cost=2_000_000_000,
        infrastructure_cost=1_000_000_000,
        marketing_cost=800_000_000,
        maintenance_cost=500_000_000,
        licensing_cost=400_000_000,
        legal_compliance_cost=300_000_000,
        office_utilities_cost=200_000_000,
        rd_cost=1_000_000_000
    )
}

# Project definitions
PROJECTS = {
    "super_apps_bali": ProjectData(
        name="Super Apps Turis Bali",
        initial_investment=2_222_000_000,
        annual_revenue_year1=3_600_000_000,
        annual_growth_rate=0.25,
        operational_cost_rate=0.35,
        development_months=12,
        market_risk_factor=0.15,
        competition_impact=0.10,
        operational_costs=DEFAULT_OPERATIONAL_COSTS["super_apps_bali"]
    ),
    "construction_mgmt": ProjectData(
        name="Manajemen Konstruksi",
        initial_investment=1_655_000_000,
        annual_revenue_year1=4_000_000_000,
        annual_growth_rate=0.18,
        operational_cost_rate=0.30,
        development_months=10,
        market_risk_factor=0.12,
        competition_impact=0.08,
        operational_costs=DEFAULT_OPERATIONAL_COSTS["construction_mgmt"]
    ),
    "data_center": ProjectData(
        name="Data Center Management",
        initial_investment=3_332_000_000,
        annual_revenue_year1=8_000_000_000,
        annual_growth_rate=0.20,
        operational_cost_rate=0.25,
        development_months=14,
        market_risk_factor=0.10,
        competition_impact=0.12,
        operational_costs=DEFAULT_OPERATIONAL_COSTS["data_center"]
    ),
    "big_data": ProjectData(
        name="Big Data Analytics",
        initial_investment=3_858_000_000,
        annual_revenue_year1=15_000_000_000,
        annual_growth_rate=0.30,
        operational_cost_rate=0.28,
        development_months=16,
        market_risk_factor=0.18,
        competition_impact=0.15,
        operational_costs=DEFAULT_OPERATIONAL_COSTS["big_data"]
    ),
    "cyber_security": ProjectData(
        name="Cyber Security Platform",
        initial_investment=3_150_000_000,
        annual_revenue_year1=22_000_000_000,
        annual_growth_rate=0.35,
        operational_cost_rate=0.22,
        development_months=12,
        market_risk_factor=0.20,
        competition_impact=0.18,
        operational_costs=DEFAULT_OPERATIONAL_COSTS["cyber_security"]
    )
}

class ProjectSimulator:
    def __init__(self, project_data: ProjectData, scenario: str = "optimistic", custom_op_costs: OperationalCosts = None, years: int = 10):
        self.project = project_data
        self.scenario = scenario
        self.years = years
        self.custom_op_costs = custom_op_costs
        
    def get_operational_costs(self) -> OperationalCosts:
        """Get operational costs (custom or default)"""
        return self.custom_op_costs if self.custom_op_costs else self.project.operational_costs
    
    def calculate_total_operational_cost(self, year: int) -> float:
        """Calculate total operational cost for a given year"""
        op_costs = self.get_operational_costs()
        
        # Apply inflation to operational costs
        inflation_factor = (1.035 ** year)  # 3.5% annual inflation
        
        # Apply growth factor for some costs (personnel, infrastructure)
        growth_factor = (1 + (self.project.annual_growth_rate * 0.3)) ** year
        
        total_cost = (
            op_costs.personnel_cost * growth_factor * inflation_factor +
            op_costs.infrastructure_cost * growth_factor * inflation_factor +
            op_costs.marketing_cost * inflation_factor +
            op_costs.maintenance_cost * inflation_factor +
            op_costs.licensing_cost * inflation_factor +
            op_costs.legal_compliance_cost * inflation_factor +
            op_costs.office_utilities_cost * inflation_factor +
            op_costs.rd_cost * inflation_factor
        )
        
        return total_cost
        
    def apply_scenario_adjustments(self, base_value: float, year: int) -> float:
        """Apply scenario-based adjustments"""
        scenario_multipliers = {
            "pessimistic": {
                "growth": 0.7,
                "risk": 1.5,
                "competition": 1.3
            },
            "realistic": {
                "growth": 0.85,
                "risk": 1.2,
                "competition": 1.1
            },
            "optimistic": {
                "growth": 1.0,
                "risk": 0.8,
                "competition": 0.9
            }
        }
        
        multiplier = scenario_multipliers[self.scenario]
        
        # Apply market saturation effect (diminishing returns)
        saturation_factor = 1 - (year * 0.05)  # 5% reduction per year
        saturation_factor = max(saturation_factor, 0.6)  # Minimum 60% of original
        
        # Apply competition impact (increases over time)
        competition_factor = 1 - (self.project.competition_impact * multiplier["competition"] * (year / self.years))
        
        # Apply market risk
        risk_factor = 1 - (self.project.market_risk_factor * multiplier["risk"] * np.random.uniform(0.5, 1.5))
        
        adjusted_value = base_value * multiplier["growth"] * saturation_factor * competition_factor * max(risk_factor, 0.3)
        
        return max(adjusted_value, base_value * 0.3)  # Minimum 30% of base value
    
    def calculate_yearly_metrics(self) -> pd.DataFrame:
        """Calculate financial metrics for each year"""
        results = []
        
        for year in range(1, self.years + 1):
            # Revenue calculation with growth
            base_revenue = self.project.annual_revenue_year1 * ((1 + self.project.annual_growth_rate) ** (year - 1))
            adjusted_revenue = self.apply_scenario_adjustments(base_revenue, year)
            
            # Detailed operational costs
            total_operational_cost = self.calculate_total_operational_cost(year)
            op_costs = self.get_operational_costs()
            inflation_factor = (1.035 ** year)
            growth_factor = (1 + (self.project.annual_growth_rate * 0.3)) ** year
            
            # Breakdown of operational costs
            personnel_cost = op_costs.personnel_cost * growth_factor * inflation_factor
            infrastructure_cost = op_costs.infrastructure_cost * growth_factor * inflation_factor
            marketing_cost = op_costs.marketing_cost * inflation_factor
            maintenance_cost = op_costs.maintenance_cost * inflation_factor
            licensing_cost = op_costs.licensing_cost * inflation_factor
            legal_compliance_cost = op_costs.legal_compliance_cost * inflation_factor
            office_utilities_cost = op_costs.office_utilities_cost * inflation_factor
            rd_cost = op_costs.rd_cost * inflation_factor
            
            # Additional yearly investments (maintenance, upgrades)
            yearly_investment = self.project.initial_investment * 0.05 if year > 1 else 0
            
            # Net profit
            net_profit = adjusted_revenue - total_operational_cost - yearly_investment
            
            # Cumulative metrics
            if year == 1:
                cumulative_investment = self.project.initial_investment + yearly_investment
                cumulative_revenue = adjusted_revenue
                cumulative_profit = net_profit - self.project.initial_investment
                cumulative_op_cost = total_operational_cost
            else:
                prev_row = results[-1]
                cumulative_investment = prev_row["cumulative_investment"] + yearly_investment
                cumulative_revenue = prev_row["cumulative_revenue"] + adjusted_revenue
                cumulative_profit = prev_row["cumulative_profit"] + net_profit
                cumulative_op_cost = prev_row["cumulative_op_cost"] + total_operational_cost
            
            # ROI calculation
            roi = (cumulative_profit / cumulative_investment) * 100 if cumulative_investment > 0 else 0
            
            # Payback period
            payback_achieved = cumulative_profit > 0
            
            results.append({
                "year": year,
                "revenue": adjusted_revenue,
                "operational_cost": total_operational_cost,
                "personnel_cost": personnel_cost,
                "infrastructure_cost": infrastructure_cost,
                "marketing_cost": marketing_cost,
                "maintenance_cost": maintenance_cost,
                "licensing_cost": licensing_cost,
                "legal_compliance_cost": legal_compliance_cost,
                "office_utilities_cost": office_utilities_cost,
                "rd_cost": rd_cost,
                "yearly_investment": yearly_investment,
                "net_profit": net_profit,
                "cumulative_investment": cumulative_investment,
                "cumulative_revenue": cumulative_revenue,
                "cumulative_profit": cumulative_profit,
                "cumulative_op_cost": cumulative_op_cost,
                "roi": roi,
                "payback_achieved": payback_achieved
            })
        
        return pd.DataFrame(results)

def format_currency(value):
    """Format currency in Indonesian Rupiah"""
    if abs(value) >= 1e12:
        return f"Rp {value/1e12:.1f}T"
    elif abs(value) >= 1e9:
        return f"Rp {value/1e9:.1f}M"
    elif abs(value) >= 1e6:
        return f"Rp {value/1e6:.1f}Jt"
    else:
        return f"Rp {value:,.0f}"

def create_operational_cost_breakdown_chart(project_df, project_name, years):
    """Create operational cost breakdown chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(f"Operational Cost Breakdown (Year 1)", f"Cost Trend Over {years} Years", 
                       "Cost vs Revenue", f"Cost Structure Percentage (Year {years})"),
        specs=[[{"type": "pie"}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "pie"}]]
    )
    
    # Year 1 cost breakdown (Pie chart)
    year1_data = project_df.iloc[0]
    cost_categories = ["Personnel", "Infrastructure", "Marketing", "Maintenance", 
                      "Licensing", "Legal & Compliance", "Office & Utilities", "R&D"]
    cost_values = [
        year1_data["personnel_cost"], year1_data["infrastructure_cost"],
        year1_data["marketing_cost"], year1_data["maintenance_cost"],
        year1_data["licensing_cost"], year1_data["legal_compliance_cost"],
        year1_data["office_utilities_cost"], year1_data["rd_cost"]
    ]
    
    fig.add_trace(
        go.Pie(labels=cost_categories, values=cost_values, name="Year 1 Costs"),
        row=1, col=1
    )
    
    # Cost trend over years (Line chart)
    for category, column in zip(cost_categories, 
                               ["personnel_cost", "infrastructure_cost", "marketing_cost", 
                                "maintenance_cost", "licensing_cost", "legal_compliance_cost",
                                "office_utilities_cost", "rd_cost"]):
        fig.add_trace(
            go.Scatter(x=project_df["year"], y=project_df[column]/1e9, 
                      name=category, mode='lines'),
            row=1, col=2
        )
    
    # Cost vs Revenue comparison
    fig.add_trace(
        go.Bar(x=project_df["year"], y=project_df["revenue"]/1e9, name="Revenue", 
               marker_color="green", opacity=0.7),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=project_df["year"], y=project_df["operational_cost"]/1e9, name="Total Op Cost", 
               marker_color="red", opacity=0.7),
        row=2, col=1
    )
    
    # Final year cost structure (Pie chart)
    final_year_data = project_df.iloc[-1]
    cost_values_final = [
        final_year_data["personnel_cost"], final_year_data["infrastructure_cost"],
        final_year_data["marketing_cost"], final_year_data["maintenance_cost"],
        final_year_data["licensing_cost"], final_year_data["legal_compliance_cost"],
        final_year_data["office_utilities_cost"], final_year_data["rd_cost"]
    ]
    
    fig.add_trace(
        go.Pie(labels=cost_categories, values=cost_values_final, name=f"Year {years} Costs"),
        row=2, col=2
    )
    
    fig.update_layout(height=800, title_text=f"Analisis Biaya Operasional Detail: {project_name}")
    
    return fig

def create_operational_cost_input_form(project_key: str, project_name: str) -> Tuple[OperationalCosts, float]:
    """Create input form for operational costs and initial investment"""
    st.subheader(f"💰 Konfigurasi Biaya: {project_name}")
    
    default_costs = DEFAULT_OPERATIONAL_COSTS[project_key]
    default_investment = PROJECTS[project_key].initial_investment
    
    # Initial Investment Input (positioned above operational costs)
    st.write("**💸 Investasi Awal**")
    initial_investment = st.number_input(
        "Investasi Awal (Rp)",
        min_value=0,
        value=int(default_investment),
        step=50_000_000,
        key=f"{project_key}_initial_investment",
        help="Investasi awal untuk pengembangan proyek"
    )
    
    # Operational Costs Section
    st.write("**📋 Biaya Operasional**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**👥 SDM & Operasional**")
        personnel_cost = st.number_input(
            "Biaya SDM (Rp/tahun)",
            min_value=0,
            value=int(default_costs.personnel_cost),
            step=50_000_000,
            key=f"{project_key}_personnel",
            help="Gaji, tunjangan, training untuk semua karyawan"
        )
        
        office_utilities_cost = st.number_input(
            "Kantor & Utilitas (Rp/tahun)",
            min_value=0,
            value=int(default_costs.office_utilities_cost),
            step=10_000_000,
            key=f"{project_key}_office",
            help="Sewa kantor, listrik, internet, dll"
        )
        
        legal_compliance_cost = st.number_input(
            "Legal & Compliance (Rp/tahun)",
            min_value=0,
            value=int(default_costs.legal_compliance_cost),
            step=10_000_000,
            key=f"{project_key}_legal",
            help="Biaya hukum, audit, sertifikasi"
        )
        
        rd_cost = st.number_input(
            "Research & Development (Rp/tahun)",
            min_value=0,
            value=int(default_costs.rd_cost),
            step=25_000_000,
            key=f"{project_key}_rd",
            help="Riset produk baru, inovasi teknologi"
        )
    
    with col2:
        st.write("**🖥️ Teknologi & Infrastruktur**")
        infrastructure_cost = st.number_input(
            "Infrastruktur IT (Rp/tahun)",
            min_value=0,
            value=int(default_costs.infrastructure_cost),
            step=25_000_000,
            key=f"{project_key}_infra",
            help="Cloud, server, hosting, CDN"
        )
        
        licensing_cost = st.number_input(
            "Lisensi Software (Rp/tahun)",
            min_value=0,
            value=int(default_costs.licensing_cost),
            step=10_000_000,
            key=f"{project_key}_license",
            help="Lisensi tools, API, third-party services"
        )
        
        maintenance_cost = st.number_input(
            "Maintenance & Support (Rp/tahun)",
            min_value=0,
            value=int(default_costs.maintenance_cost),
            step=10_000_000,
            key=f"{project_key}_maintenance",
            help="Update sistem, bug fixes, technical support"
        )
        
        marketing_cost = st.number_input(
            "Marketing & Sales (Rp/tahun)",
            min_value=0,
            value=int(default_costs.marketing_cost),
            step=25_000_000,
            key=f"{project_key}_marketing",
            help="Digital marketing, sales team, promosi"
        )
    
    # Calculate and display total
    total_operational = (
        personnel_cost + infrastructure_cost + marketing_cost +
        maintenance_cost + licensing_cost + legal_compliance_cost +
        office_utilities_cost + rd_cost
    )
    
    st.metric("🎯 Total Biaya Operasional Tahun 1", format_currency(total_operational))
    st.metric("💸 Investasi Awal", format_currency(initial_investment))
    
    # Cost breakdown visualization
    cost_breakdown = {
        "Personnel": personnel_cost,
        "Infrastructure": infrastructure_cost,
        "Marketing": marketing_cost,
        "Maintenance": maintenance_cost,
        "Licensing": licensing_cost,
        "Legal & Compliance": legal_compliance_cost,
        "Office & Utilities": office_utilities_cost,
        "R&D": rd_cost
    }
    
    fig_breakdown = go.Figure(data=[go.Pie(
        labels=list(cost_breakdown.keys()),
        values=list(cost_breakdown.values()),
        hole=0.4
    )])
    fig_breakdown.update_layout(
        title=f"Breakdown Biaya Operasional - {project_name}",
        height=400
    )
    st.plotly_chart(fig_breakdown, use_container_width=True)
    
    return OperationalCosts(
        personnel_cost=personnel_cost,
        infrastructure_cost=infrastructure_cost,
        marketing_cost=marketing_cost,
        maintenance_cost=maintenance_cost,
        licensing_cost=licensing_cost,
        legal_compliance_cost=legal_compliance_cost,
        office_utilities_cost=office_utilities_cost,
        rd_cost=rd_cost
    ), initial_investment

def create_revenue_chart(data_dict, years):
    """Create revenue comparison chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(f"Revenue Growth Over {years} Years", f"Cumulative Profit Over {years} Years", 
                        "ROI Progression", "Investment vs Revenue"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = px.colors.qualitative.Set1
    
    for i, (project_key, df) in enumerate(data_dict.items()):
        project_name = PROJECTS[project_key].name
        color = colors[i % len(colors)]
        
        # Revenue Growth
        fig.add_trace(
            go.Scatter(x=df["year"], y=df["revenue"]/1e9, name=f"{project_name} - Revenue",
                      line=dict(color=color), legendgroup=project_name),
            row=1, col=1
        )
        
        # Cumulative Profit
        fig.add_trace(
            go.Scatter(x=df["year"], y=df["cumulative_profit"]/1e9, name=f"{project_name} - Profit",
                      line=dict(color=color, dash="dash"), legendgroup=project_name,
                      showlegend=False),
            row=1, col=2
        )
        
        # ROI Progression
        fig.add_trace(
            go.Scatter(x=df["year"], y=df["roi"], name=f"{project_name} - ROI",
                      line=dict(color=color, dash="dot"), legendgroup=project_name,
                      showlegend=False),
            row=2, col=1
        )
        
        # Investment vs Revenue (Cumulative)
        fig.add_trace(
            go.Scatter(x=df["cumulative_investment"]/1e9, y=df["cumulative_revenue"]/1e9,
                      mode='markers+lines', name=f"{project_name} - Inv vs Rev",
                      marker=dict(color=color), legendgroup=project_name,
                      showlegend=False),
            row=2, col=2
        )
    
    # Update layout
    fig.update_xaxes(title_text="Tahun", row=1, col=1)
    fig.update_xaxes(title_text="Tahun", row=1, col=2)
    fig.update_xaxes(title_text="Tahun", row=2, col=1)
    fig.update_xaxes(title_text="Cumulative Investment (Miliar Rp)", row=2, col=2)
    
    fig.update_yaxes(title_text="Revenue (Miliar Rp)", row=1, col=1)
    fig.update_yaxes(title_text="Cumulative Profit (Miliar Rp)", row=1, col=2)
    fig.update_yaxes(title_text="ROI (%)", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative Revenue (Miliar Rp)", row=2, col=2)
    
    fig.update_layout(height=700, title_text=f"Analisis Finansial Portfolio Proyek Digital ({years} Tahun)")
    
    return fig

def create_portfolio_summary(data_dict, years):
    """Create portfolio summary metrics"""
    portfolio_summary = []
    
    for project_key, df in data_dict.items():
        project = PROJECTS[project_key]
        final_year = df.iloc[-1]
        
        # Calculate payback period
        payback_year = None
        for _, row in df.iterrows():
            if row["cumulative_profit"] > 0:
                payback_year = str(row["year"])
                break
        payback_year = payback_year if payback_year else "N/A"
        
        portfolio_summary.append({
            "Project": project.name,
            "Initial Investment": df.iloc[0]["cumulative_investment"] - df.iloc[0]["yearly_investment"],
            f"{years}-Year Revenue": final_year["cumulative_revenue"],
            f"{years}-Year Profit": final_year["cumulative_profit"],
            f"Final ROI (%)": final_year["roi"],
            "Payback Period (Years)": payback_year,
            "Average Annual Revenue": final_year["cumulative_revenue"] / years
        })
    
    return pd.DataFrame(portfolio_summary)

def main():
    st.title("🚀 Simulasi Proyek Digital Portfolio - Dinamis")
    st.markdown("**Analisis Finansial Komprehensif untuk 5 Proyek Digital Strategis**")
    
    # Sidebar controls
    st.sidebar.header("🎛️ Pengaturan Simulasi")
    
    # Simulation years input
    simulation_years = st.sidebar.number_input(
        "Jumlah Tahun Simulasi",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
        key="simulation_years",
        help="Jumlah tahun untuk menjalankan simulasi proyek"
    )
    
    # Scenario selection
    scenario = st.sidebar.selectbox(
        "Pilih Skenario:",
        ["optimistic", "realistic", "pessimistic"],
        index=1,
        format_func=lambda x: {
            "optimistic": "🟢 Optimis",
            "realistic": "🟡 Realistis",
            "pessimistic": "🔴 Pesimis"
        }[x],
        key="scenario_select"
    )
    
    # Project selection
    st.sidebar.subheader("Pilih Proyek untuk Analisis:")
    selected_projects = {}
    for key, project in PROJECTS.items():
        selected_projects[key] = st.sidebar.checkbox(
            f"{project.name}",
            value=True,
            key=f"checkbox_{key}"
        )
    
    # Advanced settings
    with st.sidebar.expander("⚙️ Pengaturan Lanjutan"):
        inflation_rate = st.slider("Tingkat Inflasi (%)", 0.0, 10.0, 3.5, key="inflation_slider") / 100
        tax_rate = st.slider("Tingkat Pajak (%)", 0.0, 30.0, 22.0, key="tax_slider") / 100
        discount_rate = st.slider("Discount Rate (%)", 0.0, 15.0, 8.0, key="discount_slider") / 100
    
    # Operational Cost Configuration
    st.sidebar.subheader("💰 Konfigurasi Biaya")
    use_custom_costs = st.sidebar.checkbox("Gunakan Biaya Kustom", value=False, key="custom_costs_checkbox")
    
    custom_operational_costs = {}
    
    if use_custom_costs:
        st.header("📋 Konfigurasi Biaya Operasional Detail")
        st.markdown("Sesuaikan biaya operasional dan investasi awal untuk setiap proyek sesuai kondisi spesifik Anda")
        
        tabs = st.tabs([PROJECTS[key].name for key in selected_projects.keys() if selected_projects[key]])
        
        tab_keys = [key for key in selected_projects.keys() if selected_projects[key]]
        
        for i, tab in enumerate(tabs):
            with tab:
                if i < len(tab_keys):
                    project_key = tab_keys[i]
                    project_name = PROJECTS[project_key].name
                    custom_operational_costs[project_key] = create_operational_cost_input_form(
                        project_key, project_name
                    )
    
    # Generate simulations
    if st.sidebar.button("🔄 Jalankan Simulasi", type="primary", key="run_simulation"):
        st.session_state.simulation_run = True
        st.session_state.simulation_custom_costs = custom_operational_costs if use_custom_costs else {}
    
    if not hasattr(st.session_state, 'simulation_run'):
        st.session_state.simulation_run = False
        st.session_state.simulation_custom_costs = {}
    
    if st.session_state.simulation_run:
        # Run simulations
        simulation_data = {}
        
        progress_bar = st.progress(0.0)
        status_text = st.empty()
        
        # Count total selected projects
        total_selected = sum(selected_projects.values())
        if total_selected == 0:
            st.error("Pilih setidaknya satu proyek untuk menjalankan simulasi.")
            return
        
        current_selected = 0
        
        for project_key, selected in selected_projects.items():
            if selected:
                current_selected += 1
                status_text.text(f"Memproses {PROJECTS[project_key].name}...")
                
                # Create a copy of the project data with custom values if provided
                project_data = PROJECTS[project_key]
                custom_costs = None
                custom_investment = project_data.initial_investment
                
                if use_custom_costs and project_key in st.session_state.simulation_custom_costs:
                    custom_costs, custom_investment = st.session_state.simulation_custom_costs[project_key]
                
                # Create modified project data with custom investment
                modified_project = ProjectData(
                    name=project_data.name,
                    initial_investment=custom_investment,
                    annual_revenue_year1=project_data.annual_revenue_year1,
                    annual_growth_rate=project_data.annual_growth_rate,
                    operational_cost_rate=project_data.operational_cost_rate,
                    development_months=project_data.development_months,
                    market_risk_factor=project_data.market_risk_factor,
                    competition_impact=project_data.competition_impact,
                    operational_costs=project_data.operational_costs
                )
                
                simulator = ProjectSimulator(modified_project, scenario, custom_costs, years=simulation_years)
                df = simulator.calculate_yearly_metrics()
                
                # Apply inflation and tax adjustments
                df["revenue"] = df["revenue"] / ((1 + inflation_rate) ** df["year"])
                df["net_profit"] = df["net_profit"] * (1 - tax_rate)
                df["cumulative_profit"] = df["cumulative_profit"] * (1 - tax_rate)
                
                simulation_data[project_key] = df
                
                # Update progress bar
                progress_value = min(current_selected / total_selected, 1.0)
                progress_bar.progress(progress_value)
        
        status_text.text("Simulasi selesai!")
        
        if simulation_data:
            # Main dashboard
            col1, col2, col3, col4 = st.columns(4)
            
            # Calculate portfolio totals
            total_investment = sum(df.iloc[0]["cumulative_investment"] - df.iloc[0]["yearly_investment"] for df in simulation_data.values())
            total_n_year_revenue = sum(df.iloc[-1]["cumulative_revenue"] for df in simulation_data.values())
            total_n_year_profit = sum(df.iloc[-1]["cumulative_profit"] for df in simulation_data.values())
            portfolio_roi = (total_n_year_profit / total_investment) * 100 if total_investment > 0 else 0
            
            with col1:
                st.metric("Total Investment", format_currency(total_investment))
            with col2:
                st.metric(f"{simulation_years}-Year Revenue", format_currency(total_n_year_revenue))
            with col3:
                st.metric(f"{simulation_years}-Year Profit", format_currency(total_n_year_profit))
            with col4:
                st.metric("Portfolio ROI", f"{portfolio_roi:.1f}%")
            
            # Charts
            st.plotly_chart(create_revenue_chart(simulation_data, simulation_years), use_container_width=True)
            
            # Portfolio Summary Table
            st.subheader("📊 Ringkasan Portfolio")
            portfolio_df = create_portfolio_summary(simulation_data, simulation_years)
            
            # Format the dataframe for display
            display_df = portfolio_df.copy()
            for col in ["Initial Investment", f"{simulation_years}-Year Revenue", f"{simulation_years}-Year Profit", "Average Annual Revenue"]:
                display_df[col] = display_df[col].apply(format_currency)
            
            st.dataframe(display_df, use_container_width=True)
            
            # Detailed project analysis
            st.subheader("🔍 Analisis Detail per Proyek")
            
            selected_project_key = st.selectbox(
                "Pilih proyek untuk analisis detail:",
                list(simulation_data.keys()),
                format_func=lambda x: PROJECTS[x].name,
                key="project_select"
            )
            
            if selected_project_key:
                project_df = simulation_data[selected_project_key]
                project = PROJECTS[selected_project_key]
                
                # Project details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**{project.name}**")
                    st.write(f"Investasi Awal: {format_currency(project_df.iloc[0]['cumulative_investment'] - project_df.iloc[0]['yearly_investment'])}")
                    st.write(f"Periode Development: {project.development_months} bulan")
                    st.write(f"Growth Rate: {project.annual_growth_rate*100:.1f}%")
                
                with col2:
                    final_metrics = project_df.iloc[-1]
                    st.write(f"Revenue Tahun {simulation_years}: {format_currency(final_metrics['revenue'])}")
                    st.write(f"Total Profit: {format_currency(final_metrics['cumulative_profit'])}")
                    st.write(f"ROI Final: {final_metrics['roi']:.1f}%")
                
                # Yearly breakdown chart
                fig_detail = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=("Revenue vs Costs", "Cumulative Metrics")
                )
                
                # Revenue vs Costs
                fig_detail.add_trace(
                    go.Bar(x=project_df["year"], y=project_df["revenue"]/1e9, name="Revenue", marker_color="green"),
                    row=1, col=1
                )
                fig_detail.add_trace(
                    go.Bar(x=project_df["year"], y=project_df["operational_cost"]/1e9, name="Operational Cost", marker_color="red"),
                    row=1, col=1
                )
                
                # Cumulative metrics
                fig_detail.add_trace(
                    go.Scatter(x=project_df["year"], y=project_df["cumulative_revenue"]/1e9, name="Cumulative Revenue", line=dict(color="blue")),
                    row=1, col=2
                )
                fig_detail.add_trace(
                    go.Scatter(x=project_df["year"], y=project_df["cumulative_profit"]/1e9, name="Cumulative Profit", line=dict(color="green")),
                    row=1, col=2
                )
                
                fig_detail.update_xaxes(title_text="Tahun")
                fig_detail.update_yaxes(title_text="Miliar Rupiah")
                fig_detail.update_layout(height=400, title_text=f"Analisis Detail: {project.name}")
                
                st.plotly_chart(fig_detail, use_container_width=True)
                
                # Yearly data table
                with st.expander("📋 Data Tahunan Detail"):
                    display_project_df = project_df.copy()
                    for col in ["revenue", "operational_cost", "net_profit", "cumulative_revenue", "cumulative_profit"]:
                        display_project_df[col] = display_project_df[col].apply(format_currency)
                    display_project_df["roi"] = display_project_df["roi"].apply(lambda x: f"{x:.1f}%")
                    
                    st.dataframe(display_project_df, use_container_width=True)
                
                # Operational cost breakdown chart
                st.plotly_chart(create_operational_cost_breakdown_chart(project_df, project.name, simulation_years), use_container_width=True)
            
            # Risk Analysis
            st.subheader("⚠️ Analisis Risiko")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Faktor Risiko Utama:**")
                st.write("• Kompetisi pasar yang meningkat")
                st.write("• Perubahan regulasi teknologi")
                st.write("• Fluktuasi ekonomi global")
                st.write("• Ketersediaan talent teknis")
                st.write("• Adopsi teknologi oleh pasar")
            
            with col2:
                st.write("**Rekomendasi Mitigasi:**")
                st.write("• 🔄 Diversifikasi portfolio proyek")
                st.write("• 🤝 Partnership strategis")
                st.write("• 📚 Continuous innovation")
                st.write("• 👥 Strong talent pipeline")
                st.write("• 📊 Regular market analysis")
            
            # Download results
            st.subheader("💾 Export Hasil")
            
            # Prepare combined data for export
            combined_data = []
            for project_key, df in simulation_data.items():
                project_data = df.copy()
                project_data["project"] = PROJECTS[project_key].name
                combined_data.append(project_data)
            
            export_df = pd.concat(combined_data, ignore_index=True)
            
            col1, col2 = st.columns(2)
            with col1:
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Data CSV",
                    data=csv,
                    file_name=f"simulasi_proyek_digital_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_data_csv"
                )
            
            with col2:
                summary_csv = portfolio_df.to_csv(index=False)
                st.download_button(
                    label="📋 Download Summary CSV",
                    data=summary_csv,
                    file_name=f"summary_portfolio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_summary_csv"
                )
    
    else:
        # Initial state - show project overview
        st.header("📋 Overview Proyek")
        
        overview_data = []
        for key, project in PROJECTS.items():
            overview_data.append({
                "Proyek": project.name,
                "Investasi Awal": format_currency(project.initial_investment),
                "Revenue Tahun 1": format_currency(project.annual_revenue_year1),
                "Growth Rate": f"{project.annual_growth_rate*100:.1f}%",
                "Development": f"{project.development_months} bulan",
                "Market Risk": f"{project.market_risk_factor*100:.1f}%"
            })
        
        overview_df = pd.DataFrame(overview_data)
        st.dataframe(overview_df, use_container_width=True)
        
        st.info("👆 Atur parameter di sidebar dan klik 'Jalankan Simulasi' untuk memulai analisis")

if __name__ == "__main__":
    main()