import logging
import logic
 
def main():
    logging.basicConfig(filename="log.log", level=logging.INFO)
    logging.info("Program started")

    logic.getting_new_ohlc_in_15min()
 
if __name__ == "__main__":
    main()