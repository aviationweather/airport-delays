# Data Dictionary: Flights Data

## Description

The raw flight files contain on-time arrival data for non-stop domestic flights by major air carriers, and provides such additional items as departure and arrival delays, origin and destination airports, flight numbers, scheduled and actual departure and arrival times, cancelled or diverted flights, taxi-out and taxi-in times, air time, and non-stop distance.

## Source

[Bureau of Transportation Statistics - Airline On-Time Performance Data](https://www.transtats.bts.gov/Tables.asp?DB_ID=120&DB_Name=Airline%20On-Time%20Performance%20Data&DB_Short_Name=On-Time)

## Dictionary

| Type | Field | Description |
| ------------------ | ------------------ | ------------------ |
| Time Period | Year | Year |
| Time Period | Quarter | Quarter (1-4) |
| Time Period | Month | Month |
| Time Period | DayofMonth | Day of Month |
| Time Period | DayOfWeek | Day of Week |
| Time Period | FlightDate | Flight Date (yyyymmdd) |
| Airline | UniqueCarrier | Unique Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users, for example, PA, PA(1), PA(2). Use this field for analysis across a range of years. |
| Airline | AirlineID | An identification number assigned by US DOT to identify a unique airline (carrier). A unique airline (carrier) is defined as one holding and reporting under the same DOT certificate regardless of its Code, Name, or holding company/corporation. |
| Airline | Carrier | Code assigned by IATA and commonly used to identify a carrier. As the same code may have been assigned to different carriers over time, the code is not always unique. For analysis, use the Unique Carrier Code. |
| Airline | TailNum | Tail Number |
| Airline | FlightNum | Flight Number |
| Origin | OriginAirportID | Origin Airport, Airport ID. An identification number assigned by US DOT to identify a unique airport. Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused. |
| Origin | OriginAirportSeqID | Origin Airport, Airport Sequence ID. An identification number assigned by US DOT to identify a unique airport at a given point of time. Airport attributes, such as airport name or coordinates, may change over time. |
| Origin | OriginCityMarketID | Origin Airport, City Market ID. City Market ID is an identification number assigned by US DOT to identify a city market. Use this field to consolidate airports serving the same city market. |
| Origin | Origin | Origin Airport |
| Origin | OriginCityName | Origin Airport, City Name |
| Origin | OriginState | Origin Airport, State Code |
| Origin | OriginStateFips | Origin Airport, State Fips |
| Origin | OriginStateName | Origin Airport, State Name |
| Origin | OriginWac | Origin Airport, World Area Code |
| Destination | DestAirportID | Destination Airport, Airport ID. An identification number assigned by US DOT to identify a unique airport. Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused. |
| Destination | DestAirportSeqID | Destination Airport, Airport Sequence ID. An identification number assigned by US DOT to identify a unique airport at a given point of time. Airport attributes, such as airport name or coordinates, may change over time. |
| Destination | DestCityMarketID | Destination Airport, City Market ID. City Market ID is an identification number assigned by US DOT to identify a city market. Use this field to consolidate airports serving the same city market. |
| Destination | Dest | Destination Airport |
| Destination | DestCityName | Destination Airport, City Name |
| Destination | DestState | Destination Airport, State Code |
| Destination | DestStateFips | Destination Airport, State Fips |
| Destination | DestStateName | Destination Airport, State Name |
| Destination | DestWac | Destination Airport, World Area Code |
| Departure Performance | CRSDepTime | CRS Departure Time (local time: hhmm) |
| Departure Performance | DepTime | Actual Departure Time (local time: hhmm) |
| Departure Performance | DepDelay | Difference in minutes between scheduled and actual departure time. Early departures show negative numbers. |
| Departure Performance | DepDelayMinutes | Difference in minutes between scheduled and actual departure time. Early departures set to 0. |
| Departure Performance | DepDel15 | Departure Delay Indicator, 15 Minutes or More (1=Yes) |
| Departure Performance | DepartureDelayGroups | Departure Delay intervals, every (15 minutes from <-15 to >180) |
| Departure Performance | DepTimeBlk | CRS Departure Time Block, Hourly Intervals |
| Departure Performance | TaxiOut | Taxi Out Time, in Minutes |
| Departure Performance | WheelsOff | Wheels Off Time (local time: hhmm) |
| Arrival Performance | WheelsOn | Wheels On Time (local time: hhmm) |
| Arrival Performance | TaxiIn | Taxi In Time, in Minutes |
| Arrival Performance | CRSArrTime | CRS Arrival Time (local time: hhmm) |
| Arrival Performance | ArrTime | Actual Arrival Time (local time: hhmm) |
| Arrival Performance | ArrDelay | Difference in minutes between scheduled and actual arrival time. Early arrivals show negative numbers. |
| Arrival Performance | ArrDelayMinutes | Difference in minutes between scheduled and actual arrival time. Early arrivals set to 0. |
| Arrival Performance | ArrDel15 | Arrival Delay Indicator, 15 Minutes or More (1=Yes) |
| Arrival Performance | ArrivalDelayGroups | Arrival Delay intervals, every (15-minutes from <-15 to >180) |
| Arrival Performance | ArrTimeBlk | CRS Arrival Time Block, Hourly Intervals |
| Cancellations and Diversions | Cancelled | Cancelled Flight Indicator (1=Yes) |
| Cancellations and Diversions | CancellationCode | Specifies The Reason For Cancellation |
| Cancellations and Diversions | Diverted | Diverted Flight Indicator (1=Yes) |
| Flight Summaries | CRSElapsedTime | CRS Elapsed Time of Flight, in Minutes |
| Flight Summaries | ActualElapsedTime | Elapsed Time of Flight, in Minutes |
| Flight Summaries | AirTime | Flight Time, in Minutes |
| Flight Summaries | Flights | Number of Flights |
| Flight Summaries | Distance | Distance between airports (miles) |
| Flight Summaries | DistanceGroup | Distance Intervals, every 250 Miles, for Flight Segment |
| Cause of Delay | CarrierDelay | Carrier Delay, in Minutes |
| Cause of Delay | WeatherDelay | Weather Delay, in Minutes |
| Cause of Delay | NASDelay | National Air System Delay, in Minutes |
| Cause of Delay | SecurityDelay | Security Delay, in Minutes |
| Cause of Delay | LateAircraftDelay | Late Aircraft Delay, in Minutes |
| Gate Return | FirstDepTime | First Gate Departure Time at Origin Airport |
| Gate Return | TotalAddGTime | Total Ground Time Away from Gate for Gate Return or Cancelled Flight |
| Gate Return | LongestAddGTime | Longest Time Away from Gate for Gate Return or Cancelled Flight |
| Diverted Airport Information | DivAirportLandings | Number of Diverted Airport Landings |
| Diverted Airport Information | DivReachedDest | Diverted Flight Reaching Scheduled Destination Indicator (1=Yes) |
| Diverted Airport Information | DivActualElapsedTime | Elapsed Time of Diverted Flight Reaching Scheduled Destination, in Minutes. The ActualElapsedTime column remains NULL for all diverted flights. |
| Diverted Airport Information | DivArrDelay | Difference in minutes between scheduled and actual arrival time for a diverted flight reaching scheduled destination. The ArrDelay column remains NULL for all diverted flights. |
| Diverted Airport Information | DivDistance | Distance between scheduled destination and final diverted airport (miles). Value will be 0 for diverted flight reaching scheduled destination. |
| Diverted Airport Information | Div1Airport | Diverted Airport Code1 |
| Diverted Airport Information | Div1AirportID | Airport ID of Diverted Airport 1. Airport ID is a Unique Key for an Airport |
| Diverted Airport Information | Div1AirportSeqID | Airport Sequence ID of Diverted Airport 1. Unique Key for Time Specific Information for an Airport |
| Diverted Airport Information | Div1WheelsOn | Wheels On Time (local time: hhmm) at Diverted Airport Code1 |
| Diverted Airport Information | Div1TotalGTime | Total Ground Time Away from Gate at Diverted Airport Code1 |
| Diverted Airport Information | Div1LongestGTime | Longest Ground Time Away from Gate at Diverted Airport Code1 |
| Diverted Airport Information | Div1WheelsOff | Wheels Off Time (local time: hhmm) at Diverted Airport Code1 |
| Diverted Airport Information | Div1TailNum | Aircraft Tail Number for Diverted Airport Code1 |
| Diverted Airport Information | Div2Airport | Diverted Airport Code2 |
| Diverted Airport Information | Div2AirportID | Airport ID of Diverted Airport 2. Airport ID is a Unique Key for an Airport |
| Diverted Airport Information | Div2AirportSeqID | Airport Sequence ID of Diverted Airport 2. Unique Key for Time Specific Information for an Airport |
| Diverted Airport Information | Div2WheelsOn | Wheels On Time (local time: hhmm) at Diverted Airport Code2 |
| Diverted Airport Information | Div2TotalGTime | Total Ground Time Away from Gate at Diverted Airport Code2 |
| Diverted Airport Information | Div2LongestGTime | Longest Ground Time Away from Gate at Diverted Airport Code2 |
| Diverted Airport Information | Div2WheelsOff | Wheels Off Time (local time: hhmm) at Diverted Airport Code2 |
| Diverted Airport Information | Div2TailNum | Aircraft Tail Number for Diverted Airport Code2 |
| Diverted Airport Information | Div3Airport | Diverted Airport Code3 |
| Diverted Airport Information | Div3AirportID | Airport ID of Diverted Airport 3. Airport ID is a Unique Key for an Airport |
| Diverted Airport Information | Div3AirportSeqID | Airport Sequence ID of Diverted Airport 3. Unique Key for Time Specific Information for an Airport |
| Diverted Airport Information | Div3WheelsOn | Wheels On Time (local time: hhmm) at Diverted Airport Code3 |
| Diverted Airport Information | Div3TotalGTime | Total Ground Time Away from Gate at Diverted Airport Code3 |
| Diverted Airport Information | Div3LongestGTime | Longest Ground Time Away from Gate at Diverted Airport Code3 |
| Diverted Airport Information | Div3WheelsOff | Wheels Off Time (local time: hhmm) at Diverted Airport Code3 |
| Diverted Airport Information | Div3TailNum | Aircraft Tail Number for Diverted Airport Code3 |
| Diverted Airport Information | Div4Airport | Diverted Airport Code4 |
| Diverted Airport Information | Div4AirportID | Airport ID of Diverted Airport 4. Airport ID is a Unique Key for an Airport |
| Diverted Airport Information | Div4AirportSeqID | Airport Sequence ID of Diverted Airport 4. Unique Key for Time Specific Information for an Airport |
| Diverted Airport Information | Div4WheelsOn | Wheels On Time (local time: hhmm) at Diverted Airport Code4 |
| Diverted Airport Information | Div4TotalGTime | Total Ground Time Away from Gate at Diverted Airport Code4 |
| Diverted Airport Information | Div4LongestGTime | Longest Ground Time Away from Gate at Diverted Airport Code4 |
| Diverted Airport Information | Div4WheelsOff | Wheels Off Time (local time: hhmm) at Diverted Airport Code4 |
| Diverted Airport Information | Div4TailNum | Aircraft Tail Number for Diverted Airport Code4 |
| Diverted Airport Information | Div5Airport | Diverted Airport Code5 |
| Diverted Airport Information | Div5AirportID | Airport ID of Diverted Airport 5. Airport ID is a Unique Key for an Airport |
| Diverted Airport Information | Div5AirportSeqID | Airport Sequence ID of Diverted Airport 5. Unique Key for Time Specific Information for an Airport |
| Diverted Airport Information | Div5WheelsOn | Wheels On Time (local time: hhmm) at Diverted Airport Code5 |
| Diverted Airport Information | Div5TotalGTime | Total Ground Time Away from Gate at Diverted Airport Code5 |
| Diverted Airport Information | Div5LongestGTime | Longest Ground Time Away from Gate at Diverted Airport Code5 |
| Diverted Airport Information | Div5WheelsOff | Wheels Off Time (local time: hhmm) at Diverted Airport Code5 |
| Diverted Airport Information | Div5TailNum | Aircraft Tail Number for Diverted Airport Code5 |