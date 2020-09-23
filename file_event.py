import Evtx.Evtx as evtx
import Evtx.Views as e_views
from Evtx.Views import evtx_record_xml_view
import pickle

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Dump extracted information to a json file")
    parser.add_argument("evtx", type=str, help="Path to evtx file")
    args = parser.parse_args()
    filename = args.evtx
    count = 1
    print("[")
    with evtx.Evtx(filename) as log:
        for record in log.records():
            elm = record.lxml()
            time = elm.xpath("//event:Data",namespaces={"event":"http://schemas.microsoft.com/win/2004/08/events/event"})[1].text
            image = elm.xpath("//event:Data",namespaces={"event":"http://schemas.microsoft.com/win/2004/08/events/event"})[4].text
            hashEvent = elm.xpath("//event:Data",namespaces={"event":"http://schemas.microsoft.com/win/2004/08/events/event"})[17].text
            parentImage = elm.xpath("//event:Data",namespaces={"event":"http://schemas.microsoft.com/win/2004/08/events/event"})[20].text
            print(count,end="")
            print(": { \n time:",time,",\n image:",image,",\n hash:",hashEvent,",\n parent:",parentImage,",\n <judge>:\n},\n")
            count+=1
    print("]")


if __name__ == "__main__":
    main()