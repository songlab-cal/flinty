# Detecting Exchangeability from the Terminal

This directory contains scripts and data files used to run our test of exchangeability from the terminal. As described in our Examples page, this demonstration involves the use of the [1000 Genomes Phase 3 dataset](https://www.cog-genomics.org/plink/2.0/resources). 

We encourage interested users to repurpose our scripts for their own analyses. In particular, the Python script, written to be executable from the terminal, can be modified easily.

**What is Provided**

| File Name      | Function |
| ----------- | ----------- |
| `1kg_exchange_test_python.bash`     | Automates execution of test of exchangeability for all 26 populations of 1KG       |
| `test_exchangeability.py`   | Executes test of exchangeability from terminal, given three arguments: directory to 1KG population files (BED/BIM/FAM), directory to PLINK2, resampling number for permutation test      |
| `pop_id_list.txt` | List of 1KG populations for automating execution of exchangeability test across all 26 populations | 

Additionally, an example output log file is provided in the subdirectory `examples`.  

**How to Run**  

1. Download this directory. 
2. Download the 1000G datasets and run PLINK commands as described [here](https://alanaw1.github.io/flintyR/articles/extras.html#running-our-test-from-terminal-1) (*requires knowledge of PLINK*).
3. Place the 1000G datasets in your favourite directory. Modify line 6 of `1kg_exchange_test_python.bash` to point to the directory.
4. Activate the virtual environment `flinty`.  
5. Run the following command in the terminal (*recommended: use a job scheduler, or a terminal multiplexer like [screen](https://blog.thibaut-rousseau.com/2015/12/04/screen-terminal-multiplexer.html)*)

    ```
    bash 1kg_exchange_test_python.bash
    ```
6. There will be an output log file (named `python_output_log.txt`) that should look like `examples/python_output_log_manhattan.txt`. 