# Data Dictionary: Airport Data

## Description

The raw files contain historical (time-based) information on airports used throughout the aviation databases. It provides a list of domestic and foreign airport codes and their associated world area code, country information, state information (if applicable), city name, airport name, city market information, and latitude and longitude information.

## Source

Source: [Bureau of Transportation Statistics - Aviation Support Tables : Master Coordinate](https://www.transtats.bts.gov/Fields.asp?table_id=288)

## Dictionary

|	Field Name	|	Description	|
|	---------	|	---------	|
|	AirportSeqID	|	An identification number assigned by US DOT to identify a unique airport at a given point of time. Airport attributes, such as airport name or coordinates, may change over time.	|
|	AirportID	|	An identification number assigned by US DOT to identify a unique airport. Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused.	|
|	Airport	|	A three character alpha-numeric code issued by the U.S. Department of Transportation which is the official designation of the airport. The airport code is not always unique to a specific airport because airport codes can change or can be reused.	|
|	AirportName	|	Airport Name	|
|	AirportCityName	|	Airport City Name with either U.S. State or Country	|
|	AirportWacSeqID2	|	Unique Identifier for a World Area Code (WAC) at a given point of time for the Physical Location of the Airport. See World Area Codes support table.	|
|	AirportWac	|	World Area Code for the Physical Location of the Airport	|
|	AirportCountryName	|	Country Name for the Physical Location of the Airport	|
|	AirportCountryCodeISO	|	Two-character ISO Country Code for the Physical Location of the Airport	|
|	AirportStateName	|	State Name for the Physical Location of the Airport	|
|	AirportStateCode	|	State Abbreviation for the Physical Location of the Airport	|
|	AirportStateFips	|	FIPS (Federal Information Processing Standard) State Code for the Physical Location of the Airport	|
|	CityMarketSeqID	|	An identification number assigned by US DOT to identify a city market at a given point of time. City Market attributes may change over time. For example the country associated with the city market can change over time due to geopolitical changes.	|
|	CityMarketID	|	An identification number assigned by US DOT to identify a city market. Use this field to consolidate airports serving the same city market.	|
|	CityMarketName	|	City Market Name with either U.S. State or Country	|
|	CityMarketWacSeqID2	|	Unique Identifier for a World Area Code (WAC) at a given point of time for the City Market. See World Area Codes support table.	|
|	CityMarketWac	|	World Area Code for the City Market	|
|	LatDegrees	|	Latitude, Degrees	|
|	LatHemisphere	|	Latitude, Hemisphere	|
|	LatMinutes	|	Latitude, Minutes	|
|	LatSeconds	|	Latitude, Seconds	|
|	Latitude	|	Latitude	|
|	LonDegrees	|	Longitude, Degrees	|
|	LonHemisphere	|	Longitude, Hemisphere	|
|	LonMinutes	|	Longitude, Minutes	|
|	LonSeconds	|	Longitude, Seconds	|
|	Longitude	|	Longitude	|
|	UTCLocalTimeVariation	|	Time Zone at the Airport	|
|	AirportStartDate	|	Start Date of Airport Attributes	|
|	AirportEndDate	|	End Date of Airport Attributes (Active = NULL)	|
|	AirportIsClosed	|	Indicates if the airport is closed (1 = Yes). If yes, the airport is closed is on the AirportEndDate.	|
|	AirportIsLatest	|	Indicates if this row contains the latest attributes for the Airport (1 = Yes)	|