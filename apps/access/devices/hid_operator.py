from socket import *



class Hid_dev:

    def __init__(self, ip, port=4070, isRun=True):
        self.ip = ip
        self.port = port
        self.isRun = isRun

        self.rec_data = {}

    def monitor(self):

        tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        if self.isRun == True:
            try:
                tcp_client_socket.connect((self.ip, self.port))
            except:
                tcp_client_socket.close()

            counter = 0
            while True:
                rec_data = tcp_client_socket.recv(1024).decode('utf-8')
                counter += 1
                event = Card_event(rec_data, counter)
                self.rec_data = event.get_event()
                # requests.post('/hid_monitor/', data=dic_data)


        else:
            tcp_client_socket.close()




class Card_event:
    def __init__(self, rec_data, counter):
        self.rec_data = rec_data
        self.counter = counter


    def get_event(self):

        dic = {}
        list_rec_data = self.rec_data.split(';')

        dic['v1000_ip'] = list_rec_data[2]
        dic['v100_id'] = list_rec_data[3]
        dic['reader_id'] = list_rec_data[4]
        dic['event_time'] = list_rec_data[9]
        dic['v1000_name'] = list_rec_data[10]
        dic['v100_name'] = list_rec_data[11]
        dic['reader_name'] = list_rec_data[12]
        dic['event_desc'] = list_rec_data[13]
        dic['io_msg'] = list_rec_data[14]
        dic['card_num'] = list_rec_data[15]
        dic['person_code'] = list_rec_data[16]
        dic['person_name'] = list_rec_data[17]
        dic['counter'] = self.counter

        return dic












