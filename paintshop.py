import test_processing
if __name__ == '__main__':
    def customers_generate():
        lines = []
        lines = [line.rstrip('\n') for line in open('test_cases.txt')]
        return lines
    input_lines = iter(customers_generate())
    test_count = int(next(input_lines))

    for i in range(test_count):
        customers_test = []
        color_count = int(next(input_lines))
        customer_count = int(next(input_lines))
        for z in range(customer_count):
            order_line = next(input_lines).split(" ")
            iter_order_line = iter(order_line)
            options_count = int(next(iter_order_line))
            order_tuple = (options_count,)
            for o in range(options_count):
                color_id = int(next(iter_order_line))
                color_type = int(next(iter_order_line))
                option = (color_id,color_type)
                order_tuple = order_tuple + (option,)
            order_list = [0,order_tuple]
            customers_test.append(order_list)
        result = test_processing.process_orders(customers_test,color_count, produce_all = 1)
        if result:
            print('Case #',i+1,':',*result)
        else:
            print ('Case #',i+1,': IMPOSSIBLE')