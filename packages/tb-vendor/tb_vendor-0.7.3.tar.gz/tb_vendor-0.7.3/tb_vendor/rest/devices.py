import logging
from time import sleep
from typing import List

from tb_rest_client.rest import ApiException

from tb_vendor.models import TbVirtualDevice
from tb_vendor.tb_utils import tb_paginate
import tb_vendor.rest.models as rest_models
from tb_vendor.rest.login import login_wait

logger = logging.getLogger(__name__)


def get_devices_by_type(
    rest_client: rest_models.RestClientType,
    data_type: str,
    retry_for_timeout: int,
    page_size: int = 100,
) -> List[rest_models.TbDeviceType]:
    """Get all devices by type (DEVICE_PROFILE) from Thingsboard.

    TB method: get_tenant_devices

    Args:
        rest_client: RestClient
        data_type: name of the device profile

    Returns:
        List of Devices

    Raises:
        ApiException
    """
    while True:
        logger.info(f"Get devices of type: {data_type} from TB")
        try:
            devices = tb_paginate(
                rest_client.get_tenant_devices,
                page_size=page_size,
                sort_property="createdTime",
                sort_order="ASC",
                type=data_type,
            )
        except ApiException as e:
            logger.error(f"Error when getting devices: {e}")
            logger.warning(f"Retry in {retry_for_timeout} s")
        else:
            total_devices = len(devices)
            if total_devices > 0:
                break
            logger.warning(f"No devices found, retry in {retry_for_timeout} s")
        sleep(retry_for_timeout)
    return devices


def add_credentials(
    rest_client: rest_models.RestClientType, devices: List[TbVirtualDevice]
) -> List[TbVirtualDevice]:
    """Include info about credentials for each device.

    Args:
        rest_client: RestClient
        devices: list of devices to be included
    """
    total_devices = len(devices)
    logger.info(f"Request credentials for {total_devices} devices")
    container_device_info = []
    for n, device in enumerate(devices, 1):
        logger.debug(f"Credentials {n}/{total_devices} device {device.id.id}")
        try:
            credentials = rest_client.get_device_credentials_by_device_id(
                device_id=device.id
            )
        except ApiException as e:
            logger.error(f"Error getting credentials fo {device.id.id}: {e}")
            continue
        device_info = TbVirtualDevice(
            dtype=device.type,
            device_id=device.id.id,
            name=device.name,
            entity_type=device.id.entity_type,
            access_token=credentials.credentials_id,
        )
        container_device_info.append(device_info)
    return container_device_info


def main_device_inventory(
    RestClientKlass: rest_models.RestClientClassType,
    base_url: str,
    username: str,
    password: str,
    data_type: str,
    retry_for_timeout: int = 60,
) -> List[TbVirtualDevice]:
    """Get all devices by type (DEVICE_PROFILE) from Thingsboard.

    TbVirtualDevice include data:
    - device_id
    - access_token
    - name

    TbVirtualDevice not include:
    - vendor_id
    - telemetry

    Args:
        RestClientKlass: Class of RestClientType.
        base_url: URL of Thingsboard.
        username: username for login.
        password: password for login.
        data_type: name of the device profile.
        retry_for_timeout: retry timeout if something go wrong.

    Returns:
        List of devices
    """
    with RestClientKlass(base_url=base_url) as rest_client:
        login_wait(rest_client, username, password, retry_for_timeout)
        device_list = get_devices_by_type(rest_client, data_type, retry_for_timeout)
        devices = add_credentials(rest_client, device_list)

    # Next step: Get vendor ID and relate to each device
    return devices
