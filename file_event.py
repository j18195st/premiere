import Evtx.Evtx as evtx
import tkinter
from tkinter import filedialog

import Evtx.Views as e_views
from Evtx.Views import evtx_record_xml_view
import pickle


def get_file_path():
    idir = 'C:\\'
    file_path = tkinter.filedialog.askopenfilename(initialdir=idir)
    print(file_path)
    return file_path


def get_folder_path():
    idir = 'C:\\python_test'
    folder_path = tkinter.filedialog.askdirectory(initialdir=idir)
    return folder_path


def main():
    count = 1
    file_path = get_file_path()
    with evtx.Evtx(file_path) as log:
        for record in log.records():
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

            # 出力用途
            # if len(time) != 0 and len(image) != 0 and len(srcip) != 0 and len(srcport) != 0 and len(dstip) != 0 and len(
            #         dstport) != 0:
            #     print(time[0].text, image[0].text, srcip[0].text, srcport[0].text, dstip[0].text, dstport[0].text)
        count += 1


if __name__ == "__main__":
    main()
