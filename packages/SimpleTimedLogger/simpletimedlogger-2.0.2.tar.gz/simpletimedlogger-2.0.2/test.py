from simpleTimedLogger import SimpleTimedLogger # Import logger to file

logger = SimpleTimedLogger.Logger() # Create instance of a logger class
logger.basic_config(min_level_of_logging=logger.DEBUG) # Set minimum level of messages to be printed in terminal

logger.debug("This prints message to terminal as debug message")

logger.start_timed_log("This starts timed log and prints message to terminal")
logger.end_timed_log("This ends timed log and prints message to terminal and shows elapsed time")

logger.start_timed_log("You can also provide your own key and message level", level=logger.ERROR, key='function name')
logger.end_timed_log('You can also end timed log based on key', key='function name')

logger.log(msg='You can start timed logs this way too', timed=True, level=logger.INFO)
logger.end_timed_log('When key not provided, it ends last started timed log')
