# __Vsm Rest Api Documentation__

A basic rest API developed using the Django restful framework to handle some basic and complex functionalities and to provide seamless communications to the frontend client App.

### Api EndPoint - <https://prerox-api-8d59017b6b2c.herokuapp.com/>

---

> ### __Register Store__: *<store/register>*<br>
> - register a new store.<br>
> **Request Body:<br>**
> >{<br>
"uid": "jWMfUafBI5PheP3qndE1Dec7vwo1",<br>
"store_name": "SpaceX",<br>
"owner": "Elon Musk",<br>
"description": "Space Exploration Technologies Corp, manufactures and launches advanced rockets and spacecraft.",<br>
"email": "elonmusk@gmail.com",<br>
"contact_no": "(202) 649-2722",<br>
"pricing": {"one_side":  [1,5], "double_side": [5,10] }, <br>
"address": "1 Rocket Road, Hawthorne, California, 90250",<br>
"lat": 12.969872242527739,<br>
"long": 77.62446195242269,<br><br>
"gmap_link": "<https://maps.app.goo.gl/qC4L2YosoVzFLS7CA>"<br>
}
>
> **Response:**<br>
> > {"success": "Your store has been registered successfully."}
> 

---

> ### __Get, Update & delete Store:__ *</store/>*
> > __Parameters:__
> > - (required) ***uid*** - user id of the store account from firebase.
> 
> - __GET request -__ returns the store instance. 
> 
> - __PUT request body:__
> > {<br>
> ...<br>
> "field_name": new_value,<br>
> "field_name2": new_value,<br>
> ...<br>
> }
> 
> - **DELETE request** - permanently remove the store instance.
>

---
> ### __Get Stores List:__ *</store/list>*
> - returns all the stores account in the database. 
> - Also Filtering the list of stores with specific parameters.  
> > __Parameters:__
> > - (optional) ***lat*** - latitude  
> > - (optional) ***long*** - longitude  
> > - (optional) ***rad*** - radius of area in meters.  
> 

---

> ### __Get Orders List:__ *</store/order/list>*
> - return all the orders for the specified store.
> > __Parameters:__
> > - (required) ***uid*** - user id of the store.

---

> ### __Create, Get, Update & Delete an order:__ *</store/order/list>*
> - Perform CRUD operations for a specific order from the particular store.
> > __Parameters:__
> > - (required) ***uid*** - user id of the store.
> > - (required) ***ref_id*** - reference id of the particular order. (not for post-request)
> - __GET-request -__ returns the specific order.
> 
> - __POST-request body:__
> > __Form-Data:__<br>
> > - ***store_uid*** - user id of the store.
> > - ***name*** - name of the customer. 
> > - ***contact_no*** - phone number of customer.  
> > - ***xerox-type*** - type of print.  
> > - ***copies*** - number of copies.  
> > - ***files*** - uploaded files.   
> 
> - __PUT-request body:__
> > {<br>
> status: newBoolValue,<br>
> accepted: newBoolValue<br>}
> - __DELETE-request -__ removes the specific order from the store.
"# vsm_restapi" 
> > - __URLpatterns__ 
> > -    path('store/register/', register_store, name='store_registration'),  # POST
> > -    path('store', StoreProfile.as_view(), name='store_profile'),  # GET, PUT, DELETE
> > -    path('store/list', get_stores, name='store_list'),  # GET
> > -    path('store/order', StoreOrder.as_view(), name='store_view'),  # POST, GET, PUT, DELETE
> > -    path('store/order/list', get_store_orders, name="store_orders_list"),  # GET
> > -    path('store/order/download/<int:ref_id>', generate_files, name='download_files'),
> > -    path('get-location', get_location, name="get-location"),

