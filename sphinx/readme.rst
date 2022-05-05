Installation
############

Can be installed in either use in editable, build or wheel mode. Editable mode allows easier updates, just pull
the repository directory. Contributing is also smoother with editable.

Editable mode
-------------

- clone repository
- (activate your used virtualenv if needed)
- use it in editable mode:

.. code-block:: text

    $ git clone https://github.com/vihman/da_datafix.git
    $ cd da_datafix
    $ pip install -e .

Build mode
-------------

.. code-block:: text

    $ cd da_datafix
    $ pip install -r requirements.txt -r dev-requirements.txt
    $ python -m build -w
    $ cd ../my_main_project
    $ pip install da_datafix -f ../da_datafix/dist/

Wheel mode
-------------

Download the .whl fire from latest release. Install it using pip e.g.:

.. code-block:: text

    $ pip install  da_datafix-2022.5.5-py3-none-any.whl


Examples
########

*Loading data from CSV file.*

.. code-block:: python

    from da_datafix.files import from_csv
    model = from_csv("mydatafile")
    dat = model.get_data()


*Imputating all data fields' missing values with Last Known Good value.*

.. code-block:: python

    from da_datafix.files import from_csv
    temp = from_csv("temperature.csv")
    print(temp.get_fields())
    temp.fix_lastknown("*")
    temp_pandas = temp.get_data_pd()


*Slicing time window:*

.. code-block:: python

    import matplotlib.pyplot as plt
    start = datetime.fromisoformat("2021-10-08")
    end = datetime.fromisoformat("2021-10-10")
    data_slice = temp.get_data_window(start_time=start, end_time=end)
    for field in model.get_fields():
        if field == "timestamp":
            continue
        plt.plot(data_slice["timestamp"], data_slice[field], label=field)
    plt.legend()
    plt.show()

*Fixing wandering baseline:*

.. code-block:: python

    from da_datafix.fix import fix_baseline
    room = '337_value'
    data = model.get_data()
    fix_baseline(data[room])
    plt(data["timestamp], data[room])
    plt.title("Baseline fixed")

or

.. code-block:: python

    model.fix_baseline('337_value')
    data = model.get_data()
    plt(data["timestamp], data[room])
    plt.title("Baseline fixed")
