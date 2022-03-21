# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
 
from typing import Any, Text, Dict, List
import random
 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction

import os
import json
 
# computer_choice & determine_winner functions refactored from
# https://github.com/thedanelias/rock-paper-scissors-python/blob/master/rockpaperscissors.py, MIT liscence
 

def get_schedules_(trip_id, json_trip_data):
    schedule_ids = None
    for trip_schedule in  json_trip_data['trips_schedules']:
        if trip_schedule['trip_id'] == trip_id:
            schedule_ids = trip_schedule['schedule_id']
            break
    
    schedules_list = []
    for schedules in json_trip_data['schedules']:
        if schedules['schedule_id'] in schedule_ids:
            schedules_list.append(schedules['local_hour'])

    return(schedules_list, schedule_ids)


class DisplayTrips(Action):
   
    def name(self) -> Text:
        return "action_display_trips"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 

        #dispatcher.utter_message(text=f"Hola mundo")
        departure_city = tracker.get_slot("departure_city")

        f = open('data/trips.json')
        json_trip_data = json.load(f)

        list_trips = []
        for trip in json_trip_data['trips']:
            if trip['origin'] == departure_city:
                list_trips.append(trip)
        
        if list_trips:
            dispatcher.utter_message(text=f"Here are the destinations for {departure_city}")
            for trip in list_trips:
                trip_schedules,  _= get_schedules_(trip['trip_id'], json_trip_data)
                string_schedules = ' '.join(trip_schedules)
                dispatcher.utter_message(text=f"Destination {trip['destination']} - {string_schedules}")

            #return [FollowupAction(name='utter_which_arrival_city')]
        
        else:
            dispatcher.utter_message(text=f"We weren't able to find a trip from {departure_city}")
            
        return []

class DisplaySeats(Action):
   
    def name(self) -> Text:
        return "action_display_seats"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 

        departure_city = tracker.get_slot("departure_city")
        arrival_city = tracker.get_slot("arrival_city")
        departure_time = tracker.get_slot("departure_time")

        f = open('data/trips.json')
        json_trip_data = json.load(f)

        list_trips = []
        for trip in json_trip_data['trips']:
            if trip['origin'] == departure_city:
                list_trips.append(trip)
        
        trip_id = None
        if list_trips:
            for trip in list_trips:
                if trip['destination'] == arrival_city:
                    trip_id = trip['trip_id']
                    break
            if trip_id is not None:
                trip_schedules, schedule_ids = get_schedules_(trip_id, json_trip_data)
                schedule_id = None
                for trip_schedule, schdl_id in zip(trip_schedules, schedule_ids):
                    if departure_time == trip_schedule:
                        schedule_id = schdl_id
                        break

                if schedule_id is not None:
                    current_info = json_trip_data['current_info'] 
                    price_seats = None
                    for cnt_info in current_info:
                        if (cnt_info["trip_id"] == trip_id) & (cnt_info["schedule_id"] == schedule_id):
                            price_seats = cnt_info["price_seats"]
                            break

                    if price_seats is not None:
                        dispatcher.utter_message(text=f"Available seats:")
                        dispatcher.utter_message(text=f"First class:")
                        dispatcher.utter_message(text=f"    Available seats {price_seats[0]} - Price €{price_seats[1]}")
                        dispatcher.utter_message(text=f"Second class:")
                        dispatcher.utter_message(text=f"    Available seats {price_seats[2]} - Price €{price_seats[2]}")
                    else:
                        dispatcher.utter_message(text=f"{departure_city} - {arrival_city} - {departure_time}")
                        #dispatcher.utter_message(text=f"DEBUG04: We weren't able to find a trip from {departure_city} to {arrival_city} at {departure_time}")
                else:
                    dispatcher.utter_message(text=f"{departure_city} - {arrival_city} - {departure_time}")
                    #dispatcher.utter_message(text=f"DEBUG03: We weren't able to find a trip from {departure_city} to {arrival_city} at {departure_time}")

            else:
                dispatcher.utter_message(text=f"{departure_city} - {arrival_city} - {departure_time}")
                #dispatcher.utter_message(text=f"DEBUG02: We weren't able to find a trip to {arrival_city}")
        
        else:
            dispatcher.utter_message(text=f"{departure_city} - {arrival_city} - {departure_time}")
            #dispatcher.utter_message(text=f"DEBUG01: We weren't able to find a trip from {departure_city}")
            
        return []
 
