Examples
========

Here are some examples of how **flintyPy** can be run on data. We are working on expanding our Python documentation, so please take a look at `these articles <https://alanaw1.github.io/flintyR/articles>`_ from our companion flintyR package if you are looking for more real-life examples. There, you will find many pedagogical examples accompanied by thorough explorations. 

A Simulated Binary Matrix
-------------------------

Here, we present the simplest example of running our test on a binary matrix with independent features.

.. code-block:: python

    # Import modules
    import flintypy
    import numpy as np

    # Simulate binary matrix
    X = np.random.randint(2, size=(50, 100))

    # Run test
    flintypy.v_stat.get_p_value(X)

A Real-Valued Matrix
--------------------

A slightly more complicated example is when features are partitioned into independent blocks. Here, we simulate one such array. Features are drawn from an autoregressive (`AR <https://online.stat.psu.edu/stat501/lesson/14/14.1>`_) process one block at a time, with successive blocks concatenated one after another. We use :math:`B=20` blocks, with each block containing :math:`100` draws from the AR(1) process. We sample :math:`N=10` "individuals". 

.. code-block:: python

    # Import modules
    import flintypy
    import numpy as np
    from statsmodels.tsa.arima_process import ArmaProcess

    # Define ARMA process object 
    ar = np.array([1, -0.9])
    ma = np.array([1])
    AR_object = ArmaProcess(ar, ma)

    # Simulate blocks of AR process features
    N_BLOCKS = 20
    big_array = np.array([np.array([AR_object.generate_sample(nsample=100) for i in range(10)]) for b in range(N_BLOCKS)])
    X = np.concatenate(big_array, axis = 1)
    blocks = [np.arange(b * 100, b * 100 + 100) for b in range(N_BLOCKS)]

    # Run test without accounting for block dependency
    # Use large P asymptotics since P = 20 * 100 is large
    flintypy.v_stat.get_p_value(X, large_p = True)

    # Run test accounting for block dependency
    # Use permutation test since B = 20 is small
    flintypy.v_stat.get_p_value(X, blocks = blocks)


A List of Independent Distances
-------------------------------

Our test of exchangeability works in settings where only pairwise distance data is available. Given a list of pairwise distances between :math:`N` individuals, :math:`\{D_1,\ldots,D_B\}`, and assuming these distances are independent of one another, our test can determine whether the individuals making up the :math:`N`-sample are exchangeable at a user-specified significance threshold (e.g., :math:`\alpha = 0.05`).

There are multiple practical scenarios well suited for such an approach.

- Loading the individual-by-feature matrix :math:`\mathbf{X}` into memory is computationally unfeasible
- Only distance data is available owing to privacy issues
- Independent, large sets of features exist on different computers but need to be combined to form the individual-by-feature matrix :math:`\mathbf{X}`

For illustration purposes, we generate the same dataset :math:`\mathbf{X}` using the AR(1) process described in the preceding Section. However, we assume that we only have pairwise Euclidean distances between the individuals at each block, and run the version of our test that takes in pairwise distance data, ``dist_data_p_value()``. 

.. code-block:: python

    # Import modules
    import flintypy
    import numpy as np
    from scipy.spatial.distance import pdist
    from scipy.spatial.distance import squareform
    from statsmodels.tsa.arima_process import ArmaProcess

    # Define ARMA process object 
    ar = np.array([1, -0.9])
    ma = np.array([1])
    AR_object = ArmaProcess(ar, ma)

    # Simulate blocks of AR process features
    N_BLOCKS = 20
    matrix_list = [np.array([AR_object.generate_sample(nsample=100) for i in range(10)]) for b in range(N_BLOCKS)]

    # Convert to list of pairwise distances
    dist_list = list(map(lambda x: pdist(x, metric = 'euclidean'), matrix_list)) # in vector form
    dist_mat_list = list(map(lambda x: squareform(x), dist_list)) # in square matrix form 

    # Run test on pairwise distance data
    flintypy.v_stat.dist_data_p_value(dist_list)

    # Run test on pairwise distance matrix data 
    flintypy.v_stat.dist_data_p_value(dist_mat_list)

If you run on pairwise distance data you should see the following output:

.. code-block:: console

    >>> flintypy.v_stat.dist_data_p_value(dist_list)
    Distances are in vector form
    0.954

Or if you run on pairwise distance matrix data you should see this:

.. code-block:: console

    >>> flintypy.v_stat.dist_data_p_value(dist_mat_list)
    Distances are in matrix form
    0.966

1000 Genomes Project Data
-------------------------

.. note:: 
    Here, we demonstrate the use of our test

    - on a real dataset,
    - through embedding it within a terminal-friendly script.

    Links to the scripts are provided, and we encourage users to modify and use them for their own purposes. 


The 1000 Genomes project (`The 1000 Genomes Project Consortium, 2015 <https://www.nature.com/articles/nature15393>`_) consists of individual genomes spanning :math:`26` populations and :math:`5` superpopulations. We shall test if each of the :math:`26` populations is exchangeable. 

There are some challenges associated with this task.

1. There are millions of features (called "polymorphic variants"), which makes loading the entire dataset at once memory-intensive. 
2. The input files are in BIM/BED/FAM or VCF format, requiring the use of special modules that can handle such files.

To overcome these challenges, we devise a strategy around how we want to run our test. We shall assume variants lying in different chromosomes are independent of one another. Since there are :math:`22` automosomal chromosomes, this means that our features will be grouped into :math:`22` large blocks. Moreover, there are packages like **bed-reader** (`link <https://fastlmm.github.io/bed-reader/>`_) and **pybedtools** (`link <https://daler.github.io/pybedtools/>`_) that specialise in reading genomics data files. Thus, we can accomplish our task as follows.

1. For each population, split the genome into :math:`22` autosomes.
2. Per autosome:
    - load it into Python using **bed-reader** and construct its distance matrix (*addresses challenge 2*)
    - remove the loaded autosome object from memory (*addresses challenge 1*)
3. Run test of exchangeability on list of distance matrices

We provide `here <https://github.com/alanaw1/exchangeability_test/blob/main/data-analysis/1KG/test_exchangeability.py>`_ a Python script, and `here <https://github.com/alanaw1/exchangeability_test/blob/main/data-analysis/1KG/1kg_exchange_test_python.bash>`_ a "master" bash script, for performing the steps above. Our `README <https://github.com/alanaw1/exchangeability_test/blob/main/data-analysis/1KG/README.md>`_ markdown on Github provides guidance on reproducing our results, which we report below. 


+--------------------------------------------------+-----------------+
|      *Population*                                |     *p-value*   |
+--------------------------------------------------+-----------------+
|      British in England and Scotland (GBR)       |      0.000      |
+--------------------------------------------------+-----------------+
|      Finnish in Finland (FIN)                    |      0.000      |
+--------------------------------------------------+-----------------+
|      Southern Han Chinese, China (CHS)           |      0.000      |
+--------------------------------------------------+-----------------+
|      Puerto Rican in Puerto Rico (PUR)           |      0.000      |
+--------------------------------------------------+-----------------+
|      Chinese Dai in Xishuangbanna, China (CDX)   |      0.000      |
+--------------------------------------------------+-----------------+
|      Colombian in Medellin, Colombia (CLM)       |      0.000      |
+--------------------------------------------------+-----------------+
|      Iberian populations in Spain (IBS)          |      0.000      |
+--------------------------------------------------+-----------------+
|      Peruvian in Lima, Peru (PEL)                |      0.000      |
+--------------------------------------------------+-----------------+
|      Punjabi in Lahore, Pakistan (PJL)           |      0.000      |
+--------------------------------------------------+-----------------+
|      Kinh in Ho Chi Minh City, Vietnam (KHV)     |      0.000      |
+--------------------------------------------------+-----------------+
|      African Caribbean in Barbados (ACB)         |      0.000      |
+--------------------------------------------------+-----------------+
|    Gambian in Western Division, The Gambia (GWD) |      0.000      |
+--------------------------------------------------+-----------------+
|               Esan in Nigeria (ESN)              |      0.000      |
+--------------------------------------------------+-----------------+
|           Bengali in Bangladesh (BEB)            |      0.000      |
+--------------------------------------------------+-----------------+
|           Mende in Sierra Leone (MSL)            |      0.000      |
+--------------------------------------------------+-----------------+
|         Sri Lankan Tamil in the UK (STU)         |      0.000      |
+--------------------------------------------------+-----------------+
|          Indian Telugu in the UK (ITU)           |      0.000      |
+--------------------------------------------------+-----------------+
|              Utah residents (CEU)                |      0.000      |
+--------------------------------------------------+-----------------+
|          Yoruba in Ibadan, Nigeria (YRI)         |      0.029      |
+--------------------------------------------------+-----------------+
|        Han Chinese in Beijing, China (CHB)       |      0.000      |
+--------------------------------------------------+-----------------+
|          Japanese in Tokyo, Japan (JPT)          |      0.000      |
+--------------------------------------------------+-----------------+
|      Luhya in Webuye, Kenya (LWK)                |      0.000      |
+--------------------------------------------------+-----------------+
|      African Ancestry in Southwest US (ASW)      |      0.000      |
+--------------------------------------------------+-----------------+
| Mexican Ancestry in Los Angeles, California (MXL)|      0.000      |
+--------------------------------------------------+-----------------+
|                Toscani in Italy (TSI)            |      0.000      |
+--------------------------------------------------+-----------------+
|         Gujarati Indian in Houston, TX (GIH)     |      0.000      |
+--------------------------------------------------+-----------------+

These numbers tell us that all :math:`26` populations have non-exchangeable samples. (For geneticists: note that we have included rare variants with minor allele count >= 1 in our analysis. See `this vignette <https://alanaw1.github.io/flintyR/articles/extras.html#running-our-test-from-terminal-1>`_, **Preparing the population-level files**, for details.) This observation is consistent with the importance of rare variants capturing recent demographic history, a point acknowledged by population geneticists (`Zaidi and Mathieson, 2021 <https://elifesciences.org/articles/61548>`_).