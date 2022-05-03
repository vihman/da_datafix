DA Data Control and Manipulation package
###############################################


Installation
============

Can be installed in either use in editable or build mode. Editable mode allow easier updates, you just have
to update the repository directory. Contributing is also smoother.

Editable mode
-------------

- clone repository
- (activate your used virtualenv if needed)
- use it in editable mode:

.. code-block:: text

    $ git clone https://github.com/vihman/da_datacontrol.git
    $ cd da_datacontrol
    $ pip install -e .

Build package
-------------

.. code-block:: text

    $ cd da_datafix
    $ python setup.py bdist_wheel
    $ cd ../my_main_project
    $ pip install da_datafix -f ../da_datafix/dist/


Examples
========

Loading data from CSV file.

.. code-block:: python

    from da_datafix.files import from_csv
    model = from_csv("mydatafile")
    dat = model.get_data()


Imputating all data fields' missing values with Last Known Good value.

.. code-block:: python

    from da_datafix.files import from_csv
    temp = from_csv("temperature.csv")
    print(temp.get_fields())
    temp.fix_lastknown("*")
    temp_pandas = temp.get_data_pd()


Slicing time window:

.. code-block:: python

    start = datetime.fromisoformat("2021-10-08")
    end = datetime.fromisoformat("2021-10-10")
    data_win = temp.get_data_window(start_time=start, end_time=end)
    plt.plot(data_win["timestamp"], data_win["139_value"], label="139")
    plt.plot(data_win["timestamp"], data_win["140_value"], label="140")
    plt.show()