import speedtest
import logging
import uuid
import os
from datetime import datetime
from csv import DictWriter, writer


headers = ["time", "upload", "download", "ping", "server", "group_id"]

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filemode="a", filename="speedtest.log")

def get_test_results(group_id: str):
        """returns the upload and download speed test results for the speed test
        Parameters
        ----------
        group_id: str   a uuid1 to keep testing groups together"""
        
        st = speedtest.Speedtest()

        server = st.get_best_server()
        logging.info(f"Connecting to server, {server['name']}")

        logging.info("testing download speed")
        down = st.download()
        logging.info("testing upload speed")
        up = st.upload()

        results = st.results
        now = datetime.now()

        data = {}
        data["time"] = now
        data["upload"] = up
        data["download"] = down
        data["ping"] = results.ping
        data["server"] = server["name"]
        data["group_id"] = group_id
        logging.info(f"download: {down}, upload: {up}, ping: {results.ping}, server: {server['name']}  time: {now}")
        return data



def _get_file_path()->str:
        """gets the path to csv file """
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "speedtests.csv")
        return file_path


def init_csv_file():
        """creates a blank csv file with empty headers"""
        file_path = _get_file_path()
        if(os.path.exists(file_path)):
                logging.info(f"{file_path} already exists")
                return

        with open(file_path, "a", newline='') as csv_obj:
                writer_obj = writer(csv_obj)
                writer_obj.writerow(headers)


def write_report_data(row:dict):
        """appends out a record to the csv files
        Parameters
        ----------
        row:dict        result dict from get_test_results"""
        file_path = _get_file_path()
        with open(file_path, "a", newline="") as fopen:
                dict_write = DictWriter(fopen, fieldnames=headers)
                dict_write.writerow(row)


def main():
        i=0 
        group_id =  str(uuid.uuid4())
        logging.info("Group testing id: " + group_id)
        for i in range(5):
                data = get_test_results(group_id=group_id)
                init_csv_file()
                write_report_data(data)



if __name__ == "__main__":
        try:
                main()
        except Exception as e:
                logging.error("An occurred running the speed test")
                logging.error(e.with_traceback())







