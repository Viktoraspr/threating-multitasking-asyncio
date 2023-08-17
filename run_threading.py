"""
Runs threading method.
"""
from management.data_entry import DataCreator

if __name__ == '__main__':
    proces = DataCreator()
    proces.run_threading()