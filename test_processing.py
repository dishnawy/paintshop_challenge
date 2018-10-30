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
    for d in customers:
        if d[0] != 1:
            for f in range(1,d[1][0]+1):
                orders_total.append(d[1][f])
    common_orders = Counter(orders_total).most_common()
    for z in common_orders:
        if  z[0][1] != 1:
            glossy_orders.append(z)
        else:
            matt_orders.append(z)
    if list == 0:        
        return glossy_orders
    else:
        return matt_orders

def color_status(color_flag, col_id, set=0):
    '''Check if a color is already set and get what is it set for (Glossy or Matt) (0), OR, set a color to Glossy (set=1) or Matt (set=2)'''
    if set == 0:
        return color_flag[col_id-1]

    elif color_flag[col_id-1] == 0:
        color_flag[col_id-1] = set
        main_logger.info('Color %s is now set to %s', col_id-1, set)
        return True
    elif color_flag[col_id-1] == set:
        main_logger.info('Color %s is already produced as %s for another client, GREAT!', col_id, color_flag[col_id])
        return True
    else:
        return False

def process_orders(customers,color_count, produce_all = 0):
    '''Customers list structure (flag for done, number of orders, orders tuples)
    Example: customers = [[0,(1,(1,1))], [0,(3,(1,0), (2,1), (4,0))], [0,(2,(1,1), (2,0))], [0,(1,(5,0))], [0,(1, (1,1))]]
    0 means color is not used, 1 means color is Glossy, 2 means color is Matt'''
    N = color_count
    main_logger.info('We have %s colors', N)
    color_flag = [0] * N

    for index,order in enumerate(customers):
        if matt_count(order):
            main_logger.info('Cannot order more than 1 Matt, order rejected:First found in customer#:%s',index)
            break
        num_orders = order[1][0]
        #Handling customers with only one order, if any of them can't be satisfied because of contradicting orders, IMPOSSIBLE
        if num_orders == 1:
            main_logger.info('Customer order is:%s',order)
            color = order[1][1][0]
            colorType = order[1][1][1]
            if color_status(color_flag, color, set=colorType + 1):
                customers[index][0] = 1
                main_logger.info('Customer#: %s is now satisfied',index)
                main_logger.info('Colors production status: %s',color_flag)
            else:
                main_logger.info('Color %s is already in use in a different type',color)
                main_logger.info('IMPOSSIBLE')
                return False
    else:       
        for index,order in enumerate(customers):
            if customers[index][0] != 1:  
                main_logger.info('Customer order is:%s',order)
                for best_match in common_order(customers):
                    order_best = best_match[0]
                    main_logger.info(order_best)
                    if order_best in order[1]:
                        colorid = order_best[0]
                        type_converted = order_best[1] + 1
                        if color_status(color_flag, colorid, set = type_converted):
                                customers[index][0] = 1
                                main_logger.info('Customer#: %s is now satisfied',index)
                                main_logger.info('Colors production status: %s',color_flag)
                                break
                        else:
                            main_logger.info('Color %s is already in use, trying different color',color)
                else:
                    for best_match in common_order(customers,list=1):
                        order_best = best_match[0]
                        main_logger.info(order_best)
                        if order_best in order[1]:
                            colorid = order_best[0]
                            type_converted = order_best[1] + 1
                            if color_status(color_flag, colorid, set = type_converted):
                                    customers[index][0] = 1
                                    main_logger.info('Customer#: %s is now satisfied',index)
                                    main_logger.info('Colors production status: %s',color_flag)
                                    break
                            else:
                                main_logger.info('Color %s is already in use, try different color',color)
                                continue
                        main_logger.info('IMPOSSIBLE')
                        return False
        else:
            main_logger.info('All customers Satisfied')
            main_logger.info('Final production status: %s',color_flag) 
            final_colors = [x-1 for x in color_flag]
            #Normalising colour flags to 0 & 1, if a colour is not needed, it will have 0, same as glossy
            color_flag_normalised = []
            if produce_all == 1:
                for col in final_colors:
                    if col == -1:
                        color_flag_normalised.append(0)
                    else:
                        color_flag_normalised.append(col)
                return color_flag_normalised
            else:
                return final_colors
