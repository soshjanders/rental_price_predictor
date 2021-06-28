import streamlit as st
import numpy as np
import pandas as pd
import pickle
import pgeocode
import pydeck as pdk

property_type_Aparthotel = 0
property_type_Apartment = 0
property_type_Bed_and_breakfast = 0
property_type_Boutique_hotel = 0
property_type_Bungalow = 0
property_type_Cabin = 0
property_type_Camper_RV = 0
property_type_Castle = 0
property_type_Condominium = 0
property_type_Cottage = 0
property_type_Dome_house = 0
property_type_Earth_house = 0
property_type_Guest_suite = 0
property_type_Guesthouse = 0
property_type_Hostel = 0
property_type_Hotel = 0
property_type_House = 0
property_type_Hut = 0
property_type_In_law = 0
property_type_Loft = 0
property_type_Other = 0
property_type_Resort = 0
property_type_Serviced_apartment = 0
property_type_Tiny_house = 0
property_type_Townhouse = 0
property_type_Villa = 0
room_type_Entire_home_apt = 0
room_type_Hotel_room = 0
room_type_Private_room = 0
room_type_Shared_room = 0 

zip_df = pd.DataFrame(data=[[0,0]], columns=['lat', 'lon'])


def map(lat, lon):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": 12,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
            "ScatterplotLayer",
            zip_df,       
            pickable=True,
            get_radius = 500,
            opacity = 0.4,
            get_position= ['lon', 'lat'],
            get_fill_color=[0,0,139],
),
        ]
    ))

def predict_price(x,y,z,a,b,c):
    #zip_code, accommodates, bathrooms, bedrooms, beds,
  #     deposit,
        
        var_data = [[property_type_Aparthotel,
       property_type_Apartment, property_type_Bed_and_breakfast,
       property_type_Boutique_hotel, property_type_Bungalow,
       property_type_Cabin, property_type_Camper_RV,
       property_type_Castle, property_type_Condominium,
       property_type_Cottage, property_type_Dome_house,
       property_type_Earth_house, property_type_Guest_suite,
       property_type_Guesthouse, property_type_Hostel,
       property_type_Hotel, property_type_House, property_type_Hut,
       property_type_In_law,property_type_Loft, property_type_Other,
       property_type_Resort, property_type_Serviced_apartment,
       property_type_Tiny_house, property_type_Townhouse,
       property_type_Villa, room_type_Entire_home_apt,
       room_type_Hotel_room, room_type_Private_room,
       room_type_Shared_room]]


        string_data=['property_type_Aparthotel',
       'property_type_Apartment', 'property_type_Bed and breakfast',
       'property_type_Boutique hotel', 'property_type_Bungalow',
       'property_type_Cabin', 'property_type_Camper/RV',
       'property_type_Castle', 'property_type_Condominium',
       'property_type_Cottage', 'property_type_Dome house',
       'property_type_Earth house', 'property_type_Guest suite',
       'property_type_Guesthouse', 'property_type_Hostel',
       'property_type_Hotel', 'property_type_House', 'property_type_Hut',
       'property_type_In-law', 'property_type_Loft', 'property_type_Other',
       'property_type_Resort', 'property_type_Serviced apartment',
       'property_type_Tiny house', 'property_type_Townhouse',
       'property_type_Villa', 'room_type_Entire home/apt',
       'room_type_Hotel room', 'room_type_Private room',
       'room_type_Shared room']

        position = 0
        for i in string_data:
            if i == property_type:
                position = string_data.index(i)
                #st.write(position)
                var_data[0][position] = 1
            if i == room_type:
                position = string_data.index(i)
                #st.write(position)
                var_data[0][position] = 1

     

        var_data[0].insert(0, zip_code)
        var_data[0].insert(1, accommodates)
        var_data[0].insert(2, bathrooms)
        var_data[0].insert(3, bedrooms)
        var_data[0].insert(4, beds)
        var_data[0].insert(5, deposit)


        df = pd.DataFrame(data=var_data, columns = ['zipcode', 'accommodates', 'bathrooms', 'bedrooms', 'beds',
       'security_deposit', 'property_type_Aparthotel',
       'property_type_Apartment', 'property_type_Bed and breakfast',
       'property_type_Boutique hotel', 'property_type_Bungalow',
       'property_type_Cabin', 'property_type_Camper/RV',
       'property_type_Castle', 'property_type_Condominium',
       'property_type_Cottage', 'property_type_Dome house',
       'property_type_Earth house', 'property_type_Guest suite',
       'property_type_Guesthouse', 'property_type_Hostel',
       'property_type_Hotel', 'property_type_House', 'property_type_Hut',
       'property_type_In-law', 'property_type_Loft', 'property_type_Other',
       'property_type_Resort', 'property_type_Serviced apartment',
       'property_type_Tiny house', 'property_type_Townhouse',
       'property_type_Villa', 'room_type_Entire home/apt',
       'room_type_Hotel room', 'room_type_Private room',
       'room_type_Shared room'])


        #st.dataframe(df)


        Pkl_Filename = "Pickle_RF_Model.pkl" 
        # Load the Model back from file
        with open(Pkl_Filename, 'rb') as file:  
            Pickled_RF_Model = pickle.load(file)


        x_predict = df.values

        #st.dataframe(x_predict)
        y_pred = Pickled_RF_Model.predict(x_predict)

        value_of_rental = np.exp(y_pred)

        st.header('You could list your house for: $%d a night' % (value_of_rental))




st.set_page_config(layout='wide')
st.header('Vacation Rental Calculator')
with st.form("my_form"):

    col1, col2, col3, col4 = st.beta_columns(4)
    with col1:
        zip_code = st.number_input('Zip Code', value = 90210, format='%d')
        bathrooms = st.number_input('Bathrooms', value=2, format='%d')
    with col2:
        property_type = st.selectbox('Property Type', ['property_type_Aparthotel',
       'property_type_Apartment', 'property_type_Bed and breakfast',
       'property_type_Boutique hotel', 'property_type_Bungalow',
       'property_type_Cabin', 'property_type_Camper/RV',
       'property_type_Castle', 'property_type_Condominium',
       'property_type_Cottage', 'property_type_Dome house',
       'property_type_Earth house', 'property_type_Guest suite',
       'property_type_Guesthouse', 'property_type_Hostel',
       'property_type_Hotel', 'property_type_House', 'property_type_Hut',
       'property_type_In-law', 'property_type_Loft', 'property_type_Other',
       'property_type_Resort', 'property_type_Serviced apartment',
       'property_type_Tiny house', 'property_type_Townhouse',
       'property_type_Villa'])
        bedrooms = st.number_input('Bedrooms', value=3, format='%d')
    with col3:
        room_type =  st.selectbox('Room Type', ['room_type_Entire home/apt',
       'room_type_Hotel room', 'room_type_Private room',
       'room_type_Shared room'])
        beds = st.number_input('Beds', value=3, format='%d')


    with col4:
        accommodates = st.number_input('Accomadates', value=2, format='%d' )
        deposit = st.number_input('Security-Deposit(dollars)', value=100, format='%d')
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:

        st.write("zip Code:", zip_code, 'Room Type:' , room_type, 'Property Type: ', property_type, 'accommodates: ', accommodates,
         'Security Deposit: ', deposit, 'Beds: ', beds)
        
        predict_price(zip_code, room_type, property_type, accommodates, deposit, beds)
        nomi = pgeocode.Nominatim('us')
        zip_df = nomi.query_postal_code(zip_code)
        lat = zip_df['latitude']
        lon = zip_df['longitude']
        zip_df = pd.DataFrame(data=[[lat, lon]], columns=['lat', 'lon'])
        map(lat, lon)




#Create dummy room types
#Need to exponentiate prediction value

#st.write(zip_df)
