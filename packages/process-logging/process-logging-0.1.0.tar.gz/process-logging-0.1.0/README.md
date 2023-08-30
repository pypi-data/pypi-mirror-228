# how to use
```
from process-logging import Logger

logger = Logger()
log_fime_name = "{:%Y-%m-%d}_info.log".format(datetime.now())
log_path = "./logs/"
trf_handler_args = {"filename": log_path + log_fime_name,
                    "when": "midnight",
                    "interval": 1,
                    "encoding": "utf-8"}
format_def = ("[%(levelname)s] | %(process)d | %(asctime)s | %(message)s", "%Y-%m-%d %H:%M:%S")
handler_def = {HandlerType.StreamHandler: {}, HandlerType.TimedRotateFileHandler: trf_handler_args}

if __name__ == "__main__":
    logger.set_logger(name="logger", level=logging.INFO, handler_def=handler_def, format_def=format_def)
```