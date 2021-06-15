import usb
from usb.core import USBError

### Some auxiliary functions ###
def _clean_str(s):
    '''
    Filter string to allow only alphanumeric chars and spaces

    @param s: string
    @return: string
    '''

    return ''.join([c for c in s if c.isalnum() or c in {' '}])


def _get_dev_string_info(device):
    '''
    Human readable device's info

    @return: string
    '''
    str_info = ''
    try:
        str_info = _clean_str(usb.util.get_string(device, 256, 2))
        str_info += ' ' + _clean_str(usb.util.get_string(device, 256, 3))
        return str_info
    except USBError:
        return str_info


def get_usb_devices():
    '''
    Get USB devices

    @return: list of tuples (dev_idVendor, dev_idProduct, dev_name)
    '''

    return [(device.idVendor, device.idProduct, _get_dev_string_info(device),device.serial_number,device.bDeviceClass) 
                for device in usb.core.find(find_all=True)
                    if (device.idProduct > 2) and (device.bDeviceClass==0)
                    #if device.serial_number in ('9000864F11D97D98','E69214006C25')
                    ]

if __name__=='__main__':
    u = get_usb_devices()
    print(u)
    print('qqq')