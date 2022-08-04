import datetime


class get_logs:
    '''
    class name :  get_logs

    Description : Create logger object and write logs in respective logging mode

    parameters :
        mode : mode oe level of logging : "info" , "error"

        file_name : The name of file in which the logs should be written

    Written By : Yatrik Shah

    '''

    def __init__(self ,file_object ):

        # Aliasing logger file object
        self.file_object = file_object



    def write_logs(self ,  log_message):
        '''
        method name :  write_logs

        parameters :
            log_message : Thr log message sto be written

        return: None

        Written by : Yatrik Shah
        '''


        time = datetime.datetime.now()


        self.file_object.write(
         str(time) + "\t" + log_message + "\n")






