import re

SLIDE_REGEX = re.compile(r'^(!!!(?P<next_slide>.*?)(?=!!!))|(!!!(?P<last_slide>.*))', re.DOTALL | re.MULTILINE)
