import Evtx.Evtx as evtx
import tkinter
from tkinter import filedialog
import json

import Evtx.Views as e_views
from Evtx.Views import evtx_record_xml_view
import pickle


def get_connection_data(filename):
    data = []
    with open(filename,'r') as f:
        for s_line in f:
            data.append(s_line.replace('\n',''))
    print(len(data))
    return data


def get_file_path():
    idir = 'C:\\'
    file_path = tkinter.filedialog.askopenfilename(initialdir=idir)
    return file_path


def get_folder_path():
    idir = 'C:\\'
    folder_path = tkinter.filedialog.askdirectory(initialdir=idir)
    return folder_path


def dict_to_json(li, filename):
    with open(filename, 'w') as f:
        json.dump(li, f)


def get_connect_log(data):
    total_log = []
    duplication_list = []
    del_duplication_log = []
    total_count = 0
    duplication_count = 0
    file_path = get_file_path()
    with evtx.Evtx(file_path) as evt_log:
        for record in evt_log.records():
            elm = record.lxml()

            time = elm.xpath("//event:Data[@Name='UtcTime']",
                             namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"})
            srcip = elm.xpath(
                "//event:Data[@Name='SourceIp']",
                namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"}
            )
            srcport = elm.xpath(
                "//event:Data[@Name='SourcePort']",
                namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"}
            )
            dstip = elm.xpath(
                "//event:Data[@Name='DestinationIp']",
                namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"}
            )
            dstport = elm.xpath(
                "//event:Data[@Name='DestinationPort']",
                namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"}
            )
            image = elm.xpath("//event:Data[@Name ='Image']",
                              namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"})

            con_flag = srcport in data
            if len(time) != 0 and len(srcip) != 0 and len(srcport) != 0 and len(dstip) != 0 and len(
                    dstport) != 0 and len(image) != 0:
                total_count += 1
                total_log.append({total_count:
                                      {"time": time[0].text, "srcip": srcip[0].text, "srcport": srcport[0].text,
                                       "dstip": dstip[0].text,
                                       "dstport": dstport[0].text, "image": image[0].text, "compared":con_flag}})
                if image[0].text not in duplication_list:
                    duplication_list.append(image[0].text)
                    duplication_count += 1
                    del_duplication_log.append({duplication_count:
                                                    {"time": time[0].text, "srcip": srcip[0].text,
                                                     "srcport": srcport[0].text,
                                                     "dstip": dstip[0].text,
                                                     "dstport": dstport[0].text, "image": image[0].text, "compared":con_flag}})

    return total_log, del_duplication_log


def get_evt_log():
    duplication_list = []
    del_duplication_log = []
    log = []
    total_count = 0
    duplication_count = 0
    file_path = get_file_path()
    with evtx.Evtx(file_path) as evt_log:
        for record in evt_log.records():
            elm = record.lxml()

            time = elm.xpath("//event:Data[@Name='UtcTime']",
                             namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"})
            hash = elm.xpath(
                "//event:Data[@Name='Hashes']",
                namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"}
            )
            parent = elm.xpath(
                "//event:Data[@Name='ParentImage']",
                namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"}
            )
            image = elm.xpath("//event:Data[@Name ='Image']",
                              namespaces={"event": "http://schemas.microsoft.com/win/2004/08/events/event"})

            if len(time) != 0 and len(image) != 0 and len(hash) != 0 and len(parent) != 0:
                total_count += 1
                log.append({total_count:
                                {"time": time[0].text, "image": image[0].text, "hash": hash[0].text,
                                 "parent": parent[0].text,"vt_info":""}})
                if image not in duplication_list:
                    duplication_count += 1
                    duplication_list.append(hash[0].text)
                    del_duplication_log.append({duplication_count:
                                                    {"time": time[0].text, "image": image[0].text, "hash": hash[0].text,
                                                     "parent": parent[0].text,"vt_info":""}})

    return log, del_duplication_log


if __name__ == "__main__":
    data = get_connection_data('compare.txt')
    li_evt, li_edited_evt = get_evt_log()
    dict_to_json(li_edited_evt, 'edited_evt_log.json')
    li_con,li_edited_con = get_connect_log(data)
    dict_to_json(li_edited_con, 'edited_evt_con.json')
