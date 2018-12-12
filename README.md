# Paint Shop Challenge
> This code is a proposed answer to the common paintshop challenge in coding.

A paint shop needs to satisfy customers orders, one order per customer would be enough to satisfy a customer order. At the sametime, the paintshop would like to minimize the number of Matte orders as much as possible.



## Prerequisites
The project depends on built-in Python libraries:
logging, collections, and sys. As such, you do not need to install any additional libraries.

The project should run on Python 2 & Python 3. Though, please note that the project was tested ONLY on Python 3.6 environment. In case of any issue while running the code, please reach out to the author.


## Usage example

A file with name ``test_cases.txt`` is provided for testing purposes. 

### Input Example:
```sh
2
5
3
1 1 1
2 1 0 2 0
1 5 0
1
2
1 1 0
1 1 1
```
### To run the code:
```sh
python paintshop.py
```
To add new test cases, you can either overwrite the existing ``test_cases.txt`` file, OR, edit the file ``paintshop.py`` line 5 and replace FILENAME with your input file name:
```sh
        lines = [line.rstrip('\n') for line in open('FILENAME')]
```

### Output Example:
```sh
Case # 1 : 1 0 0 0 0
Case # 2 : IMPOSSIBLE
```
The output is C lines, one for each test case in the order they occur in the input file, each containing the string
``"Case #X: "`` where X is the ``number of the test case``, starting from 1, followed by:
The string ``"IMPOSSIBLE"``, if the customers' preferences cannot be satisfied; OR
``N space-separated integers, one for each color from 1 to N``, which are 

* ``0`` if the corresponding paint
should be prepared ``glossy``,

* ``1`` if it should be ``matte``

Please note that there is an option as well to flag a color with ``-1`` not to be prepared at all for optimum operation. The algorithm optimise the number of glossy colours as well to be produced not to over produce colours, thus, extra costs. (even though glossy is cheaper than Matte, it still costs to produce any unnecessary colours)

In that case below is added to the other two options above:

 * ``-1`` if the colour ``shouldn't be prepared`` at all.

To activate this option please modify line 26 in ``paintshop.py`` to be:
```sh
        result = test_processing.process_orders(customers_test,color_count)
```
removing ``produce_all = 1`` from the process_orders function. You can set it to ``0`` as well (which is the default)

## Solution Logic:
The algorithm follows the following logic in order

1) The ``paintshop.py`` reads the test case file and process it to ``test_processing.py``, which then:
2) Check if any customer ordered more than 1 Matte, and reject the order if so
3) Try to sastisfy customers with single orders first, if any failed, reject order.
4) If all single order customers are satisfied with no contradictions (ex. one of them order red glossy and the other order red but Matte), the algorithm then try to satisfy each remaining customer, preferably with a colour already produced, or the most common Glossy colour, if not, then most common Matte colour. The most common is counted based on the remaining unsatisfied customers orders.

5) If the algorithm managed to satisfy all orders, it returns back the colours processing to ``paintshop.py`` which then print it, if failed, it inform as well ``paintshop.py`` to print impossible. The algorithm sends the Case number as well along the result.

## Logging:
Logs are recored in ``logs.log``, where you can follow the decision tree for each test case, customer, and order. This is used to track changes whenever needed, and for debugging purposes in future. If you want to view the logs while running in the console, please uncomment line 23 in ``test_processing.py``
```sh
        logger.addHandler(get_console_handler())
```

## General comments:
* ``iter`` library is used in reading files to avoid memory overload by the ``readlines`` function often used, which could cause issues in larger sets of data.
* ``iter`` is utilised as well in several cases instead of for-loop minimize overloading the memory by loading a large list into it, while only one item is needed to process.
* ``Tuples`` are used in customer orders since they are immutable, as such, protect the orders from any changes.

## Possible Improvements
* Using NumPy to improve performance in sorting.
* Using Python ``sorted`` library to partial processing speed optimisation.
* Utilising a database in the case of big data that includes a scaled size of customers and colours to produce.
* Using Elastic to search for common orders and other optimisation tasks, that could yeild into performance improvement in the case of larger data sizes.



## Release History

* 0.1.0
    * First version submitted
* 0.0.1
    * Work in progress

## Meta

Dish – dish@floralytics.com

Distributed under the MIT license. See ``LICENSE`` for more information. This project was made with confidentiality and shared only for knowledge, you are not allowed to share that code in an interview process with any company, or fork it for that. 
