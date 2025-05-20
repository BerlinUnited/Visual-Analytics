from vaapi.client import Vaapi
import os


def get_logs():
    response = client.ballmodel.list(
        log=30,
    )
    print(response[1])


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    get_logs()


"""
OUTPUT: 
id=4839660 
frame=3675713 
representation_data={
    'knows': False, 
    'speed':                  {'x': -4.105163061329835e-20, 'y': -5.5511136051995765e-17}, 
    'valid': True, 
    'position':               {'x': -4023.7337836735774,    'y': -622.2727245648697}, 
    'positionPreview':        {'x': -4023.7337836735774,    'y': -622.2727245648697}, 
    'positionPreviewInLFoot': {'x': -4000.926060298418,     'y': -669.4468961567557}, 
    'positionPreviewInRFoot': {'x': -3999.614725983466,     'y': -578.5145090444447}}
"""


