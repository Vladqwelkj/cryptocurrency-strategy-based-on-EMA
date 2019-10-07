import logging
import logic
import db_interface
def main():
    logging.basicConfig(filename="log.log", level=logging.INFO)
    logging.info("Program started")
    db_interface.connect_db()
    logic.getting_new_ohlc_in_15min()
 
if __name__ == "__main__":
    main()