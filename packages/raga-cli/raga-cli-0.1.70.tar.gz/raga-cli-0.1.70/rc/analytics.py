import json
import logging
import os

logger = logging.getLogger(__name__)

def collect_and_send_report(args=None, return_code=None):
    """
    Collect information from the runtime/environment and the command
    being executed into a report and send it over the network.

    To prevent analytics from blocking the execution of the main thread,
    sending the report is done in a separate process.

    The inter-process communication happens through a file containing the
    report as a JSON, where the _collector_ generates it and the _sender_
    removes it after sending it.
    """
    import tempfile

    report = {}

    # Include command execution information on the report only when available.
    if args and hasattr(args, "func"):
        report.update({"cmd_class": args.func.__name__})

    if return_code is not None:
        report.update({"cmd_return_code": return_code})

    with tempfile.NamedTemporaryFile(delete=False, mode="w") as fobj:
        print(report)
        # print(logger.)
        json.dump(report, fobj)
    # daemon(["analytics", fobj.name])