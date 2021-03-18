from datetime import datetime as dt
from redisclient import r as redis

FORMAT_STRING = "%d-%b-%Y (%H:%M:%S.%f)"


def generate_key(userID, assetID):
    return f"{userID}:{assetID}"


def add_to_storage(userID, assetID, position):
    # Edge Case: if args are None or invalid syntax
    if not userID or not assetID or not position:
        return False
    key = generate_key(userID, assetID)
    timestamp_str = dt.now().strftime(FORMAT_STRING)
    asset_info = {"position": position, "last-modified": timestamp_str}
    redis_response = redis.hmset(key, asset_info)
    return redis_response


def get_position_from_storage(userID, assetID):
    if not userID or not assetID:
        return False
    key = generate_key(userID, assetID)
    if not redis.exists(key):
        return False
    position_str = redis.hget(key, "position").decode('utf-8')

    return position_str


def get_asset_info_from_storage(key):
    # Get dict from redis
    asset_info = redis.hgetall(key)
    # Collect string values
    _id = key.decode('utf-8').split(':').pop()
    _pos = asset_info[b'position'].decode('utf-8')
    _last_modified = asset_info[b'last-modified'].decode('utf-8')
    # Convert back to datetime object
    dateObj = dt.strptime(_last_modified, FORMAT_STRING)
    # Make list of all asset values
    asset_values = [_id, _pos, dateObj]

    return asset_values


def generate_list(userID):
    if not userID:
        return False
    pattern = f"{userID}:*"
    keys = redis.keys(pattern)
    # If userID has no keys in storage
    if not keys:
        return keys
    asset_list = []
    for key in keys:
        asset_info = get_asset_info_from_storage(key)
        asset_list.append(asset_info)

    # Sorted compared with date in descending order
    asset_list.sort(key=lambda item: item[2], reverse=True)
    return asset_list


def delete(userID, assetID):
    if not userID or not assetID:
        return False
    key = generate_key(userID, assetID)
    redis_response = redis.delete(key)
    return redis_response
