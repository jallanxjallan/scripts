#!/home/jeremy/Python3.12Env/bin/python
from script_lib import load_conf 
import fire


def main():
    conf = load_conf()
    data = vars(conf)
    return data 

if __name__ == "__main__":
    fire.Fire(main)
