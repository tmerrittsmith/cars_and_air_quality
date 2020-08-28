import json
import requests
import time
import datetime as dt

image_url = "https://www.netraveldata.co.uk/api/v2/cctv/images/NC_A188C1.jpg"
update_url = "https://www.netraveldata.co.uk/api/v2/cctv/dynamic/NC_A188C1"
auth = "AUTH DETAILS"


def extract_lastupdated_timestamp(cctv_result_json, remove_trailing_figures=-9, time_format='%Y-%m-%dT%H:%M:%S'):
    """Given a cctv json result, extract a timestampe of the last update to the cctv image"""
    timestamp_string = cctv_result_json['dynamics'][0]['lastUpdated']
    timestamp = dt.datetime.strptime(timestamp_string[:remove_trailing_figures], time_format)
    return timestamp

def cctv_has_update(cctv_url, api_auth, last_update):
    
    """
    Checks the url to see whether there has been an update since the last image..
    args: 
        cctv_url: (str)
                   The url you want to listen on
        api_auth: (str)
                   Authentication for the api
        last_update:(datetime obj) 
                   The timestamp for the last update
    returns:
        (True, updated_timestamp): if there is a new update
         False, None: if there is not a new update
    """
    r = requests.get(cctv_url, auth=api_auth)
    if r.status_code != 200:
        return False, last_update
    result = json.loads(r.text)
    new_update = extract_lastupdated_timestamp(result)
    if (new_update - last_update).seconds > 0:
        return True, new_update
    else:
        return False, last_update


def download_image(image_url, api_auth, timestamp):
    """
    Download an image, save it to file as a PNG with a timestamp in the filename.
    args:
        image_url: (str)
                   The url for the cctv image
        api_auth: (str)
                  Authentication for the api
        timestamp: (str)
                    timestamp to add to the filename
    returns:
        None

    """
    r = requests.get(image_url, auth=api_auth)
    if r.status_code != 200:
        return timestamp, False
    image = r.content
    with open(timestamp + ".png", "wb") as f:
        f.write(image)
    return timestamp, True


if __name__ == "__main__":
    import time
    import datetime as dt
    import argparse

    parser = argparse.ArgumentParser(description='Set the stop time for downloading images')
    parser.add_argument('stop_time')
    args = parser.parse_args()
    stop_time = dt.datetime.strptime(args.stop_time, '%Y-%m-%dT%H%M') 

    downloaded = []
    check_time = dt.datetime.now() 
    while (stop_time - dt.datetime.now()).days >= 0:
        update, check_time  = cctv_has_update(update_url, auth, check_time)
        if update:
            download_image(image_url, auth, dt.datetime.strftime(check_time,'%Y%m%d%H%M%S'))
            time.sleep(60 * 3)
        else:
            time.sleep(60)



