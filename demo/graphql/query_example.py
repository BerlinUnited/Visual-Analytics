import os
from vaapi.client import VATClient

query = """
query{
logstatus(filters:[{field:"log_id", value:"2"}]){
    FrameInfo
    BallModel
  }
}
"""

query = """
query{
cogrepr(filters:[{field:"log_id", value:"1"}, {field: "representation_name", value:"FieldPercept"}]){
    representationData
  }
}
"""

query = """
query{
images(filters:[{field:"log_id", value:"1"}, {field: "blurredness_value", value:null}]){
    frameNumber
    imageUrl
    blurrednessValue
  }
}
"""

existing_logs = """
query{
  logs{id
  logPath}
}
"""
log_status = """
query log_status($id: String!) {
  logstatus(filters: [{ field: "log_id", value: $id }]) {
    logId {id}
    numJpgTop
    numJpgBottom
    numTop
    numBottom
  }
}
"""
log_status_var = {"id": "12"}
# this would be cooler if it only returns fields that are null since this is what we are checking for in 05_calculate_num_frames is_done
log_status_cognition_frames = """query cognition_status($id: String!) {
  logstatus(filters: [{ field: "log_id", value: $id }]) {
    FrameInfo
    BallModel
    BallCandidates
    BallCandidatesTop
    CameraMatrix
    CameraMatrixTop
    FieldPercept
    FieldPerceptTop
    GoalPercept
    GoalPerceptTop
    MultiBallPercept
    RansacLinePercept
    RansacCirclePercept2018
    ShortLinePercept
    ScanLineEdgelPercept
    ScanLineEdgelPerceptTop
    OdometryData
    numCognitionFrames
  }
}"""
log_status_motion_frames = """
query cognition_status($id: String!){
logstatus(filters: [{ field: "log_id", value: $id }]){
    FrameInfo
    IMUData
    FSRData 
    ButtonData
    SensorJointData
    AccelerometerData
    InertialSensorData
    MotionStatus
    MotorJointData
    GyrometerData
    numMotionFrames
    }}
"""

image_without_stats = """query($id: String!){
  images(filters:[{field:"blurredness_value",value:"null"},{field:"log_id",value:$id}])
  {
    id
    frameNumber
    imageUrl
    blurrednessValue
  }
}"""


if __name__ == "__main__":
    client = VATClient(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    data = client.execute(image_without_stats, log_status_var)
    print(data)
