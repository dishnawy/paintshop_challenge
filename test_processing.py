#process_orders(customers_test,color_count,customer_count)

#Copyright 2018 - Eldishnawy - dish@floralytics.com
import logging
from collections import Counter
import sys
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "logs.log"

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler
def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) 
   '''uncomment below line if you want to show logs on console as well'''
   #logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   logger.propagate = False
   return logger

main_logger = get_logger("__main__")


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

 
def matt_count(ord):
    '''Check if any customer requested more than 1 Matt color '''
    num_orders = ord[1][0]
    matt_col_count = 0
    for i in range(1,num_orders+1):
        if ord[1][i][1] == 1:
            matt_col_count = matt_col_count + 1      
    if matt_col_count > 1:
        return True
    else:
        return False

def common_order(customers, list = 0):
    '''if list is set to 0, returns list of most common glossy color (in order), if 1, it returns most common matt color (in order)'''
    orders_total = []
    glossy_orders= []
    matt_orders = []
    customers_iter = iter(customers)
    for z in range(len(customers)):
        d = next(customers_iter)
        for f in range(1, d[1][0]+1):
            orders_total.append(d[1][f])
    common_orders = Counter(orders_total).most_common()
    common_orders_iter = iter(common_orders)

    for f in range(len(common_orders)):
        z = next(common_orders_iter)
        if z[0][1] != 1:
            glossy_orders.append(z)
        else:
            matt_orders.append(z)
    if list == 0:
        return glossy_orders
    else:
        return matt_orders


def color_status(color_flag, col_id, set):
    '''Try to set color to 0 if glossy, or 1 if Matte'''
    if set == 0:
        if  color_flag[col_id-1][0] == 0:
            color_flag[col_id-1] = [1, 0]
            main_logger.info('Color %s is by default glossy', col_id)
            return True
        else:
            if color_flag[col_id-1][1] == 0:
                main_logger.info('Color %s is already glossy', col_id) 
                return True
            else:
                main_logger.info('Color %s is set as Matte by another order', col_id)
                return False
    else:
        if  color_flag[col_id-1][0] == 0:
            color_flag[col_id-1] = [1,1]
            main_logger.info('Color %s is now set as Matte', col_id)
            return True
        else:
            if color_flag[col_id-1][1] == 1:
                main_logger.info('Color %s is already Matte', col_id)
                return True
            else:
                main_logger.info('Color %s is set as glossy for another order', col_id)
                return False


def process_orders(customers,color_count):
    '''Customers list structure (flag for done, number of orders, orders tuples)
    Example: customers = [[0,(1,(1,1))], [0,(3,(1,0), (2,1), (4,0))], [0,(2,(1,1), (2,0))], [0,(1,(5,0))], [0,(1, (1,1))]]
    0 means color is not used, or glossy, 1 means color is Matt'''
    N = color_count
    main_logger.info('We have %s colors', N)
    color_flag = [[0,0]] * N

    for index,order in enumerate(customers):
        if matt_count(order):
            main_logger.info('Cannot order more than 1 Matte, order rejected:First found in customer#:%s',index)
            return False
        num_orders = order[1][0]
        #Handling customers with only one order, if any of them can't be satisfied because of contradicting orders, IMPOSSIBLE
        if num_orders == 1:
            main_logger.info('Customer order is:%s',order)
            color = order[1][1][0]
            colorType = order[1][1][1]
            if color_status(color_flag, color, set=colorType):
                customers[index][0] = 1
                main_logger.info('Customer#: %s is now satisfied',index)
                main_logger.info('Colors production status: %s',color_flag)
            else:
                main_logger.info('Color %s is already in use differently',color)
                main_logger.info('IMPOSSIBLE')
                return False
    else:       
        for index,order in enumerate(customers):
            if customers[index][0] != 1:  
                main_logger.info('Customer order is:%s', order)
                try:
                    common_list = common_order(customers)
                    common_list_iter = iter(common_list)
                    for l in range(len(common_list)):
                        best_match = next(common_list_iter)
                        order_best = best_match[0]
                        main_logger.info('active best glossy order is %s', order_best)
                        main_logger.info(order[1])
                        if order_best in order[1]:
                            colorid = order_best[0]
                            type_converted = order_best[1]
                            if color_status(color_flag, colorid, set = type_converted):
                                    customers[index][0] = 1
                                    main_logger.info('Customer#: %s is now satisfied', index)
                                    main_logger.info('Colors production status: %s', color_flag)
                                    break
                            else:
                                main_logger.info('Color %s is already in use, trying different color',colorid)
                    else:
                        common_list_matte = common_order(customers, list=1)
                        common_list_matte_iter = iter(common_list_matte)
                        for t in range(len(common_list_matte)):
                            best_match = next(common_list_matte_iter)
                            order_best = best_match[0]
                            main_logger.info('active best matte order is %s', order_best)
                            if order_best in order[1]:
                                colorid = order_best[0]
                                type_converted = order_best[1]
                                if color_status(color_flag, colorid, set = type_converted):
                                        customers[index][0] = 1
                                        main_logger.info('Customer#: %s is now satisfied',index)
                                        main_logger.info('Colors production status: %s',color_flag)
                                        break
                                else:
                                    main_logger.info('Color %s is already in use, try different color', colorid)
                        else:
                            main_logger.info('IMPOSSIBLE')
                            return False
                except:
                    print('something went wrong')
            #Update progress bar
            ln = len(customers)
            printProgressBar(index + 1, ln, prefix='Progress:', suffix='Complete', length=50)
        else:
            main_logger.info('All customers Satisfied')
            main_logger.info('Final production status: %s',color_flag) 
            final_colors = [x[1] for x in color_flag]
            return final_colors
