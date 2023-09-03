SAMPLE_CONF = [{"user": f"line {i}", "default": f"line {i}"} for i in range(20)]

SAMPLE_CM = [
    {
        "band": "5GHz",
        "SSID": "Vill-Urugi-LGWAN_p",
        "MAC": "B6:0A:9A:8B:EE:AD",
        "Vendor": "<Random MAC>",
        "Tx": "97300000",
        "Rx": "16",
        "RSSI": "-72",
        "connect": "1h9m16s",
        "idle": "9s",
    },
    {
        "band": "2.4GHz",
        "SSID": "Vill-Urugi-LGWAN_p",
        "MAC": "B6:0A:9A:8B:EE:AD",
        "Vendor": "<Random MAC>",
        "Tx": "97300000",
        "Rx": "16",
        "RSSI": "-72",
        "connect": "1h9m16s",
        "idle": "9s",
    },
    {
        "band": "5GHz",
        "SSID": "Vill-Urugi-LGWAN_p",
        "MAC": "B6:0A:9A:8B:EE:AD",
        "Vendor": "<Random MAC>",
        "Tx": "97300000",
        "Rx": "16",
        "RSSI": "-72",
        "connect": "1h9m16s",
        "idle": "9s",
    },
]

SAMPLE_WM = [
    {
        "Index": "1",
        "MAC": "d4:2c:46:51:2b:41",
        "Vendor": "BUFFALO.INC",
        "SSID": "NO_test_2.4",
        "Channel": "2",
        "Mode": "802.11g/n/ax",
        "RSSI": "-23",
        "Noise": "-95",
        "Security": "AES",
    },
    {
        "Index": "2",
        "MAC": "88:57:ee:6f:db:a5",
        "Vendor": "BUFFALO.INC",
        "SSID": "23_11g_CPSE_AY",
        "Channel": "11",
        "Mode": "802.11g/n",
        "RSSI": "-25",
        "Noise": "-95",
        "Security": "AES",
    },
    {
        "Index": "3",
        "MAC": "88:57:ee:6f:db:a4",
        "Vendor": "BUFFALO.INC",
        "SSID": "19_11g_CPSE_KH",
        "Channel": "11",
        "Mode": "802.11g/n",
        "RSSI": "-25",
        "Noise": "-95",
        "Security": "AES",
    },
]

SAMPLE_SYSLOG = [
    {
        "datetime": "2023/09/01 14:14:40",
        "facility": "WIRELESS",
        "message": "wl1 (2.4GHz): Detect interference(74per) [with Non-802.11] on channel 1.",
    },
    {
        "datetime": "2023/09/01 14:11:44",
        "facility": "WIRELESS",
        "message": "wl1 (2.4GHz): Detect interference(82per) [with Non-802.11] on channel 1.",
    },
    {
        "datetime": "2023/09/01 14:11:33",
        "facility": "WIRELESS",
        "message": "wl1 (2.4GHz): Detect interference(76per) [with Non-802.11] on channel 1.",
    },
]
