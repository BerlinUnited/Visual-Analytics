from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from tqdm import tqdm
from vaapi.client import Vaapi
import time
import traceback
import gzip
import json


def fill_option_map(log_id):
    # TODO I could build this why parsing the BehaviorComplete representation - saving a call to the database
    try:
        response = client.behavior_option.list(
            log_id=log_id
        )
    except Exception as e:
        print(response)
        print(e)
        print("Could not fetch the list of options for this log")
        quit()
    for option in response:
        state_response = client.behavior_option_state.list(
            log_id=log_id,
            option_id=option.id,
        )
        state_dict = dict()
        for state in state_response:
            state_dict.update(
                {"id":option.id, state.xabsl_internal_state_id:state.id}
            )
        option_map.update({option.xabsl_internal_option_id: state_dict})

def get_option_id(internal_options_id):
    try:
        return option_map[internal_options_id]['id']
    except Exception as e:
        print(option_map)
        print()
        print(f"internal_options_id: {internal_options_id}")
        print()
        print(e)
        quit()

def get_state_id(internal_options_id, internal_state_id):
    try:
        state_id = option_map[internal_options_id][internal_state_id]
    except Exception as e:
        print(option_map)
        print()
        print(f"internal_options_id: {internal_options_id} - internal_state_id: {internal_state_id}")
        print()
        print(e)
        quit()
    return state_id

def parse_sparse_option(log_id, frame, time, parent, node):
    internal_options_id = node.option.id
    internal_state_id = node.option.activeState
    global_options_id = get_option_id(internal_options_id)
    global_state_id = get_state_id(internal_options_id,internal_state_id)
    json_obj = {
        "log_id":log_id,
        "options_id":global_options_id,
        "active_state":global_state_id,
        "parent":parent, # FIXME we could make it a reference to options if we would have the root option in the db
        "frame":frame,
        "time":time,
        "time_of_execution":node.option.timeOfExecution,
        "state_time":node.option.stateTime,
    }
    parse_sparse_option_list.append(json_obj)

    # iterating through sub-options
    for sub in node.option.activeSubActions:
        if sub.type == 0: # Option
            parse_sparse_option(log_id=log_id, frame=frame, time=time, parent=node.option.id, node=sub)
        elif sub.type == 2: # SymbolAssignement
            # NOTE: i don't see any benefit in saving the SymbolAssignement; the resulting value is already in the 'outputsymbols'
            pass
        else:
            # NOTE: at the moment i didn't saw any other type ?!
            print(sub)

def is_behavior_done(data):
    print("\tcheck inserted behavior frames")
    if data.num_cognition_frames and int(data.num_cognition_frames) > 0:
        print(f"\tcognition frames are {data.num_cognition_frames}")
        
        response = client.behavior_frame_option.get_behavior_count(log_id=data.id)
        print(f"\tbehavior frames are {response['count']}")
        return response["count"] == int(data.num_cognition_frames)
    else:
        return False

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path

    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path

        print(log_path)
        if not data.num_cognition_frames or int(data.num_cognition_frames) == 0:
            print("\tWARNING: first calculate the number of cognitions frames and put it in the db")
            continue
        
        # check if we need to insert this log
        if is_behavior_done(data):
            print("\tbehavior already inserted, will continue with the next log")
            continue
        
        my_parser = Parser()
        game_log = LogReader(str(log_path), my_parser)
        combined_symbols = list()
        option_map = dict()
        
        output_decimal_lookup = dict()  # will be updated on each frame
        output_boolean_lookup = dict()  # will be updated on each frame
        input_decimal_lookup = dict()  # will be updated on each frame
        input_boolean_lookup = dict()  # will be updated on each frame
        broken_behavior = False

        for idx, frame in enumerate(tqdm(game_log, desc=f"Parsing frame", leave=True)):
            if 'FrameInfo' in frame:
                fi = frame['FrameInfo']
            else:
                print(f"frame {idx} does not have frame info representation so we dont go further")
                print("it could be that there is one more behavior frame in the next frame but this is one is not finished.")
                break

            if "BehaviorStateComplete" in frame:
                try:
                    full_behavior = frame["BehaviorStateComplete"]
                except Exception as e:
                    traceback.print_exc() 
                    print("can't parse the Behavior will continue with the next log")
                    broken_behavior = True
                    break
                # TODO: idea here is to build a enumeration lookup table that we use when inserting data
                """
                enumeration_lookup_list = list()
                for i, enum in enumerate(full_behavior.enumerations):
                    elem = [a.name for a in enum.elements]
                    enum_dict = {enum.name: elem}
                    #print()
                    #print(enum)
                    #print()
                    #print(enum_dict)
                    #print()
                    #print(type(elem))
                    #print(elem)

                    #for item in enum.elements:
                    #    self.sql_queue.put(("INSERT INTO behavior_enumerations VALUES (?,?,?,?,?)", [log_num, i, enum.name, item.value, item.name]))
                    break
                """
                # create a lookup table for current decimal output symbols
                for i, item in enumerate(full_behavior.outputSymbolList.decimal):
                    output_decimal_lookup.update({i: {"name":item.name, "value":item.value}})

                for i, item in enumerate(full_behavior.outputSymbolList.boolean):
                    output_boolean_lookup.update({i: {"name":item.name, "value":item.value}})

                # create a lookup table for current decimal input symbols
                for i, item in enumerate(full_behavior.inputSymbolList.decimal):
                    input_decimal_lookup.update({i: {"name":item.name, "value":item.value}})

                # create a lookup table for current boolean input symbols
                for i, item in enumerate(full_behavior.inputSymbolList.boolean):
                    input_boolean_lookup.update({i: {"name":item.name, "value":item.value}})
            
            if "BehaviorStateSparse" in frame:
                # TODO build a check that makes sure behaviorcomplete was parsed already
                sparse_behavior = frame["BehaviorStateSparse"]

                # update the decimal output symbols
                for i, item in enumerate(sparse_behavior.outputSymbolList.decimal):
                    output_decimal_lookup[item.id]["value"]= item.value
                
                # update the boolean output symbols
                for i, item in enumerate(sparse_behavior.outputSymbolList.boolean):
                    output_boolean_lookup[item.id]["value"]= item.value

                # update the decimal input symbols
                for i, item in enumerate(sparse_behavior.inputSymbolList.decimal):
                    input_decimal_lookup[item.id]["value"]= item.value

                # update the boolean input symbols
                for i, item in enumerate(sparse_behavior.inputSymbolList.boolean):
                    input_boolean_lookup[item.id]["value"]= item.value

                for k, v in output_decimal_lookup.items():
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "output",
                        "symbol_name":v["name"],
                        "symbol_value":v["value"],
                    }
                    combined_symbols.append(json_obj)

                for k, v in output_boolean_lookup.items():
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "output",
                        "symbol_name":v["name"],
                        "symbol_value":str(v["value"]),
                    }
                    combined_symbols.append(json_obj)

                for k, v in input_decimal_lookup.items():
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "input",
                        "symbol_name":v["name"],
                        "symbol_value":v["value"],
                    }
                    combined_symbols.append(json_obj)

                for k, v in input_boolean_lookup.items():
                    json_obj = {
                        "log_id":log_id,
                        "frame":fi.frameNumber,
                        "symbol_type": "input",
                        "symbol_name":v["name"],
                        "symbol_value":str(v["value"]),
                    }
                    combined_symbols.append(json_obj)

            if idx % 25 == 0:
                try:
                    response = client.xabsl_symbol.bulk_create(
                        data_list=combined_symbols
                        )
                except Exception as e:
                    print(f"error inputing the data {log_path}")
                    print(e)
                    quit()
                combined_symbols.clear()

        # if we abort in BehaviorStateComplete we should not do this here
        if not broken_behavior:
            try:
                response = client.xabsl_symbol.bulk_create(
                    data_list=combined_symbols
                    )
                #print(f"\t{response}")
            except Exception as e:
                print(f"error inputing the xabsl symbols {log_path}")
                print(e)
            break