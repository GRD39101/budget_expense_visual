import streamlit as st

#tite
st.title('Budget Visualizer Project')
# header and subheader
st.header('Visualize your budget monthly expenses')
st.subheader('The goal of this project is to visualize your monthly expenses in a pie chart and bar chart.')
def subscription_name():
    subscription_name = st.text_input('Enter the name of the subscription:')

    return subscription_name
def subscription_cost():
    subscription_cost = st.number_input('Enter the cost of the subscription:', min_value=0.0, format="%.2f")
    return subscription_cost


def main():
    subscription_name_input = subscription_name()
    subscription_cost_input = subscription_cost()
    print(f'{subscription_name} cost ${subscription_cost}')

    # Do something with the inputs (e.g., create a chart)

if __name__ == "__main__":
    main()
