#!/usr/bin/python
# encoding: utf-8

import os
import sys
import subprocess

from workflow import Workflow, MATCH_SUBSTRING

log = None

def main(wf):

    query = wf.args[0]

    # We need to pass an invalid command (in this case "_") to `aws` in order
    # for it to spit out the list of valid commands.
    def get_commands():
      return subprocess.check_output("aws _ 2>&1|grep '|'|sed 's/|//'",
                                       shell=True)

    results = wf.filter(query,
                        wf.cached_data('commands', get_commands, max_age=600).split(),
                        match_on=MATCH_SUBSTRING)

    for i in results:
      icon = 'icons/resource/{}.png'.format(i)
      icon = icon if os.path.isfile(icon) else 'icons/AWS.png'
      wf.add_item(i,
                  arg=i,
                  icon=icon,
                  valid=True)

    wf.send_feedback()


if __name__ == u'__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
