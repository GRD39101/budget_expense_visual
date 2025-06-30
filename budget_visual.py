import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title
st.title('Budget Visualizer Project')

# Header and subheader
st.header('Visualize your budget monthly expenses')
st.subheader('The goal of this project is to visualize your monthly expenses in a pie chart and bar chart.')

def subscription_name():
    subscription_name = st.text_input('Enter the name of the subscription:')
    return subscription_name

def subscription_cost():
    subscription_cost = st.number_input('Enter the cost of the subscription:', min_value=0.0, format="%.2f")
    return subscription_cost

def main():
    # Initialize session state for storing multiple subscriptions
    if 'subscriptions' not in st.session_state:
        st.session_state.subscriptions = []
    
    # Create two columns for input form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        subscription_name_input = subscription_name()
        subscription_cost_input = subscription_cost()
    
    with col2:
        st.write("")  # Add spacing
        st.write("")  # Add spacing
        add_button = st.button('➕ Add Subscription', type='primary')
    
    # Add subscription when button is clicked
    if add_button:
        if subscription_name_input and subscription_cost_input > 0:
            # Check if subscription already exists
            existing_names = [sub['name'].lower() for sub in st.session_state.subscriptions]
            if subscription_name_input.lower() in existing_names:
                st.warning(f'⚠️ {subscription_name_input} already exists! Please use a different name or remove the existing one first.')
            else:
                # Add to session state
                st.session_state.subscriptions.append({
                    'name': subscription_name_input,
                    'cost': subscription_cost_input
                })
                st.success(f'✅ Added {subscription_name_input} - ${subscription_cost_input:.2f} to your budget!')
                st.rerun()
        else:
            st.error('❌ Please enter both subscription name and cost!')
    
    # Display current subscription being entered (preview)
    if subscription_name_input and subscription_cost_input > 0:
        st.info(f'💡 Ready to add: {subscription_name_input} - ${subscription_cost_input:.2f}')
    
    # Display all subscriptions if any exist
    if st.session_state.subscriptions:
        st.divider()
        st.subheader('📋 Your Monthly Subscriptions')
        
        # Calculate total first
        total = sum(sub['cost'] for sub in st.session_state.subscriptions)
        
        # Display total prominently
        st.metric("💰 Total Monthly Cost", f"${total:.2f}", delta=f"{len(st.session_state.subscriptions)} subscriptions")
        
        # Display detailed list
        st.subheader('📝 Detailed List:')
        
        # Create a nice formatted list
        for i, sub in enumerate(st.session_state.subscriptions, 1):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**{i}. {sub['name']}**")
            
            with col2:
                st.write(f"${sub['cost']:.2f}")
            
            with col3:
                if st.button('🗑️', key=f'delete_{i}'):
                    st.session_state.subscriptions.pop(i-1)
                    st.success(f'Removed {sub["name"]}!')
                    st.rerun()
        
        # Create DataFrame for visualizations
        df = pd.DataFrame(st.session_state.subscriptions)
        
        # Display as a nice table
        st.subheader('📊 Summary Table:')
        # Format the DataFrame for better display
        df_display = df.copy()
        df_display['cost'] = df_display['cost'].apply(lambda x: f"${x:.2f}")
        df_display.columns = ['Subscription Name', 'Monthly Cost']
        df_display.index = range(1, len(df_display) + 1)
        
        st.dataframe(df_display, use_container_width=True)
        
        # Add percentage breakdown
        st.subheader('📈 Cost Breakdown:')
        for sub in st.session_state.subscriptions:
            percentage = (sub['cost'] / total) * 100
            st.write(f"• **{sub['name']}**: ${sub['cost']:.2f} ({percentage:.1f}% of total)")
        
        # Create visualizations
        st.divider()
        st.subheader('📊 Visual Analysis')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('🥧 Distribution Pie Chart')
            fig_pie = px.pie(df, values='cost', names='name', 
                           title='Budget Distribution by Subscription')
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader('📊 Cost Comparison Bar Chart')
            fig_bar = px.bar(df, x='name', y='cost', 
                           title='Monthly Subscription Costs',
                           color='cost',
                           color_continuous_scale='viridis')
            fig_bar.update_xaxes(tickangle=45)
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Additional insights
        st.subheader('💡 Budget Insights:')
        avg_cost = total / len(st.session_state.subscriptions)
        most_expensive = max(st.session_state.subscriptions, key=lambda x: x['cost'])
        cheapest = min(st.session_state.subscriptions, key=lambda x: x['cost'])
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            st.metric("Average Cost", f"${avg_cost:.2f}")
        
        with insight_col2:
            st.metric("Most Expensive", f"{most_expensive['name']}", f"${most_expensive['cost']:.2f}")
        
        with insight_col3:
            st.metric("Cheapest", f"{cheapest['name']}", f"${cheapest['cost']:.2f}")
        
        # Yearly projection
        yearly_total = total * 12
        st.info(f"💸 **Yearly Projection**: You'll spend approximately **${yearly_total:.2f}** per year on these subscriptions!")
    
    # Clear all button
    if st.session_state.subscriptions:
        st.divider()
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button('🗑️ Clear All', type='secondary'):
                st.session_state.subscriptions = []
                st.success('All subscriptions cleared!')
                st.rerun()
        with col2:
            st.write("")  # Empty space
    
    else:
        # Show example when no subscriptions
        st.info("👋 **Get Started!** Add your first subscription above. For example:\n- Netflix: $15.49\n- Spotify: $9.99\n- Hulu: $5.99")
        
        # Add sample data button
        if st.button('📝 Add Sample Data'):
            st.session_state.subscriptions = [
                {'name': 'Netflix', 'cost': 15.49},
                {'name': 'Spotify', 'cost': 9.99},
                {'name': 'Hulu', 'cost': 5.99},
                {'name': 'Disney+', 'cost': 7.99},
                {'name': 'Amazon Prime', 'cost': 14.99}
            ]
            st.success('Sample data added!')
            st.rerun()

if __name__ == "__main__":
    main()