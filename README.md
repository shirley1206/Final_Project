Data source:
	
	U of m off campus housing: https://offcampushousing.umich.edu/
	
	Google place API: get geo coordinate information for each housing

Code structure:

Housing_final.py: 

	Get_housing(): scrape from the u of m off campus housing site.
	
	Create_housing_database(): create tables.
	
	Populate_housing_database(): insert data into database.

Model.py: 

	get housing(): access the database based on the input criteria to generate output. 
	
	maponplotly(): make a scatter plot on plotly for the results, on hover shows title, address and rent info.
	
	graph(): calculate housing numbers for the results and generate a pie chart for different buildingtypes.
	
	bar(): calculate average rent for the results and generate a bar chart for different buildingtypes.

User guide:

	RUN app.py to start and go to local host (/search)

On the html interface('/search'), a user can choose to use search or filters to get the off campus housing result. Click on the button "list view", "map view" or "graphs" to see different types of data presentation.




***Plotly installation info:

To install Plotly's python package, use the package manager pip inside your terminal.
	
	$ pip install plotly 
	or 
	$ sudo pip install plotly 

