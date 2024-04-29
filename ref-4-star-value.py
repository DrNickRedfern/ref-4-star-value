import pandas as pd
from skimpy import clean_columns
import streamlit as st

def four_star_value(
    mainstream_allocation: int | float,
    outputs_required: int,
    three_star_activity: int | float,
    four_star_activity: int | float
    ) -> float:
    """
    Calculate the value of a four star output or impact case study.
    
    Parameters:
        mainstream_allocation (int | float): The total mainstream QR funding allocation.
        outputs_required (int): The number of outputs required to be returned for the sub-profile.
        three_star_activity (float): The percentage of three star activity.
        four_star_activity (float): The percentage of four star activity.
    
    Returns:
        float: The value of a four star output or impact case study.
    """
    denominator = (4 * (outputs_required * (four_star_activity / 100))) + (outputs_required * (three_star_activity / 100))
    
    value = round(4 * (mainstream_allocation / denominator), 2)
    
    return value

st.title('REF 4 Star value calculator')

st.markdown('''
This app calculates the value of 4 star research outputs and impact case studies using the 
method described in Jon Collett's [blog post](https://www.fasttrackimpact.com/post/how-much-are-ref2021-4-impact-case-studies-and-4-outputs-worth).
''')

# can't get latex working at all
# st.markdown('''
# ## Calculating the value of a single 4 star in a sub-profile
# The formula for calculating the value of a single 4 star impact case study is:
# ''')
# st.latex(r'''
# \text{4* ICS value} = 4 \times \frac{\text{Mainstream QR allocation}}{]\left 4 \times \text{Outputs required} \times \left\frac{\text{4* output score}}{100}\right \right + \left\text{Outputs required} \times \left\frac{\text{3* output score}}{100}\right \right}'
# ''')

st.markdown('''
## Data format

To calculate the annual value of a 4 star output or impact case study, upload a csv file with the following columns:

- Main panel
- Unit of Assessment
- Sub-profile
- Percentage of activity rated 3*
- Percentage of activity rated 4*
- Mainstream QR allocation
- Required number of items to be returned for sub-profile

*Please note*: the columns in the csv file must have **exactly** the same names as listed above.
 
''')

st.sidebar.header('Upload your data')
uploaded_file = st.sidebar.file_uploader('CSV files only', type=['csv'], accept_multiple_files=False)

if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
       df = pd.read_csv(file)
       return df
    
    df = load_data(uploaded_file)
    df = clean_columns(df)
    
    # TODO check the uploaded csv file has the correct column names
    
    df = df.rename(columns = {'required_number_of_items_to_be_returned_for_sub_profile': 'outputs_required'})
    
    df['four_star_value_of_item_in_subprofile'] = df.apply(lambda df: four_star_value(df['mainstream_qr_allocation'], 
                                                                                      df['outputs_required'], 
                                                                                      df['percentage_of_research_activity_rated_3'], 
                                                                                      df['percentage_of_research_activity_rated_4']), 
                                                           axis=1)
    
    if st.sidebar.button('Calculate value'):
        st.dataframe(df)

        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False)

        st.download_button('Download formatted csv file', 
                           data=convert_df_to_csv(df), 
                           file_name='four_star_value.csv', 
                           mime='text/csv', 
                           key='download-formatted-csv')