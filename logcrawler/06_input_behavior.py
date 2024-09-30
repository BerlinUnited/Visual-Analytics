from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from vaapi.client import Vaapi

def fill_option_map(log_id):
    # TODO I could build this why parsing the BehaviorComplete representation - saving a call to the database
    response = client.behavior_option.list(
        log_id=log_id
    )
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
    return option_map[internal_options_id]['id']

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

    # TODO add inserting of params here

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
    if data.num_cognition_frames and int(data.num_cognition_frames) > 0:
        response = client.behavior_frame_option.list(log_id=data.id)

        my_list = [None] * len(response)
        for idx, behavior_data in enumerate(response):
            my_list[idx] = behavior_data.frame

        return len(set(my_list)) == int(data.num_cognition_frames)
    else:
        return False

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def myfunc(data):
        return data.sensor_log_path

    for data in sorted(existing_data, key=myfunc):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path
        print("log_path: ", log_path)

        if not data.num_cognition_frames or int(data.num_cognition_frames) == 0:
            print("\tWARNING: first calculate the number of cognitions frames and put it in the db")
            continue

        # Hack for demo - remove later
        if int(data.game_id) != 23 and int(data.game_id) != 24 and int(data.id) != 7:
            continue
        
        # check if we need to insert this log
        if is_behavior_done(data):
            print("behavior already inserted, will continue with the next log")
            continue
        
        my_parser = Parser()
        game_log = LogReader(str(log_path), my_parser)
        parse_sparse_option_list = list()
        option_map = dict()

        for idx, frame in enumerate(game_log):
            print(idx)
            if 'FrameInfo' in frame:
                fi = frame['FrameInfo']
            else:
                print(f"frame {idx} does not have frame info representation")
                break
            # TODO build something to check how many frames are already inserted
            # maybe have an endpoint that checks number of unique frames in BehaviorFrameOption model
            # That means I need to make sure to have num cognition frames calculated before
            if "BehaviorStateComplete" in frame:
                #continue
                full_behavior = frame["BehaviorStateComplete"]

                for i, option in enumerate(full_behavior.options):
                    #print(option.name)
                    try:
                        option_response = client.behavior_option.create(
                            log_id=log_id,
                            xabsl_internal_option_id=i,
                            option_name=option.name
                        )
                        #print(f"\t{option_response}")
                    except Exception as e:
                        print(f"error inputing the data {log_path}")
                        print(e)
                        quit()

                    for j, state in enumerate(option.states):
                        #print(f"\t{state.name}")
                        try:
                            response = client.behavior_option_state.create(
                                log_id=log_id,
                                option_id=option_response.id,
                                xabsl_internal_state_id=j,
                                name=state.name,
                                target=state.target,
                                )
                            #print(f"\t{response}")
                        except Exception as e:
                            print(f"error inputing the data {log_path}")
                            print(e)
                fill_option_map(log_id)
            
            if "BehaviorStateSparse" in frame:
                sparse_behavior = frame["BehaviorStateSparse"]
                for root in sparse_behavior.activeRootActions:
                    if root.type != 0: # Option
                        print("Root node must be an option!")
                    else:
                        parse_sparse_option(log_id=log_id, frame=fi.frameNumber, time=fi.time, parent=-1, node=root)
            if idx % 100 == 0:
                try:
                    response = client.behavior_frame_option.bulk_create(
                        data_list=parse_sparse_option_list
                        )
                except Exception as e:
                    print(f"error inputing the data {log_path}")
                    print(e)
                    quit()
                parse_sparse_option_list.clear()
        try:
            response = client.behavior_frame_option.bulk_create(
                data_list=parse_sparse_option_list
                )
            #print(f"\t{response}")
        except Exception as e:
            print(f"error inputing the data {log_path}")
            print(e)
        quit()


