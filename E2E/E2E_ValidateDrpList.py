import os
import sys
#print(sys.path)
import time

from Functions.Functions import ROOT_DIR, print_timeDuration

sys.argv = [2, 'arg2'] #Pass PreID number to use


#Start time
strat_Secs = time.perf_counter()

exec(open(os.path.join(ROOT_DIR, 'GlobalSQA_Units', 'OpenUrl.py'), "r").read())
exec(open(os.path.join(ROOT_DIR, 'GlobalSQA_Units', 'DropDownListValid.py'), "r").read())

# End time
end_Secs = time.perf_counter()
# Print out time duration
print_timeDuration(strat_Secs, end_Secs)